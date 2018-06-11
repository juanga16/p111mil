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


import StringIO
import errno
from wb_common import InvalidPasswordError, PermissionDeniedError, joinpath, Users, sanitize_sudo_output, parentdir



class Frequency(object):
    #TODO : If once is added back this needs to be taken care of
    #       as the numbers will be different for full & inc
    hourly   = 0
    daily    = 1
    weekly   = 2
    monthly  = 3


class WBBackupServerInterface(object):
    def __init__(self, context):
        self._context = context
        self._needs_admin = None

    def get_verify_backup_command(self):
        pass

    def get_schedule_command(self, profile, type):
        pass

    def get_unschedule_command(self, profile, type):
        pass

    def execute_backup(self, profile, type, filename, output_handler=None):
        command = self.create_backup_command_call(profile, type, to_schedule=False, filename=filename)
        result = self._context.ctrl_be.server_helper.execute_command(command, as_user=self._context.mysql_user, user_password=self._context.ctrl_be.password_handler.get_password_for("file"), output_handler=output_handler)
        return result

    def unschedule_backup(self, profile):
        # Unschedules the full backup if exists
        command = self.get_unschedule_command(profile, 'full')
        self.perform_as_user(self._context.mysql_user, lambda as_user, user_password: self._context.ctrl_be.server_helper.execute_command(command, as_user=as_user, user_password=user_password))

        # Unschedules the incremental backup if exists
        command = self.get_unschedule_command(profile, 'incremental')
        self.perform_as_user(self._context.mysql_user, lambda as_user, user_password: self._context.ctrl_be.server_helper.execute_command(command, as_user=as_user, user_password=user_password))

    def schedule_backup(self, profile):
        # Reschedules the full backup if needed
        if profile.full_backups.enabled:
            command = self.get_schedule_command(profile, 'full')
            ret = self.perform_as_user(self._context.mysql_user, lambda as_user, user_password: self._context.ctrl_be.server_helper.execute_command(command, as_user=as_user, user_password=user_password))

        # Reschedules the incremental backup if needed
        if profile.inc_backups.enabled:
            command = self.get_schedule_command(profile, 'incremental')
            ret = self.perform_as_user(self._context.mysql_user, lambda as_user, user_password: self._context.ctrl_be.server_helper.execute_command(command, as_user=as_user, user_password=user_password))

    def create_backup_command_call(self, profile, type, to_schedule, filename=None):
        cmd_data = []
        if ' ' in self._context.config.backup_command:
            cmd_data.append('"%s"' % self._context.config.backup_command)
        else:
            cmd_data.append('%s' % self._context.config.backup_command)

        # Uses the configuration file for the backup (MUST be the 1st option)
        cmd_data.append('--defaults-file=%s' % profile.defaults_file)

        # If a filename is explicitly requested, then use it
        if filename:
            if type == 'incremental':
                #cmd_data.append('--backup-dir=%s' % joinpath(profile.backup_directory, filename))
                cmd_data.append('--incremental-backup-dir=%s' % joinpath(profile.backup_directory, filename))
            else:
                cmd_data.append('--backup-dir=%s' % joinpath(profile.backup_directory, filename))

        # Passes the mutually excluyent parameters
        if type == 'full':
            # The compress option is set only for full backups when apply-log is not
            # enabled, this is because --compress will be ignored anyway
            if profile.compress and not profile.apply_log:
                cmd_data.append('--compress')

        elif type == 'incremental':
            cmd_data.append('--incremental')

        # apply-log is only used on full backups when enabled
        if profile.apply_log and type == 'full':
            cmd_data.append('backup-and-apply-log')
        else:
            cmd_data.append('backup')

        return " ".join(cmd_data)


    def create_restore_command_call(self, backup_path, base_defaults_file, server_defaults_file):
        cmd_data = []
        cmd_data.append('"%s"' % self._context.config.backup_command)
        cmd_data.append('--defaults-file="%s"' % base_defaults_file)
        cmd_data.append('--defaults-extra-file="%s"' % server_defaults_file)
        cmd_data.append('--backup-dir="%s"' % backup_path)
        cmd_data.append('copy-back')
        return " ".join(cmd_data)


    def restore_backup(self, backup_entry, output_handler=None):
        # create a defaults file containing the cnf data saved by mysqlbackup in backup-my.cnf and
        # the last known correct datadir
        import uuid
        restore_defaults_file = joinpath(self._context.config.backup_home, str(uuid.uuid1())+"-restore.cnf")
        data = self.get_file_content(joinpath(backup_entry.data_path, "backup-my.cnf"))
        data += "datadir = %s\n" % self._context.config.datadir
        self.perform_as_user(self._context.mysql_user, lambda as_user, user_password: self._context.ctrl_be.server_helper.set_file_content(restore_defaults_file, data, as_user, user_password))

        try:
            command = self.create_restore_command_call(backup_entry.data_path, restore_defaults_file, backup_entry.profile.defaults_file)
            result = self._context.ctrl_be.server_helper.execute_command(command, as_user=self._context.mysql_user, user_password=self._context.ctrl_be.password_handler.get_password_for("file"), output_handler=output_handler)
        finally:
            try:
                self.perform_as_user(self._context.mysql_user, lambda as_user, user_password: self._context.ctrl_be.server_helper.delete_file(restore_defaults_file, as_user, user_password))
            except Exception, e:
                if output_handler:
                    output_handler("Could not delete temporary defaults file %s: %s\n" % (restore_defaults_file, e))
        return result


    def get_file_content(self, path):
        data= self.perform_as_user(self._context.mysql_user, lambda as_user, user_password: self._context.ctrl_be.server_helper.get_file_content(path, as_user, user_password))
        return sanitize_sudo_output(data)


    def execute_command(self, command, output_handler=None):
        return self.perform_as_user(Users.ADMIN, lambda as_user, user_password: self._context.ctrl_be.server_helper.execute_command(command, as_user, user_password, output_handler))


    def execute_as_mysql(self, command, output_handler=None):
        return self.perform_as_user(self._context.mysql_user, lambda as_user, user_password: self._context.ctrl_be.server_helper.execute_command(command, as_user, user_password, output_handler))


    def create_directory(self, path):
        raise NotImplementedError("create_directory must be overriden")


    def perform_as_user(self, as_user, callback):
        """
            Executes the passed in callback taking care of admin password handling.

            callback(as_user, user_password)
            """
        if self._needs_admin is None:
            try:
                r = callback(as_user = as_user, user_password = '')
                self._needs_admin = False
                return r
            except IOError, e:
                if e.errno == errno.EACCES:
                    # fallthrough to the password request looop
                    pass
                raise
            except PermissionDeniedError, e:
                # fallthrough to the password request looop
                self._needs_admin = True
            except InvalidPasswordError, e:
                # fallthrough to the password request looop
                self._needs_admin = True

        while True:
            user_password = self._context.ctrl_be.password_handler.get_password_for("file")

            try:
                # If called with a specific user ADMIN is not attempted, just the same
                # user with the retrieved password
                if as_user == Users.CURRENT:
                    as_user == Users.ADMIN

                return callback(as_user = as_user, user_password = user_password)
            except InvalidPasswordError, e:
                self._context.ctrl_be.password_handler.reset_password_for("file")
                continue


    def backup_apply_log(self, backup_path, is_compressed, output_handler):
        cmd_data = []
        cmd_data.append('"%s"' % self._context.config.backup_command)
        cmd_data.append('--backup-dir="%s"' % backup_path)
        if is_compressed:
            cmd_data.append('--uncompress')
        cmd_data.append('apply-log')
        return self.execute_as_mysql(" ".join(cmd_data), output_handler)


    def _apply_incremental_backup(self, backup_path, incremental_path, output_handler):
        cmd_data = []
        cmd_data.append('"%s"' % self._context.config.backup_command)
        cmd_data.append('--incremental-backup-dir="%s"' % incremental_path)
        cmd_data.append('--backup-dir="%s"' % backup_path)
        cmd_data.append('apply-incremental-backup')
        return self.execute_as_mysql(" ".join(cmd_data), output_handler)


    def _update_apply_log(self, backup_path, incremental_path):
        pass


    def _mark_incremental_applied(self, incremental_path):
        # if mysqlbackup some day adds this internally, this should be changed to only do it for older versions
        self.perform_as_user(self._context.mysql_user, lambda as_user, user_password: self._context.ctrl_be.server_helper.set_file_content(joinpath(incremental_path, "applied.txt"), "", as_user, user_password))


    def backup_apply_incremental(self, backup_path, incremental_path, archive_dir, output_handler):
        # 1- apply the incremental backup
        output_handler("Applying incremental backup...\n")
        ret = self._apply_incremental_backup(backup_path, incremental_path, output_handler)
        if ret != 0:
            output_handler("Apply incremental returned with exit code %i\n" % ret)
            raise RuntimeError("Apply incremental failed")
        else:
            output_handler("Apply finished successfully\n")

        # 2- mark the backup as already applied
        output_handler("Marking incremental backup as already applied\n")
        self._mark_incremental_applied(incremental_path)

        # 3- create our own metadata file for the full backup, containing info about incremental backups that were applied to it
        #self._update_apply_log(backup_path, incremental_path)

        # 4- move the incremental backup (since it's now useless) to the archive directory.. or just delete it
        output_handler("Moving applied incremental backup %s to archive directory\n" % incremental_path)
        self.move_file(incremental_path, archive_dir)


