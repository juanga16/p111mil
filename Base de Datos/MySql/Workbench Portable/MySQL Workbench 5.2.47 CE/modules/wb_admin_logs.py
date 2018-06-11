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

"""
How to handle MySQL logs
*************************

Among other things this module needs to establish:

1. Which of the logs (if any) are enabled.
2. Whether the output of the enabled logs are stored in a table or in a log file.


Determining the state of the logs
-----------------------------------

There are two possible scenarios:

the server is down:
    In this case all logs are assumed to be **disabled** since the server won't
    be logging anything unless it's running.

the server is up:
    Starting with MySQL Server 5.1.29 the relevant server variables changed.
    This derives in two new scenarios:

    server version < 5.1.29:
        :general query log:
            The state of this log is reflected in the server variable ``log``
            which will be set to ``'OFF'`` if the log is disabled or to either
            ``'ON'`` or to ``'1'`` or to a file path if the log is enabled.

        :slow query log:
            Its state is reflected in the server variable ``log_slow_queries``
            which will be set to ``'OFF'`` if the log is disabled or to
            ``'ON'`` or to ``'1'``  if the log is enabled.

        :error log:
            Its state is reflected in the server variable ``log_error``
            which will be set to ``''`` (the empty string) if the log is disabled
            or to the path to the error log file if the log is enabled.

            .. note::

               The error logs are not going to be written to the error log file
               if the server was started with the ``--console`` command line
               option on Windows, even if ``log_error`` has a path set up. In
               this case error logs are written to stderr.

               It seems that there's no way to query the server to determine if
               this ``--console`` option is in place.

        .. note::

           The ``log_slow_queries`` and ``log`` variable were removed in MySQL
           Server 5.6.

    server version >= 5.1.29:
        :general query log:
            If enabled the ``general_log`` variable will be set to ``'ON'`` or
            to ``'1'``. Otherwise it will be set to ``'OFF'`` or to ``'0'``.

        :slow query log:
            If enabled the ``slow_query_log`` variable will be set to ``'ON'`` or
            to ``'1'``. Otherwise it will be set to ``'OFF'`` or to ``'0'``.

        :error log:
            Its state is reflected in the server variable ``log_error`` as
            explained for server version < 5.1.29.

    .. note::

       For MySQL Server versions >= 5.1.6, if the variable ``log_output``
       contains the value ``'NONE'``, the general query log and the slow
       query log will not record any new log entry.

       The general log can also be disabled by setting to ``'1'`` the session
       variable ``sql_log_off``.


Determining where the logs are being written
---------------------------------------------

Starting from MySQL Server 5.1.6 there's the possibility of sending the logs
from the general query log or from the slow query log to a server table instead
of to a log file. This is controlled by the value of the variable ``log_output``
which can be a combination of the values ``'FILE'`` (log into log files),
``'TABLE'`` (log into a server table) or ``'NONE'`` (don't log). If given, ``'NONE'``
takes precedence over the other values.

.. warning::

   For MySQL Server versions older than 5.1.29 there's no reliable way to know
   where the general and slow query logs are being written (if they are logged
   to a file). Their default values are ``$datadir + $hostname + '.log'`` and
   ``$datadir + $hostname + '-slow.log'``, respectively. This can be changed
   in the command line or in the configuration file and the real paths will not
   be exposed in any server variable.

Starting from MySQL Server 5.1.29 the paths to the general and slow query log
files are stored in the ``general_query_log_file`` and in the``slow_query_log_file``
variables, respectively. *The server creates the file in the data directory unless
an absolute path name is given to specify a different directory.*



Use cases for the server logs
---------------------------------

1. The server is running. All logs are enabled and WB can precisely determine their
   sources. Every log is shown in its corresponding tab.

2. The ``log_output`` server variable contains both ``'FILE'`` and ``'TABLE'``.
   WB will select on a per log basis which source should be chosen. Will select
   table logs if the server is local or if the server is remote and any of these
   happen:

   * Cannot reliably determine the paths to the log file.
   * The user running WB has no read permissions on the log file.
   * The log file does not exist.
   * The user explicitly requested to read from log table.

3. ``log_output`` contains ``'NONE'``. Nonetheless WB will check for log sources
   and will show them, alerting the user about log not being updated because of
   that. *What to do if there are log files and log tables available in this case?*

4. The server is logging to files and WB can precisely determine their paths but
   the log file is missing in the file system. The situation will be reported to
   the user (advising him to ``FLUSH LOGS`` or restart the server and start querying)
   The log will not be shown as long as this situation persists.

5. The server is logging to tables and the connection to the server is lost. If the
   server is also logging to files, and a log file exists in the file system, the
   log file will be shown and the user will be warned about this change.

6. The server is logging to files and WB cannot precisely determine the path to the
   log file (i.e. server version < 5.1.29). WB will try to get the path from these
   sources in this order:

   1. The server's configuration file.
   2. The default path assumed by the server when no log path is specified.

   If no such file is found in the file system the log will not be shown.

7. The user changed the source of a log or the path to a log file while WB was
   showing the previous source/path. WB will switch to the new source/path and will
   inform the user of the change.

8. [Postponed] The user clicks on a *Add new log* button. A dialog will be shown in
   which the user will select the type of log to be added (error, general or slow),
   the log source (a database table or a log file) and the name of the log table/file.
   A new tab showing the user selected log will be shown and will persist during the
   session or until the user clicks on the tab's *Close* button.
"""

