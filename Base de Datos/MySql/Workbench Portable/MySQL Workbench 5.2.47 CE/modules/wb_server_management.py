# Copyright (c) 2007, 2012, Oracle and/or its affiliates. All rights reserved.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; version 2 of the
# License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301  USA

import shutil
import platform
import os
import errno
import threading
import stat
import tempfile
import StringIO
import subprocess
default_sudo_prefix       = '/usr/bin/sudo -p EnterPasswordHere'

from wb_common import splitpath, Users, sanitize_sudo_output
from wb_admin_ssh import WbAdminSSH

from wb_common import InvalidPasswordError, PermissionDeniedError, joinpath

from grt import log_info, log_error, log_warning, log_debug, log_debug2, log_debug3
_this_file = os.path.basename(__file__)

class wbaOS(object):
    unknown = "unknown"
    windows = "windows"
    linux   = "linux"
    darwin  = "darwin"

    def __setattr__(self, name, value):
        raise NotImplementedError

def quote_path(path):
    if path.startswith("~/"):
        # be careful to not quote shell special chars
        return '~/"%s"' % path[2:]
    else:
        return '"%s"' % path.replace('"', r'\"')

def quote_path_win(path):
    return '"%s"' % path.replace("/", "\\").replace('"', r'\"')


def wrap_for_sudo(command, sudo_prefix, as_user = Users.ADMIN):
    if not command:
        raise Exception("Empty command passed to execution routine")
        
    if not sudo_prefix:
        sudo_prefix = default_sudo_prefix
      
    # If as_user is the CURRENT then there's no need to sudo
    if as_user != Users.CURRENT:

        #sudo needs to use -u <user> for non admin
        if as_user != Users.ADMIN:
            sudo_user = "sudo -u %s" % as_user
            sudo_prefix = sudo_prefix.replace('sudo', sudo_user)

        if '/bin/sh' in sudo_prefix or '/bin/bash' in sudo_prefix:
            command = sudo_prefix + " \"" + command.replace('\\', '\\\\').replace('"', r'\"').replace('$','\\$') + "\""
        else:
            command = sudo_prefix + " /bin/sh -c \"" + command.replace('\\', '\\\\').replace('"', r'\"').replace('$','\\$') + "\""
            
            
    return command

###



class SSH(WbAdminSSH):
    def __init__(self, profile, password_delegate):
        self.mtx = threading.Lock()
        self.wrapped_connect(profile, password_delegate)

    def __del__(self):
        log_debug(_this_file, "Closing SSH connection\n")
        self.close()

    def get_contents(self, filename):
        self.mtx.acquire()
        try:
            ret = WbAdminSSH.get_contents(self, filename)
        finally:
            self.mtx.release()
        return ret

    def set_contents(self, filename, data):
        self.mtx.acquire()
        try:
            ret = WbAdminSSH.set_contents(self, filename, data)
        finally:
            self.mtx.release()
        return ret

    def exec_cmd(self, cmd, as_user = Users.CURRENT, user_password = None, output_handler = None, read_size = 128, get_channel_cb = None):
        output   = None
        retcode  = None

        self.mtx.acquire()
        log_debug3(_this_file, '%s:exec_cmd(cmd="%s", sudo=%s)\n' % (self.__class__.__name__, cmd, str(as_user)) )
        try:
            (output, retcode) = WbAdminSSH.exec_cmd(self, cmd,
                                            as_user=as_user,
                                            user_password=user_password,
                                            output_handler=output_handler,
                                            read_size = read_size,
                                            get_channel_cb = get_channel_cb)
            log_debug3(_this_file, '%s:exec_cmd(): Done cmd="%s"\n' % (self.__class__.__name__, cmd) )
        finally:
            self.mtx.release()

        return (output, retcode)


##===================================================================================================
## Local command execution
def local_run_cmd_linux(command, as_user = Users.CURRENT, user_password=None, sudo_prefix=default_sudo_prefix, output_handler=None):
    # pexpect used only in linux
    import pexpect

    # wrap cmd
    if as_user != Users.CURRENT:
        command = wrap_for_sudo(command, sudo_prefix, as_user)
    script = command.strip(" ")
    if script is None or len(script) == 0:
        return None
    script_to_log = script

    temp_file = tempfile.NamedTemporaryFile()

    script = script + " ; echo CMDRESULT$? >> " + temp_file.name

    result = None

    #if "'" in script:
    #    log_debug2(_this_file, "local_run_cmd_linux(): ' found in script:\n%s\n" %  script )
    #    raise Exception("WBA: Internal error, unexpected character in script to be executed")

    # Exec the command
    waiting_rest_of_password_prompt = False
    child = pexpect.spawn("/bin/bash", ["-c", script]) # script should already have sudo prefix
    if as_user != Users.CURRENT:
        # If sudo is being used, we need to input the password
        try:
            child.expect('assword', timeout=10) # 10s timeout
            if not child.isalive():
                raise Exception("expect died")
            waiting_rest_of_password_prompt = True
            if user_password is not None:
                child.sendline(user_password)
            else:
                child.sendline("")
        except pexpect.TIMEOUT:
            #though we are not able to get the expected output, the password is fed anyway
            if user_password is not None:
                child.sendline(user_password)
            else:
                child.sendline("")
        except pexpect.EOF:
            if output_handler:
                output_handler(child.before.replace("\r\n", "\n"))
            #Nothing we can do, client is terminatd for some reason, try to read anything available
            # usually happens when sudo was executed recently and it doesn't ask for pwd again
            log_debug2(_this_file,"local_run_cmd_linux(): Pipe from sudo is closed. script =\n%s\n" % script )

    if child.isalive():
        should_quit_read_loop = False
        while not should_quit_read_loop and child.isalive():
            try:
                current_text = child.read_nonblocking(256, 30) # 30s timeout
                if waiting_rest_of_password_prompt and current_text.startswith("Here"):
                    waiting_rest_of_password_prompt = False
                    current_text = current_text[4:]

                # If Password prompt shows up again, it means the password we tried earlier was wrong.. so raise an exception
                if as_user != Users.CURRENT and current_text.find('EnterPasswordHere') >= 0:
                    try:
                        child.close()
                    except:
                        pass
                    temp_file.close()
                    raise InvalidPasswordError("Incorrect password for sudo")
                else:
                    if output_handler:
                        # pexpect replaces newlines with \r\n
                        output_handler(current_text.replace("\r\n", "\n"))
            except pexpect.TIMEOUT:
                pass
            except pexpect.EOF:
                should_quit_read_loop = True

    #Try to read anything left
    current_text = child.read()
    if waiting_rest_of_password_prompt and current_text.startswith("Here"):
        waiting_rest_of_password_prompt = False
        current_text = current_text[4:]
    if current_text and output_handler:
        output_handler(current_text.replace("\r\n", "\n"))

    child.close();

    text = temp_file.read()
    
    temp_file.close()
    
    idx = text.rfind("CMDRESULT")
    if (idx != -1):
        result = int(text[idx+9:].strip(" \r\t\n"))

    log_debug3(_this_file, 'local_run_cmd_linux(): script="%s", ret="%s"\n' % (script_to_log, str(result)) )
    return result


def local_run_cmd_windows(command, as_user=Users.CURRENT, user_password=None, sudo_prefix=None, output_handler=None):
    # wrap cmd
    out_str =""
    retcode = 1

    if as_user != Users.CURRENT:

        command = "cmd.exe /C " + command

        try:
            from ctypes import c_int, WINFUNCTYPE, windll
            from ctypes.wintypes import HWND, LPCSTR, UINT
            prototype = WINFUNCTYPE(c_int, HWND, LPCSTR, LPCSTR, LPCSTR, LPCSTR, UINT)
            scriptparts = command.partition(" ")
            cmdname = scriptparts[0]
            cmdparams = scriptparts[2]
            paramflags = (1, "hwnd", 0), (1, "operation", "runas"), (1, "file", cmdname), (1, "params", cmdparams), (1, "dir", None), (1, "showcmd", 0)
            SHellExecute = prototype(("ShellExecuteA", windll.shell32), paramflags)
            ret = SHellExecute()
            # > 32 is OK, < 32 is error code
            retcode = 1
            if ret > 32:
                retcode = 0
            else:
                if ret == 0:
                    log_error(_this_file, 'local_run_cmd_windows(): Out of memory executing "%s"\n' % command)
                else:
                    log_error(_this_file, 'local_run_cmd_windows(): Error %i executing "%s"\n' % (ret, command) )
            return retcode
        except:
            import traceback
            traceback.print_exc()
    else:
        try:
            process = subprocess.Popen(command, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell=True)

            for line in iter(process.stdout.readline, ""):
                if output_handler:
                    output_handler(line)

            process.wait()

            retcode = process.returncode
        except Exception, exc:
            import traceback
            traceback.print_exc()
            retcode = 1
            out_str = "Internal error: %s"%exc

    return retcode


