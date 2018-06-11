# Copyright (c) 2012, 2013, Oracle and/or its affiliates. All rights reserved.
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

import grt
import mforms
from wb_admin_meb_editor import BackupEditorPanel
from wb_admin_meb_overview import BackupOverviewPanel
from wb_admin_meb_config import BackupConfigurationPanel
from wb_admin_meb_common import WBBackupWindowsInterface, WBBackupUnixInterface, WBBackupConfig, add_table_info_row, Users
from wb_admin_meb_restore import WbAdminEnterpriseRestore
from wb_server_management import wbaOS


def register(context, main_view):
    meb = WbAdminEnterpriseBackup(context, main_view)
    main_view.add_content_page(meb, "ENTERPRISE BACKUP", "Backup", "admin_meb_backup_win")


class WbAdminEnterpriseBackup(mforms.Box):
    def __init__(self, context, main_view):
        super(WbAdminEnterpriseBackup, self).__init__(False)
        self._ui_created = False
        self.context = context
        self.ctrl_be = context.ctrl_be
        self._main_view = main_view

        self._current_label = None

        self.set_padding(0)
        self.set_spacing(12)
        self.set_back_color("#ffffff")

        table = mforms.newTable()
        table.set_padding(12)
        table.set_row_count(5)
        table.set_column_count(2)
        table.set_row_spacing(6)
        table.set_column_spacing(4)

        self._server_info_table = table
        self._host = add_table_info_row(table, 0, "Target Host:")
        self._server_version = add_table_info_row(table, 1, "Server Version:")
        self._source_datadir = add_table_info_row(table, 2, "MySQL Data Directory:")
        self._operating_system = add_table_info_row(table, 3, "Server Operating System:")
        self._backups_home = add_table_info_row(table, 4, "Backups Home:")

        self.add(table, False, True)
    

    def create_ui(self):
        if self._ui_created:
            return
        self._ui_created = True

        # remote windows is not supported yet
        if self.context.server_profile.target_os == wbaOS.windows and not self.context.is_local:
            self._server_info_table.show(False)
            label = mforms.newLabel("MySQL Workbench does not currently support managing MySQL Enterprise Backup in non-local Windows machines.\nYou may use Workbench directly in the target machine or call mysqlbackup from the command line.")
            label.set_style(mforms.BoldStyle)
            label.set_text_align(mforms.MiddleCenter)
            self.add(label, True, True)
            return
            
        if self.context.ctrl_be.ssh is None and not self.context.is_local:
            self._server_info_table.show(False)
            label = mforms.newLabel("MySQL Workbench requires an SSH connection to support managing MySQL Enterprise Backup remotely.")
            label.set_style(mforms.BoldStyle)
            label.set_text_align(mforms.MiddleCenter)
            self.add(label, True, True)
            return

        # init and load config from file
        self.context.init_config()

        self._config_panel = BackupConfigurationPanel(self, self.context)
        self.add(self._config_panel, True, True)
        self._config_panel.show(False)

        self._overview_panel = BackupOverviewPanel(self, self.context)
        self.add(self._overview_panel, True, True)
        self._overview_panel.show(False)

        self._editor_panel = BackupEditorPanel(self, self.context)
        self.add(self._editor_panel, True, True)
        self._editor_panel.show(False)

        # Sets the callback to update the overview tab when a profile is saved
        self._editor_panel.profile_saved_callback = self._overview_panel.profile_saved
        self._editor_panel.label_validation = self._overview_panel.label_validation
        self._editor_panel.profile_delete_callback = self._overview_panel.profile_delete

        self._backups_home.set_text(self.context.config.backup_home)
        
        # Updates the cached data on the condiguration file
        self.detect_target_info()

        self.context.config.check_backup_account_exists()

        # Loads the configuration from the server...
        if self.context.config.loaded:
            self.context.config.validate()
        else:
            # If the information was not loaded from the cfg file, tries
            # to locate the backup command automatically
            self.context.config.autodetect(self.context.server_interface)
            # Performs the validation so the proper errors are set
            self.context.config.validate()
        
        if self.context.config.valid:
            # If anything changed updates the configuration file
            if self.context.config.changed:
                self.context.config.save()
                
            self.hide_config()
            self._config_panel.allow_cancel(True)
        else:
            self.show_config()
            self._config_panel.allow_cancel(False)


    def detect_target_info(self):
        if self.context.has_connection:
            values = self.ctrl_be.exec_query("SHOW VARIABLES LIKE 'version%'")
            version = ""
            version_comment = ""
            version_compile_machine = ""
            version_compile_os = ""

            datadir = self.ctrl_be.get_server_variable('datadir', '')

            if not datadir:
                raise RuntimeError("Server datadir could not be detected")
            
            while values and values.nextRow():
                key = values.stringByName("Variable_name")
                value = values.stringByName("Value")
                if key == "version":
                    version = value
                elif key == "version_comment":
                    version_comment = value
                elif key == "version_compile_machine":
                    version_compile_machine = value
                elif key == "version_compile_os":
                    version_compile_os = value
                    
            self.context.config.server_version = "%s %s" % (version_comment, version)
            self.context.config.os = "%s for %s" % (version_compile_os, version_compile_machine)
            
            self.context.config.host = self.ctrl_be.get_server_variable('hostname', '')
            self.context.config.port = self.ctrl_be.get_server_variable('port', '')
            self.context.config.socket = self.ctrl_be.get_server_variable('socket', '')
            basedir = self.ctrl_be.get_server_variable('basedir', '')
            

            # check if the datadir is not an absolute path
            if version_compile_os in ('Win32','Win64','Windows'):
                if not datadir.startswith("\\") and not (len(datadir) > 2 and datadir[1]==":"):
                    datadir = basedir+"\\"+datadir
            else:
                if not datadir.startswith("/"):
                    datadir = basedir+"/"+datadir
                    
            self.context.config.datadir = datadir

            ib_datadir = self.ctrl_be.get_server_variable('innodb_data_home_dir', '')
            
            if ib_datadir and ib_datadir != datadir:
                self._source_datadir.set_text("%s\nInnoDB: %s"%(ib_datadir, ib_datadir))
            else:
                self._source_datadir.set_text(ib_datadir)
                
            self.context.config.innodb_data_home_dir = ib_datadir

            # On windows uses the current user
            if self.context.server_profile.target_os == wbaOS.windows:
                self.context.config.mysql_user = Users.CURRENT
            else:
                self.context.config.mysql_user = self.ctrl_be.server_helper.get_file_owner(datadir)
        else:
            pass


    def show_target_info(self):
        if self.context.has_connection:
            self._server_version.set_text(self.context.config.server_version)
            self._server_version.set_style(mforms.NormalStyle)
        else:
            self._server_version.set_text("No connection to server")
            self._server_version.set_style(mforms.BoldStyle)
        self._operating_system.set_text(self.context.config.os)
        self._host.set_text("%s   Port: %s" % (self.context.config.host, self.context.config.port))
        if self.context.config.innodb_data_home_dir and self.context.config.innodb_data_home_dir != self.context.config.datadir:
            self._source_datadir.set_text("%s\nInnoDB: %s"%(self.context.config.innodb_data_home_dir, self.context.config.datadir))
        else:
            self._source_datadir.set_text(self.context.config.datadir)
            

    def show_config(self, allow_update_home = None):
        self._server_info_table.show(False)
        self._overview_panel.show(False)
        self._config_panel.init()
        self._config_panel.show(True, allow_update_home)

    def hide_config(self):
        self.show_target_info()
        self._server_info_table.show(True)
        self._overview_panel.show(True)
        self._config_panel.show(False)

    def show_editor(self, profile):
        self._overview_panel.show(False)
        self._editor_panel.refresh(profile)
        self._editor_panel.show(True)

    def hide_editor(self):
        self._overview_panel.show(True)
        self._editor_panel.show(False)

    def page_activated(self):
        self.create_ui()
        if self._current_label:
            self._main_view.set_content_label(self._current_label)

    def update_main_view_label(self, label):
        self._current_label = label
        self._main_view.set_content_label(label)
    

