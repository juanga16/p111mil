# Copyright (c) 2009, 2012, Oracle and/or its affiliates. All rights reserved.
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

import sys
import subprocess
import os
import threading

# import the wb module
from wb import *
# import the grt module
import grt

import mforms

# define this Python module as a GRT module
ModuleInfo = DefineModule(name= "PyWbUtils", author= "Sun Microsystems Inc.", version="1.0")


# this is just a function used by the plugin, it's not exported
def printTableLine(fields, filler= " "):
  print "|",
  for text, size in fields:
    print text.ljust(size, filler), "|",
  print


# @wbexport makes this function be exported by the module and also describes the return and 
# argument types of the function
# @wbplugin defines the name of the plugin to "wb.catalog.util.dumpColumns", sets the caption to be 
# shown in places like the menu, where to take input arguments from and also that it should be included
# in the Catalog submenu in Plugins.
@ModuleInfo.plugin("wb.catalog.util.dumpColumns", caption= "Dump All Table Columns", input= [wbinputs.currentCatalog()], pluginMenu= "Catalog")
@ModuleInfo.export(grt.INT, grt.classes.db_Catalog)
def printAllColumns(catalog):
  lines= []
  schemalen= 0
  tablelen= 0
  columnlen= 0
  typelen= 0

  for schema in catalog.schemata:
    schemalen= max(schemalen, len(schema.name))
    for table in schema.tables:
      tablelen= max(tablelen, len(table.name))
      for column in table.columns:
        columnlen= max(columnlen, len(column.name))
        typelen= max(typelen, len(column.formattedType))
        lines.append((schema.name, table.name, column.name, column.formattedType))

  printTableLine([("-", schemalen), ("-", tablelen), ("-", columnlen), ("-", typelen)], "-")
  printTableLine([("Schema", schemalen), ("Table", tablelen), ("Column", columnlen), ("Type", typelen)])

  printTableLine([("-", schemalen), ("-", tablelen), ("-", columnlen), ("-", typelen)], "-")

  for s,t,c,dt in lines:
    printTableLine([(s, schemalen), (t, tablelen), (c, columnlen), (dt, typelen)])

  printTableLine([("-", schemalen), ("-", tablelen), ("-", columnlen), ("-", typelen)], "-")
  print len(lines), "columns printed"

  return 0
  

def get_linux_terminal_program():
    paths = os.getenv("PATH").split(":")
    if not paths:
        paths = ['/usr/bin', '/usr/local/bin', '/bin']

    for term in ["gnome-terminal", "konsole", "xterm", "rxvt"]:
        for d in paths:
            full_path = os.path.join(d, term)
            if os.path.exists(full_path):
                return full_path

    return None


@ModuleInfo.plugin("wb.tools.cmdlineClient", caption="Start Command Line Client", input= [wbinputs.selectedConnection()], pluginMenu="Home/Connections")
@ModuleInfo.export(grt.INT, grt.classes.db_mgmt_Connection)
def startCommandLineClientForConnection(conn):
    import platform
    import os
    if "ssh" in conn.driver.name.lower():
        host = "127.0.0.1"
        tun = grt.modules.DbMySQLQuery.openTunnel(conn)
        if tun < 0:
            mforms.Utilities.show_error("Start Command Line Client", "Could not open SSH tunnel to host.", "OK", "", "")
            return
        port = grt.modules.DbMySQLQuery.getTunnelPort(tun)
        socket = ""
    elif "socket" in conn.driver.name.lower():
        if platform.system() == "Windows":
            host = "."
        else:
            host = "localhost"
        port = None
        socketName = conn.parameterValues["socket"]
        if socketName is None:
            socketName = "MySQL"
        socket = "--socket=" + socketName
    else:
        host = conn.parameterValues["hostName"].replace("\\", "\\\\").replace('"', '\\"')
        port = conn.parameterValues["port"]
        socket = ""

    user = conn.parameterValues["userName"].replace("\\", "\\\\").replace('"', '\\"')
    if port is None:
        port = 3306
    schema = conn.parameterValues["schema"]
    if schema:
        schema = schema.replace("\\", "\\\\").replace('"', '\\"')
    else:
        schema = ""

    if platform.system() == "Darwin":
        command = """mysql \\"-u%s\\" \\"-h%s\\" -P%i %s -p %s""" % (user, host, port, socket, schema)
        os.system("""osascript -e 'tell application "Terminal" to do script "%s"'""" % command)
    elif platform.system() == "Windows":
        command = """start cmd /C mysql -u%s -h%s -P%i %s -p %s""" % (user, host, port, socket, schema)
        subprocess.Popen(command, shell = True)
    else:
        command = """mysql \\"-u%s\\" \\"-h%s\\" -P%i %s -p %s""" % (user, host, port, socket, schema)
        subprocess.call(["/bin/bash", "-c", "%s -e \"%s\" &" % (get_linux_terminal_program(), command)])


if sys.platform == "linux2":
    odbcadmin = os.getenv("MWB_MODULE_DIR")+"/../iodbcadm-gtk"
    @ModuleInfo.export(grt.INT)
    def startODBCAdmin():
        if os.path.exists(odbcadmin):
            subprocess.call(odbcadmin + " &", shell=True)
            return 1
        else:
            return 0
elif sys.platform == "darwin":
    @ModuleInfo.export(grt.INT)
    def startODBCAdmin():
        ret = subprocess.call("open -a 'ODBC Administrator'", shell=True)
        if ret == 1:
            ret = subprocess.call("open -a 'ODBC Manager'", shell=True)
        return 0 if ret == 1 else 1