import os

from mforms import newBox, newLabel, newTreeNodeView, newTabView, newButton
import mforms
from wb_admin_utils import not_running_warning_label, not_running_warning_label_text
from wb_log_reader import GeneralQueryLogReader, SlowQueryLogReader, GeneralLogFileReader, SlowLogFileReader, ErrorLogFileReader

from wb_common import LogFileAccessError, ServerIOError, OperationCancelledError, InvalidPasswordError, log_error_decorator

from grt import log_info, log_error, log_warning, log_debug, log_debug2, log_debug3
_this_file = os.path.basename(__file__)

class LogView(mforms.Box):
    '''
    Main front end view class for displaying log entries.

    Each page in the Tab View is an instance of this class.
    '''
    def __init__(self, owner, BackendLogReaderClass, *args):
        '''
        The arguments following BackendLogReaderClass will be passed to
        BackendLogReaderClass to instantiate it in order to get a log
        reader object.
        '''

        super(LogView, self).__init__(False)
        self.set_managed()
        self.set_release_on_add()
        self.owner = owner

        self.BackendLogReaderClass = BackendLogReaderClass
        self.args = args

        self.log_reader = None
        self.error_box = None
        self.tree = None
        self.bbox = None
        self.warning_box = None
        self.update_ui()

    @log_error_decorator
    def _show_error(self, error):
        if self.error_box:
            self.remove(self.error_box)
            self.error_box = None
        self.error_box = newBox(True)
        self.error_box.set_spacing(8)
        error_label = newLabel(str(error))
        self.error_box.add(error_label, False, False)
        try_again_button = newButton()
        try_again_button.set_text('Try again')
        self.error_box.add(try_again_button, False, False)
        try_again_button.add_clicked_callback(self.update_ui)
        self.add(self.error_box, False, True)

    def update_ui(self):
        # Clean up:
        if self.error_box:
            self.remove(self.error_box)
            self.error_box = None

        if self.tree:
            self.remove(self.tree)
            self.tree = None

        if self.bbox:
            self.remove(self.bbox)
            self.bbox = None

        if self.warning_box:
            self.remove(self.warning_box)
            self.warning_box = None

        self.set_padding(8)
        self.set_spacing(8)

        try:
            self.log_reader = self.BackendLogReaderClass(*self.args)
        except (ServerIOError, LogFileAccessError, OperationCancelledError, InvalidPasswordError, IOError, ValueError), error:
            self._show_error(error)
            return

        if self.log_reader.partial_support:
            self.warning_box = newBox(True)
            self.warning_box.set_spacing(8)
            warning_label = newLabel(self.log_reader.partial_support)
            self.warning_box.add(warning_label, False, False)
            self.add(self.warning_box, False, True)

        self.tree = newTreeNodeView(mforms.TreeFlatList)
        self.tree.set_selection_mode(mforms.TreeSelectMultiple)

        for colspec in self.log_reader.column_specs:
            self.tree.add_column(mforms.StringColumnType,
                                 colspec[0],  # column header
                                 colspec[1],  # column width
                                 False)
        self.tree.end_columns()

        self.add(self.tree, True, True)

        self.bbox = newBox(True)
        self.bbox.set_spacing(8)
        self.add_end(self.bbox, False, True)

        self.range_label = newLabel("")
        self.bbox.add(self.range_label, True, True)

        self.view_button = newButton()
        self.view_button.set_text("Copy Selected")
        self.bbox.add(self.view_button, False, True)
        self.view_button.add_clicked_callback(self.copy_details)

        self.bof_button = newButton()
        self.bof_button.set_text("<<")
        self.bbox.add(self.bof_button, False, True)
        self.bof_button.add_clicked_callback(self.go_bof)

        self.back_button = newButton()
        self.back_button.set_text("<")
        self.bbox.add(self.back_button, False, True)
        self.back_button.add_clicked_callback(self.go_back)

        self.next_button = newButton()
        self.next_button.set_text(">")
        self.bbox.add(self.next_button, False, True)
        self.next_button.add_clicked_callback(self.go_next)

        self.eof_button = newButton()
        self.eof_button.set_text(">>")
        self.bbox.add(self.eof_button, False, True)
        self.eof_button.add_clicked_callback(self.go_eof)

        self.refresh_button = newButton()
        self.refresh_button.set_text("Refresh")
        self.bbox.add(self.refresh_button, False, True)
        self.refresh_button.add_clicked_callback(self.refresh)

        try:
            self.refresh(self.log_reader.last())
        except (ServerIOError, LogFileAccessError, OperationCancelledError, InvalidPasswordError, IOError, ValueError), error:
            self._show_error(error)

    def refresh(self, records=None):
        if self.log_reader:
            try:
                self.log_reader.refresh()

                if not records:
                    records = self.log_reader.current()
                self.tree.clear()
                for rec in records:
                    row = self.tree.add_node()
                    for idx, col in enumerate(rec):
                        row.set_string(idx, col.strip())
                self.range_label.set_text(self.log_reader.range_text())
                self.bof_button.set_enabled(self.log_reader.has_previous())
                self.back_button.set_enabled(self.log_reader.has_previous())
                self.eof_button.set_enabled(self.log_reader.has_next())
                self.next_button.set_enabled(self.log_reader.has_next())
            except (ServerIOError, LogFileAccessError, OperationCancelledError, InvalidPasswordError, IOError, ValueError), error:
                self._show_error(error)

    def copy_details(self):
        selection = self.tree.get_selection()
        text = []
        for node in selection:
            text.append(node.get_string(self.log_reader.detail_column))
        if text:
            mforms.Utilities.set_clipboard_text("\n".join(text))

        #sel = self.tree.get_selected_node()
        #if sel:
        #    text = sel.get_string(self.log_reader.detail_column)
        #    mforms.Utilities.set_clipboard_text(text)

    def go_bof(self):
        try:
            self.refresh(self.log_reader.first())
        except (ServerIOError, LogFileAccessError, OperationCancelledError, InvalidPasswordError, IOError, ValueError), error:
            self._show_error(error)

    def go_eof(self):
        try:
            self.refresh(self.log_reader.last())
        except (ServerIOError, LogFileAccessError, OperationCancelledError, InvalidPasswordError, IOError, ValueError), error:
            self._show_error(error)

    def go_back(self):
        try:
            records = self.log_reader.previous() if self.log_reader.has_previous() else None
            self.refresh(records)
        except (ServerIOError, LogFileAccessError, OperationCancelledError, InvalidPasswordError, IOError, ValueError), error:
            self._show_error(error)

    def go_next(self):
        try:
            records = self.log_reader.next() if self.log_reader.has_next() else None
            self.refresh(records)
        except (ServerIOError, LogFileAccessError, OperationCancelledError, InvalidPasswordError, IOError, ValueError), error:
            self._show_error(error)


