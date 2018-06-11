# Copyright (c) 2012, Oracle and/or its affiliates. All rights reserved.
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
import os
import re
import uuid
import mforms
import StringIO
import ConfigParser
import grt
import errno
from datetime import datetime, timedelta
from workbench.db_utils import QueryError, escape_sql_string
from xml.dom.minidom import parseString
from wb_server_management import wbaOS
from wb_admin_meb_syshelpers import WBBackupUnixInterface, WBBackupWindowsInterface, Frequency
from grt import log_debug, log_debug2, log_debug3, log_warning, log_info, log_error
_this_file = os.path.basename(__file__)

from wb_common import OperationCancelledError, parentdir, joinpath, splitpath, Users, sanitize_sudo_output


class BackupRestoreValidationException(RuntimeError):
    pass


def add_table_field_label(table, row, caption):
    label = mforms.newLabel(caption)
    label.set_text_align(mforms.MiddleRight)
    #label.set_style(mforms.BoldStyle)
    label.set_size(250, -1)
    table.add(label, 0, 1, row, row+1, mforms.HFillFlag)
    return label


def add_table_field_help(table, row, text):
    label = mforms.newLabel(text)
    label.set_style(mforms.SmallHelpTextStyle)
    table.add(label, 2, 3, row, row+1, mforms.HFillFlag)
    return label


def add_table_field_value(table, row, control, flags = mforms.HFillFlag|mforms.HExpandFlag, col = 2):
    table.add(control, col-1, col, row, row+1, flags)

def add_table_info_row(table, row, caption, defvalue = "n/a"):
    if caption is not None:
        add_table_field_label(table, row, caption)
    label = mforms.newLabel(defvalue)
    add_table_field_value(table, row, label)
    return label

def read_config_value(document, section, item, mandatory = False, default = None):
    value = default
      
    try:
        value = document.get(section, item)
    except:
        if mandatory:
            raise
        else:
            pass
      
    return value


class WBBackupContext:
    _initialized = False
    def __init__(self, server_profile, ctrl_be):
        self.server_profile = server_profile
        self.ctrl_be = ctrl_be
        self.server_interface = None
        self.config = None
        self._needs_admin = None


    def init_config(self):
        if self._initialized:
            return False
        self._initialized = True

        if self.server_profile.target_os == wbaOS.windows:
            self.server_interface = WBBackupWindowsInterface(self)
        else:
            self.server_interface = WBBackupUnixInterface(self)
        self.config = WBBackupConfig(self)

        self.config.load()


    @property
    def is_local(self):
        return self.server_profile.is_local

    @property
    def has_connection(self):
        return self.ctrl_be.is_sql_connected()

    def load_backup_profiles(self):
        backup_files = []
        profiles = {}
        if self.config.loaded:
            backup_files = self.ctrl_be.server_helper.listdir(self.config.backup_home)

        for file in backup_files:
            # For now assummes all the xmls on the folder are
            # backup profiles
            if file.endswith(".cnf"):
                profile = WBBackupProfile(self)
                if profile.load(file):
                    profiles[profile.label] = profile

        return profiles

    def count_backup_profiles(self):
        backup_files = []
        if self.config.loaded:
            backup_files = self.ctrl_be.server_helper.listdir(self.config.backup_home)

        count = 0
        for file in backup_files:
            # For now assummes all the xmls on the folder are
            # backup profiles
            if file.endswith(".cnf"):
                count = count + 1

        return count

    @property
    def mysql_user(self):
        return self.config.mysql_user