elif sys.platform == "win32":
    @ModuleInfo.export(grt.INT)
    def startODBCAdmin():
        subprocess.call("odbcad32.exe", shell=True)
        return 1


# Utilities only work in Py 2.6
disable_utilities = False
# find out version of default python interpreter
if sys.platform != "win32":
    pyversion, junk = subprocess.Popen("python --version", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate()
    if pyversion < '2.6':
        disable_utilities = True

if not disable_utilities:
    @ModuleInfo.plugin("wb.tools.utilitiesShell", caption="Start Shell for MySQL Utilities", groups=["Others/Menu/Ungrouped"])
    @ModuleInfo.export(grt.INT)
    def startUtilitiesShell():
        import platform
        import os
        import time

        if platform.system() == "Windows":
            command = 'start cmd /K \"cd utilities && echo The following utilities are available: && echo. && dir *.exe /B /W\"'
            subprocess.Popen(command, shell = True)
        elif platform.system() == "Darwin":
            import tempfile
            fd, setup_script = tempfile.mkstemp(prefix="delme.", dir=mforms.App.get().get_user_data_folder())
            f = os.fdopen(fd, "w+")
            f.write('PATH="$PATH:%s/scripts"\n' % mforms.App.get().get_resource_path(""))
            f.write('MYSQL_UTILITIES_FOLDER="%s/scripts"\n' % mforms.App.get().get_resource_path(""))
            f.write('export PYTHONPATH="%s"\n' % os.getenv("PYTHONPATH", ""))
            f.write('clear\n')
            f.write('echo "The following MySQL Utilities are available:"\n')
            f.write('ls "%s/scripts"\n' %  mforms.App.get().get_resource_path(""))
            f.write('rm -f "%s"\n' % setup_script)
            f.close()
            os.chmod(setup_script, 0700)
            os.system("""osascript -e 'tell application "Terminal" to do script "source \\"%s\\""' -e 'tell front window of application "Terminal" to set custom title to "MySQL Utilities"'""" % setup_script)
        else:
            term = get_linux_terminal_program()
            if term:
                import tempfile
                fd, setup_script = tempfile.mkstemp(prefix="delme.", dir=mforms.App.get().get_user_data_folder())
                f = os.fdopen(fd, "w+")
                f.write('echo "The following MySQL Utilities are available:"\n')
                f.write('echo $MYSQL_UTILITIES_COMMANDS\n')
                f.write('rm -f "%s"\n' % setup_script)
                f.write('bash -i\n')
                f.close()
                os.chmod(setup_script, 0700)

                if 'konsole' in term:
                    subprocess.call([term, "-e", "/bin/bash", setup_script])
                else:
                    subprocess.call(["/bin/bash", "-c", "%s -e %s &" % (term, setup_script)])
            else:
                raise RuntimeError("Terminal program could not be found")


class CheckForUpdateThread(threading.Thread):
    def __init__(self):
        self.is_running = False
        self.finished = False
        super(CheckForUpdateThread, self).__init__()
    
    def run(self):
        if self.is_running:
            return
        
        self.is_running = True
        try:
            import xml.dom.minidom
            import urllib2
            
            self.dom = xml.dom.minidom.parse(urllib2.urlopen('http://wb.mysql.com/installer/products.xml'))
        except Exception, error:
            self.dom = None
            self.error = str(error)        
    
    def checkForUpdatesCallback(self):
        if self.isAlive():
            return True  # Don't do anything until the dom is built
        
        if not self.dom:
            if hasattr(self, 'error'):
                mforms.Utilities.show_error("Check for updates failed", str(self.error), "OK", "", "")
        else:
            try:
                current_version = (grt.root.wb.info.version.majorNumber, grt.root.wb.info.version.minorNumber, grt.root.wb.info.version.releaseNumber)
                edition = '' if grt.root.wb.info.license == 'GPL' else '-commercial'
                
                packages = ( package for package in self.dom.getElementsByTagName('Package') if package.parentNode.parentNode.attributes['name'].nodeValue == u'workbench-win32' + edition)
                version_strings = ( node.attributes['thisVersion'].nodeValue for node in packages if node.attributes['type'].nodeValue == 'MSI' )
                versions = ( tuple( int(num) for num in version_string.split('.') ) for version_string in version_strings )
                newest_version = max( versions ) if versions else current_version
                
                if newest_version > current_version:
                    if mforms.Utilities.show_message('New Version Available', 'The new MySQL Workbench %s has been released.\nYou can download the latest version from\nhttp://www.mysql.com/downloads/workbench.' % '.'.join( [str(num) for num in newest_version] ),
                                                  'OK', 'Cancel', 'Get it Now') == mforms.ResultOther:
                        mforms.Utilities.open_url('http://www.mysql.com/downloads/workbench')
                else:
                    mforms.Utilities.show_message('MySQL Workbench is Up to Date', 'You are already using the latest version of MySQL Workbench.', 'OK', '', '')
        
            except Exception, error:
                mforms.Utilities.show_error("Check for updates failed", str(error), "OK", "", "")

        mforms.App.get().set_status_text('Ready.')
        self.is_running = False
        self.finished = True
        return False


# Global variable:
thread = CheckForUpdateThread()

@ModuleInfo.plugin("wb.tools.checkForUpdates", caption="Check for Updates")
@ModuleInfo.export(grt.INT)
def checkForUpdates():
    global thread
    
    if thread.is_running:
        return 0
    
    if thread.finished:
        thread = CheckForUpdateThread()
    thread.start()
    mforms.App.get().set_status_text('Checking for updates...')
    mforms.Utilities.add_timeout(1.0, thread.checkForUpdatesCallback)
