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

import re
import os
import time
from datetime import datetime
import mforms
import StringIO
from mforms import newBox, newLabel, newButton, newTextEntry, newTreeNodeView, newTable, newRadioButton, newListBox, newSelector, newPanel, newTabView, Utilities, newCheckBox, newImageBox, App
from wb_admin_meb_common import WBBackupProfile, add_table_field_label, add_table_field_value, add_table_info_row
from wb_server_management import local_get_cmd_output, wbaOS
from wb_common import OperationCancelledError, parentdir, joinpath, Users
from wb_execute_window import CommandExecutePanel
from wb_admin_meb_management import BackupLogViewerDialog
from workbench.db_utils import QueryError

MYSQL_ERR_TABLE_DOESNT_EXIST = 1146

class BackupOverviewPanel(mforms.Box):
    _first_time_show = True
    _command_panel = None
    def __init__(self, owner, context):
        mforms.Box.__init__(self, False)
        self._owner = owner
        self._context = context
        self._node_edited = None;
        self._backup_profiles = {}

        self._recent_list_limit = 1
                
        hbox = mforms.newBox(True)
        hbox.set_padding(12)


        self._job_menu = mforms.newMenu()
        self._job_menu.set_handler(self.handle_context_menu)
        self._job_menu.add_item("New Job", "new")
        self._job_menu.add_separator()
        self._job_menu.add_item("Configure Job...", "edit")
        self._job_menu.add_item("Delete Job", "delete")
        self._job_menu.add_separator()
        self._job_menu.add_item("Start Full Backup Now", "full_backup")
        self._job_menu.add_item("Start Incremental Backup Now", "incr_backup")
        self._job_menu.add_separator()
        self._job_menu.add_item("Copy Backup Command to Clipboard", "copy_command")
        
        self._job_list = mforms.newTreeNodeView(mforms.TreeFlatList)
        self._job_list.add_column(mforms.StringColumnType, "Backup Job", 200, False)
        self._job_list.add_column(mforms.StringColumnType, "Type", 120, False)
        self._job_list.end_columns()
        self._job_list.set_size(300, -1)
        self._job_list.add_changed_callback(self.selected_job_changed)
        self._job_list.add_activated_callback(lambda r, c: self.edit_job_clicked())
        hbox.add(self._job_list, False, True)
        self._job_list.set_context_menu(self._job_menu)
        
        table = mforms.newTable()

        table.set_row_count(8)
        table.set_column_count(2)
        table.set_row_spacing(6)
        table.set_column_spacing(4)

        self._info_table = table

        self._info_label = add_table_info_row(table, 0, "Backup Profile:")
        self._info_label.set_style(mforms.BoldStyle)

        self._latest_full = add_table_info_row(table, 1, "Latest Full Backup:")
        self._latest_inc = add_table_info_row(table, 2, "Latest Incremental Backup:")
        self._next_full = add_table_info_row(table, 3, "Next Full Backup:")
        self._next_inc = add_table_info_row(table, 4, "Next Incremental Backup:")
        self._destdir = add_table_info_row(table, 5, "Destination Directory:")
        self._available_space = add_table_info_row(table, 6, "Available Space:")

        hbox.add(table, True, True)
        self.add(hbox, False, True)

        hbox = mforms.newBox(True)
        hbox.set_spacing(12)
        hbox.set_padding(12)
        
        self._add_job = mforms.newButton()
        self._add_job.set_text("New Job")
        self._add_job.add_clicked_callback(self.new_job_clicked)
        hbox.add(self._add_job, False, True)

        self._change_button = mforms.newButton()
        self._change_button.set_text("Configure")
        self._change_button.set_enabled(False)
        self._change_button.add_clicked_callback(self.edit_job_clicked)
        hbox.add(self._change_button, False, True)

        self._manage_button = mforms.newButton()
        self._manage_button.set_text("Manage Backups...")
        self._manage_button.add_clicked_callback(self.manage_backups_clicked)
        #hbox.add(self._manage_button, False, True)


        self._settings_button = mforms.newButton()
        self._settings_button.set_text("Settings...")
        self._settings_button.add_clicked_callback(self.backup_settings_clicked)
        hbox.add_end(self._settings_button, False, True)

        self.add(hbox, False, True)


        label = mforms.newLabel("Recent Activity")
        label.set_style(mforms.BoldStyle)
        self.add(label, False, True)

        #self._limit_menu = mforms.newMenu()
        #self._limit_menu.set_handler(self.handle_context_menu)
        #self._limit_menu.add_item("Last 1 Month", "last_1")
        #self._limit_menu.add_item("Last 2 Months", "last_2")
        #self._limit_menu.add_item("Last 3 Months", "last_3")
        #self._limit_menu.add_item("Last 4 Months", "last_4")
        #self._limit_menu.add_item("Last 5 Months", "last_5")
        #self._limit_menu.add_item("Last 6 Months", "last_6")
        self._recent_menu = mforms.newMenu()
        self._recent_menu.set_handler(self.handle_context_menu)
        #self._recent_menu.add_item("View Details", "viewdetails")
        self._recent_menu.add_item("View Backup Log", "viewlog")
        self._recent_menu.add_separator()
        #self._recent_menu.add_submenu("Show Activity For", self._limit_menu)
        self._recent_menu.add_item("Refresh", "refresh_recent")

        #self._limit_menu.set_item_enabled(self._recent_list_limit-1, True)

        self._recent_list = mforms.newTreeNodeView(mforms.TreeFlatList)
        self._recent_list.set_context_menu(self._recent_menu)
        self._recent_list.add_column(mforms.StringColumnType, "Job", 150, False)
        self._recent_list.add_column(mforms.StringColumnType, "Type", 100, False)
        self._recent_list.add_column(mforms.StringColumnType, "Start Time", 140, False)
        self._recent_list.add_column(mforms.StringColumnType, "Total Time", 80, False)
        self._recent_list.add_column(mforms.IconStringColumnType, "Status", 500, False)
        self._recent_list.end_columns()
        self.add(self._recent_list, True, True)

        self._recent_list.add_activated_callback(lambda r, c: self.handle_context_menu("viewlog"))


    def show(self, flag):
        mforms.Box.show(self, flag)
        if flag:
            self._owner.update_main_view_label(" MySQL Enterprise Backup - Overview")
            if self._first_time_show:
                def refresh_on_idle():
                    self.refresh(True)
                    return False
                # refresh after going to event loop so that the UI has time to display 1st
                mforms.Utilities.add_timeout(0.1, refresh_on_idle)
            else:
                self.refresh(False)
            self._first_time_show = False


    def refresh(self, reload_profiles=True):
        if reload_profiles:
            self._backup_profiles = self._context.load_backup_profiles()

            # Fills the profile list
            self._job_list.clear()
            for label, profile in sorted(self._backup_profiles.iteritems()):
                self.display_profile_in_list(label, profile)
            if self._job_list.count() > 0:
                self._job_list.select_node(self._job_list.node_at_row(0))
            self.selected_job_changed()

        if len(self._backup_profiles) > 0:
            self._add_job.set_text("New Job")
        else:
            self._add_job.set_text("Setup Job")

        self._job_menu.set_item_enabled("full_backup", self._context.has_connection)
        self._job_menu.set_item_enabled("incr_backup", self._context.has_connection)

        self.refresh_recent_activity()


    def display_profile_in_list(self, label, profile, row = None):
        if row is None:
            row = self._job_list.add_node()
            
        row.set_string(0, label)
            
        if profile.full_backups.enabled and profile.inc_backups.enabled:
            row.set_string(1, 'Full + Incr.')
        elif profile.full_backups.enabled:
            row.set_string(1, 'Full')
        elif profile.inc_backups.enabled:
            row.set_string(1, 'Incremental')
        else:
            row.set_string(1, 'Not Scheduled')
        return row


    def show_backup_log(self, profile, backup_path):
        viewer = BackupLogViewerDialog(self._context, profile, backup_path)
        viewer.show()


    def handle_context_menu(self, action):
        if action == "new":
            self.new_job_clicked()
        elif action == "edit":
            self.edit_job_clicked()
        elif action == "delete":
            self.profile_delete()
        elif action == "full_backup":
            self.backup_now_clicked()
        elif action == "incr_backup":
            self.inc_backup_now_clicked()
        elif action == "copy_command":
            command = self._context.server_interface.create_backup_command_call(self.selected_profile, 'full', to_schedule=False)
            command += " --with-timestamp"
            mforms.Utilities.set_clipboard_text(command)
        elif action == "refresh_recent":
            self.refresh_recent_activity()
        elif action == "viewlog":
            node = self._recent_list.get_selected_node()
            if node:
                data_path = node.get_tag().split("\n")[1]
                self.show_backup_log(self.selected_profile, data_path)
        elif action == "viewdetails":
            node = self._recent_list.get_selected_node()


    def profile_delete(self):
        node = self._job_list.get_selected_node()
        if node is not None:
            label = node.get_string(0)
            if self._context.ctrl_be.server_helper.file_exists(self._backup_profiles[label].backup_directory):
                if self._context.ctrl_be.server_helper.listdir(self._backup_profiles[label].backup_directory):
                    message = "The backup data for this profile will be left at %s" % self._backup_profiles[label].backup_directory
                    Utilities.show_message("Delete Backup Job", message, "OK", "", "")
                else:
                    self._context.perform_as_user(self.context.mysql_user, lambda as_user, user_password: self._context.ctrl_be.server_helper.remove_directory(self._backup_profiles[label].backup_directory, as_user, user_password))

            self._context.server_interface.unschedule_backup(self._backup_profiles[label])
            self._backup_profiles[label].delete()

            row = self._job_list.row_for_node(node)

            node.remove_from_parent()
            del self._backup_profiles[label]

            if row >= self._job_list.count():
                row -= 1
                self._job_list.select_node(self._job_list.node_at_row(row))
            self.selected_job_changed()
            self.refresh(False)
        

    def new_job_clicked(self):
        new_profile = WBBackupProfile(self._context)
        new_profile.host = "localhost"
        new_profile.port = self._context.config.port
        new_profile.socket = self._context.config.socket
        new_profile.label = "backup"
        new_profile.backup_directory = joinpath(self._context.config.backup_home, new_profile.label)
        new_profile.user = self._context.config.backup_account
        new_profile.password = self._context.config.backup_account_password
        new_profile.source_data_dir = self._context.config.datadir
        new_profile.innodb_data_home_dir = self._context.config.innodb_data_home_dir

        self._node_edited = None;
        self._owner.show_editor(new_profile)
      
    def edit_job_clicked(self):
        node = self._job_list.get_selected_node()
        if node is not None:
            label = node.get_string(0)
            backup_profile = self._backup_profiles[label]
            self._node_edited = node
            self._owner.show_editor(backup_profile)

    def manage_backups_clicked(self):
        pass

    def backup_settings_clicked(self):
        self._owner.show_config(len(self._backup_profiles)==0)

    @property
    def selected_profile(self):
        node = self._job_list.get_selected_node()
        if node is not None:
            label = node.get_string(0)
            return self._backup_profiles[label]
        return None

    # Function to validate the duplicate labes across profiles
    def label_validation(self, label, profile):
        ret_val = True
        
        if self._backup_profiles.has_key(label):
            existing = self._backup_profiles[label]
            ret_val = (existing == profile)
            
        return ret_val;
        
            
    def profile_saved(self, profile):
        # Removes profile from the dictionary in case it was renamed
        if self._node_edited is not None:
            del self._backup_profiles[self._node_edited.get_string(0)]

        # Adds the profile again and displays it
        self._backup_profiles[profile.label] = profile
        node = self.display_profile_in_list(profile.label, profile, self._node_edited)

        self.refresh(False)

        self._job_list.select_node(node)
        self.selected_job_changed()


    def selected_job_changed(self):
        node = self._job_list.get_selected_node()
        enabled = node is not None

        if node:
            self.display_profile_info()
        else:
            if not self._backup_profiles:
                self._info_label.set_text("No backups setup, click [Setup Job] to configure it.")
            else:
                self._info_label.set_text("")

        # update the context menu
        self._job_menu.set_item_enabled("edit", enabled)
        self._job_menu.set_item_enabled("delete", enabled)
        self._job_menu.set_item_enabled("full_backup", enabled)
        self._job_menu.set_item_enabled("incr_backup", enabled)
        #self._job_menu.set_item_enabled("copy_command", enabled)

        # Enables the buttons accordingly
        self._change_button.set_enabled(enabled)

    def get_lastest_backup_dates(self, profile, type):
        last_end = "n/a"

        # This replace will affect windows paths and is needed
        # when using LIKE comparison
        backup_path = profile.backup_directory.replace('\\','\\\\\\\\')

        if self._context.has_connection:
            try:
                result = self._context.ctrl_be.exec_query("""
                SELECT end_time
                    FROM mysql.backup_history
                    WHERE backup_destination like '%s'
                    AND backup_type = '%s'
                    AND exit_state = 'SUCCESS'
                    ORDER BY end_time DESC
                    LIMIT 1
                    """ % (backup_path + '%', type))
                    
                if result and result.nextRow():
                    last_end = result.stringByName('end_time')
            except QueryError, e:
                if e.error != MYSQL_ERR_TABLE_DOESNT_EXIST: # table doesn't exist yet, just ignore
                    raise e

        return last_end


    def display_profile_info(self):
        # Displays the profile name
        self._info_label.set_text(self.selected_profile.label)

        # Retrieves and displays the last backup dates
        last_full_end = self.get_lastest_backup_dates(self.selected_profile,'FULL')
        last_inc_end  = self.get_lastest_backup_dates(self.selected_profile,'INCREMENTAL')

        self._latest_full.set_text(last_full_end)
        self._latest_inc.set_text(last_inc_end)

        # Calculates and displays the next backup operations
        next_full_backup = "n/a"
        next_inc_backup = "n/a"

        # For windows will use local time for now...
        current_date = datetime.now()

        # On non windows will retrieve the server time
        if self._context.server_profile.target_os != wbaOS.windows:
            output_text = StringIO.StringIO()
            result = self._context.ctrl_be.server_helper.execute_command("date +'%Y-%m-%d %H:%M:%S'", as_user=Users.CURRENT, user_password=None, output_handler=output_text.write)

            if result == 0:
                current_date = datetime.strptime(output_text.getvalue().strip(),"%Y-%m-%d %H:%M:%S") 

        next_full_time = self.selected_profile.get_next_backup_time('FULL', current_date)
        next_inc_time = self.selected_profile.get_next_backup_time('INCREMENTAL', current_date)

        if next_full_time:
            next_full_backup = next_full_time.strftime("%Y-%m-%d %H:%M:%S")

        if next_inc_time:
            next_inc_backup = next_inc_time.strftime("%Y-%m-%d %H:%M:%S")

        self._next_full.set_text(next_full_backup)
        self._next_inc.set_text(next_inc_backup)

        # Displays the target directory
        self._destdir.set_text(self.selected_profile.backup_directory)

        # available space
        space = self._context.ctrl_be.server_helper.get_available_space(self.selected_profile.backup_directory)
        self._available_space.set_text(space)


    def _command_done(self, returncode, profile, filename):
        # save the log output
        log = self._command_panel.get_log_text()

        filename = joinpath(profile.backup_directory, filename+".log")
        set_file_content_cb = lambda as_user, user_password: self._context.ctrl_be.server_helper.set_file_content(filename, log, as_user, user_password)
        try:
            self._context.server_interface.perform_as_user(self._context.mysql_user, set_file_content_cb)
            self._command_panel.append_log("Saved log file to %s\n" % filename)
        except OperationCancelledError:
            self._command_panel.append_log("Cancelled\n")
        except Exception, e:
            self._command_panel.append_log("Could not save log file for the backup to %s: %s\n" % (filename, e))
        #if returncode != 0:
            #btn = mforms.newButton()
            #btn.set_text("Delete Backup")
            #btn.add_clicked_callback(self.delete_callback())
            #self._command_panel.bbox.add(btn, False, True)

        self.refresh_recent_activity()

        # must return True if the executed command succeeded
        return returncode == 0


    def _command_close(self):
        self._command_panel.close()
        self._command_panel = None
        self.set_enabled(True)


    def backup_now_clicked(self):
        profile = self.selected_profile
        self.set_enabled(False)
        self._command_panel = CommandExecutePanel(self._context.ctrl_be, "Performing full online backup of MySQL server...", None, self._command_close)
        self._command_panel.set_title("Backup")
        self._command_panel.show(True)
        filename = time.strftime("%Y-%m-%d_%H-%M-%S")
        self._command_panel.run_command(
                lambda output_handler: self._context.server_interface.execute_backup(profile, 'full', filename, output_handler),
                lambda rc: self._command_done(rc, profile, filename))


    def inc_backup_now_clicked(self):
        profile = self.selected_profile
        self._command_panel = CommandExecutePanel(self._context.ctrl_be, "Performing incremental online backup of MySQL server...", None, self._command_close)
        self._command_panel.set_title("Incremental Backup")
        self._command_panel.show(True)
        filename = "inc/"+time.strftime("%Y-%m-%d_%H-%M-%S")
        self._command_panel.run_command(
                lambda output_handler: self._context.server_interface.execute_backup(profile, 'incremental', filename, output_handler),
                lambda rc: self._command_done(rc, profile, filename))

    def refresh_recent_activity(self):
        self._recent_list.clear()

        if not self._context.has_connection:
            return
            
        fields = ["backup_id", "backup_type", "start_time", "elapsed_time", "backup_destination", "exit_state", "error_message"]
            
        result_rows = []
        
        try:
            result = self._context.ctrl_be.exec_query("""
                SELECT backup_id, backup_type, start_time, end_time-start_time as elapsed_time, backup_destination, exit_state,
                          (SELECT bp.error_message FROM mysql.backup_progress bp WHERE bp.backup_id = bh.backup_id AND bp.error_code <> 0 LIMIT 1) as error_message
                    FROM mysql.backup_history bh
                    WHERE DATEDIFF(NOW(), start_time) <= %s
                    GROUP BY backup_id
                    ORDER BY start_time DESC
                    """ % (self._recent_list_limit * 30))
                    
            if result is not None:
                while result.nextRow():
                    row = {}
                    for field in fields:
                        value = result.stringByName(field)
                        row[field] = value
                    result_rows.append(row)
                    
        except QueryError, err:
            if err.error == MYSQL_ERR_TABLE_DOESNT_EXIST:
                return
            else:
                raise
                    
        def format_time(s):
            if s < 60:
                return "%is" % s
            elif s < 3600:
                return "%imin %is" % ((s / 60) % 60, s % 60)
            else:
                return "%ih %imin %is" % (s / 3600, (s / 60) % 60, s % 60)

        if len(result_rows):
            # Tries to match each retrieved record with the configured
            # Backup profiles
            for row in result_rows:
                target_path = parentdir(row["backup_destination"])
                row["profile"] = self.get_profile_by_path(row["backup_type"], target_path)

            # Finally fill the recent table with the information
            for row in result_rows:
                tree_row = self._recent_list.add_node()
                tree_row.set_tag("%s\n%s" % (row["backup_id"], row["backup_destination"]))
                message = row["error_message"]
                if row["exit_state"] == 'SUCCESS':
                    tree_row.set_icon_path(4, "mini_ok.png")
                    message = 'SUCCESS'
                elif row["exit_state"] == 'FAILURE':
                    tree_row.set_icon_path(4, "mini_error.png")
                else:
                    tree_row.set_icon_path(4, "mini_warning.png")
                tree_row.set_string(0, row["profile"])
                tree_row.set_string(1, row["backup_type"])
                tree_row.set_string(2, row["start_time"])
                tree_row.set_string(3, format_time(int(row["elapsed_time"])))
                tree_row.set_string(4, message or "FAILURE")
        
    def get_profile_by_path(self, type, path):
        for label, profile in self._backup_profiles.iteritems():
            profile_path = profile.backup_directory
            
            # Compares the received path vs the path stored on the profile
            if type == 'INCREMENTAL':
                profile_path = joinpath(profile_path, 'inc')
                
            if profile_path == path:
                return label
        
        # When the profile has not been found, returns Unknown
        return "Unknown"
        