class WbAdminLogs(mforms.Box):
    ui_created = False

    def __init__(self, ctrl_be, server_profile, main_view):
        super(WbAdminLogs, self).__init__(False)
        main_view.ui_profile.apply_style(self, 'page')
        self.set_managed()
        self.ctrl_be = ctrl_be
        self.server_profile = server_profile
        self.main_view = main_view
        self.disable_log_refresh = False
        self.main_view.add_content_page(self, "MANAGEMENT", "Server Logs", "admin_server_logs_win")

    def create_ui(self):
        self.warning = not_running_warning_label()
        self.add(self.warning, False, True)
        self.warning.show(False)

        self.tabView = newTabView(False)
        self.add(self.tabView, True, True)

        self.general_log_tab = None
        self.slow_log_tab = None
        self.general_file_log_tab = None
        self.slow_file_log_tab = None
        self.error_file_log_tab = None

    def get_log_destination(self):
        dest = {}
        if self.ctrl_be.is_sql_connected():  # If server is up, query the destination from there
            if self.ctrl_be.server_version < (5, 1, 6):  # Logging to TABLE was introduced in v5.1.6
                try:
                    result = self.ctrl_be.exec_query("SHOW VARIABLES LIKE 'log'")
                    if not result.nextRow():
                        return dest
                except:
                    return dest
                self.server_profile.log_output = 'FILE' if result.stringByName("Value")=='ON' else 'NONE'
                log_debug(_this_file, '%s: log_output = %s\n' % (self.__class__.__name__, self.server_profile.log_output) )
            else:
                try:
                    result = self.ctrl_be.exec_query("SHOW VARIABLES LIKE 'log_output'")
                    if not result.nextRow():
                        return dest
                except:
                    return dest
                self.server_profile.log_output = result.stringByName("Value")

                if 'FILE' in self.server_profile.log_output and 'TABLE' in self.server_profile.log_output:
                    def open_remote_file(path):
                        import wb_admin_ssh, wb_server_control
                        ssh = wb_admin_ssh.WbAdminSSH()
                        ssh.wrapped_connect(self.server_profile, wb_server_control.PasswordHandler(self.server_profile))
                        sftp = ssh.client.open_sftp()
                        if not ssh.is_connected():
                            raise IOError, ''
                        sftp.open(path)

                    # Can't read logs from files if admin is disabled:
                    if not self.server_profile.admin_enabled:
                        dest['general_log'] = 'TABLE'
                        dest['slow_log'] = 'TABLE'
                        log_debug(_this_file, '%s: log_output = %s\n' % (self.__class__.__name__, dest) )
                        return dest

                    # Try to prioritize the files if they are readable
                    if not getattr(self, 'stored_general_log_source_choice', None):
                        if self.server_profile.general_log_file_path:
                            try:
                                open(self.server_profile.general_log_file_path) if self.server_profile.is_local else open_remote_file(self.server_profile.general_log_file_path)
                                dest['general_log'] = 'FILE'
                            except:
                                dest['general_log'] = 'TABLE'
                        else:
                            dest['general_log'] = 'TABLE'
                        self.stored_general_log_source_choice = dest['general_log']
                    else:
                        dest['general_log'] = self.stored_general_log_source_choice

                    if not getattr(self, 'stored_slow_log_source_choice', None):
                        if self.server_profile.slow_log_file_path:
                            try:
                                open(self.server_profile.slow_log_file_path) if self.server_profile.is_local else open_remote_file(self.server_profile.slow_log_file_path)
                                dest['slow_log'] = 'FILE'
                            except:
                                dest['slow_log'] = 'TABLE'
                        else:
                            dest['slow_log'] = 'TABLE'
                        self.stored_slow_log_source_choice = dest['slow_log']
                    else:
                        dest['slow_log'] = self.stored_slow_log_source_choice
                log_debug(_this_file, '%s: log_output = %s\n' % (self.__class__.__name__, dest) )
        return dest

    def show_message_panel(self, msg):
        self.warning.set_text(msg)
        self.warning.show(True)
        self.tabView.show(False)

    def _remove_tabs(self, *source):
        if 'TABLE' in source:
            source = list(source) + ['general_tab', 'slow_tab']

        if 'FILE' in source:
            source = list(source) + ['general_file_tab', 'slow_file_tab']

        if 'general_tab' in source and self.general_log_tab:
            self.tabView.remove_page(self.general_log_tab)
            self.general_log_tab = None
        if 'slow_tab' in source and self.slow_log_tab:
            self.tabView.remove_page(self.slow_log_tab)
            self.slow_log_tab= None
        if 'general_file_tab' in source and self.general_file_log_tab:
            self.tabView.remove_page(self.general_file_log_tab)
            self.general_file_log_tab = None
        if 'slow_file_tab' in source and self.slow_file_log_tab:
            self.tabView.remove_page(self.slow_file_log_tab)
            self.slow_file_log_tab = None
        if 'error_file_tab' in source and self.error_file_log_tab:
            self.tabView.remove_page(self.error_file_log_tab)
            self.error_file_log_tab = None

    def _add_tabs(self, *source):
        if 'TABLE' in source:
            source = list(source) + ['general_tab', 'slow_tab']

        if 'FILE' in source:
            source = list(source) + ['general_file_tab', 'slow_file_tab']

        if 'error_file_tab' in source and self.server_profile.error_log_file_path and not self.error_file_log_tab:
            try:
                self.error_file_log_tab = LogView(self, ErrorLogFileReader, self.ctrl_be, self.server_profile.error_log_file_path)
                self.tabView.add_page(self.error_file_log_tab, "Error Log File")
            except IOError:
                self.show_message_panel('There was a problem reading %s. Please verify that you have read permissions on that file' % self.server_profile.error_log_file_path)
                self.error_file_log_tab = None

        if 'general_file_tab' in source and self.server_profile.general_log_enabled and self.server_profile.general_log_file_path and not self.general_file_log_tab:
            try:
                self.general_file_log_tab = LogView(self, GeneralLogFileReader, self.ctrl_be, self.server_profile.general_log_file_path)
                self.tabView.add_page(self.general_file_log_tab, "General Log File")
            except IOError:
                self.show_message_panel('There was a problem reading %s.\nPlease verify that you have read permissions on that file' % self.server_profile.general_log_file_path)
                self.general_file_log_tab = None


        if 'slow_file_tab' in source and self.server_profile.slow_log_enabled and self.server_profile.slow_log_file_path and not self.slow_file_log_tab:
            try:
                self.slow_file_log_tab = LogView(self, SlowLogFileReader, self.ctrl_be, self.server_profile.slow_log_file_path)
                self.tabView.add_page(self.slow_file_log_tab, "Slow Log File")
            except IOError:
                self.show_message_panel('There was a problem reading %s. Please verify that you have read permissions on that file' % self.server_profile.slow_log_file_path)
                self.slow_file_log_tab = None

        if 'general_tab' in source and self.server_profile.general_log_enabled and not self.general_log_tab:
            self.general_log_tab = LogView(self, GeneralQueryLogReader, self.ctrl_be)
            self.tabView.add_page(self.general_log_tab, 'General Log Table')

        if 'slow_tab' in source and self.server_profile.slow_log_enabled and not self.slow_log_tab:
            self.slow_log_tab = LogView(self, SlowQueryLogReader, self.ctrl_be)
            self.tabView.add_page(self.slow_log_tab, 'Slow Query Log Table')

    def update_ui(self):
        dest = self.get_log_destination()

        self._add_tabs('error_file_tab')

        if not self.server_profile.log_output:
            self.server_profile.log_output = 'TABLE,FILE'

        if 'NONE' in self.server_profile.log_output:
            self._remove_tabs('TABLE', 'FILE')

        elif self.server_profile.log_output == 'FILE':
            self._remove_tabs('TABLE')
            self._add_tabs('FILE')

        elif self.server_profile.log_output == 'TABLE':
            self._remove_tabs('FILE')
            self._add_tabs('TABLE')

        elif self.server_profile.log_output == 'TABLE,FILE' or self.server_profile.log_output == 'FILE,TABLE':
            tabs = set(['general_tab', 'slow_tab', 'general_file_tab', 'slow_file_tab'])
            to_be_added = []
            if not self.ctrl_be.is_sql_connected():
                to_be_added = ['general_file_tab', 'slow_file_tab']
            else:
                to_be_added.append( 'general_file_tab' if dest['general_log'] == 'FILE' else 'general_tab')
                to_be_added.append( 'slow_file_tab' if dest['slow_log'] == 'FILE' else 'slow_tab')
            self._remove_tabs( *tuple(tabs - set(to_be_added)) )  # Remove the ones that aren't added
            self._add_tabs( *tuple(to_be_added) )

        else:
            msg = """We have detected a problem in your current Log Destination.
It is set to %s. Please refer to the documentation for further information:
http://dev.mysql.com/doc/refman/5.1/en/log-destinations.html""" % self.server_profile.log_output
            self.show_message_panel(msg)
            return

        self.warning.show(False)
        self.tabView.show(True)

    def page_activated(self):
        self.main_view.set_content_label(" Server Logs")
        if not self.ui_created:
            self.create_ui()
            self.ui_created = True

        self.update_ui()
        try:
            self.refresh()
        except Exception, e:
            r = mforms.Utilities.show_warning("Log Refresh", "An error occurred while displaying MySQL server logs: %s" % e, "Ignore", "Cancel", "")
            if r == mforms.ResultCancel:
                self.disable_log_refresh = True

    def refresh(self):
        if self.disable_log_refresh:
            return
        if self.ctrl_be.is_sql_connected():
            if self.general_log_tab:
                self.general_log_tab.refresh()
            if self.slow_log_tab:
                self.slow_log_tab.refresh()
        if self.general_file_log_tab:
            self.general_file_log_tab.refresh()
        if self.slow_file_log_tab:
            self.slow_file_log_tab.refresh()
        if self.error_file_log_tab:
            self.error_file_log_tab.refresh()

    def do_refresh(self):
        pass