class WBBackupConfig(object):
    def __init__(self, context):
        self._context = context
        self._server = context.ctrl_be.server_helper
        self.backup_command = ""
        self.backup_account = "mysqlbackup"
        self.backup_account_password = None
        self.backup_account_exists = False

        # Target server attributes
        self.server_version = ""
        self.os = ""
        self.host = ""
        self.port = ""
        self.socket = ""
        self.datadir = ""
        self.innodb_data_home_dir = ""
        self.mysql_user = ""
        self.changed = False

        if self._context.server_profile.target_is_windows:
            self.backup_home = "C:\\MysqlBackupHome"
        else:
            self.backup_home = "/var/db/mysqlbackuphome"
            
        # Flags...
        self.loaded = False
        self.valid = False
        self.valid_command = False
        self.command_error = ""
        self.valid_home = False
        self.home_error = ""
        self.valid_backup_account = False
        self.backup_account_error = ""

        self._file_name = joinpath(parentdir(self._context.server_profile.config_file_path), "mysqlwb_meb.cnf")

        self.changed = False


    def __setattr__(self, name, value):
        if name in self.__dict__ and self.__dict__[name] != value:        
            self.__dict__["changed"] = True
            
        self.__dict__[name] = value
            
        
    def get_admin_password(self):
        if self.user_password is not None:
            return self.user_password
        self.user_password = self.ctrl_be.password_handler.get_password_for("file")
        return self.user_password

    def forget_admin_password(self):
        self.ctrl_be.password_handler.reset_password_for("file")

       
    def load(self):
        get_file_content_cb = lambda as_user, user_password: self._server.get_file_content(self._file_name, as_user, user_password)
            
        try:
            if self._context.server_profile.target_os == wbaOS.windows:
                user = Users.CURRENT
            else:
                user = Users.ADMIN

            self._context.server_interface._needs_admin = True
            config_data = self._context.server_interface.perform_as_user(user, get_file_content_cb)
            if config_data:
                config_data = sanitize_sudo_output(config_data)

                doc = ConfigParser.ConfigParser()

                doc.readfp(StringIO.StringIO(config_data))
                
                self.backup_command = read_config_value (doc, 'wbbackup', 'command', True)
                self.backup_home = read_config_value (doc, 'wbbackup', 'home', True)
                self.user = read_config_value (doc, 'wbbackup', 'user', True)
                self.backup_account_password = read_config_value (doc, 'wbbackup', 'password', True)
                doc.set('wbbackup', 'password', self.backup_account_password)
                
                self.server_version = read_config_value (doc, 'target_server', 'server_version')
                self.os = read_config_value (doc, 'target_server', 'os')
                self.host = read_config_value (doc, 'target_server', 'host')
                self.port = read_config_value (doc, 'target_server', 'port')
                self.socket = read_config_value (doc, 'target_server', 'socket')
                self.datadir = read_config_value (doc, 'target_server', 'datadir')
                self.innodb_data_home_dir = read_config_value (doc, 'target_server', 'innodb_data_home_dir')
                self.mysql_user = read_config_value (doc, 'target_server', 'mysql_os_user')
                
                self.loaded = True

                self.changed = False

        # This exception is harmless, nothing needs to be displayed whenever the configuration failed
        # To read, the user will be directed to the configuration screen on the UI
        # So the error will just get logged
        except Exception, e:
            log_error(_this_file, "Error Reading Configuration : File %s: %s\n" % (self._file_name, e))
        
        return self.loaded
              

    def autodetect(self, server_interface):
        output_text = StringIO.StringIO()

        command = server_interface.get_verify_backup_command()
        
        result = self._server.execute_command(command, as_user=Users.CURRENT, user_password=None, output_handler=output_text.write)
        
        if result == 0:
            self.backup_command = output_text.getvalue().strip()
        else:
            self.backup_command = "mysqlbackup"


    def check_backup_account_exists(self):
        before_changed = self.changed
        try:
            self._context.ctrl_be.exec_query("SHOW GRANTS FOR %s@localhost" % self.backup_account)
            self.backup_account_exists = True
            self.changed = before_changed
            return
        except QueryError, e:
            if e.error != 1141: # ERROR 1141 (42000): There is no such grant defined for user 'mysqlbackup' on host 'localhost'
                raise
        self.backup_account_error = "The account mysqlbackup does not exist on this server."
        self.backup_account_exists = False
        self.changed = before_changed


    def create_backup_account(self):
        grt.log_info("MEB", "Creating user for mysqlbackup %s@localhost\n" % self.backup_account)

        self._context.ctrl_be.exec_sql("CREATE USER %s@localhost" % (self.backup_account))
        self._context.ctrl_be.exec_sql("SET PASSWORD FOR %s@localhost = PASSWORD('%s')" % (self.backup_account, escape_sql_string(self.backup_account_password)))
        self._context.ctrl_be.exec_sql("GRANT RELOAD, REPLICATION CLIENT, SUPER ON *.* TO %s@localhost" % self.backup_account)
        self._context.ctrl_be.exec_sql("GRANT CREATE, INSERT, DROP ON mysql.ibbackup_binlog_marker TO %s@localhost" % self.backup_account)
        self._context.ctrl_be.exec_sql("GRANT CREATE, INSERT, DROP ON mysql.backup_progress TO %s@localhost" % self.backup_account)
        self._context.ctrl_be.exec_sql("GRANT CREATE, INSERT, DROP, SELECT ON mysql.backup_history TO %s@localhost" % self.backup_account)
        self._context.ctrl_be.exec_sql("GRANT CREATE TEMPORARY TABLES ON mysql.* TO %s@localhost" % self.backup_account)
        self._context.ctrl_be.exec_sql("FLUSH PRIVILEGES")

        self.backup_account_exists = True


    def save(self):
        if not self.backup_account_exists:
            self.create_backup_account()

        doc = ConfigParser.ConfigParser()
        doc.add_section('wbbackup')
        doc.set('wbbackup', 'command', self.backup_command)
        doc.set('wbbackup', 'home', self.backup_home)
        doc.set('wbbackup', 'user', self.backup_account)
        doc.set('wbbackup', 'password', self.backup_account_password)
        
        doc.add_section('target_server')
        doc.set('target_server', 'server_version', self.server_version)
        doc.set('target_server', 'os', self.os)
        doc.set('target_server', 'host', self.host)
        doc.set('target_server', 'port', self.port)
        doc.set('target_server', 'socket', self.socket)
        doc.set('target_server', 'datadir', self.datadir)
        doc.set('target_server', 'innodb_data_home_dir', self.innodb_data_home_dir)
        doc.set('target_server', 'mysql_os_user', self.mysql_user)
        
        stream = StringIO.StringIO()
        
        stream.write("# Server wide settings for MySQL Workbench, Enterprise Backup\n\n")
        
        doc.write(stream)
        
        set_file_content_cb = lambda as_user, user_password: self._server.set_file_content(self._file_name, stream.getvalue(), as_user, user_password)
        
        try:
            self._context.server_interface.perform_as_user(Users.ADMIN, set_file_content_cb)
            # Once saved resets the changed flag
            self.changed = False
            # Flag the configs as valid
            self.loaded = True

            # On windows deploys the windows script for backups
            if self._context.server_profile.target_os == wbaOS.windows:
                self.deploy_windows_script()

            self.changed = False

        except OperationCancelledError:
            return

    def deploy_windows_script(self):
        script = """
' Copyright (c) 2012, Oracle and/or its affiliates. All rights reserved.
'
' This program is free software; you can redistribute it and/or
' modify it under the terms of the GNU General Public License as
' published by the Free Software Foundation; version 2 of the
' License.
'
' This program is distributed in the hope that it will be useful,
' but WITHOUT ANY WARRANTY; without even the implied warranty of
' MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
' GNU General Public License for more details.
'
' You should have received a copy of the GNU General Public License
' along with this program; if not, write to the Free Software
' Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
' 02110-1301  USA

' These variables will be retrieved from the backup profile
DIM command
DIM backups_home
DIM backup_dir
DIM incremental_backup_dir

SET fso = CreateObject ("Scripting.FileSystemObject")

' Reads the received parameters
compress = Wscript.Arguments.Item(1)
incremental = Wscript.Arguments.Item(2)
bkcommand = Wscript.Arguments.Item(3)

IF Wscript.Arguments.Count > 4 THEN
  file_name = Wscript.Arguments.Item(4)
ELSE
  file_name = ""
END IF

' Reads from the backup configuration the information needed to
' create the command
ReadBackupConfiguration()

' Reads from the backup profile the information needed to
' create the command
ReadProfileData(backups_home & "\\" & Wscript.Arguments.Item(0))

' Creates the timestamp used for the backup directory and log
' Unless specified differently this is the default behavior
target_name = GetTargetName()

' Starts creating the backup command
backup_command = \"\"\"\" & command & \"\"\"\" & " --defaults-file=\"\"\" & backups_home & "\\" & Wscript.Arguments.Item(0) & \"\"\"\"

' Adds to the command the compress/incremental options if needed
IF compress = "1" THEN backup_command = backup_command & " --compress"

' The final path and log name will  be configured based on
' The type of backup and other input parameters
path_parameter = " --backup-dir"

IF incremental = "1" THEN 
	backup_command = backup_command & " --incremental"
	backup_dir = incremental_backup_dir
    path_parameter = " --incremental-backup-dir"
END IF

' Configures the backup directory for the backup
' When a filename is received uses that to create the target backup and log
' In other case, uses the timestamp
IF file_name <> "" THEN
	target_name = file_name
END IF

backup_command = backup_command & path_parameter & "=" & backup_dir & "\\" & target_name

' Appends the command parameter for the mysqlbackup
backup_command = backup_command & " " & bkcommand

' Creates the log file
Set logFile = fso.CreateTextFile(backup_dir & "\\" & target_name & ".log")

' Creates the scripting shell to execute the backup
Set shell = WScript.CreateObject("WScript.Shell")

' Executes the backup
Set exec = shell.Exec(backup_command)

' Reads the command output and creates the log file
Set stderr = exec.StdErr
While Not stderr.AtEndOfStream
   strLine = stderr.ReadLine
   logFile.WriteLine(strLine)
Wend

logFile.Close()

' Function used to create the target name in case it is a timestamp
FUNCTION GetTargetName
  
  ts = Now()

  ts_short = FormatDateTime(ts, vbShortTime)

  ' Formats the elements to be 2 chars length with leading 0's
  ' if needed
  the_month = Right("0" & Month(ts), 2)
  the_day = Right("0" & Day(ts), 2)
  the_hour = Right("0" & MID(ts_short, 1, InStr(ts_short, ":") -1), 2)
  the_minute = Right("0" & Minute(ts), 2)
  the_second = Right("0" & Second(ts), 2)
  
  GetTargetName = Year(ts) & "-" & the_month & "-" & the_day & "_" & the_hour & "-" & the_minute & "-" & the_second

END FUNCTION

' Reads from the profile backup the information needed for the
' operation
SUB ReadBackupConfiguration()

  backup_config_file = fso.GetParentFolderName(wscript.ScriptFullName) & "\\mysqlwb_meb.cnf"

  set file = fso.OpenTextFile(backup_config_file)
  
  WHILE NOT file.AtEndOfStream
    strLine = file.ReadLine()
    strLine = TRIM(strLine)
	
    lineLen = LEN(strLine)
    IF (lineLen > 0) THEN
      IF (INSTR(1, strLine, "'", 1) <> 1) AND (INSTR(1, strLine, "[", 1) <> 1) THEN
        index = INSTR(1, strLine, "=", 1)
		IF index > 1 THEN
        attName  = LCASE(TRIM(MID(strLine, 1, index - 1)))
        attValue = TRIM(MID(strLine, index + 1, lineLen - index))
		
		SELECT CASE attName
			CASE "command"
				IF attValue <> "" THEN command = attValue
			CASE "home"
				IF attValue <> "" THEN backups_home = attValue
		END SELECT
		END IF
      END IF
    END IF
  WEND
  
  file.Close()
END SUB

' Reads from the profile backup the information needed for the
' operation
SUB ReadProfileData(fileName)

  set file = fso.OpenTextFile(fileName)
  
  WHILE NOT file.AtEndOfStream
    strLine = file.ReadLine()
    strLine = TRIM(strLine)

    lineLen = LEN(strLine)
    IF (lineLen > 0) THEN
      IF (INSTR(1, strLine, "'", 1) <> 1) AND (INSTR(1, strLine, "[", 1) <> 1) THEN
		
        index = INSTR(1, strLine, "=", 1)

        IF index > 1 THEN
            attName  = LCASE(TRIM(MID(strLine, 1, index - 1)))
            attValue = TRIM(MID(strLine, index+1, lineLen - index))
		
		    SELECT CASE attName
			    CASE "command"
				    IF attValue <> "" THEN command = attValue
			    CASE "backups_home"
				    IF attValue <> "" THEN backups_home = attValue
			    CASE "backup_dir"
				    IF attValue <> "" THEN backup_dir = attValue
			    CASE "incremental_backup_dir"
				    IF attValue <> "" THEN incremental_backup_dir = attValue
		    END SELECT
        END IF
      END IF
    END IF
  WEND
  
  file.Close()
END SUB
        """
        script_name = joinpath(parentdir(self._context.server_profile.config_file_path), "mysqlwbbackup.vbs")
        set_file_content_cb = lambda as_user, user_password: self._server.set_file_content(script_name, script, as_user, user_password)
        
        try:
          self._context.server_interface.perform_as_user(Users.ADMIN, set_file_content_cb)
          
        except OperationCancelledError:
          return       


    def validate_command(self, command=None):
        if command is None:
            command = self.backup_command

        output_text = StringIO.StringIO()

        # Gets the user domain/user to be used on the file for scheduling
        valid_command = False
        error = "Invalid path to the mysqlbackup command"
        if command != "":
            test_command = "\"%s\" --version" % command

            exec_cb = lambda as_user, user_password: self._context.ctrl_be.server_helper.execute_command(test_command, as_user, user_password, output_text.write)
            self._context.server_interface.perform_as_user(self.mysql_user, exec_cb)
            #self._context.server_interface.execute_command(test_command, gather_output)
            output_text = sanitize_sudo_output(output_text.getvalue()).strip()

            if output_text.startswith('EnterPasswordHere'):
                _, output_text = output_text.split('\n', 1)  # Strip the first line

            if len(output_text) > 0:
                if output_text.startswith("MySQL Enterprise Backup"):
                    tokens = output_text.split()
                    version_tokens = tokens[4].split('.')

                    major = int(version_tokens[0])
                    minor = int(version_tokens[1])
                    revision = int(version_tokens[2])
                    
                    # We require mysqlbackup 3.7.1+
                    if major < 3 or ( major == 3 and minor < 7) or \
                       ( major == 3 and minor == 7 and revision < 1 ):
                        error = "Selected mysqlbackup has version %s, but 3.7.1+ is required." % tokens[4]
                    else:
                        valid_command = True
                        error = ""
                elif "Permission denied" in output_text:
                    error = "Permission denied executing the specified command."
                elif "not found" in output_text:
                    error = "The specified mysqlbackup command was not found."

           
        # Updates the valid flag 
        self.valid_command = valid_command
        self.command_error = error
            
        return (valid_command, error)

    def validate_home(self, home=None):
        internal = False
        if home is None:
            home = self.backup_home
            internal = True

        error = ""
        ret_val = True
        try:
            dir_writable_cb = lambda as_user, user_password: self._context.ctrl_be.server_helper.check_dir_writable(home, as_user, user_password)

            self._context.server_interface._needs_admin = True
            self._context.server_interface.perform_as_user(self.mysql_user, dir_writable_cb)
        except OperationCancelledError, e:
            error = 'User cancelled verification'
            ret_val = False
        except Exception, e:
            error = str(e)
            ret_val = False

        # Updates the valid flag if needed
        if internal:
            self.valid_home = ret_val
            self.home_error = error
            
        return (ret_val, error)


    def validate_backup_account(self, password=None):
        if not self.backup_account_exists:
            return (False, "Backup account doesn't exist")
        if not self.valid_command:
            import traceback
            traceback.print_stack()
            return (False, "Cannot validate account without valid mysqlbackup command")
        internal = False
        if password is None:
            internal = True
            password = self.backup_account_password

        ret_val = True
        # XXX use a temp file for account info
        # must check the account using mysqlbackup, since we must connect locally relative to the target server
        check_command = '"%s" --user=%s --password=%s backup --databases=mysql' % (self.backup_command, self.backup_account, password or '')

        buf = StringIO.StringIO()
        self._context.server_interface.perform_as_user(self.mysql_user, lambda as_user, user_password: self._context.ctrl_be.server_helper.execute_command(check_command, as_user, user_password, buf.write))

        error = ""        
        if "Access denied for user" in buf.getvalue():
            ret_val = False
            error = "Access denied for the backup account"

        if internal:
            self.valid_backup_account = ret_val
            self.backup_account_error = error
            
        return (ret_val, error)

    def validate(self):
        # Because the validation process may affect the
        # changed status, we will prevent that by restoring
        # the status at the end
        changed_before = self.changed

        self.check_backup_account_exists()
        
        self.validate_command()
        self.validate_home()
        self.validate_backup_account()

        error = "\n".join([self.command_error, self.home_error, self.backup_account_error]).strip()
        
        self.valid = (error == "")

        self.changed = changed_before

        return error