if platform.system() == "Windows":
    local_run_cmd = local_run_cmd_windows
else:
    local_run_cmd = local_run_cmd_linux

def local_get_cmd_output(command, as_user=Users.CURRENT, user_password=None):
    output = []
    output_handler = lambda line, l=output: l.append(line)
    rc = local_run_cmd(command=command, as_user=as_user, user_password=user_password, sudo_prefix=None, output_handler=output_handler)
    return ("\n".join(output), rc)

##===================================================================================================
## Process Execution


_process_ops_classes = []


class ProcessOpsBase(object):
    cmd_output_encoding = ""

    def __init__(self, **kwargs):
        pass

    def post_init(self):
        pass

    def expand_path_variables(self, path):
        return path

    def get_cmd_output(self, command, as_user=Users.CURRENT, user_password=None):
        output = []
        output_handler = lambda line, l=output: l.append(line)
        rc = self.exec_cmd(command, as_user, user_password, output_handler)
        return ("\n".join(output), rc)


class ProcessOpsNope(ProcessOpsBase):
    @classmethod
    def match(cls, (host, target, connect)):
        return connect == 'none'

    def expand_path_variables(self, path):
        return path

    def exec_cmd(self, command, as_user=Users.CURRENT, user_password=None, output_handler=None):
        return None

    def get_cmd_output(self, command, as_user=Users.CURRENT, user_password=None):
        return ("", None)

_process_ops_classes.append(ProcessOpsNope)


class ProcessOpsLinuxLocal(ProcessOpsBase):
    @classmethod
    def match(cls, (host, target, connect)):
        return connect == 'local' and (host in (wbaOS.linux, wbaOS.darwin) and target in (wbaOS.linux, wbaOS.darwin))

    def __init__(self, **kwargs):
        ProcessOpsBase.__init__(self, **kwargs)
        self.sudo_prefix= kwargs.get("sudo_prefix", default_sudo_prefix)

    def exec_cmd(self, command, as_user=Users.CURRENT, user_password=None, output_handler=None):
        return local_run_cmd_linux(command, as_user, user_password, self.sudo_prefix, output_handler)

_process_ops_classes.append(ProcessOpsLinuxLocal)


class ProcessOpsLinuxRemote(ProcessOpsBase):
    @classmethod
    def match(cls, (host, target, connect)):
        # host doesn't matter
        return connect == 'ssh' and target in (wbaOS.linux, wbaOS.darwin)

    def __init__(self, **kwargs): # Here should be at least commented list of args
        ProcessOpsBase.__init__(self, **kwargs)

        self.sudo_prefix= kwargs.get("sudo_prefix", default_sudo_prefix)
        self.ssh = kwargs["ssh"]

    def exec_cmd(self, command, as_user=Users.CURRENT, user_password=None, output_handler=None):
        #if not self.ssh:
        #    raise Exception("No SSH session active")

        if as_user != Users.CURRENT:
            command = wrap_for_sudo(command, self.sudo_prefix, as_user)

        def ssh_output_handler(ssh_channel, handler):
            import socket
            loop = True
            while loop:
                try:
                    chunk = ssh_channel.recv(128)
                    if chunk is not None and chunk != "":
                        handler(chunk)
                    else:
                        loop = False
                except socket.timeout:
                    loop = False

        if output_handler:
            handler = lambda chan, h=output_handler: ssh_output_handler(chan, h)
        else:
            handler = None

        if self.ssh:
            # output_handler taken by ssh.exec_cmd is different from the one used elsewhere
            dummy_text, ret = self.ssh.exec_cmd(command,
                    as_user=as_user, user_password=user_password,
                    output_handler=handler)
        else:
            ret = 1
            if output_handler:
                output_handler("No SSH connection is active")
            else:
                print("No SSH connection is active")
                log_info(_this_file, 'No SSH connection is active\n')

        return ret

_process_ops_classes.append(ProcessOpsLinuxRemote)




WIN_REG_QUERY_PROGRAMFILES = 'reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion /v "ProgramFilesDir"'
WIN_REG_QUERY_PROGRAMFILES_x86 = 'reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion /v "ProgramFilesDir (x86)"'

WIN_PROGRAM_FILES_VAR = "%ProgramFiles%"
WIN_PROGRAM_FILES_X86_VAR = "%ProgramFiles(x86)%"
WIN_PROGRAM_FILES_X64_VAR = "%ProgramW6432%"
WIN_PROGRAM_DATA_VAR = "%ProgramData%"


class ProcessOpsWindowsLocal(ProcessOpsBase):
    @classmethod
    def match(cls, (host, target, connect)):
        return (host == wbaOS.windows and target == wbaOS.windows and connect in ('wmi', 'local'))

    def __init__(self, **kwargs):
        ProcessOpsBase.__init__(self, **kwargs)
        self.target_shell_variables = {}

    def post_init(self):
        self.fetch_windows_shell_info()

    def exec_cmd(self, command, as_user, user_password, output_handler=None):
        return local_run_cmd_windows(command, as_user, user_password, None, output_handler)

    def expand_path_variables(self, path):
        """
        Expand some special variables in the path, such as %ProgramFiles% and %ProgramFiles(x86)% in
        Windows. Uses self.target_shell_variables for the substitutions, which should have been
        filled when the ssh connection to the remote host was made.
        """
        for k, v in self.target_shell_variables.iteritems():
            path = path.replace(k, v)
        return path

    def fetch_windows_shell_info(self):
        # get some info from the remote shell
        result, code = self.get_cmd_output("chcp.com")
        if code == 0:
            result = result.strip(" .\r\n").split()
            if len(result) > 0:
                self.cmd_output_encoding = "cp" + result[-1]
        else:
            print "WARNING: Unable to determine codepage from shell: %s" % result
            log_warning(_this_file, '%s.fetch_windows_shell_info(): WARNING: Unable to determine codepage from shell: "%s"\n' % (self.__class__.__name__, str(result)) )

        result, code = self.get_cmd_output("echo %PROCESSOR_ARCHITECTURE%")
        if result:
            result = result.strip()
						
        ProgramFilesVar = None
        x86var = None
        if result != "x86":#we are on x64 win in x64 mode
            x86var = WIN_PROGRAM_FILES_X86_VAR
            ProgramFilesVar = WIN_PROGRAM_FILES_VAR
        else:
            result, code = self.get_cmd_output("echo %PROCESSOR_ARCHITEW6432%")
            if result:
                result = result.strip()
            if result == "%PROCESSOR_ARCHITEW6432%":#we are on win 32
                x86var = WIN_PROGRAM_FILES_VAR
                ProgramFilesVar = WIN_PROGRAM_FILES_VAR
            else:#32bit app on x64 win
                x86var = WIN_PROGRAM_FILES_VAR
                ProgramFilesVar = WIN_PROGRAM_FILES_X64_VAR

        result, code = self.get_cmd_output("echo "+ ProgramFilesVar)
        if code == 0:
            self.target_shell_variables["%ProgramFiles%"] = result.strip("\r\n")
            if ProgramFilesVar != "%ProgramFiles%":
                self.target_shell_variables[ProgramFilesVar] = result.strip("\r\n")
        else:
            print "WARNING: Unable to fetch ProgramFiles value in Windows machine: %s"%result
            log_warning(_this_file, '%s.fetch_windows_shell_info(): WARNING: Unable to fetch ProgramFiles value in Windows machine: "%s"\n' % (self.__class__.__name__, str(result)) )

        # this one only exists in 64bit windows
        result, code = self.get_cmd_output("echo "+ x86var)
        if code == 0:
            self.target_shell_variables["%ProgramFiles(x86)%"] = result.strip("\r\n")
        else:
            print "WARNING: Unable to fetch ProgramFiles(x86) value in local Windows machine: %s"%result
            log_warning(_this_file, '%s.fetch_windows_shell_info(): WARNING: Unable to fetch ProgramFiles(x86) value in local Windows machine: "%s"\n' % (self.__class__.__name__, str(result)) )

        # Fetches the ProgramData path
        result, code = self.get_cmd_output("echo "+ WIN_PROGRAM_DATA_VAR)
        if code == 0:
            self.target_shell_variables[WIN_PROGRAM_DATA_VAR] = result.strip("\r\n")
        else:
            # If not found, it will use the %ProgramFiles% variable value
            self.target_shell_variables[WIN_PROGRAM_DATA_VAR] = self.target_shell_variables[ProgramFilesVar]
            print "WARNING: Unable to fetch ProgramData value in local Windows machine: %s, using ProgramFiles path instead: %s" % (result, self.target_shell_variables[WIN_PROGRAM_DATA_VAR])
            log_warning(_this_file, '%s.fetch_windows_shell_info(): WARNING: Unable to fetch ProgramData value in local Windows machine: "%s"\n' % (self.__class__.__name__, str(result)) )
						
        log_debug(_this_file, '%s.fetch_windows_shell_info(): Encoding: "%s", Shell Variables: "%s"\n' % (self.__class__.__name__, self.cmd_output_encoding, str(self.target_shell_variables)))


