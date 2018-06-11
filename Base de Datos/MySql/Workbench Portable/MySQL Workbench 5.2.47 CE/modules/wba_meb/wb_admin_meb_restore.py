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

import mforms
from mforms import newLabel, newTreeNodeView, newTextBox
from wb_admin_meb_common import BackupRestoreValidationException, joinpath
from wb_server_management import wbaOS

from workbench.wizard_page_widget import WizardPage
from workbench.wizard_progress_page_widget import WizardProgressPage


def register(context, main_view):
    restore = WbAdminEnterpriseRestore(context, main_view)
    main_view.add_content_page(restore, "ENTERPRISE BACKUP", "Recovery", "admin_meb_restore_win")





class ProfileSelectionPage(WizardPage):
    def __init__(self, owner, context):
        WizardPage.__init__(self, owner, "Recover Backup - Select Backup", wide=True)

        self.context = context
        self._backup_profiles = {}

        self.advanced_button_text = "Restore from File..."
        self.advanced_button_tooltip = """Pick a backup file created with mysqlbackup to be restored.
You may pick a single file/backup image file (.mbi) or a backup directory. 
When picking a backup directory, select the meta/backup_context.xml file inside the desired backup directory."""

        l = newLabel("""To recover a MySQL server from a backup, select the profile that was used to create it.
To recover from a different backup, click [Restore from File...] and select
a MySQL Enterprise Backup image file or backup directory.
Note: the server will be shutdown during restore.""")
        self.content.add(l, False, True)

        hbox = mforms.newBox(True)
        hbox.set_spacing(8)
        hbox.set_padding(20)
        hbox.add(newLabel("Backup Profile:", True), False, True)
        self._profile = mforms.newSelector()
        self._profile.set_name("profile")
        self._profile.add_changed_callback(self.profile_selected)
        hbox.add(self._profile, True, True)
        self._use_most_recent = mforms.newCheckBox()
        self._use_most_recent.set_text("Use most recent backup")
        self._use_most_recent.add_clicked_callback(self.most_recent_toggled)
        self._use_most_recent.set_active(True)
        hbox.add(self._use_most_recent, False, True)
        self.content.add(hbox, False, False)

        self._table_h = newLabel("Select Backup from List")
        self.content.add(self._table_h, False, True)
        self._table = newTreeNodeView(mforms.TreeFlatList)
        self._table.add_column(mforms.StringColumnType, "Date of Backup", 200, False)
        self._table.add_column(mforms.StringColumnType, "Full/Incr.", 60, False)
        self._table.add_column(mforms.IconStringColumnType, "State", 200, False)
        self._table.add_column(mforms.StringColumnType, "LSN Range", 200, False)
        self._table.add_column(mforms.StringColumnType, "Binlog Position", 200, False)
        self._table.end_columns()

        self.content.add(self._table, True, True)

        self.content.add(newLabel("Details:"), False, True)

        self._text = newTextBox(mforms.VerticalScrollBar)
        self.content.add(self._text, True, True)

        self._error_icon = mforms.App.get().get_resource_path("mini_error.png")


    def refresh(self):
        self._backup_profiles = self.context.load_backup_profiles().values()
        self._backup_profiles.sort(lambda a,b: cmp(a.label, b.label))
        self._profile.clear()
        self._profile.add_items(["%s (%s)" % (p.label, "partial" if p.is_partial else "full") for p in self._backup_profiles])

        self.profile_selected()
        self.most_recent_toggled()


    def advanced_clicked(self):
        filechooser = mforms.FileChooser(mforms.OpenFile)
        filechooser.set_title("Choose Backup File")
        if filechooser.run_modal():
            filename = filechooser.get_path()
            print filename


    @property
    def selected_profile(self):
        s = self._profile.get_selected_index()
        if s >= 0 and s < len(self._backup_profiles):
            return self._backup_profiles[s]
        return None


    @property
    def selected_backup(self):
        profile = self.selected_profile
        if profile:
            if self._use_most_recent.get_active():
                return profile.most_recent_usable_backup
            else:
                node = self._table.get_selected_node()
                if node:
                    return profile.all_backups[self._table.row_for_node(node)]
        return None


    def profile_selected(self):
        self._table.clear()
        profile = self.selected_profile
        if profile:
            if self._use_most_recent.get_active():
                backup_entry = profile.most_recent_usable_backup
                if backup_entry:
                    node = self._table.add_node()
                    node.set_string(0, backup_entry.timestamp)
                    node.set_string(1, "incremental" if backup_entry.is_incremental else "full")
                    if backup_entry.error:
                        node.set_icon_path(2, self._error_icon)
                    node.set_string(2, backup_entry.status_text)
                    node.set_string(3, "%s - %s" % (backup_entry.start_lsn or "?", backup_entry.end_lsn or "?"))
                    node.set_string(4, backup_entry.metadata.get("binlog_position", ""))
                else:
                    print "Most recent backup could not be determined"
            else:
                self.refresh_backup_list()
            if self._table.count() > 0:
                self._table.select_node(self._table.node_at_row(0))
        self.backup_selected()

    def refresh_backup_list(self):
        profile = self.selected_profile
        self._table.clear()
        if profile:
            backups = profile.all_backups
            for backup_entry in backups:
                node = self._table.add_node()
                node.set_string(0, backup_entry.timestamp)
                node.set_string(1, "increm." if backup_entry.is_incremental else "full")
                if backup_entry.error:
                    node.set_icon_path(2, self._error_icon)
                node.set_string(2, backup_entry.status_text)
                node.set_string(3, "%s - %s" % (backup_entry.start_lsn or "?", backup_entry.end_lsn or "?"))
                node.set_string(4, backup_entry.metadata.get("binlog_position", ""))


    def backup_selected(self):
        if self.selected_profile and self.selected_profile.has_backups:
            backup = self.selected_backup
            self._text.set_value(backup.summary if backup else "No backup selected")
        else:
            backup = None
            self._text.set_value("There are no backups for this profile yet")
        if backup:
            text = ""
            if backup.valid:
                text += "Backup Type: %s\n" % ("Incremental (backup will be applied to its corresponding full backup before it is restored)" if backup.is_incremental else "Full")
                if not backup.apply_log_done:
                    text += "apply-log will be performed on the backup before it is restored.\n"
                if backup.is_partial:
                    text += "\nContents: partial\n"
                else:
                    text += "\nContents: whole server\n"

                self.selected_profile.load_backup_manifest(backup)

                # show summary of contents
                #text += backup.manifest['backup_content']['files']
                #text += backup.manifest['backup_content']['definitions']

                text += "\n"
                text += "Backup Start Time: %s\n" % backup.start_time
                text += "Backup Finish Time: %s\n" % backup.end_time

                text += "\nBackup Variables:\n"
                text += "    "+"\n    ".join(["%s=%s" % i for i in backup.metadata.items()])
            else:
                text += "WARNING: This backup appears to be corrupted/unfinished and cannot be used.\n"
                text += backup.error
            self._text.set_value(text)


    def most_recent_toggled(self):
        use_most_recent = self._use_most_recent.get_active()
        self._table.show(not use_most_recent)
        self._table_h.show(not use_most_recent)
        if not use_most_recent:
            self.refresh_backup_list()
        if self._table.count() > 0:
            self._table.select_node(self._table.node_at_row(0))
        self.backup_selected()