class ScheduleData(object):
    def __init__(self):
        self.enabled = False
        self.frequency = 0
        self.month_day = 0
        self.week_day = 0
        self.hour = 0
        self.minute = 0
        self.changed = False

    def __setattr__(self, name, value):
        if name in self.__dict__ and self.__dict__[name] != value:        
            self.__dict__["changed"] = True
            
        self.__dict__[name] = value


class BackupEntry:
    def __init__(self, profile, data_path, log_path):
        self.profile = profile
        self.data_path = data_path
        self.log_path = log_path
        self.error = "Backup data missing" if not data_path else None
        self.metadata = {}
        self.manifest = None


    def set_error(self, err):
        self.error = err

    def process_variables_txt(self, data):
        doc = ConfigParser.ConfigParser()
        try:
            doc.readfp(StringIO.StringIO(data))
        except Exception, e:
            self.set_error("Could not parse backup metadata: %s" % e)
        if not doc.has_section('backup_variables'):
            self.set_error("Backup metadata in unexpected format")
        else:
            self.metadata = dict(doc.items('backup_variables'))

    def process_metadata(self, xmldata):
        doc = parseString(xmldata)
        elem = doc.getElementsByTagName("other_metadata")
        if not elem:
            raise Exception("Backup metadata not in expected format")
        elem = elem[0]
        for ch in elem.childNodes:
            if not ch.nodeName.startswith("#"):
                self.other_metadata[ch.nodeName] = ch.firstChild.nodeValue

    def process_contents(self, xmldata):
        doc = parseString(xmldata)

        def process(node):
            if len(node.childNodes) == 1:
                return node.firstChild.nodeValue
            value = {}
            for ch in node.childNodes:
                if not ch.nodeName.startswith("#"):
                    value[ch.nodeName] = process(ch)
            return value

        self.manifest = process(doc).get('manifest_backup_content', {})

    @property
    def failed(self):
        return self.data_path is None


    @property
    def timestamp(self):
        if self.data_path:
            date, _, time = splitpath(self.data_path)[1].partition("_")
        else:
            tmp = os.path.splitext(self.log_path)[0]
            date, _, time = splitpath(tmp)[1].partition("_")
        return date + " " + time.replace("-", ":")


    @property
    def start_time(self):
        # requires self.process_contents() to have been called previously
        if self.manifest:
            return self.manifest['backup_content']['other_metadata']['start_time']
        return None


    @property
    def end_time(self):
        # requires self.process_contents() to have been called previously
        if self.manifest:
            return self.manifest['backup_content']['other_metadata']['end_time']
        return None


    @property
    def valid(self):
        return self.error is None and self.data_path is not None


    @property
    def status_text(self):
        if self.error:
            return self.error
        if not self.apply_log_done:
            return "apply-log pending"
        else:
            return "OK"

    @property
    def start_lsn(self):
        if self.metadata:
            return long(self.metadata['start_lsn'])
        return None


    @property
    def end_lsn(self):
        if self.metadata:
            return long(self.metadata['end_lsn'])
        return None


    @property
    def is_incremental(self):
        if self.metadata:
            return self.metadata['is_incremental'] == '1'
        return None

    @property
    def is_compressed(self):
        if self.metadata:
            return self.metadata['is_compressed'] == '1'
        return None

    @property
    def is_partial(self):
        if self.metadata:
            return self.metadata['is_partial'] == '1'
        return None

    @property
    def apply_log_done(self):
        if self.metadata:
            return self.metadata['apply_log_done'] == '1'
        return None

    @property
    def summary(self):
        return ""