_process_ops_classes.append(ProcessOpsWindowsLocal)


class ProcessOpsWindowsRemoteSSH(ProcessOpsWindowsLocal):
    @classmethod
    def match(cls, (host, target, connect)):
        # host doesn't matter
        return (target == wbaOS.windows and connect == 'ssh')

    def __init__(self, **kwargs):
        ProcessOpsWindowsLocal.__init__(self, **kwargs)

        self.ssh = kwargs["ssh"]


    def post_init(self):
        if self.ssh:
            self.fetch_windows_shell_info()


    def exec_cmd(self, command, as_user=Users.CURRENT, user_password=None, output_handler=None):
        command = "cmd.exe /c " + command

        if not self.ssh:
            raise Exception("No SSH session active")

        def ssh_output_handler(ssh_channel, handler):
            import socket
            loop = True
            while loop:
                try:
                    chunk = ssh_channel.recv(128)
                    if chunk is not None and chunk != "":
                        handler(chunk)
                    else:
                        loop = False
                except socket.timeout:
                    loop = False

        if output_handler:
            handler = lambda chan, h=output_handler: ssh_output_handler(chan, h)
        else:
            handler = None

        # output_handler taken by ssh.exec_cmd is different from the one used elsewhere
        dummy_text, ret = self.ssh.exec_cmd(command,
                as_user=as_user, user_password=user_password,
                output_handler=handler)
        return ret




_process_ops_classes.append(ProcessOpsWindowsRemoteSSH)



##===================================================================================================
## File Operations

_file_ops_classes = []

class FileOpsNope(object):
    @classmethod
    def match(cls, target_os, connection_method):
        return connection_method == "none"

    def __init__(self, process_ops, ssh = None, target_os = None):
        pass

    def save_file_content(self, filename, content, as_user = Users.CURRENT, user_password = None):
        pass

    def save_file_content_and_backup(self, filename, content, backup_extension, as_user = Users.CURRENT, user_password = None):
        pass

    def get_file_content(self, filename, as_user = Users.CURRENT, user_password = None):
        return ""

    def _copy_file(self, source, dest, as_user = Users.CURRENT, user_password = None): # not used externally
        pass

    def check_dir_writable(self, path, as_user=Users.CURRENT, user_password=None):
        return False

    def file_exists(self, path, as_user = Users.CURRENT, user_password = None):
        return False

    def get_file_owner(self, path, as_user = Users.CURRENT, user_password = None):
        return False
        
    def create_directory(self, path, as_user = Users.CURRENT, user_password = None):
        pass

    def get_available_space(self, path, as_user = Users.CURRENT, user_password = None):
        return False

    # Return format is list of entries in dir (directories go first, each dir name is follwoed by /)
    def listdir(self, path, as_user = Users.CURRENT, user_password = None): # base operation to build file_exists and remote file selector
        return []

    def get_owner(self, path): # base operation to build file_exists and remote file selector
        return []
_file_ops_classes.append(FileOpsNope)