class RecoveryProgressPage(WizardProgressPage):
    selected_backup = None
    def __init__(self, owner, context):
        WizardProgressPage.__init__(self, owner, "Recover Backup - Progress", description = """The following tasks will now be executed to revert the state of your server to that of the selected backup.\nClick [Restore >] to start the recovery process.""")
        self.context = context
        self.set_managed()
        self.set_release_on_add()
        self.next_button.set_text("Restore >")

        self.add_threaded_task(self.prepare, "Calculate preparation steps")
        self.add_threaded_task(self.process_full_backup, "Prepare full backup file for recovery")
        self.add_threaded_task(self.process_incremental_backups, "Prepare and apply incremental backup files for recovery")
        self.add_threaded_task(self.stop_server, "Shutdown MySQL server")
        self.add_threaded_task(self.restore, "Recover backup")
        self.add_threaded_task(self.start_server, "Start MySQL server")


    def reset(self, clear_log_box= False):
        self.next_button.set_enabled(True)
        WizardProgressPage.reset(self, clear_log_box)
        self.cancel_button.set_text("Cancel")


    def stop_server(self):
        if self.context.ctrl_be.server_control and not self.context.ctrl_be.server_control.stop_async(self.async_stop_callback):
            raise Exception("Could not stop server")


    def async_stop_callback(self, status):
        print status


    def start(self):
        if mforms.Utilities.show_warning("Restore Backup",
                                    "Restore MySQL backup to datadir '%s'\n"
                                    "This will restore the server to the state it was when the backup was made. "
                                    "Any changes from after the backup will be lost." % self.context.config.datadir,
                     "Restore", "Cancel", "") != mforms.ResultOk:
            return
        self.selected_backup = self.main.selected_backup_entry
        self.prep_full_backup = None
        self.prep_apply_list = []
        self.prep_inc_apply_list = []
        self.output_buffer = ""
        WizardProgressPage.start(self)


    def prepare(self):
        backup = self.selected_backup

        self.send_info("Verifying backup file for recovery...\n")

        if backup.is_incremental:
            self.send_info("The selected backup '%s' is incremental. Verifying steps necessary to restore it...\n" % backup.data_path)

            try:
                # Check the files needed for restore (ie all incremental backups from the selected one up to the full one)
                full_backup, apply_list = backup.profile.get_backups_needed_to_restore_incremental(backup)
                assert full_backup != None

                self.prep_full_backup = full_backup
                if not apply_list:
                    self.send_info("Incremental backup is already applied to the full backup '%s', using that instead...\n" % full_backup.data_path)
                else:
                    self.send_info("The following incremental backups will be applied to the full backup '%s' so it can be restored:\n" % full_backup.data_path)
                    for b in apply_list:
                        self.send_info("    %s\n" % b.data_path)
                        if not b.apply_log_done:
                            self.prep_apply_list.append(b)
                        self.prep_inc_apply_list.append(b)
            except BackupRestoreValidationException, e:
                self.send_error("It is not possible to restore the incremental backup '%s'\n    %s" % (backup.data_path, e))
                raise e
        else:
            # Apply-log on the full backup if needed
            self.prep_full_backup = backup
            self.send_info("The selected backup '%s' is a full backup\n" % backup.data_path)


    def process_full_backup(self):
        # Apply incremental backup, from oldest to newest if needed
        if self.prep_full_backup.apply_log_done:
            self.send_info("Full backup file is already processed, apply-log not needed\n")
        else:
            self.send_info("Full backup file is raw and requires apply-log... This may take a long time\n")

            if self.context.server_interface.backup_apply_log(self.prep_full_backup.data_path, self.prep_full_backup.is_compressed, self.send_raw) != 0:
                raise RuntimeError("mysqlbackup exited with error")


    def process_incremental_backups(self):
        archive_dir = joinpath(self.prep_full_backup.profile.backup_directory, "archive")
        for b in self.prep_inc_apply_list:
            self.send_info("Applying incremental backup %s onto full backup...\n" % b.data_path)
            if self.context.server_interface.backup_apply_incremental(self.prep_full_backup.data_path, b.data_path, archive_dir, self.send_raw) != 0:
                raise RuntimeError("mysqlbackup exited with error")

        self.send_info("Preparations finished.\n")


    def restore(self):
        self.send_info("Starting backup recovery...\n")
        ret = self.context.server_interface.restore_backup(self.prep_full_backup, self.send_raw)
        self.send_info("mysqlbackup copy-back exited with status %i\n" % ret)
        if ret != 0:
            raise RuntimeError("Backup recovery failed")
        self.send_info("Backup recovery finished successfully.\n")


    def start_server(self):
        if self.context.ctrl_be.server_control and not self.context.ctrl_be.server_control.start_async(self.async_stop_callback):
            raise Exception("Could not start server")


    def go_cancel(self):
        self.reset()
        self.main.reset()


    def tasks_finished(self):
        self.back_button.set_enabled(False)
        self.next_button.set_enabled(False)
        self.cancel_button.set_text("Done")
        self.cancel_button.set_enabled(True)


    def tasks_failed(self, canceled):
        self.back_button.set_enabled(False)
        self.next_button.set_enabled(False)
        self.cancel_button.set_enabled(True)



