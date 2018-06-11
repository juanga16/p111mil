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
from mforms import newBox, newLabel, newButton, newTextEntry, newTextBox, newTreeNodeView, newTable, newListBox, newSelector, newPanel, newTabView, Utilities, newCheckBox, newImageBox, App
from mforms import FileChooser, OpenDirectory
from wb_admin_meb_common import WBBackupProfile, add_table_field_label, add_table_field_value, add_table_info_row
from wb_common import stripdir, parentdir, joinpath

class BackupEditorPanel(mforms.Box):
    _updating_name = False
    _old_name = None

    def __init__(self, owner, context):
        mforms.Box.__init__(self, False)
        self._owner = owner
        self._context = context
        self._profile = None
        self._days   = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        self._months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self._freqs =  ["Hour", "Day", "Week", "Month"]
        self._monthdays = []
        
        self.profile_saved_callback = None
        self.profile_delete_callback = None
        self.label_validation = None

        for index in range(31):
            suffix = "th"
            day = index+1
            if day in [1,21,31]:
                suffix = "st"
            elif day in [2,22]:
                suffix = "nd"
            elif day in [3,23]:
                suffix = "rd"
          
            self._monthdays.append(str(day) + suffix)
            

        table = mforms.newTable()
        table.set_padding(12)
        table.set_row_count(1)
        table.set_column_count(2)
        table.set_row_spacing(6)
        table.set_column_spacing(4)

        add_table_field_label(table, 0, "Profile Name:")
        self._name = newTextEntry()
        self._name.add_changed_callback(self.name_edited)
        self._name.set_size(200, -1)
        self._backup_type = newLabel("", True)
        hbox = newBox(True)
        hbox.set_spacing(12)
        hbox.set_padding(12)
        hbox.add(self._name, False, True)
        hbox.add(self._backup_type, False, True)
        table.add(hbox, 1, 2, 0, 1, mforms.HFillFlag)

        self.add(table, True, True)

        # Creates the configuration tabs
        self._configuration = newTabView(False)
        self.add(self._configuration, True, True)
        
        # enable back when supported self.create_contents_tab()
        self.create_destination_tab()
        self.create_schedule_tab()
        self.create_comments_tab()

        # Creates the buttons line at the bottom of the screen
        hbox = newBox(True)
        hbox.set_spacing(12)
        hbox.set_padding(12)
        self.add(hbox, False, True)

        self._cancel_button = mforms.newButton()
        self._cancel_button.set_text("Cancel")
        self._cancel_button.add_clicked_callback(self.cancel_changes)
        hbox.add_end(self._cancel_button, False, True)

        self._ok_button = mforms.newButton()
        self._ok_button.set_text("Save and Reschedule")
        self._ok_button.add_clicked_callback(self.save_changes)
        hbox.add_end(self._ok_button, False, True)

        self._del_job_button = mforms.newButton()
        self._del_job_button.set_text("Delete")
        self._del_job_button.add_clicked_callback(self.delete_clicked)
        hbox.add_end(self._del_job_button, False, True)



    def show(self, flag):
        mforms.Box.show(self, flag)
        if flag:
            self._owner.update_main_view_label(" MySQL Enterprise Backup - Backup Profile")

    def create_contents_tab(self):
        self._contents = newBox(False)
        self._contents.set_spacing(12)
        self._contents.set_padding(12)
        self._configuration.add_page(self._contents, "Contents")
          
        self._type = newSelector()
        self._contents.add(self._type, False, True)
        
        self._contents.add(mforms.newLabel("Select additional schemas to backup. InnoDB tables are always backed up."), False, True)
        
        self._schema_list = mforms.newTreeNodeView(mforms.TreeDefault)
        self._schema_list.add_column(mforms.CheckColumnType, "Backup", 40, False)
        self._schema_list.add_column(mforms.StringColumnType, "Schema", 400, False)
        self._schema_list.add_column(mforms.IntegerColumnType, "InnoDB Tables", 120, False)
        self._schema_list.add_column(mforms.IntegerColumnType, "MyISAM Tables", 120, False)
        self._schema_list.add_column(mforms.IntegerColumnType, "Other Tables", 120, False)
        self._schema_list.end_columns()
        self._contents.add(self._schema_list, True, True)
        
        l = mforms.newLabel("Note: Backups of InnoDB tables will be performed while the system is live, but the MyISAM and other tables will be made read-only during backup.")
        l.set_style(mforms.SmallHelpTextStyle)
        self._contents.add(l, False, True)

    def create_destination_tab(self):
        self._destination = newBox(False)
        self._destination.set_spacing(12)
        self._destination.set_padding(12)
        self._configuration.add_page(self._destination, "Options")

        table = mforms.newTable()

        table.set_row_count(7)
        table.set_column_count(2)
        table.set_row_spacing(8)
        table.set_column_spacing(4)

        add_table_field_label(table, 0, "Backup Storage Directory:")
        hbox = mforms.newBox(True)
        self._dest_directory  = newTextEntry()
        self._dest_directory.set_size(300,-1)
        hbox.add(self._dest_directory, False, False)
        self._dest_dir_button = newButton()
        self._dest_dir_button.set_text("Browse...")
        self._dest_dir_button.enable_internal_padding(False)
        self._dest_dir_button.add_clicked_callback(lambda: self.open_file_chooser(OpenDirectory, self._dest_directory))
        
        hbox.add(self._dest_dir_button, False, False)
        add_table_field_value(table, 0, hbox, mforms.HFillFlag)

        l = mforms.newLabel("Backups will be written to the specified directory in the target MySQL server.\nA new subdirectory is created for each backup, named with its timestamp.")
        l.set_style(mforms.SmallHelpTextStyle)
        add_table_field_value(table, 1, l)
        
        self._compress_backup = mforms.newCheckBox()
        self._compress_backup.set_text("Compress backup (non-incremental InnoDB backups only)")
        add_table_field_value(table, 3, self._compress_backup)
        
        self._apply_log = mforms.newCheckBox()
        self._apply_log.set_text("Apply log after backup (backup-and-apply-log)")
        add_table_field_value(table, 5, self._apply_log)
        l = mforms.newLabel("After a backup is done, an apply-log operation is needed before it can be recovered.\nThat may be done right after backup, before recovering it or at any other time.")
        l.set_style(mforms.SmallHelpTextStyle)
        add_table_field_value(table, 6, l)
        
        self._destination.add(table, False, False)
    
    def create_schedule_tab(self):
        self._schedule = newBox(False)
        self._schedule.set_spacing(12)
        self._schedule.set_padding(12)
        self._configuration.add_page(self._schedule, "Schedule")

        
        self._full_backup_schedule = mforms.newCheckBox()
        self._full_backup_schedule.set_text("Perform full backups every")
        self._schedule.add(self._full_backup_schedule, False, False)
        self._full_backup_schedule.add_clicked_callback(self.full_backup_schedule_clicked)

        self._full_backup_box = mforms.newBox(True)

        # Selector for frequency
        self._full_backup_frequency  = newSelector()
        self._full_backup_frequency.set_size(100, -1)
        for freq in self._freqs:
            self._full_backup_frequency.add_item(freq)
        self._full_backup_frequency.add_changed_callback(self.schedule_full_freq_changed)
        self._full_backup_box.add(self._full_backup_frequency, False, False)
        
        self._full_label1 = newLabel(" on ")
        self._full_backup_box.add(self._full_label1, False, False)
        
        # Selector for days of the week
        dayhbox = newBox(True)
        self._full_backup_dow  = newSelector()
        self._full_backup_dow.set_size(100, -1)
        for day in self._days:
            self._full_backup_dow.add_item(day)
        dayhbox.add(self._full_backup_dow, False, False)
        
        # Selector for days in the month
        self._full_backup_dom  = newSelector()
        self._full_backup_dom.set_size(50, -1)
        for day in self._monthdays:
            self._full_backup_dom.add_item(day)
        dayhbox.add(self._full_backup_dom, False, False)
        self._full_backup_box.add(dayhbox, False, False)
        
        self._full_label2 = newLabel(" at ")
        self._full_backup_box.add(self._full_label2, False, False)

        # Selector for the hour
        self._full_backup_hour  = newSelector()
        self._full_backup_hour.set_size(50, -1)
        for index in range(24):
            self._full_backup_hour.add_item(str(index).zfill(2))
        self._full_backup_box.add(self._full_backup_hour, False, False)
        
        self._full_label3 = newLabel(" : ")
        self._full_backup_box.add(self._full_label3, False, False)
        
        self.schedule_full_freq_changed()
        self._full_backup_box.set_enabled(False)

        # Selector for the minute
        self._full_backup_minute  = newSelector()
        self._full_backup_minute.set_size(50, -1)
        for index in range(60):
            self._full_backup_minute.add_item(str(index).zfill(2))
        self._full_backup_box.add(self._full_backup_minute, False, False)
        self._schedule.add(self._full_backup_box, False, False)
        
        self._inc_backup_schedule = mforms.newCheckBox()
        self._inc_backup_schedule.set_text("Perform incremental backups every")
        self._schedule.add(self._inc_backup_schedule, False, False)
        self._inc_backup_schedule.add_clicked_callback(self.inc_backup_schedule_clicked)
        
        self._inc_backup_box = mforms.newBox(True)

        # Selector for frequency
        self._inc_backup_frequency  = newSelector()
        self._inc_backup_frequency.set_size(100, -1)
        for freq in self._freqs:
            self._inc_backup_frequency.add_item(freq)
        self._inc_backup_frequency.add_changed_callback(self.schedule_inc_freq_changed)
        self._inc_backup_box.add(self._inc_backup_frequency, False, False)
        
        self._inc_label1 = newLabel(" on ")
        self._inc_backup_box.add(self._inc_label1, False, False)
        
        # Selector for days of the week
        dayhbox = newBox(True)
        self._inc_backup_dow  = newSelector()
        self._inc_backup_dow.set_size(100, -1)
        for day in self._days:
            self._inc_backup_dow.add_item(day)
        dayhbox.add(self._inc_backup_dow, False, False)
        
        # Selector for days in the month
        self._inc_backup_dom  = newSelector()
        self._inc_backup_dom.set_size(50, -1)
        for day in self._monthdays:
            self._inc_backup_dom.add_item(day)
        dayhbox.add(self._inc_backup_dom, False, False)
        self._inc_backup_box.add(dayhbox, False, False)
        
        self._inc_label2 = newLabel(" at ")
        self._inc_backup_box.add(self._inc_label2, False, False)

        # Selector for the hour
        self._inc_backup_hour  = newSelector()
        self._inc_backup_hour.set_size(50, -1)
        for index in range(24):
            self._inc_backup_hour.add_item(str(index).zfill(2))
        self._inc_backup_box.add(self._inc_backup_hour, False, False)
        
        self._inc_label3 = newLabel(" : ")
        self._inc_backup_box.add(self._inc_label3, False, False)

        # Selector for the minute
        self._inc_backup_minute  = newSelector()
        self._inc_backup_minute.set_size(50, -1)
        for index in range(60):
            self._inc_backup_minute.add_item(str(index).zfill(2))
        self._inc_backup_box.add(self._inc_backup_minute, False, False)
        self._schedule.add(self._inc_backup_box, False, False)
        
        self.schedule_inc_freq_changed()
        self._inc_backup_box.set_enabled(False)
        
        self._schedule.add(newLabel("Incremental backups will create a backup of all changes that have occurred since the lastest backup, full or incremental."), False, False)
        self._schedule.add_end(newLabel("Note: backups are scheduled and executed from the target server, using the systems task scheduler."), False, False)

    def create_comments_tab(self):
        self._comments = newBox(False)
        self._comments.set_spacing(12)
        self._comments.set_padding(12)
        self._configuration.add_page(self._comments, "Comments")
        
        self._comment = newTextBox(mforms.BothScrollBars)
        self._comments.add(self._comment, True, True)
    
    def schedule_full_freq_changed(self):
        freq = self._full_backup_frequency.get_string_value()
        self._full_backup_dow.show( freq == "Week" )
        self._full_backup_dom.show( freq in ["Once", "Month"] )
        self._full_backup_hour.show( freq != "Hour" )
        self._full_label1.show( freq in ["Once", "Week","Month"])
        self._full_label2.set_text(" at minute " if freq == "Hour" else " at ")
        self._full_label3.show( freq != "Hour")
        
    def full_backup_schedule_clicked(self):
        self._full_backup_box.set_enabled(self._full_backup_schedule.get_active())

        # The first parameter needs to be updated when partial backups are enabled
        self.refresh_type(True, self._full_backup_schedule.get_active(), self._inc_backup_schedule.get_active())
        
    
    def schedule_inc_freq_changed(self):
        freq = self._inc_backup_frequency.get_string_value()
        self._inc_backup_dow.show( freq == "Week" )
        self._inc_backup_dom.show( freq == "Month" )
        self._inc_backup_hour.show( freq != "Hour" )
        self._inc_label1.show( freq in ["Once", "Week","Month"])
        self._inc_label2.set_text(" at minute " if freq == "Hour" else " at ")
        self._inc_label3.show( freq != "Hour")

    def inc_backup_schedule_clicked(self):
        self._inc_backup_box.set_enabled(self._inc_backup_schedule.get_active())
        
        # The first parameter needs to be updated when partial backups are enabled
        self.refresh_type(True, self._full_backup_schedule.get_active(), self._inc_backup_schedule.get_active())
        

    def name_edited(self):
        if not self._updating_name and self._profile and not self._profile.is_saved:
            name = self._name.get_string_value()
            path = self._dest_directory.get_string_value()

            if self._old_name == stripdir(path):
                if '/' in path:
                    path = parentdir(path) + "/" + name
                else:
                    path = parentdir(path) + "\\" + name
                self._dest_directory.set_value(path)
                self._old_name = name


    def open_file_chooser(self, file_chooser_type, textfield):
        filechooser = FileChooser(file_chooser_type)
        filechooser.set_directory(textfield.get_string_value())
        if filechooser.run_modal():
            filename = filechooser.get_directory()
            if filename and (type(filename) is str or type(filename) is unicode):
                filename = filename.replace("\\", "/") # TODO: Check for backslashed spaces and so on
                textfield.set_value(filename)


    def refresh_type(self, full_data, full_schedule, inc_schedule):
        data = "Whole Server" if full_data else "Partial"
        
        if full_schedule and inc_schedule:
          schedule = "Full + Incremental"
        elif full_schedule:
          schedule = "Full Only"
        elif inc_schedule:
          schedule = "Incr. Only"
        else:
          schedule = "Not Scheduled"
          
        self._backup_type.set_text("%s / %s" % (data, schedule))
        
    def refresh(self, profile):
        self._profile = profile

        self._del_job_button.set_enabled(self._profile.is_saved)

        self._updating_name = True
        if self._profile:
            self._name.set_value(self._profile.label)
            self._old_name = self._profile.label
        else:
            self._name.set_value("")
            self._old_name = ""
        self._updating_name = False

        # The first parameter needs to be updated when partial backups are enabled
        self.refresh_type(True, self._profile.full_backups.enabled, self._profile.inc_backups.enabled)

        self.refresh_contents()
        self.refresh_destination()
        self.refresh_schedule()
        self.refresh_comments()
      
    def refresh_contents(self):
        pass
      
    def refresh_destination(self):
        if self._profile is not None:
            self._dest_directory.set_value(self._profile.backup_directory)
            self._compress_backup.set_active(self._profile.compress)
            self._apply_log.set_active(self._profile.apply_log)
        else:
            self._dest_directory.set_value('')
            self._compress_backup.set_active(False)
            self._apply_log.set_active(False)

    def refresh_schedule(self):
        if self._profile is not None:
            self._full_backup_schedule.set_active(self._profile.full_backups.enabled)
            self.full_backup_schedule_clicked()
            self._full_backup_frequency.set_selected(self._profile.full_backups.frequency)
            self.schedule_full_freq_changed()
            self._full_backup_dow.set_selected(self._profile.full_backups.week_day)
            self._full_backup_dom.set_selected(self._profile.full_backups.month_day-1)
            self._full_backup_hour.set_selected(self._profile.full_backups.hour)
            self._full_backup_minute.set_selected(self._profile.full_backups.minute)

            self._inc_backup_schedule.set_active(self._profile.inc_backups.enabled)
            self.inc_backup_schedule_clicked()
            self._inc_backup_frequency.set_selected(self._profile.inc_backups.frequency)
            self.schedule_inc_freq_changed()
            self._inc_backup_dow.set_selected(self._profile.inc_backups.week_day)
            self._inc_backup_dom.set_selected(self._profile.inc_backups.month_day)
            self._inc_backup_hour.set_selected(self._profile.inc_backups.hour)
            self._inc_backup_minute.set_selected(self._profile.inc_backups.minute)
        else:
            self._full_backup_schedule.set_active(False)
            self.full_backup_schedule_clicked()
            self._full_backup_frequency.set_selected(0)
            self.schedule_full_freq_changed()
            self._full_backup_dow.set_selected(0)
            self._full_backup_dom.set_selected(0)
            self._full_backup_hour.set_selected(0)
            self._full_backup_minute.set_selected(0)

            self._inc_backup_schedule.set_active(False)
            self.inc_backup_schedule_clicked()
            self._inc_backup_frequency.set_selected(0)
            self.schedule_inc_freq_changed()
            self._inc_backup_dow.set_selected(0)
            self._inc_backup_dom.set_selected(0)
            self._inc_backup_hour.set_selected(0)
            self._inc_backup_minute.set_selected(0)
        
    def refresh_comments(self):
        if self._profile is not None:
            self._comment.set_value(self._profile.comment)
        else:
            self._comment.set_value('')


    def delete_clicked(self):
        r = mforms.Utilities.show_message("Delete Backup Profile",
                                      "Please confirm deletion of this backup profile. Backups will be also unscheduled but backup data will be left intact.", "Delete", "Cancel", "")
        if r == mforms.ResultOk:
            self.profile_delete_callback()
            self._owner.hide_editor()

      
    def validate(self):
        error = ""
        if self._dest_directory.get_string_value() == "":
            error = "The backup directory must be specified."
        elif self._name.get_string_value().strip() == "":
            error = "A label to identify the profile must be set."

        if self.label_validation is not None:
            if not self.label_validation(self._name.get_string_value(), self._profile):
                error = "A unique label to identify the profile must be set."

        # compress doesn't work with apply-log
        if not error and self._compress_backup.get_active() and self._apply_log.get_active():
            error = "Compress cannot be used with the backup-and-apply-log option, please unselect either one."

        if error != "":
            Utilities.show_error("Save Backup Profile", error, "OK", "", "")
            return False
        else:
            return True
        

    def save_changes(self):
        if self.validate():
            path = self._dest_directory.get_string_value()
            if not self._context.ctrl_be.server_helper.file_exists(path):
                r = mforms.Utilities.show_warning("Save Backup Profile", "Target backup directory '%s' does not exist, would you like to create it?" % path, "Create", "Cancel", "")
                if r == mforms.ResultOk:
                    self._context.server_interface.create_directory(path)
                else:
                    return

            self.flush_data()
            
            # The next operations ONLY apply if anything changed on the profile
            if self._profile.has_changed:
                self._profile.save()
            
                path = joinpath(path, "inc")
                if not self._context.ctrl_be.server_helper.file_exists(path):
                    self._context.server_interface.create_directory(path)
            
                # Reschedules the backup with the new information
                self._context.server_interface.unschedule_backup(self._profile)
                self._context.server_interface.schedule_backup(self._profile)
                
                if self.profile_saved_callback is not None:
                    self.profile_saved_callback(self._profile)
                
            self._owner.hide_editor()


    def flush_data(self):
        self._profile.label = self._name.get_string_value()
        self.flush_contents()
        self.flush_destination()
        self.flush_schedule()
        self.flush_comments()
      
    def flush_contents(self):
        pass
      
    def flush_destination(self):
        self._profile.backup_directory = self._dest_directory.get_string_value()
        self._profile.compress = self._compress_backup.get_active()
        self._profile.apply_log = self._apply_log.get_active()

    def flush_schedule(self):
        self._profile.full_backups.enabled = self._full_backup_schedule.get_active()
        self._profile.full_backups.frequency = self._full_backup_frequency.get_selected_index()
        self._profile.full_backups.week_day = self._full_backup_dow.get_selected_index()
        self._profile.full_backups.month_day = self._full_backup_dom.get_selected_index()+1
        self._profile.full_backups.hour = self._full_backup_hour.get_selected_index()
        self._profile.full_backups.minute = self._full_backup_minute.get_selected_index()

        self._profile.inc_backups.enabled = self._inc_backup_schedule.get_active()
        self._profile.inc_backups.frequency = self._inc_backup_frequency.get_selected_index()
        self._profile.inc_backups.week_day = self._inc_backup_dow.get_selected_index()
        self._profile.inc_backups.month_day = self._inc_backup_dom.get_selected_index()
        self._profile.inc_backups.hour = self._inc_backup_hour.get_selected_index()
        self._profile.inc_backups.minute = self._inc_backup_minute.get_selected_index()
        
    def flush_comments(self):
        self._profile.comment = self._comment.get_string_value().encode("utf8")
        
    def cancel_changes(self):
        self._owner.hide_editor()