#===============================================================================
# The local file ops are context free, meaning that they
# do not need active shell session to work on
# local  all  plain
#   save_file_content  - python
#   get_file_content   - python
#   copy_file          - python
#   get_dir_access     - python (returns either rw or ro or none)
#   listdir            - python
# local  all  sudo derives from local-all-plain
#   save_file_content  - shell
#   get_file_content   - python (maybe sudo if file is 0600)
#   copy_file          - shell
#   get_dir_access     - python (returns either rw or ro or none)
#   listdir            - python/shell(for ro-dirs)
class FileOpsLocalUnix(object):
    @classmethod
    def match(cls, target_os, connection_method):
        return connection_method == "local" and target_os in (wbaOS.linux, wbaOS.darwin)

    process_ops = None
    def __init__(self, process_ops, ssh=None, target_os = None):
        self.target_os = target_os
        self.process_ops = process_ops
        self.tempdir = os.path.expanduser('~')

    def file_exists(self, filename, as_user=Users.CURRENT, user_password=None):
        res = self.process_ops.exec_cmd('test -e ' + quote_path(filename),
                            as_user,
                            user_password,
                            output_handler = lambda line:None)
        return res == 0

    def get_available_space(self, path, as_user=Users.CURRENT, user_password=None):
        output_text = StringIO.StringIO()
        res = self.process_ops.exec_cmd("df -Ph %s" % quote_path(path),
                            as_user,
                            user_password,
                            output_handler = output_text.write)

        output_text = sanitize_sudo_output(output_text.getvalue()).strip()
        
        available = "Could not determine"
        if output_text:
            tokens = output_text.split("\n")[-1].strip().split()
            available = "%s of %s available" % (tokens[3], tokens[1])
        
        return available
        
    def get_file_owner(self, path, as_user = Users.CURRENT, user_password = None):
        if self.target_os == wbaOS.linux:
          command = 'stat -c %U '
        else:
          command = 'stat -f "%Su" '
      
        output = []
        command = command + quote_path(path)
        
        self.process_ops.exec_cmd(command,
                            as_user,
                            user_password,
                            output_handler= lambda line,l=output: l.append(line))
             
        res = "\n".join(output).strip()
        return res


    # content must be a string
    def save_file_content(self, filename, content, as_user = Users.CURRENT, user_password = None):
        self.save_file_content_and_backup(filename, content, None, as_user, user_password)


    def save_file_content_and_backup(self, filename, content, backup_extension, as_user = Users.CURRENT, user_password = None):
        log_debug(_this_file, '%s: Saving file "%s" with backup (sudo="%s")\n' %  (self.__class__.__name__, filename, as_user) )
        if as_user != Users.CURRENT:
            # The delete argument is only available starting from py 2.6 (NamedTemporaryFile deletes files on close in all cases, unless you pass delete=False)
            tmp = tempfile.NamedTemporaryFile()
            tmp_name = tmp.name
            try:
                log_debug(_this_file, '%s: Writing file contents to tmp file "%s"\n' %  (self.__class__.__name__, tmp_name) )
                tmp.write(content)
                tmp.flush()
                if backup_extension and os.path.exists(filename):
                    log_debug(_this_file, '%s: Creating backup of "%s" to "%s"\n' %  (self.__class__.__name__, filename, filename+backup_extension))
                    
                    # The old file is backed up as the requested user
                    self._copy_file(source = filename, dest = filename + backup_extension,
                                    as_user = as_user, user_password = user_password)

                log_debug(_this_file, '%s: Copying over tmp file to final filename using sudo: %s -> %s\n' % (self.__class__.__name__, tmp_name, filename) )
                
                # The new file is copied as the root user
                self._copy_file(source = tmp_name, dest = filename, as_user = Users.ADMIN, user_password = user_password)
                
                # If needed changes the ownership of the new file to the requested user
                if as_user != Users.ADMIN:
                
                    # TODO: Does this need any validation being executed by root??
                    self.process_ops.exec_cmd("chown %s %s" % (as_user, quote_path(filename)),
                                  as_user   = Users.ADMIN,
                                  user_password = user_password)
                                  
                log_debug(_this_file, '%s: Copying file done\n' % self.__class__.__name__)
                tmp.close()
            except Exception, exc:
                log_error(_this_file, '%s: Exception caught: %s\n' % (self.__class__.__name__, str(exc)) )
                if tmp:
                    tmp.close()
                raise
        else:
            target_dir = splitpath(filename)[0]

            if not os.path.exists(target_dir):
                log_debug(_this_file, '%s: Target directory "%s" does not exist\n' % (self.__class__.__name__, target_dir ) )
                raise IOError(errno.ENOENT, "The directory %s does not exist" % target_dir)

            try:
                self.check_dir_writable(target_dir)
            except Exception, e:
                log_debug(_this_file, '%s: Target directory "%s" is not writable: %s\n' % (self.__class__.__name__, target_dir, e) )
                raise PermissionDeniedError("Cannot write to target directory")

            if os.path.exists(filename) and backup_extension:
                log_debug(_this_file, '%s: Target file "%s" exists, creating backup\n' % (self.__class__.__name__, filename) )
                # backup config file
                self._copy_file(filename, filename+backup_extension)
            try:
                f = open(filename, 'w')
            except OSError, err:
                if err.errno == errno.EACCES:
                    raise PermissionDeniedError("Could not open file %s for writing" % filename)
                raise err
            f.write(content)
            f.close()


    # UseCase: If get_file_content fails with exception of access, try sudo
    def get_file_content(self, filename, as_user = Users.CURRENT, user_password = None):
        cont = []
        if as_user != Users.CURRENT:
            output = StringIO.StringIO()
            local_run_cmd_linux('cat %s' % filename, as_user, user_password, sudo_prefix=self.process_ops.sudo_prefix, output_handler=output.write)
            output = output.getvalue()
            if "No such file or directory" in output:
                error = IOError()
                error.errno = errno.ENOENT
                raise error

            return output
        else:
            try:
                f = open(filename, 'r')
            except (IOError, OSError), e:
                if e.errno == errno.EACCES:
                    raise PermissionDeniedError("Can't open file '%s'" % filename)
                raise e
            cont = f.read()
            f.close()
        return cont


    def create_directory(self, path, as_user = Users.CURRENT, user_password = None):
        if as_user == Users.CURRENT:
            try:
                os.mkdir(path)
            except (IOError, OSError), err:
                if err.errno == errno.EACCES:
                    raise PermissionDeniedError("Could not create directory %s" % path)
                raise err
        else:
            output = []
            res = self.process_ops.exec_cmd("/bin/mkdir " + quote_path(path),
                                            as_user   = as_user,
                                            user_password = user_password,
                                            output_handler = lambda line, l= output: l.append(line)
                                            )
            if res != 0:
                output = "\n".join(output)
                raise RuntimeError(output)


    def remove_directory(self, path, as_user = Users.CURRENT, user_password = None):
        if as_user == Users.CURRENT:
            try:
                os.rmdir(path)
            except (IOError, OSError), err:
                if err.errno == errno.EACCES:
                    raise PermissionDeniedError("Could not remove directory %s" % path)
                raise err
        else:
            output = []
            res = self.process_ops.exec_cmd("/bin/rmdir " + quote_path(path),
                                            as_user   = as_user,
                                            user_password = user_password,
                                            output_handler = lambda line, l= output: l.append(line)
                                            )
            if res != 0:
                output = "\n".join(output)
                raise RuntimeError(output)


    def delete_file(self, path, as_user = Users.CURRENT, user_password = None):
        if as_user == Users.CURRENT:
            try:
                os.remove(path)
            except (IOError, OSError), err:
                if err.errno == errno.EACCES:
                    raise PermissionDeniedError("Could not delete file %s" % path)
                raise err
        else:
            output = []
            res = self.process_ops.exec_cmd("/bin/rm " + quote_path(path),
                                            as_user   = as_user,
                                            user_password = user_password,
                                            output_handler = lambda line, l= output: l.append(line)
                                            )
            if res != 0:
                output = "\n".join(output)
                raise RuntimeError(output)


    def _copy_file(self, source, dest, as_user = Users.CURRENT, user_password = None): # not used externally
        if as_user == Users.CURRENT:
            try:
                shutil.copy(source, dest)
            except (IOError, OSError), e:
                if e.errno == errno.EACCES:
                    raise PermissionDeniedError("Can't copy %s to %s" % (source, dest))
                raise
        else:
            output = []
            res = self.process_ops.exec_cmd("/bin/cp " + quote_path(source) + " " + quote_path(dest),
                          as_user   = as_user,
                          user_password = user_password,
                          output_handler = lambda line, l= output: l.append(line)
                         )

            if res != 0:
                output = "\n".join(output)
                if output.find("Permission denied") != -1:
                  raise PermissionDeniedError("Permission denied copying %s to %s" % (source, dest) )
                else:
                  
                  print "file copy as %s failed: " % as_user, output, res

                # TODO: Add handling of errors

    def check_dir_writable(self, path, as_user=Users.CURRENT, user_password=None):
    
        filename = joinpath(path, '.wb_write_test')
        
        output = []

        res = self.process_ops.exec_cmd('touch ' + quote_path(filename),
                            as_user,
                            user_password,
                            output_handler = lambda line, l= output: l.append(line))
        if res == 0:
            self.process_ops.exec_cmd('/bin/rm ' + quote_path(filename),
                            as_user,
                            user_password,
                            output_handler = lambda line:None)
        else:
            output = sanitize_sudo_output('\n'.join(output).strip())
            error = None
            if "No such file or directory" in output:
                error = IOError("The directory does not exist")
                error.errno = errno.ENOENT
            elif "Permission denied" in output:
                error = PermissionDeniedError("Permission denied for writing")
                error.errno = errno.EACCES
            else:
                error = Exception("Unable to verify directory is writable: %s" % output)
                
            raise error
          
        return res == 0
        

    # Return format is list of entries in dir (directories go first, each dir name is followed by /)
    def listdir(self, path, as_user = Users.CURRENT, user_password = None): # base operation to build file_exists and remote file selector
        dirlist = []
        if as_user == Users.CURRENT:
            try:
                _path = path
                dlist = os.listdir(_path)
                # mod = ""
                for item in dlist:
                    _path = os.path.join(path, item)
                    item_stat = os.stat(_path).st_mode
                    if stat.S_ISDIR(item_stat):
                        dirlist.insert(0, item + '/')
                    elif stat.S_ISREG(item_stat) or stat.S_ISLNK(item_stat):
                        dirlist.append(item)
            except (IOError, OSError), e:
                if e.errno == errno.EACCES:
                    raise PermissionDeniedError("Permission denied accessing %s" % _path)
                raise
            return dirlist
        else:
            output = StringIO.StringIO()
            res = self.process_ops.exec_cmd('/bin/ls -1 -p ' + quote_path(path),
                                            as_user,
                                            user_password,
                                            output_handler = output.write)
            output = sanitize_sudo_output(output.getvalue())
            if res != 0:
                if "Permission denied" in output:
                    raise PermissionDeniedError("Permission denied accessing %s" % path)
                raise RuntimeError(output)
            else:
                return [s.strip() for s in output.split("\n")]

_file_ops_classes.append(FileOpsLocalUnix)