class WbAdminEnterpriseRestore(mforms.Box):
    def __init__(self, context, main_view):
        super(WbAdminEnterpriseRestore, self).__init__(False)
        self.set_release_on_add()
        self.set_managed()

        self.set_back_color("#ffffff")

        self._ui_created = False
        self.context = context
        self._main_view = main_view
        
        self._page_list = []
        self._page_trail = []
        self._current_page = 0


    @property
    def selected_backup_entry(self):
        return self._profile_page.selected_backup


    def point_in_time_restore(self):
        r = mforms.Utilities.show_message("Point in Time Restore",
        """Point in Time restore allows the database to be rolled back to a past state using
the MySQL binary log. For that, the following conditions are necessary:
 - The MySQL server version must be 5.1 or newer
 - A backup created before the desired rollback point must be restored first
 - Binary logging must have been enabled in the server at least since the time of that backup

To perform a Point in Time restore, proceed with a backup restore and select the appropriate
option. If the backup has already been restored, click [Restore from Logs].
""", "OK", "", "Restore from Logs")



    def advanced(self):
        self._page_trail[-1].advanced_clicked()


    def reset(self):
        self._current_page = 0
        self._page_trail = [self._page_list[0]]
        self.switch_page()


    def create_ui(self):
        if self._ui_created:
            return
        self.context.init_config()

        # remote windows is not supported yet
        if self.context.server_profile.target_os == wbaOS.windows and not self.context.is_local:
            label = mforms.newLabel("MySQL Workbench does not currently support managing MySQL Enterprise Backup in non-local Windows machines.\nYou may use Workbench directly in the target machine or call mysqlbackup from the command line.")
            label.set_style(mforms.BoldStyle)
            label.set_text_align(mforms.MiddleCenter)
            self.add(label, True, True)
            return

        self._ui_created = True
        self._profile_page = ProfileSelectionPage(self, self.context)
        self._progress_page = RecoveryProgressPage(self, self.context)
        self._page_list = [self._profile_page, self._progress_page]
        for p in self._page_list:
            self.add(p, True, True)
            p.show(False)

        self._page_trail = [self._page_list[self._current_page]]
        self.switch_page()

    
    def switch_page(self):
        curpage = self._page_trail[-1]
        for p in self._page_list:
            p.show(p == curpage)

#        if self._current_page == 0:
#            self._pit_button.show(True)
#        else:
#            self._pit_button.show(False)

    def go_next_page(self):
        self._current_page += 1
        self._page_trail.append(self._page_list[self._current_page])
        self.switch_page()


    def go_previous_page(self):
        if len(self._page_trail) > 1:
            self._page_trail.pop()
            self._current_page = self._page_list.index(self._page_trail[-1])
            self.switch_page()


    def page_activated(self):
        self.create_ui()
        self._main_view.set_content_label(" MySQL Enterprise Backup - Recovery")
        # refresh if we're in the 1st page
        if self._page_list and self._current_page == 0:
            self._profile_page.refresh()