class WBBackupWindowsInterface(WBBackupServerInterface):
    def __init__(self, owner):
        WBBackupServerInterface.__init__(self, owner)
        output_text = []
        def gather_output(line, l=output_text):
            l.append(line)
        # Gets the user domain/user to be used on the file for scheduling
        self._context.ctrl_be.server_helper.execute_command('echo %userdomain%\%username%', as_user=Users.CURRENT, user_password=None, output_handler=gather_output)

        self._windows_user = output_text[0].strip()

    def get_verify_backup_command(self):
        return 'where mysqlbackup'

    def get_unschedule_command(self, profile, type):
        unschedule = []
        unschedule.append('schtasks')
        unschedule.append('/Delete')
        unschedule.append('/TN')
        unschedule.append('%s-%s' % (profile._uuid, type))
        unschedule.append('/F')
        return " ".join(unschedule)

    def get_schedule_command(self, profile, type):
        command = self.create_backup_command_call(profile, type, to_schedule=True)


        schedule_data = profile.full_backups if type == 'full' else profile.inc_backups

        weekdays=['SUN', 'MON','TUE','WED','THU','FRI','SAT']
        schedule = []
        schedule.append('schtasks')
        schedule.append('/Create')
        schedule.append('/TN')
        schedule.append('%s-%s' % (profile._uuid, type))
        schedule.append('/SC')

        if schedule_data.frequency == Frequency.hourly:
            schedule.append('HOURLY')
            schedule.append('/ST 00:%s' % str(schedule_data.minute).zfill(2))
        elif schedule_data.frequency == Frequency.daily:
            schedule.append('DAILY')
            schedule.append('/ST %s:%s' % (str(schedule_data.hour).zfill(2), str(schedule_data.minute).zfill(2)))
        elif schedule_data.frequency == Frequency.weekly:
            schedule.append('WEEKLY')
            schedule.append('/D')
            schedule.append(weekdays[schedule_data.week_day])
            schedule.append('/ST %s:%s' % (str(schedule_data.hour).zfill(2), str(schedule_data.minute).zfill(2)))
        elif schedule_data.frequency == Frequency.monthly:
            schedule.append('MONTHLY')
            schedule.append('/D')
            schedule.append(str(schedule_data.month_day))
            schedule.append('/ST %s:%s' % (str(schedule_data.hour).zfill(2), str(schedule_data.minute).zfill(2)))


        schedule.append('/TR')
        schedule.append('"%s"' % command)

        return " ".join(schedule)


    def create_directory(self, path):
        self.perform_as_user(self._context.mysql_user, lambda as_user, user_password: self._context.ctrl_be.server_helper.create_directory(path, as_user, user_password))


    def create_backup_command_call(self, profile, type, to_schedule, filename=None):
        # If the command is not to be scheduled it will return the direct call to
        # the mysqlbackup command
        if not to_schedule:
            return super(WBBackupWindowsInterface, self).create_backup_command_call(profile, type, to_schedule, filename)

        cmd_data = []

        script_name = joinpath(parentdir(self._context.server_profile.config_file_path), "mysqlwbbackup.vbs")

        cmd_data.append('\\"%s\\"' % script_name)

        # Uses the configuration file for the backup (MUST be the 1st option)
        cmd_data.append('%s.cnf' % profile._uuid)

        # Creates the values for compress and incremental
        compress_incremental = "0 0"
        if type == 'full':
            # The compress option is set only for full backups when apply-log is not
            # enabled, this is because --compress will be ignored anyway
            if profile.compress and not profile.apply_log:
                # 1 to indicate compress, 0 to indicate NOT incremental
                compress_incremental = '1 0'

        elif type == 'incremental':
            compress_incremental = "0 1"

        cmd_data.append(compress_incremental)

        # apply-log is only used on full backups when enabled
        if profile.apply_log and type == 'full':
            cmd_data.append('backup-and-apply-log')
        else:
            cmd_data.append('backup')

        # If a filename is explicitly requested, then use it
        if filename:
            cmd_data.append(filename)

        return " ".join(cmd_data)

    def move_file(self, from_path, to_path):
        command = "move %s %s" % (from_path, to_path)
        self.execute_as_mysql(command)