#===============================================================================
class FileOpsLocalWindows(FileOpsLocalUnix): # Used for remote as well, if not using sftp
    @classmethod
    def match(cls, target_os, connection_method):
        return connection_method in ("local", "wmi") and target_os == wbaOS.windows


    def __init__(self, process_ops, ssh=None, target_os = None):
        FileOpsLocalUnix.__init__(self, process_ops, ssh, target_os)

        tempdir, rc= self.process_ops.get_cmd_output("echo %temp%")
        if tempdir and tempdir.strip():
            self.tempdir = tempdir.strip()


    def get_file_owner(self, path, as_user = Users.CURRENT, user_password = None):
        
        # This doesn't work properly tho is not needed in windows

        command = 'dir /q %s*' % quote_path(path)
      
        output = []
        
        self.process_ops.exec_cmd(command,
                            as_user,
                            user_password,
                            output_handler= lambda line,l=output: l.append(line))

        res = ""
        for line in output:
            line_data = line.split()

            if line[len(line)-1] == path:
                res = line[len(line)-2]

        return res

    def check_dir_writable(self, path, as_user=Users.CURRENT, user_password=None):
    
        filename = joinpath(path, '.wb_write_test')
        
        output = []
        
        res = self.process_ops.exec_cmd('echo "tst" > ' + quote_path(filename),
                            as_user,
                            user_password,
                            output_handler = lambda line, l= output: l.append(line))
                            
        if res == 0:
            self.process_ops.exec_cmd('del ' + quote_path(filename),
                            as_user,
                            user_password,
                            output_handler = lambda line:None)
        else:
            output = '\n'.join(output)
            error = None
                
            if "The system cannot find the path specified" in output:
                error = IOError("The directory does not exist")
                error.errno = errno.ENOENT
            elif "Access is denied" in output:
                error = PermissionDeniedError("Permission denied for writing")
                error.errno = errno.EACCES
            else:
                error = Exception("Unable to verify directory is writable")
                
            raise error
          
        return res == 0

    def file_exists(self, filename, as_user = Users.CURRENT, user_password=None):
        command = 'exist ' + quote_path_win(filename)

        res = self.process_ops.exec_cmd('dir ' + quote_path_win(filename),
                          as_user   = as_user,
                          user_password = user_password,
                          output_handler = lambda line:None
                         )

        return res == 0

    def get_available_space(self, path, as_user=Users.CURRENT, user_password=None):
        out = []        

        res = self.process_ops.exec_cmd('dir %s' % quote_path(path),
                            as_user,
                            user_password,
                            output_handler = lambda line, l = out:l.append(line))

        available = "Could not determine"
        if res == 0 and len(out):
            measures = ['B', 'KB', 'MB', 'GB', 'TB']
            tokens = out[-1].strip().split()
            
            total = float(tokens[2].replace(",",""))
            index = 0
            while index < len(measures) and total > 1024:
                total = total / 1024
                index = index + 1


            available = "%.2f %s available" % (total, measures[index])
        
        return available


    def save_file_content_and_backup(self, filename, content, backup_extension, as_user = Users.CURRENT, user_password = None):
        log_debug(_this_file, '%s: Saving file "%s" with backup (sudo="%s")\n' % (self.__class__.__name__, filename, str(as_user)) )
        if as_user != Users.CURRENT:
            tmp = tempfile.NamedTemporaryFile("w+b", delete = False)
            tmp_name = tmp.name
            try:
                log_debug(_this_file, '%s: Writing file contents to tmp file "%s"\n' % (self.__class__.__name__, tmp_name) )
                tmp.write(content)
                tmp.close()

                if backup_extension and os.path.exists(filename):
                    #dprint_ex(1, "Creating backup of %s to %s" % (filename, filename+backup_extension))
                    #self._copy_file(source = filename, dest = filename + backup_extension,
                    #                as_user = as_user, user_password = user_password)

                    # Create backup and copy over file to final destination in a single command
                    # This is done because running copy twice, would bring up the UAC dialog twice

                    script = "copy /Y %s %s && copy /Y %s %s" % (quote_path_win(filename), quote_path_win(filename + backup_extension),
                                                                 quote_path_win(tmp_name), quote_path_win(filename))
                    log_debug(_this_file, '%s: Creating backup and commiting tmp file: "%s"\n' % (self.__class__.__name__, script) )
                    output = []
                    res = self.process_ops.exec_cmd(script,
                          as_user   = as_user,
                          user_password = user_password,
                          output_handler = lambda line, l= output: l.append(line)
                         )
                    if res != 0:
                        output = "\n".join(output)
                        raise RuntimeError("Error while executing '%s'. Output = '%s'" % (script, output))
                else:
                    log_debug(_this_file, '%s: Copying over tmp file to final filename using sudo: %s -> %s\n' % (self.__class__.__name__, tmp_name, filename) )
                    self._copy_file(source = tmp_name, dest = filename, as_user = as_user, user_password = user_password)


                log_debug(_this_file, '%s: Delete tmp file "%s"\n' % (self.__class__.__name__, tmp_name) )
                # delete tmp file

                ## BIZARRE STUFF GOING ON HERE
                # commenting out the following line, will make something in committing config file change fail
                # even tho the copies happen before this line.. wtf
               # os.remove(tmp_name)

                log_debug(_this_file, '%s: Done.\n' % self.__class__.__name__)
            except Exception, exc:
                log_error(_this_file, '%s: Exception caught: %s\n' % (self.__class__.__name__, str(exc)) )
                if tmp:
                    tmp.close()
                raise
        else:
            FileOpsLocalUnix.save_file_content_and_backup(self, filename, content, backup_extension, as_user, user_password)

    # UseCase: If get_file_content fails with exception of access, try sudo
    def get_file_content(self, filename, as_user = Users.CURRENT, user_password = None):
        if as_user != Users.CURRENT:
            output = StringIO.StringIO()
            local_run_cmd_windows('type %s' % quote_path_win(filename), Users.ADMIN, user_password, sudo_prefix=None, output_handler=output.write)
            output = output.getvalue()
            if "No such file or directory" in output:
                error = IOError()
                error.errno = errno.ENOENT
                raise error

            return output
        else:
            return FileOpsLocalUnix.get_file_content(self, filename, as_user, user_password)


    def _copy_file(self, source, dest, as_user = Users.CURRENT, user_password = None): # not used externally, but in superclass
        if as_user == Users.CURRENT:
            try:
                shutil.copyfile(source, dest)
            except (IOError, OSError), e:
                if e.errno == errno.EACCES:
                    raise PermissionDeniedError("Can't copy %s to %s" % (source, dest))
                raise
        else:
            output = []
            res = self.process_ops.exec_cmd("copy /Y " + quote_path_win(source) + " " + quote_path_win(dest),
                          as_user   = as_user,
                          user_password = user_password,
                          output_handler = lambda line, l= output: l.append(line)
                         )
            if res != 0:
                output = "\n".join(output)
                raise RuntimeError("Error copying file %s to %s\n%s" % (source, dest, output.strip()))


    def create_directory(self, path, as_user = Users.CURRENT, user_password = None):
        if as_user == Users.CURRENT:
            try:
                os.mkdir(path)
            except (IOError, OSError), err:
                if err.errno == errno.EACCES:
                    raise PermissionDeniedError("Could not create directory %s" % path)
                raise err
        else:
            output = []
            res = self.process_ops.exec_cmd("mkdir " + quote_path_win(path),
                                            as_user   = as_user,
                                            user_password = user_password,
                                            output_handler = lambda line, l= output: l.append(line)
                                            )
            if res != 0:
                output = "\n".join(output)
                raise RuntimeError(output)


    def remove_directory(self, path, as_user = Users.CURRENT, user_password = None):
        if as_user == Users.CURRENT:
            try:
                os.rmdir(path)
            except (IOError, OSError), err:
                if err.errno == errno.EACCES:
                    raise PermissionDeniedError("Could not remove directory %s" % path)
                raise err
        else:
            output = []
            res = self.process_ops.exec_cmd("rmdir " + quote_path_win(path),
                                            as_user   = as_user,
                                            user_password = user_password,
                                            output_handler = lambda line, l= output: l.append(line)
                                            )
            if res != 0:
                output = "\n".join(output)
                raise RuntimeError(output)


    def delete_file(self, path, as_user = Users.CURRENT, user_password = None):
        if as_user == Users.CURRENT:
            try:
                os.remove(path)
            except (IOError, OSError), err:
                if err.errno == errno.EACCES:
                    raise PermissionDeniedError("Could not delete file %s" % path)
                raise err
        else:
            output = []
            res = self.process_ops.exec_cmd("del " + quote_path_win(path),
                                            as_user   = as_user,
                                            user_password = user_password,
                                            output_handler = lambda line, l= output: l.append(line)
                                            )
            if res != 0:
                output = "\n".join(output)
                raise RuntimeError(output.strip())

    def listdir(self, path, as_user = Users.CURRENT, user_password = None):
        if as_user == Users.CURRENT: # derived from FileOpsLocalUnix
            return FileOpsLocalUnix.listdir(self, path)
        else:
            output = StringIO.StringIO()
            res = self.process_ops.exec_cmd("dir /B " + quote_path_win(path),
                                            as_user   = as_user,
                                            user_password = user_password,
                                            output_handler = output.write
                                            )
            if res != 0:
                output = output.getvalue().strip()
                if "File not found" in output:
                    raise IOError(errno.ENOENT, output)
                raise RuntimeError(output)
            else:
                return [s.strip() for s in output.strip().split("\n")]

