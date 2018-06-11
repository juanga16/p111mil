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
import time
from mforms import newBox, newLabel, newButton, newTextEntry, newTable, newRadioButton, newListBox, newSelector, newPanel, newTabView, Utilities
from wb_admin_meb_common import add_table_field_label, add_table_field_value
from mforms import FileChooser, OpenDirectory, OpenFile
from wb_common import PermissionDeniedError, InvalidPasswordError, OperationCancelledError, parentdir, Users, joinpath

class BackupConfigurationPanel(mforms.Box):
    def __init__(self, owner, context):
        mforms.Box.__init__(self, False)
        self.set_managed()
        self.set_release_on_add()
        self._owner = owner
        self._context = context

        self.set_padding(8)
        self.set_spacing(8)

        label = mforms.newLabel("""MySQL Enterprise Backup allows MySQL server instances to be backed up "online"\nthat is, while the server is running and without locking InnoDB tables.\nTables using storage engines other than InnoDB can also be backed up\nbut table locking is necessary.\n\nTo be used, MySQL Enterprise Backup (mysqlbackup) must be installed in the target server.""")
        self.add(label, False, False)

        label = mforms.newLabel("Basic Settings")
        label.set_style(mforms.BoldStyle)
        self.add(label, False, False)

        label = mforms.newLabel("Provide the location in the remote server for the mysqlbackup utility and the backup home.\nBackup profiles and data will be placed in the backup home.")
        self.add(label, False, True)

        table = mforms.newTable()
        table.set_padding(20)
        table.set_row_count(5)
        table.set_column_count(2)
        table.set_row_spacing(6)
        table.set_column_spacing(4)

        add_table_field_label(table, 0, "MySQL Backup command path:")
        hbox = mforms.newBox(True)
        self._backup_command  = newTextEntry()
        self._backup_command.set_size(300,-1)
        self._backup_command.add_changed_callback(self.validate_command_when_idle)
        hbox.add(self._backup_command, False, False)
        self._command_button = newButton()
        self._command_button.set_text("...")
        self._command_button.enable_internal_padding(False)
        self._command_button.add_clicked_callback(lambda: self.open_file_chooser(OpenFile, self._backup_command))
        hbox.add(self._command_button, False, False)
        add_table_field_value(table, 0, hbox, mforms.HFillFlag)
        self._command_state = newLabel("")
        self._command_state.set_size(150, -1)
        hbox.add(self._command_state, False, True)
        
        self._command_error_lbl = newLabel("")
        self._command_error_lbl.set_text_align(mforms.MiddleLeft)
        self._command_error_lbl.set_color("#aa0000")
        table.add(self._command_error_lbl, 1, 2, 1, 2, mforms.HExpandFlag|mforms.HFillFlag)
        

        add_table_field_label(table, 2, "MySQL Backup home directory:")
        hbox = mforms.newBox(True)
        self._backup_home  = newTextEntry()
        self._backup_home.set_size(300,-1)
        self._backup_home.add_changed_callback(self.validate_home_when_idle)
        hbox.add(self._backup_home, False, False)
        self._home_button = newButton()
        self._home_button.set_text("...")
        self._home_button.enable_internal_padding(False)
        self._home_button.add_clicked_callback(lambda: self.open_file_chooser(OpenDirectory, self._backup_home))
        hbox.add(self._home_button, False, False)
        
        self._make_dir = newButton()
        self._make_dir.set_text("Create Directory")
        self._make_dir.add_clicked_callback(self.create_directory)
        hbox.add(self._make_dir, False, False)
        
        add_table_field_value(table, 2, hbox, mforms.HFillFlag)
        self._home_state = newLabel("")
        self._home_state.set_size(150, -1)
        hbox.add(self._home_state, False, True)
        
        self._home_error_lbl = newLabel("")
        self._home_error_lbl.set_color("#aa0000")
        self._home_error_lbl.set_text_align(mforms.MiddleLeft)
        table.add(self._home_error_lbl, 1, 2, 3, 4, mforms.HExpandFlag|mforms.HFillFlag)

        self.add(table, False, False)


        label = mforms.newLabel("MySQL Account for Backup")
        self.add(label, False, True)
        label.set_style(mforms.BoldStyle)

        self._account_label = mforms.newLabel("The mysqlbackup account will be used for backups.")
        self.add(self._account_label, False, False)
        table = mforms.newTable()
        table.set_row_count(2)
        table.set_column_count(2)
        table.set_row_spacing(8)
        table.set_column_spacing(8)
        self._password_label = add_table_field_label(table, 0, "Password:")
        self._password = newTextEntry(mforms.PasswordEntry)
        self._password.set_size(200, -1)
        add_table_field_value(table, 0, self._password)
        self._confirm_label = add_table_field_label(table, 1, "Confirm Password:")
        self._confirm = newTextEntry(mforms.PasswordEntry)
        self._confirm.set_size(200, -1)
        add_table_field_value(table, 1, self._confirm)
        self.add(table, False, True)

        hbox = mforms.newBox(True)
        hbox.set_spacing(12)
        hbox.set_padding(12)
        
        self._cancel_button = mforms.newButton()
        self._cancel_button.set_text("Cancel")
        self._cancel_button.add_clicked_callback(self.cancel_changes)
        hbox.add_end(self._cancel_button, False, True)

        self._ok_button = mforms.newButton()
        self._ok_button.set_text("OK")
        self._ok_button.add_clicked_callback(self.save_changes)
        hbox.add_end(self._ok_button, False, True)
        
        self.add_end(hbox, False, False)
        self._last_type_command_time = 0
        self._last_type_home_time = 0

        self._valid_home = False
        self._home_error = ""
        self._valid_command = False
        self._command_error = ""
        self._valid_backup_account = False

    def show(self, flag, allow_update_home = None):
        mforms.Box.show(self, flag)
        if flag:
            self._owner.update_main_view_label(" MySQL Enterprise Backup - Setup")

            self._home_error_lbl.set_color("#aa0000")

            # If not specified, counts the profiles to determine if the home can
            # be changed or not
            if allow_update_home is None:
                if self._home_error == "":
                    allow_update_home = (self._context.count_backup_profiles() == 0)

            if not allow_update_home is None:
                self._backup_home.set_enabled(allow_update_home)
                self._home_button.set_enabled(allow_update_home)
                if not allow_update_home:
                    self._home_error_lbl.set_color("#000000")
                    self._home_error_lbl.set_text("The backups home can't be changed because there are configured profiles.");
                    self._home_error_lbl.show(True)
                else:
                    self._home_error_lbl.show(False)


    def allow_cancel(self, flag):
        self._cancel_button.show(flag)


    def init(self):
        self._backup_command.set_value(self._context.config.backup_command)
        self._backup_home.set_value(self._context.config.backup_home)

        if self._context.config.backup_account_password is not None:
            self._password.set_value(self._context.config.backup_account_password)

        if 0:
            logbin = self._context.ctrl_be.exec_query("SHOW VARIABLES LIKE 'log_bin'")
            logbin = logbin.stringByName("Value") == "ON" if logbin and logbin.nextRow() else False
            if logbin:
                self._server_notes.set_text("Point in time recovery enabled (binary logging is ON)")
            else:
                self._server_notes.set_text("Point in time recovery disabled (binary logging is OFF)")

        # The configuration was validated when the object was created
        # This updates the UI to display the correct errors
        self._valid_home = self._context.config.valid_home
        self._home_error = self._context.config.home_error
        self._valid_command = self._context.config.valid_command
        self._command_error = self._context.config.command_error
        self._valid_backup_account = self._context.config.valid_backup_account
        self._backup_account_error = self._context.config.backup_account_error

        self.refresh_home_ui()
        self.refresh_command_ui()
        self.refresh_backup_account_ui()
        

    def validate_home_when_idle(self):
        self._last_type_home_time = time.time()
        mforms.Utilities.add_timeout(2, self.validate_home_if_idle)

    def validate_command_when_idle(self):
        self._last_type_command_time = time.time()
        mforms.Utilities.add_timeout(2, self.validate_command_if_idle)

    def validate_home_if_idle(self):
        if time.time() - self._last_type_home_time > 2:
            self.validate_home(False)
        return False
        
    def validate_command_if_idle(self):
        if time.time() - self._last_type_command_time > 2:
            self.validate_command(False)
        return False

    def open_file_chooser(self, file_chooser_type, textfield):
        filename = None
        if self._context.is_local:
            filechooser = FileChooser(file_chooser_type)
            filechooser.set_directory(textfield.get_string_value())
            if filechooser.run_modal():
                filename = filechooser.get_directory() if file_chooser_type is OpenDirectory else filechooser.get_path()
        else:
            from wba_ssh_ui import remote_file_selector
            filename = remote_file_selector(self._context.server_profile, self._context.ctrl_be.password_handler, self._context.ctrl_be.ssh, title="Select Remote File")

        if filename and (type(filename) is str or type(filename) is unicode):
            textfield.set_value(filename)

            # For now this criteria is enough to know what to validate
            if file_chooser_type == OpenFile:
                self.validate_command(False)
            else:
                self.validate_home(False)

    def validate_home(self, warn_errors):
        (self._valid_home, self._home_error) = self._context.config.validate_home(self._backup_home.get_string_value())

        if warn_errors and self._home_error != "":
            Utilities.show_error("Configuration Error", self._home_error, "OK", "", "")

        self.refresh_home_ui()

        return self._valid_home

    def refresh_home_ui(self):
        error = ""

        if self._valid_home:
            self._home_state.set_text("OK")
            self._home_state.set_color("#00aa00")
            self._home_error_lbl.set_text("")
            self._make_dir.show(False)
        else:
            self._home_state.set_text("Error")
            self._home_state.set_color("#aa0000")
            self._home_error_lbl.set_text(self._home_error)
            self._make_dir.show('The directory does not exist' in self._home_error)


    def validate_command(self, warn_errors):
        error = ""
        (self._valid_command, self._command_error) = self._context.config.validate_command(self._backup_command.get_string_value())

        if warn_errors and not self._valid_command:
            Utilities.show_error("Configuration Error", self._command_error, "OK", "", "")

        self.refresh_command_ui()

        return self._valid_command

    def refresh_command_ui(self):
        if self._valid_command:
            self._command_state.set_text("OK")
            self._command_state.set_color("#00aa00")
            self._command_error_lbl.set_text("")
        else:
            self._command_state.set_text("Error")
            self._command_state.set_color("#aa0000")
            self._command_error_lbl.set_text(self._command_error)


    def validate_backup_account(self, warn_errors):
        self._backup_account_error = ""

        # Gets the password
        p = self._password.get_string_value()

        # If it is a new account, ensures both passwords are equal
        if not self._context.config.backup_account_exists:
            c = self._confirm.get_string_value()
            if not p:
                self._backup_account_error = "Please specify a password for the mysqlbackup account."
            elif p != c:
                self._backup_account_error = "Password and confirmation for the mysqlbackup account don't match."

        # In an existing account, validates it against the password
        else:
            (self._valid_backup_account, self._backup_account_error) = self._context.config.validate_backup_account(p)

        if warn_errors and self._backup_account_error:
            Utilities.show_error("Configuration Error", self._backup_account_error, "OK", "", "")

        self._valid_backup_account = (self._backup_account_error == "")

        self.refresh_backup_account_ui()

        return self._valid_backup_account


    def refresh_backup_account_ui(self):
        if not self._context.has_connection:
            self._account_label.set_text("There is no connection to the MySQL server. The server must be running for backup to be configured.")
            self._password.show(False)
            self._password_label.show(False)
            self._confirm.show(False)
            self._confirm_label.show(False)
        else:
            if not self._context.config.backup_account_exists:
                self._account_label.set_text("A MySQL user account called '%s'@localhost has to be created to be used for backups.\nPlease provide a password for it." % self._context.config.backup_account)
                self._password.show(True)
                self._password_label.show(True)
                self._confirm.show(True)
                self._confirm_label.show(True)
            else:
                if self._valid_backup_account:
                    self._account_label.set_text("The '%s' MySQL user account will be used for backups." % self._context.config.backup_account)
                    self._password.show(False)
                    self._password_label.show(False)
                    self._confirm.show(False)
                    self._confirm_label.show(False)
                else:
                    self._account_label.set_text("The '%s' MySQL user account will be used for backups.\nPlease provide its password below." % self._context.config.backup_account)
                    self._password.show(True)
                    self._password_label.show(True)
                    self._confirm.show(False)
                    self._confirm_label.show(False)
                    
                    
    def validate_config(self, warn_errors):

        ret_val = self.validate_command(warn_errors)
        
        if ret_val:
            ret_val = self.validate_home(warn_errors)

        if ret_val:
            ret_val = self.validate_backup_account(warn_errors)

        return ret_val

    def create_directory(self, as_user = Users.CURRENT):
        admin_password = None
        while True:
            try:
                # TODO: move this to ServerInterface and make it so that a chown is executed afterwards
                self._context.ctrl_be.server_helper.create_directory(self._backup_home.get_string_value(), as_user, admin_password)

                self._context.ctrl_be.server_helper.create_directory(joinpath(self._backup_home.get_string_value(), 'archive'), as_user, admin_password)
                break
            except InvalidPasswordError:
                self._context.forget_admin_password()
            except PermissionDeniedError, e:
                if as_user == Users.CURRENT:
                    as_user = Users.ADMIN
            except Exception, e:
                mforms.Utilities.show_error("Create Directory", str(e), "OK", "", "")
                return
            try:
                admin_password = self._context.get_admin_password()
            except OperationCancelledError, e:
                return

        self.validate_home(False)


    def save_changes(self):

        if self.validate_config(True):
            # Updates the data on the configuration...
            self._context.config.backup_command = self._backup_command.get_string_value()
            self._context.config.backup_home = self._backup_home.get_string_value()
            self._context.config.backup_account_password = self._password.get_string_value()

            if self._context.config.changed:
                # At this point all the validations must be reset on the loaded config
                # as the new values are OK
                self._context.config.valid_home = self._valid_home
                self._context.config.home_error = self._home_error
                self._context.config.valid_command = self._valid_command
                self._context.config.command_error = self._command_error
                self._context.config.valid_backup_account = self._valid_backup_account
                self._context.config.backup_account_error = self._backup_account_error

                self._context.config.save()

            self._owner.hide_config()
            self.allow_cancel(True)


    def cancel_changes(self):
        self._owner.hide_config()
        