class WBBackupUnixInterface(WBBackupServerInterface):
    def __init__(self, owner):
        WBBackupServerInterface.__init__(self, owner)


    def get_verify_backup_command(self):
        return '/usr/bin/which mysqlbackup'

    def get_unschedule_command(self, profile, type):
        cron_file = "%s/wb_cron_file" % profile.backup_directory

        if type == 'full':
            return 'crontab -l | grep -v %s > %s; crontab %s;rm %s' % (profile._uuid, cron_file, cron_file, cron_file)
        else:
            return 'crontab -l | grep -v \"%s --incremental\" > %s; crontab %s;rm %s' % (profile._uuid, cron_file, cron_file, cron_file)

    def get_schedule_command(self, profile, type):
        # Configures the backup and log target paths
        log_path = profile.backup_directory
        filename = "\$BACKUP_NAME"
        
        if type == "incremental":
            filename = "inc/\$BACKUP_NAME"
            log_path = joinpath(log_path, 'inc')
            
        log_path = joinpath(log_path, "\$BACKUP_NAME.log 2>&1")
            
        # Creates the mysqlbackup command call
        command = self.create_backup_command_call(profile, type, to_schedule=True, filename=filename)
        
        # Chooses the proper scheduling data and creates the schedule command
        schedule_data = profile.full_backups if type == 'full' else profile.inc_backups

        schedule = []
        schedule.append(str(schedule_data.minute))
        schedule.append('*' if schedule_data.frequency == Frequency.hourly else str(schedule_data.hour))
        schedule.append('*' if schedule_data.frequency in [Frequency.hourly,Frequency.daily,Frequency.weekly] else str(schedule_data.month_day))
        schedule.append('*')
        schedule.append('*' if schedule_data.frequency != Frequency.weekly else str(schedule_data.week_day))
        schedule.append("BACKUP_NAME=\$(date +\%Y-\%m-\%d_\%H-\%M-\%S); " + command)

        schedule.append("> " + log_path)

        # A temporary file to store the crontab
        cron_file = "%s/wb_cron_file" % profile.backup_directory

        cron_entry = " ".join(schedule)
        schedule_command = 'crontab -l > %s; echo "%s" >> %s; crontab %s; rm %s' % (cron_file, cron_entry, cron_file, cron_file, cron_file)
        
        return schedule_command


    def create_directory(self, path):
        self.perform_as_user(Users.ADMIN, lambda as_user, user_password: self._context.ctrl_be.server_helper.create_directory(path, as_user, user_password))

        h = StringIO.StringIO()
        if self.execute_command("chown %s '%s'" % (self._context.mysql_user, path), h.write) != 0:
            raise RuntimeError(sanitize_sudo_output(h.getvalue()))

    def move_file(self, from_path, to_path):
        command = "mv %s %s" % (from_path, to_path)
        self.execute_as_mysql(command)