_file_ops_classes.append(FileOpsLocalWindows)

#===============================================================================
# This remote file ops are shell dependent, they must be
# given active ssh connection, possibly, as argument
# remote unix sudo/non-sudo
#   save_file_content  - shell
#   get_file_content   - shell
#   copy_file          - shell
#   get_dir_access     - shell(returns either rw or ro or none)
#   listdir            - shell(for ro-dirs)
class FileOpsRemoteUnix(object):
    @classmethod
    def match(cls, target_os, connection_method):
        return connection_method == "ssh" and target_os in (wbaOS.linux, wbaOS.darwin)

    def __init__(self, process_ops, ssh, target_os = None):
        self.process_ops = process_ops
        self.ssh = ssh
        self.target_os = target_os


    def file_exists(self, filename, as_user=Users.CURRENT, user_password=None):
        if self.ssh:
            log_debug3(_this_file, '%s: %s\n' % (self.__class__.__name__, 'Checking if file "%s" exists ' + 
                                                'as admin' if as_user == Users.ADMIN else 
                                                ('as the ' + 'regular' if as_user == Users.CURRENT else as_user + ' user') ) )
            if as_user != Users.CURRENT:
                # -t doesn't mean the same thing in osx
                command = wrap_for_sudo('test -e ' + quote_path(filename), self.process_ops.sudo_prefix, as_user)
                out, ret = self.ssh.exec_cmd(command, as_user, user_password)
                if ret != 0:
                    raise InvalidPasswordError('Incorrect password for sudo')
                return True
            else:
                try:
                    return self.ssh.file_exists(filename)
                except IOError, exc:
                    if exc.errno == errno.EACCES:
                        raise PermissionDeniedError("Permission denied attempting to read file %s" % filename)
                    elif exc.errno == errno.ENOENT:
                        return False
                    raise
        else:
            print "Attempt to read remote file with no ssh session"
            log_error(_this_file, '%s: Attempt to read remote file with no ssh session\n' % self.__class__.__name__)
            import traceback
            traceback.print_stack()
            raise Exception("Cannot read remote file without an SSH session")
        return False

    def get_available_space(self, path, as_user=Users.CURRENT, user_password=None):
        output_text = StringIO.StringIO()
        res = self.process_ops.exec_cmd("df -Ph %s" % quote_path(path),
                            as_user,
                            user_password,
                            output_handler = output_text.write)

        output_text = sanitize_sudo_output(output_text.getvalue()).strip()
        
        available = "Could not determine"
        if output_text:
            tokens = output_text.split("\n")[-1].strip().split()
            available = "%s of %s available" % (tokens[3], tokens[1])
        
        return available

    def get_file_owner(self, filename, as_user=Users.CURRENT, user_password=None):
        if self.ssh:
            if self.target_os == wbaOS.linux:
                command = 'stat -c %U '
            else:
                command = 'stat -f "%Su" '
                
            command = command + quote_path(filename)
                  
            if as_user != Users.CURRENT:
                command = wrap_for_sudo(command, self.process_ops.sudo_prefix, as_user)
                
            out, ret = self.ssh.exec_cmd(command, as_user, user_password)
            
            if ret != 0:
                raise InvalidPasswordError('Incorrect password for sudo')
                
            return out.strip()
        else:
            print "Attempt to read remote file with no ssh session"
            log_error(_this_file, '%s: Attempt to read remote file with no ssh session\n' % self.__class__.__name__)
            import traceback
            traceback.print_stack()
            raise Exception("Cannot read remote file without an SSH session")
        return False
        
    def create_directory(self, path, as_user = Users.CURRENT, user_password = None):
        if as_user == Users.CURRENT:
            try:
                self.ssh.mkdir(path)
            except (IOError, OSError), err:
                if err.errno == errno.EACCES:
                    raise PermissionDeniedError("Could not create directory %s" % path)
                raise err
        else:
            output = []
            command = wrap_for_sudo('/bin/mkdir ' + quote_path(path), self.process_ops.sudo_prefix, as_user)
            out, ret = self.ssh.exec_cmd(command, as_user, user_password)
            if ret != 0:
                raise RuntimeError(out)


    def remove_directory(self, path, as_user = Users.CURRENT, user_password = None):
        if as_user == Users.CURRENT:
            try:
                self.ssh.rmdir(path)
            except (IOError, OSError), err:
                if err.errno == errno.EACCES:
                    raise PermissionDeniedError("Could not remove directory %s" % path)
                raise err
        else:
            output = []
            command = wrap_for_sudo('/bin/rmdir ' + quote_path(path), self.process_ops.sudo_prefix, as_user)
            out, ret = self.ssh.exec_cmd(command, as_user, user_password)
            if ret != 0:
                raise RuntimeError(out)

    def delete_file(self, path, as_user = Users.CURRENT, user_password = None):
        if as_user == Users.CURRENT:
            try:
                self.ssh.remove(path)
            except (IOError, OSError), err:
                if err.errno == errno.EACCES:
                    raise PermissionDeniedError("Could not delete file %s" % path)
                raise err
        else:
            output = []
            command = wrap_for_sudo('/bin/rm ' + quote_path(path), self.process_ops.sudo_prefix, as_user)
            out, ret = self.ssh.exec_cmd(command, as_user, user_password)
            if ret != 0:
                raise RuntimeError(out)

    # UseCase: If get_file_content fails with exception of access, try sudo
    def get_file_content(self, filename, as_user = Users.CURRENT, user_password = None): # may raise IOError
        if self.ssh:
            if as_user != Users.CURRENT:
                command = wrap_for_sudo('cat %s' % filename, self.process_ops.sudo_prefix, as_user)
                out, ret = self.ssh.exec_cmd(command, as_user, user_password)
                
                # Validating the type of error to return the proper exception
                if ret != 0:
                    if 'No such file or directory' in out:
                        error = IOError()
                        error.errno = errno.ENOENT
                        raise error
                    else:
                        raise Exception('Error executing "%s" via SSH in remote server' % command)
                        
                if out.startswith('EnterPasswordHere'):
                    _, out = out.split('\n', 1)  # Strip the first line
                return out
            else:
                try:
                    return self.ssh.get_contents(filename)
                except (IOError, OSError), exc:
                    if exc.errno == errno.EACCES:
                        raise PermissionDeniedError("Permission denied attempting to read file %s" % filename)
        else:
            print "Attempt to read remote file with no ssh session"
            log_error(_this_file, '%s: Attempt to read remote file with no ssh session\n' % self.__class__.__name__)
            import traceback
            traceback.print_stack()
            raise Exception("Cannot read remote file without an SSH session")
        return None

    #-----------------------------------------------------------------------------
    def save_file_content(self, filename, content, as_user = Users.CURRENT, user_password = None):
        self.save_file_content_and_backup(filename, content, None, as_user, user_password)

    #-----------------------------------------------------------------------------
    def save_file_content_and_backup(self, path, content, backup_extension, as_user = Users.CURRENT, user_password = None):
        # Check if dir, where config file will be stored is writable
        dirname, filename = splitpath(path)

        if as_user == Users.CURRENT:
            try:
                self.check_dir_writable(dirname.strip(" \r\t\n"))
            except Exception:
                raise PermissionDeniedError("Cannot write to directory %s" % dirname)

        if self.ssh is not None:
            ## Get home dir for using as tmpdir
            homedir, status = self.process_ops.get_cmd_output("echo ~")
            if type(homedir) is unicode:
                homedir = homedir.encode("utf8")
            if type(homedir) is str:
                homedir = homedir.strip(" \r\t\n")
            else:
                homedir = None
            log_debug2(_this_file, '%s: Got home dir: "%s"\n' % (self.__class__.__name__, homedir) )

            if not homedir:
                raise Exception("Unable to get path for remote home directory")

            tmpfilename = homedir + "/.wba.temp"

            log_debug(_this_file, '%s: Remotely writing contents to temporary file "%s"\n' % (self.__class__.__name__, tmpfilename) )
            log_debug3(_this_file, '%s: %s\n' % (self.__class__.__name__, content) )
            self.ssh.set_contents(tmpfilename, content)

            if backup_extension:
                log_debug(_this_file, '%s: Backing up %s\n' % (self.__class__.__name__, path) )
                backup_cmd = "/bin/cp " + quote_path(path) + " " + quote_path(path+backup_extension)
                self.process_ops.exec_cmd(backup_cmd, as_user, user_password)

            copy_to_dest = "/bin/cp " + quote_path(tmpfilename) + " " + quote_path(path)
            delete_tmp = "/bin/rm " + quote_path(tmpfilename)
            log_debug(_this_file, '%s: Copying file to final destination: "%s"\n' % (self.__class__.__name__, copy_to_dest) )
            
            # The new file is copied as the root user
            self.process_ops.exec_cmd(copy_to_dest, Users.ADMIN, user_password)
            
            # If needed changes the ownership of the new file to the requested user
            if as_user != Users.ADMIN:
                
                # TODO: Does this need any validation being executed by root??
                self.process_ops.exec_cmd("chown %s %s" % (as_user, quote_path(path)),
                                  as_user   = Users.ADMIN,
                                  user_password = user_password)
            
            log_debug(_this_file, '%s: Deleting tmp file: "%s"\n' % (self.__class__.__name__, delete_tmp) )
            self.process_ops.exec_cmd(delete_tmp)
        else:
            raise Exception("No SSH session active, cannot save file remotely")



    def check_dir_writable(self, path, as_user=Users.CURRENT, user_password=None):
        filename = joinpath(path, '.wb_write_test')
        
        output = []
        
        res = self.process_ops.exec_cmd('touch ' + quote_path(filename),
                            as_user,
                            user_password,
                            output_handler = lambda line, l= output: l.append(line))
                            
        if res == 0:
            self.process_ops.exec_cmd('/bin/rm ' + quote_path(filename),
                            as_user,
                            user_password,
                            output_handler = lambda line:None)
        else:
            output = '\n'.join(output)
            error = None
            if "No such file or directory" in output:
                error = IOError(errno.ENOENT, "The directory does not exist")
            elif "Permission denied" in output:
                error = PermissionDeniedError("Permission denied for writing")
                error.errno = errno.EACCES
            else:
                error = Exception("Unable to verify directory is writable: %s" % output.strip())
                
            raise error
          
        return res == 0
        


    def listdir(self, path, as_user = Users.CURRENT, user_password = None): # base operation to build file_exists and remote file selector
        dlist = []
        if self.ssh is not None:
            if as_user == Users.CURRENT:
                (output, status) = self.ssh.exec_cmd('/bin/ls -1 -p %s' % path)
                if status == 0:
                    raw_list = output.split('\n')
                    for item in raw_list:
                        if item[-1:] == '/':
                            dlist.insert(0, item)
                        else:
                            dlist.append(item)
            else:
                output = StringIO.StringIO()
                rc = self.process_ops.exec_cmd("/bin/ls -1 -p %s" % quote_path(path),
                                          as_user   = as_user,
                                          user_password = user_password,
                                          output_handler = output.write)
                output = output.getvalue()
                if rc != 0:
                    if "No such file or directory" in output:
                        raise IOError(errno.ENOENT, "Directory %s does not exist" % path)
                    elif "Permission denied" in output:
                        raise PermissionDeniedError("Permission denied for reading from %s" % path)
                    else:
                        raise Exception(output.strip())
                else:
                    dlist = [s.strip() for s in output.strip().split("\n")]
        else:
            raise Exception("No SSH session active, cannot get remote directory list")
            
        return dlist
        