class WBBackupProfile:
    def __init__(self, context):
        self.context = context
        self.backup_home = self.context.config.backup_home

        # Identification data
        self._uuid = None

        # Connection Data
        self.host = "localhost"
        self.port = 0
        self.socket = ""
        self.source_data_dir = ""
        self.innodb_data_home_dir = ""
        self.user = ""
        self.password = ""
    
        # Destination Data
        self.backup_directory = ""
        self.compress = False
        self.apply_log = False

        # Schedule Data
        self.full_backups = ScheduleData()
        self.inc_backups = ScheduleData()
    
        # Comments Data
        self.label = ""
        self.comment = ""

        # For partial backups
        self.partial_selection = None
    
        # Backup Data cache
        self._backup_file_list = None
        self._backup_log_file_list = None
        self._inc_backup_file_list = None
        self._inc_backup_log_file_list = None
        self._backup_file_info = []
        self._backup_file_info_loaded = False
        self.next_backup = ""
        self.available_space = ""
        
        self.changed = False
        
    def __setattr__(self, name, value):
        if name in self.__dict__ and self.__dict__[name] != value:        
            self.__dict__["changed"] = True
            
        self.__dict__[name] = value
        
    @property
    def has_changed(self):
        return self.changed or self.full_backups.changed or self.inc_backups.changed
        
        
    def read_config_value(self, document, section, item, default = None):
        value = default
        try:
            value = document.get(section, item)
        except:
            raise
        return value
    
      
    def load(self, file):
        ret_val = False

        file = joinpath(self.backup_home, file.encode('utf8'))
        
        try:
            # Profile files are saved under mysql credentials, so they need to be read the same way
            self.context.server_interface._needs_admin = True
            get_file_content_cb = lambda as_user, user_password: self.context.ctrl_be.server_helper.get_file_content(file, as_user, user_password)
            
            config_data = self.context.server_interface.perform_as_user(self.context.mysql_user, get_file_content_cb)
            
            if config_data:
                config_data = sanitize_sudo_output(config_data)

                doc = ConfigParser.ConfigParser() # allow_no_value=True does not exist in older Python
                try:
                    doc.readfp(StringIO.StringIO(config_data))
                except Exception, e:
                    log_error(_this_file, "Error Reading Configuration : File %s: %s\n" % (self._file_name, e))
                    return False

                self.port = self.read_config_value (doc, 'client', 'port')
                self.socket = self.read_config_value (doc, 'client', 'socket')
                self.user = self.read_config_value (doc, 'client', 'user')
                self.password = self.read_config_value (doc, 'client', 'password')

                self.source_data_dir = self.read_config_value (doc, 'mysqlbackup', 'datadir')
                self.innodb_data_home_dir = self.read_config_value (doc, 'mysqlbackup', 'innodb_data_home_dir')
                self.backup_directory = self.read_config_value (doc, 'mysqlbackup', 'backup_dir')
                self.comment = self.read_config_value (doc, 'mysqlbackup', 'comments')

                self._uuid = self.read_config_value (doc, 'mysqlwbbackup', 'uuid')
                self.host = self.read_config_value (doc, 'mysqlwbbackup', 'host')
                self.compress = self.read_config_value (doc, 'mysqlwbbackup', 'compress') == 'True'
                self.apply_log = self.read_config_value (doc, 'mysqlwbbackup', 'apply_log') == 'True'
                self.label = self.read_config_value (doc, 'mysqlwbbackup', 'label')

                self.full_backups.enabled = self.read_config_value (doc, 'full_backups', 'enabled') == 'True'
                self.full_backups.frequency = int(self.read_config_value (doc, 'full_backups', 'frequency'))
                self.full_backups.month_day = int(self.read_config_value (doc, 'full_backups', 'month_day'))
                self.full_backups.week_day = int(self.read_config_value (doc, 'full_backups', 'week_day'))
                self.full_backups.hour = int(self.read_config_value (doc, 'full_backups', 'hour'))
                self.full_backups.minute = int(self.read_config_value (doc, 'full_backups', 'minute'))
                    
                self.inc_backups.enabled = self.read_config_value (doc, 'inc_backups', 'enabled') == 'True'
                self.inc_backups.frequency = int(self.read_config_value (doc, 'inc_backups', 'frequency'))
                self.inc_backups.month_day = int(self.read_config_value (doc, 'inc_backups', 'month_day'))
                self.inc_backups.week_day = int(self.read_config_value (doc, 'inc_backups', 'week_day'))
                self.inc_backups.hour = int(self.read_config_value (doc, 'inc_backups', 'hour'))
                self.inc_backups.minute = int(self.read_config_value (doc, 'inc_backups', 'minute'))
                    
                ret_val = True
                
                self.changed = False
                self.full_backups.changed = False
                self.inc_backups.changed = False

        except Exception, e:
            #TODO : This should be logged properly
            #       On failure reading simply ignore the file and return False
            import traceback
            traceback.print_exc()
            grt.log_error("MEB", "Error reading backup profile %s: %s\n" % (file, e))
            pass
                
        return ret_val
        
    def delete(self):
        if self._uuid:
            self.context.server_interface.perform_as_user(self.context.mysql_user, lambda as_user, user_password: self.context.ctrl_be.server_helper.delete_file(self.defaults_file, as_user=as_user, user_password=user_password))


    def save(self):
        # Identification Data
        if not self._uuid:
            self._uuid = str(uuid.uuid1())
        
        doc = ConfigParser.ConfigParser() # allow_no_value=True does not exist in older Python
        doc.add_section('client')
        doc.set('client', 'port', self.port)
        doc.set('client', 'socket', self.socket)
        doc.set('client', 'user', self.user)
        doc.set('client', 'password', self.password)

        # required when restoring
        doc.add_section('mysqld')
        doc.set('mysqld', 'datadir', self.source_data_dir)

        doc.add_section('mysqlbackup')
        doc.set('mysqlbackup', 'datadir', self.source_data_dir)
        doc.set('mysqlbackup', 'innodb_data_home_dir', self.innodb_data_home_dir)
        doc.set('mysqlbackup', 'backup_dir', self.backup_directory)
        doc.set('mysqlbackup', 'incremental_backup_dir', joinpath(self.backup_directory, 'inc'))
        doc.set('mysqlbackup', 'incremental_base', 'history:last_backup')
        doc.set('mysqlbackup', 'comments', self.comment)
        
        doc.add_section('mysqlwbbackup')
        doc.set('mysqlwbbackup', 'uuid', self._uuid)
        doc.set('mysqlwbbackup', 'host', self.host)
        doc.set('mysqlwbbackup', 'compress', self.compress)
        doc.set('mysqlwbbackup', 'apply_log', self.apply_log)
        doc.set('mysqlwbbackup', 'label', self.label)

        doc.add_section('full_backups')
        doc.set('full_backups', 'enabled', self.full_backups.enabled)
        doc.set('full_backups', 'frequency', self.full_backups.frequency)
        doc.set('full_backups', 'month_day', self.full_backups.month_day)
        doc.set('full_backups', 'week_day', self.full_backups.week_day)
        doc.set('full_backups', 'hour', self.full_backups.hour)
        doc.set('full_backups', 'minute', self.full_backups.minute)
        
        doc.add_section('inc_backups')
        doc.set('inc_backups', 'enabled', self.inc_backups.enabled)
        doc.set('inc_backups', 'frequency', self.inc_backups.frequency)
        doc.set('inc_backups', 'month_day', self.inc_backups.month_day)
        doc.set('inc_backups', 'week_day', self.inc_backups.week_day)
        doc.set('inc_backups', 'hour', self.inc_backups.hour)
        doc.set('inc_backups', 'minute', self.inc_backups.minute)
        
        stream = StringIO.StringIO()
        stream.write("# Created and maintained by MySQL Workbench\n")
        stream.write("# Use this file for mysqlbackup parameters when backing up manually\n\n")
        doc.write(stream)

        set_file_content_cb = lambda as_user, user_password: self.context.ctrl_be.server_helper.set_file_content(self.defaults_file, stream.getvalue(), as_user, user_password)
        
        try:
          # The backup profile will be saved as the mysql user so the file
          # password is needed
          self.context.server_interface._needs_admin = True
          
          ret_val = self.context.server_interface.perform_as_user(self.context.mysql_user, set_file_content_cb)
          
          # Once saved resets the changed flag
          self.changed = False
          
        except OperationCancelledError, e:
          return False


    @property
    def defaults_file(self):
        return "%s/%s.cnf" % (self.backup_home, self._uuid)


    @property
    def is_saved(self):
        return self._uuid is not None

    def _get_backup_files_from(self, path):
        files = self.context.server_interface.perform_as_user(self.context.mysql_user, lambda as_user, user_password: self.context.ctrl_be.server_helper.listdir(path, as_user, user_password))

        file_list = []
        log_file_list = []

        for b in files:
            if b.endswith("/") or b.endswith("\\"):
                b = b[:-1]
            m = re.match("^(20[0-9][0-9]-[0-1][0-9]-[0-3][0-9]_[0-2][0-9]-[0-5][0-9]-[0-5][0-9]?)$", b)
            if m:
                file_list.append(b)
            if b.endswith(".log"):
                log_file_list.append(b)

        # sort by name (timestamp) descending
        file_list.sort()
        file_list.reverse()
        return file_list, log_file_list

    @property
    def backup_file_list(self):
        """Returns list of backup file names for this profile. If the list was already fetched before, a cached value
        will be returned.
        """
        if self._backup_file_list is not None:
            return self._backup_file_list
        self._backup_file_list, self._backup_log_file_list = self._get_backup_files_from(self.backup_directory)
        return self._backup_file_list

    @property
    def incremental_backup_file_list(self):
        if self._inc_backup_file_list is not None:
            return self._inc_backup_file_list
        self._inc_backup_file_list, self._inc_backup_log_file_list = self._get_backup_files_from(joinpath(self.backup_directory, 'inc'))
        self._inc_backup_file_list = ['inc/'+p for p in self._inc_backup_file_list]
        self._inc_backup_log_file_list = ['inc/'+p for p in self._inc_backup_log_file_list]
        return self._inc_backup_file_list

    @property
    def has_backups(self):
        return len(self.backup_file_list) > 0


    def cleanup_backup_dir(self):
        # perform clean up in the backup directory by:
        # - renaming failed backups to .failed
        # - creating an "applied" dummy file inside incremental backup dirs that were already applied
        pass


    def load_backup_manifest(self, entry):
        if entry.data_path and entry.valid:
            try:
                data = self.context.server_interface.get_file_content(joinpath(entry.data_path, "meta", "backup_content.xml"))
                entry.process_contents(data.strip())
            except Exception, e:
                import traceback
                grt.log_error("MEB", str(traceback.format_exc()))
                entry.set_error("Backup contents info could not be read: %s" % e)


    def load_backup_metadata(self, entry):
        if entry.data_path:
            try:
                data = self.context.server_interface.get_file_content(joinpath(entry.data_path, "meta", "backup_variables.txt"))
                entry.process_variables_txt(data)
            except Exception, e:
                import traceback
                grt.log_error("MEB", str(traceback.format_exc()))
                entry.set_error("Backup info could not be read: %s" % e)

    @property
    def most_recent_usable_backup(self):
        if self._backup_file_info:
            # try to use cached info
            for entry in self._backup_file_info:
                if entry.valid:
                    return entry
        file_list = reversed(sorted(self.backup_file_list + self.incremental_backup_file_list, lambda a, b: cmp(splitpath(a)[1], splitpath(b)[1])))
        for backup_name in file_list:
            # get info about the 1st backup file in the backup dir list... don't bother
            # about log files for missing backup dir
            entry = BackupEntry(self, joinpath(self.backup_directory, backup_name), None)
            self._backup_file_info.append(entry)
            self.load_backup_metadata(entry)
            if entry.valid:
                return entry
        return None


    @property
    def all_backups(self):
        if self._backup_file_info_loaded:
            return self._backup_file_info

        backup_list = self.backup_file_list + self.incremental_backup_file_list
        known_backups = self._backup_file_info[:]

        # we've made sure during backup creation that the log file will always have the same name as the backup
        # so we pair up these 2 in here
        for log_file in self._backup_log_file_list + self._inc_backup_log_file_list:
            # skip backup entries already processed (likely the most recent one)
            if any(x.log_path == log_file for x in known_backups):
                continue

            datafile = splitpath(log_file)[1]
            if datafile.endswith(".log"):
                datafile = datafile[:-4]
            if datafile in backup_list:
                backup_list.remove(datafile)

                backup_entry = BackupEntry(self, joinpath(self.backup_directory, datafile), log_file)
            else:
                # log file exists but data file is missing!?
                backup_entry = BackupEntry(self, None, log_file)
                backup_entry.set_error("Backup data not found")
            self._backup_file_info.append(backup_entry)

        # backups with no logfile
        for backup in backup_list:
            entry = BackupEntry(self, joinpath(self.backup_directory, backup), None)
            self._backup_file_info.append(entry)

        # sort and reverse in timestamp order (newest 1st)
        self._backup_file_info.sort(lambda a, b: cmp(a.timestamp, b.timestamp))
        self._backup_file_info.reverse()

        # load metadata for entries (slow)
        for entry in self._backup_file_info:
            self.load_backup_metadata(entry)

        self._backup_file_info_loaded = True

        return self._backup_file_info


    def get_backups_needed_to_restore_incremental(self, backup):
        # if this is already a full back, nothing is needed
        if not backup.is_incremental:
            return backup, []

        # backup_list is ordered from newest to oldest
        backup_list = [x for x in self.all_backups if x.data_path] # only consider backups with data (other invalid causes are OK since it can be relevant)

        # get the index of the selected backup in the full backup list
        final_index = backup_list.index(backup)

        # go through the backup list and find the base full backup that we have to apply onto
        # we do that by using the start_lsn/end_lsn values for each backup
        restore_list = []
        full_backup = None
        for i in range(final_index, len(backup_list)):
            entry = backup_list[i]
            if entry.is_incremental:
                restore_list.append(entry)
            else:
                if not entry.valid:
                    grt.log_warning("MEB", "Skipping full backup candidate for restore %s [%s] of %s because it's not valid\n" % (entry.data_path, entry.log_path, backup.data_path))
                else:
                    full_backup = entry
                break
        if not full_backup:
            grt.log_error("MEB", "Full backup for selected incremental backup %s not found\n" % backup.data_path)
            raise BackupRestoreValidationException("The base full backup for incremental backup %s could not be found" % backup.data_path)
        grt.log_debug("MEB", "Full backup for incremental backup %s is %s\n" % (backup.data_path, full_backup.data_path))
        grt.log_debug("MEB", "Checking LSN sequence of incremental backups...\n")
        # now validate the LSN sequence of the incremental backups..
        # the full backup might already have some of the incremental backups applied,
        # but any other deviation will be rejected
        end_lsn = full_backup.end_lsn
        prev = full_backup
        pending_restore_list = []
        for incr in restore_list:
            if not incr.valid:
                grt.log_warning("MEB", "Next incremental backup between %s and %s is %s, but it is not valid (%s)" % full_backup.data_path, backup.data_path, incr.data_path, incr.error)
                continue
            if end_lsn+1 > incr.start_lsn:
                grt.log_debug("MEB", "Incremental backup %s (%s) is already applied to %s\n" % (incr.data_path, incr.start_lsn, full_backup.data_path))
            elif end_lsn+1 == incr.start_lsn:
                grt.log_debug("MEB", "Incremental backup %s (%s) has expected LSN and needs to be applied\n" % (incr.data_path, incr.start_lsn))
                end_lsn = incr.end_lsn
                pending_restore_list.append(incr)
            else:
                # if the start_lsn of the next incremental backup is bigger than the end of the previous one, there's something missing!
                grt.log_error("MEB", "There is a LSN gap between incremental backup %s (%s) and previous backup %s (%s)\n" % (incr.data_path, incr.start_lsn, prev.data_path, end_lsn))
                raise BackupRestoreValidationException("LSN sequence of incremental backup %s has a gap relative to the previous one (%s)\n" % (incr.data_path, prev.data_path))
            prev = incr
        # the end_lsn of everything that was processed must be the same as the backup we're restoring
        if end_lsn != backup.end_lsn:
            grt.log_error("MEB", "The incremental backup %s cannot be restored because there are missing backups up to the most recent full back for it\n" % backup.data_path)
            raise BackupRestoreValidationException("The incremental backup %s cannot be restored because there are missing backups up to the most recent full back for it" % backup.data_path)

        return full_backup, pending_restore_list


    @property
    def is_partial(self):
        return self.partial_selection is not None

    def get_next_backup_time(self, type, dt):

        # Takes the schedule data based on the received type
        schedule_data = self.full_backups if type == 'FULL' else self.inc_backups

        next_date = None

        # Only returns a valie if the schedule is enabled
        if schedule_data.enabled:

            if schedule_data.frequency == Frequency.hourly:
                # Creates a timestamp using the current time but with the configured target minute
                next_date = datetime(dt.year, dt.month, dt.day, dt.hour, schedule_data.minute, 0,0)

                # If the created time is already in the past, shifts the time one hour ahead
                if next_date < dt:
                    delta = timedelta(hours=1)
                    next_date = next_date + delta
            elif schedule_data.frequency == Frequency.daily:
                # Creates a timestamp using the current time but with the configured target hour and minute
                next_date = datetime(dt.year, dt.month, dt.day, schedule_data.hour, schedule_data.minute, 0,0)

                # If the created time is already in the past, shifts the time one day ahead
                if next_date < dt:
                    delta = timedelta(days=1)
                    next_date = next_date + delta
            elif schedule_data.frequency == Frequency.weekly:

                # The mod 7 operation on the days is needed because by the way the schedulers work
                # It was decided to let sunday as day 0 and continue with 1, 2.... being saturday = 6
                dtweek_day = dt.isoweekday() % 7
                delta_days = schedule_data.week_day - dtweek_day

                # Creates a timestamp using the current time but with the configured target day, hour and minute
                next_date = datetime(dt.year, dt.month, dt.day + delta_days, schedule_data.hour, schedule_data.minute, 0,0)

                # If the created time is already in the past, shifts the time 7 days ahead
                if next_date < dt:
                    delta = timedelta(days=7)
                    next_date = next_date + delta
            elif schedule_data.frequency == Frequency.monthly:
                # Creates a timestamp using the current time but with the configured target month day, hour and minute
                next_date = datetime(dt.year, dt.month, schedule_data.month_day, schedule_data.hour, schedule_data.minute, 0,0)

                # If the created time is already in the past, shifts the time 1 month ahead, 
                # taking care of the year shift as well
                if next_date < dt:
                    month = 1 if dt.month == 12 else dt.month + 1
                    year  = dt.year + 1 if dt.month == 12 else dt.year
                    next_date = datetime(year, month, schedule_data.month_day, schedule_data.hour, schedule_data.minute, 0,0)

        return next_date


