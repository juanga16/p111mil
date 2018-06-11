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

import os

write_log = False
logfile = "wbadebug.log"
debug_level = os.getenv("DEBUG_ADMIN")
if debug_level is not None:
    debug_level = int(debug_level)
    import inspect
else:
    debug_level = 0

if debug_level:
    print "Debug level -", debug_level

def dprint_ex(level, *args):
    if level <= debug_level:
        fr = inspect.currentframe().f_back
        cls = ""
        slf = fr.f_locals.get('self')
        if slf:
            cls = str(slf.__class__) + '.'
        ctx = inspect.getframeinfo(fr)
        # In Python 2.5, ctx is a tuple
        #method = cls + ctx.function + ':' + str(ctx.lineno)
        method = cls + ctx[2] + ":" + str(ctx[1])

        msg = method + " : " + " ".join([type(s) is str and s or str(s) for s in args])

        print msg
        if write_log:
            f = open(logfile, "a")
            f.write(msg)
            f.write("\n")
            f.close()



def splitpath(path):
    path_tuple = None

    idx = path.rfind('/')
    if idx == -1:
        idx = path.rfind('\\')

    if idx >= 0:
        path_tuple = (path[:idx + 1], path[1 + idx:])
    else:
        path_tuple = ('', path)

    return path_tuple


def parentdir(path):
    if '/' in path:
        return "/".join(path.split("/")[:-1])
    else:
        return "\\".join(path.split("\\")[:-1])

def stripdir(path):
    if '/' in path:
        return path.split("/")[-1]
    else:
        return path.split("\\")[-1]


def joinpath(path, *comps):
    if '/' in path:
        if not path.endswith('/'):
            path += '/'
        path += '/'.join(comps)
    else:
        if not path.endswith('\\'):
            path += '\\'
        path += '\\'.join(comps)
    return path


def sanitize_sudo_output(output):
    # in Mac OS X, XCode sets some DYLD_ environment variables when debugging which dyld
    # doesn't like and will print a warning to stderr, so we must filter that out
    if output.startswith("dyld: "):
        warning, _, output = output.partition("\n")
    return output

#===============================================================================
class Users:
  ADMIN = "root"
  CURRENT = ""

class OperationCancelledError(Exception):
    pass

# Put what is the wrong password in the exception message
class InvalidPasswordError(RuntimeError):
    pass

class PermissionDeniedError(RuntimeError):
    pass

class LogFileAccessError(RuntimeError):
    pass

class ServerIOError(RuntimeError):
    pass

class NoDriverInConnection(RuntimeError):
    pass

# Decorator to log an exception
def log_error_decorator(method):
    def wrapper(self, error):
        import grt
        grt.log_error(self.__class__.__name__, str(error) + '\n')
        return method(self, error)
    return wrapper