_file_ops_classes.append(FileOpsRemoteUnix)


#===============================================================================
# remote win sudo/non-sudo
#   save_file_content  - sftp
#   get_file_content   - sftp
#   copy_file          - sftp
#   get_dir_access     - sftp(returns either rw or ro or none)
#   listdir            - sftp(for ro-dirs)
class FileOpsRemoteWindows(FileOpsRemoteUnix):
    @classmethod
    def match(cls, target_os, connection_method):
        return connection_method == "ssh" and target_os == wbaOS.windows

    def __init__(self, process_ops, ssh, target_os):
        FileOpsRemoteUnix.__init__(self, process_ops, ssh, target_os)
        self.process_ops = process_ops
        self.ssh = ssh

    def file_exists(self, filename, as_user=Users.CURRENT, user_password=None):
        if self.ssh:
            try:
                return self.ssh.file_exists(filename)
            except IOError, exc:
                raise
        else:
            print "Attempt to read remote file with no ssh session"
            log_error(_this_file, '%s: Attempt to read remote file with no ssh session\n' % self.__class__.__name__)
            import traceback
            traceback.print_stack()
            raise Exception("Cannot read remote file without an SSH session")
        return False

    def get_available_space(self, path, as_user=Users.CURRENT, user_password=None):
        out = []        

        res = self.process_ops.exec_cmd('dir %s' % quote_path(path),
                            as_user,
                            user_password,
                            output_handler = lambda line, l = out:l.append(line))

        available = "Could not determine"
        if res == 0 and len(out):
            measures = ['B', 'KB', 'MB', 'GB', 'TB']
            tokens = out[0].strip().split("\n")[-1].strip().split()
            
            total = float(tokens[2].replace(",",""))
            index = 0
            while index < len(measures) and total > 1024:
                total = total / 1024
                index = index + 1


            available = "%.2f %s available" % (total, measures[index])
        
        return available

    def create_directory(self, path, as_user = Users.CURRENT, user_password = None):
        if as_user == Users.CURRENT:
            try:
                self.ssh.mkdir(path)
            except OSError, err:
                if err.errno == errno.EACCES:
                    raise PermissionDeniedError("Could not create directory %s" % path)
                raise err
        else:
            output = []
            command = wrap_for_sudo('mkdir ' + quote_path_win(path), self.process_ops.sudo_prefix, as_user)
            out, ret = self.ssh.exec_cmd(command, as_user, user_password)
            if ret != 0:
                raise RuntimeError(out)


    def remove_directory(self, path, as_user = Users.CURRENT, user_password = None):
        if as_user == Users.CURRENT:
            try:
                self.ssh.rmdir(path)
            except OSError, err:
                if err.errno == errno.EACCES:
                    raise PermissionDeniedError("Could not remove directory %s" % path)
                raise err
        else:
            output = []
            command = wrap_for_sudo('rmdir ' + quote_path_win(path), self.process_ops.sudo_prefix, as_user)
            out, ret = self.ssh.exec_cmd(command, as_user, user_password)
            if ret != 0:
                raise RuntimeError(out)

    def delete_file(self, path, as_user = Users.CURRENT, user_password = None):
        if as_user == Users.CURRENT:
            try:
                self.ssh.remove(path)
            except OSError, err:
                if err.errno == errno.EACCES:
                    raise PermissionDeniedError("Could not delete file %s" % path)
                raise err
        else:
            output = []
            command = wrap_for_sudo('del ' + quote_path_win(path), self.process_ops.sudo_prefix, as_user)
            out, ret = self.ssh.exec_cmd(command, as_user, user_password)
            if ret != 0:
                raise RuntimeError(out)

    def save_file_content_and_backup(self, path, content, backup_extension, as_user = Users.CURRENT, user_password = None):
        # Check if dir, where config file will be stored is writable
        dirname, filename = splitpath(path)

        if as_user == Users.CURRENT:
            try:
                self.check_dir_writable(dirname.strip(" \r\t\n"))
            except Exception, e:
                print e
                raise PermissionDeniedError("Cannot write to directory %s" % dirname)

        if self.ssh is not None:
            ## Get temp dir for using as tmpdir
            tmpdir, status = self.process_ops.get_cmd_output("echo %temp%")
            if type(tmpdir) is unicode:
                tmpdir = tmpdir.encode("utf8")
            if type(tmpdir) is str:
                tmpdir = tmpdir.strip(" \r\t\n")
                if tmpdir[1] == ":":
                    tmpdir = tmpdir[2:]
                else:
                    log_debug(_this_file, '%s: Temp directory path "%s" is not in expected form. The expected form is something like "C:\\Windows\\Temp"\n' % (self.__class__.__name__, tmpdir) )
                    tmpdir = None
                log_debug2(_this_file, '%s: Got temp dir: "%s"\n' % (self.__class__.__name__, tmpdir) )
            else:
                tmpdir = None

            if not tmpdir:
                tmpdir = dirname

            tmpfilename = tmpdir + r"\workbench-temp-file.ini"

            log_debug(_this_file, '%s: Remotely writing contents to temporary file "%s"\n' % (self.__class__.__name__, tmpfilename) )
            log_debug3(_this_file, '%s: %s\n' % (self.__class__.__name__, content) )
            self.ssh.set_contents(tmpfilename, content)

            if backup_extension:
                log_debug(_this_file, '%s: Backing up "%s"\n' % (self.__class__.__name__, path) )
                backup_cmd = "copy /y " + quote_path_win(path) + " " + quote_path_win(path+backup_extension)
                msg, code = self.process_ops.get_cmd_output(backup_cmd)
                if code != 0:
                    print backup_cmd, "->", msg
                    log_error(_this_file, '%s: Error backing up file: %s\n' % (self.__class__.__name__, backup_cmd+'->'+msg) )
                    raise RuntimeError("Error backing up file: %s" % msg)

            copy_to_dest = "copy /y " + quote_path_win(tmpfilename) + " " + quote_path_win(path)
            delete_tmp = "del " + quote_path_win(tmpfilename)
            log_debug(_this_file, '%s: Copying file to final destination: "%s"\n' % (self.__class__.__name__, copy_to_dest) )
            msg, code = self.process_ops.get_cmd_output(copy_to_dest)
            if code != 0:
                print copy_to_dest, "->", msg
                log_error(_this_file, '%s: Error copying temporary file over destination file: %s\n%s to %s\n' % (self.__class__.__name__, msg, tmpfilename, path) )
                raise RuntimeError("Error copying temporary file over destination file: %s\n%s to %s" % (msg, tmpfilename, path))
            log_debug(_this_file, '%s: Deleting tmp file: "%s"\n' % (self.__class__.__name__, delete_tmp) )
            msg, code = self.process_ops.get_cmd_output(delete_tmp)
            if code != 0:
                print "Could not delete temporary file %s: %s" % (tmpfilename, msg)
                log_info(_this_file, '%s: Could not delete temporary file "%s": %s\n' % (self.__class__.__name__, tmpfilename, msg) )
        else:
            raise Exception("No SSH session active, cannot save file remotely")

    # UseCase: If get_file_content fails with exception of access, try sudo
    def get_file_content(self, filename, as_user = Users.CURRENT, user_password = None):
        if self.ssh:
            # Supposedly in Windows, sshd account has admin privileges, so Users.ADMIN can be ignored
            try:
                return self.ssh.get_contents(filename)
            except IOError, exc:
                if exc.errno == errno.EACCES:
                    raise PermissionDeniedError("Permission denied attempting to read file %s" % filename)
        else:
            print "Attempt to read remote file with no ssh session"
            import traceback
            traceback.print_stack()
            raise Exception("Cannot read remote file without an SSH session")

    def check_dir_writable(self, path, as_user=Users.CURRENT, user_password=None):
        msg, code = self.process_ops.get_cmd_output('echo 1 > ' + quote_path(path + "/wba_tmp_file.bak"))
        ret = (code == 0)
        if ret:
            msg, code = self.process_ops.get_cmd_output('del ' + quote_path(path + "/wba_tmp_file.bak"))
        return ret

    def listdir(self, path, as_user = Users.CURRENT, user_password = None): # base operation to build file_exists and remote file selector
        # TODO: user elevation
        sftp = self.ssh.getftp()
        (dirs, files) = sftp.ls(path)
        ret = []
        for d in dirs:
            ret.append(d + "/")
        return tuple(ret + list(files))
        
_file_ops_classes.append(FileOpsRemoteWindows)


#===============================================================================
#
#===============================================================================
class ServerManagementHelper(object):
    def __init__(self, profile, ssh):
        self.tmp_files = [] # TODO: make sure the files will be deleted on exit

        self.profile = profile

        klass = None
        match_tuple = (profile.host_os, profile.target_os, profile.connect_method)
        for k in _process_ops_classes:
            if k.match(match_tuple):
                klass = k
                break
        if klass:
        
            sudo_prefix=profile.sudo_prefix
            
            if not sudo_prefix:
                sudo_prefix = default_sudo_prefix
        
            # use -k to force the password to be requested, otherwise we'll be stuck waiting for the password prompt
            # This is necessary in osx also because without it an I/O error happens for unknown reasons... in linux this doesn't seem necessary
            
            if profile.target_os == wbaOS.darwin and " -k " not in sudo_prefix:
                sudo_prefix = sudo_prefix.replace("sudo", "sudo -k ")

            self.shell = klass(sudo_prefix=sudo_prefix, ssh=ssh)
            self.shell.post_init()
        else:
            raise Exception("Unsupported administration target type: %s"%str(match_tuple))

        klass = None
        for k in _file_ops_classes:
            if k.match(profile.target_os, profile.connect_method):
                klass = k
                break

        if klass:
            self.file = klass(self.shell, ssh=ssh, target_os = profile.target_os)
        else:
            raise Exception("Unsupported administration target type: %s:%s" % (str(profile.target_os), str(profile.connect_method)))


    @property
    def cmd_output_encoding(self):
        if self.shell:
            return self.shell.cmd_output_encoding
        return ""

    #-----------------------------------------------------------------------------
    def check_dir_writable(self, path, as_user=Users.CURRENT, user_password=None):
        return self.file.check_dir_writable(path, as_user, user_password)

    #-----------------------------------------------------------------------------
    def file_exists(self, path, as_user = Users.CURRENT, user_password=None):
        return self.file.file_exists(path, as_user, user_password)

    #-----------------------------------------------------------------------------
    def get_available_space(self, path, as_user = Users.CURRENT, user_password=None):
        return self.file.get_available_space(path, as_user, user_password)

    #-----------------------------------------------------------------------------
    def get_file_owner(self, path, as_user = Users.CURRENT, user_password=None):
        return self.file.get_file_owner(path, as_user, user_password)

    #-----------------------------------------------------------------------------
    def create_directory(self, path, as_user = Users.CURRENT, user_password=None):
        return self.file.create_directory(path, as_user, user_password)

    #-----------------------------------------------------------------------------
    def remove_directory(self, path, as_user = Users.CURRENT, user_password=None):
        return self.file.remove_directory(path, as_user, user_password)

    #-----------------------------------------------------------------------------
    def delete_file(self, path, as_user = Users.CURRENT, user_password=None):
        return self.file.delete_file(path, as_user, user_password)

    #-----------------------------------------------------------------------------
    # Make sure that file is readable only by user!
    def make_local_tmpfile(self):
        # Here we create that file name blah-blah-blah
        # if total_success:
        #   self.tmp_files.append(filename)
        raise NotImplementedError

    #-----------------------------------------------------------------------------
    def get_file_content(self, path, as_user = Users.CURRENT, user_password = None):
        return self.file.get_file_content(path, as_user=as_user, user_password=user_password)

    #-----------------------------------------------------------------------------
    def set_file_content(self, path, contents, as_user = Users.CURRENT, user_password = None):
        return self.file.save_file_content(path, contents, as_user=as_user, user_password=user_password)

    #-----------------------------------------------------------------------------
    def listdir(self, path, as_user = Users.CURRENT, user_password = None):
        return self.file.listdir(path, as_user, user_password)

    #-----------------------------------------------------------------------------
    def set_file_content_and_backup(self, path, contents, backup_extension, as_user = Users.CURRENT, user_password = None):
        if type(contents) is unicode:
            contents = contents.encode("utf8")
        return self.file.save_file_content_and_backup(path, contents, backup_extension, as_user=as_user, user_password=user_password)

    #-----------------------------------------------------------------------------
    # Returns Status Code
    # Text Output is given to output_handler, if there is any
    def execute_command(self, command, as_user = Users.CURRENT, user_password=None, output_handler=None):
        return self.shell.exec_cmd(command, as_user, user_password, output_handler)
