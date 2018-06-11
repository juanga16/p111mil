# Copyright (c) 2011, 2012, Oracle and/or its affiliates. All rights reserved.
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
.. module:: wb_log_reader
   :synopsis: Reads and parses a log source to retrieve sets of records from it.

This module defines several classes to handle MySQL server logs. It supports logs
stored in the database as well as logs stored in files.

All of the defined classes adhere to a common interface defining and implementing
these public attributes and methods:

Attributes:

    column_specs (tuple):  Specifies each field in the log entries. The elements
            of this tuple are also tuples having the form
            (column_name, column_widh, [column_table_name])
            where:
                column_name (str):  A human readable name for the column. Frontend
                                    code should use this name wherever a column
                                    title is needed.
                column_width (int): The recommended with of the column
                column_table_name (str):  (Optional) the name of the field referred
                                          by this column in the log table for DB logs

    partial_support:        False if the log source is fully supported or a
                            string explaining the limitations regarding the implemented
                            log source reader class otherwise.

Methods:

    has_previous():    Returns True if there are older entries that can be
                       retrieved and False otherwise.

    has_next():        Returns True if there are newer entries that can be
                       retrieved and False otherwise.

    first():           Returns a list of the first (oldest) records in the log.
                       Each element in this list represents a single log entry
                       and is also a list whose elements are the values for the
                       columns defined in `column_specs`.

    last():            The same as `first()` but the records returned are the
                       newest ones.

    previous():        Returns the records that precede the last retrieved
                       records. Before calling it you should verify that
                       `has_previous()` returns True.

    next():            Returns the records that follow the last retrieved
                       records. Before calling it you should verify that
                       `has_next()` returns True.

    current():         Returns the last retrieved records.

    range_text():      Returns a string that gives an indication of the position
                       of the current records in the existent log set (if
                       available). E.g. 'Records 1..50 of 145'


    refresh():         After calling this function the log reader should be able
                       to manage new log entries that were added since the last
                       call to this function or since the creation of the log
                       reader object. This function doesn't return anything.

If it is not possible to read the log entries, the class should raise an
exception with a descriptive message to let the user know the reasons of
the failure.

Current limitations:
----------------------

* No remote server support for logs stored in files.

* Cannot read files that aren't readable by the user running Workbench.

"""

import re
import os
import StringIO

from wb_admin_ssh import WbAdminSSH, ConnectionError
from wb_server_control import PasswordHandler

from wb_common import LogFileAccessError, ServerIOError, InvalidPasswordError, Users
from workbench.utils import server_os_path

#========================= Query Based Readers ================================

class BaseQueryLogReader(object):
    """
    The base class for logs stored in a database.

    **This is not intended for direct instantiation.**
    """
    def __init__(self, ctrl_be, log_table, column_specs, ordering_column):
        """Constructor

        :param ctrl_be:  Control backend instance to make queries
        :param log_table: The name of the table where the log entries are stored
        :type log_table: str
        :param column_specs: Column definitions as explained in the module docstring
        :type column_specs: tuple
        :param ordering_column: The index for the column in `column_specs` that stores
                                the timestamp of the log entries
        :type ordering_column: int
        """
        self.log_table = log_table
        self.ctrl_be = ctrl_be
        self.column_specs = column_specs
        self.ordering_column = ordering_column

        self.partial_support = False

        self.total_count = 0
        self.refresh()  # Updates self.total_count
        self.show_count = 50
        self.show_start = max(self.total_count - self.show_count, 0)
        self.colnames = [ colspec[2] for colspec in column_specs ]

    def has_previous(self):
        return self.show_start > 0

    def has_next(self):
        return self.show_start < self.total_count - 1

    def current(self):
        return self._query_records()

    def previous(self):
        self.show_start = max(self.show_start - self.show_count, 0)
        return self._query_records()

    def next(self):
        self.show_start = min(self.show_start + self.show_count, self.total_count)
        return self._query_records()

    def first(self):
        self.show_start = 0
        return self._query_records()

    def last(self):
        self.show_start = max(self.total_count - self.show_count, 0)
        return self._query_records()

    def range_text(self):
        return 'Records %d..%d of %d' % (self.show_start,
                                         min(self.show_start + self.show_count, self.total_count),
                                         self.total_count)

    def refresh(self):
        try:
            result = self.ctrl_be.exec_query("SELECT count(*) AS count FROM %s" % self.log_table)
        except Exception, e:
            raise ServerIOError('Error fetching log contents: %s' % e)
        if not result or not result.nextRow():
            raise ServerIOError('Error fetching log contents')
        self.total_count = result.intByName('count')

    def _query_records(self):
        query = "SELECT * FROM %s ORDER BY %s DESC LIMIT %i, %i"  % (
                        self.log_table,
                        self.colnames[self.ordering_column],
                        self.show_start,
                        self.show_count)
        try:
            result = self.ctrl_be.exec_query(query)
        except Exception, e:
            raise ServerIOError('Error fetching log contents: %s' % e)

        records = []
        if result:
            while result.nextRow():
                row = [ result.stringByName(colname) for colname in self.colnames ]
                records.append(row)
        elif self.total_count:
            raise IOError('There were problems querying the server table %s.' % self.log_table)

        return records


class GeneralQueryLogReader(BaseQueryLogReader):
    def __init__(self, ctrl_be, table_name='mysql.general_log'):
        column_specs = (
            ('Time', 150, 'event_time'),
            ('From', 120, 'user_host'),
            ('Thread', 80, 'thread_id'),
            ('Server', 80, 'server_id'),
            ('Command Type', 80, 'command_type'),
            ('Detail', 500, 'argument')
                        )
        self.detail_column = 5
        super(GeneralQueryLogReader, self).__init__(ctrl_be, table_name, column_specs, 0)

class SlowQueryLogReader(BaseQueryLogReader):
    def __init__(self, ctrl_be, table_name='mysql.slow_log'):
        column_specs = (
            ('Start Time', 150, 'start_time'),
            ('From', 120, 'user_host'),
            ('Query Time', 150, 'query_time'),
            ('Lock Time', 150, 'lock_time'),
            ('Rows Sent', 50, 'rows_sent'),
            ('Rows Examined', 50, 'rows_examined'),
            ('DB', 80, 'db'),
            ('Last Insert ID', 50, 'last_insert_id'),
            ('Insert ID', 50, 'insert_id'),
            ('Server ID', 50, 'server_id'),
            ('SQL', 500, 'sql_text'),
                        )
        self.detail_column = 10
        super(SlowQueryLogReader, self).__init__(ctrl_be, table_name, column_specs, 0)


#========================= File Based Readers =================================

class BaseLogFileReader(object):
    '''
    The base class for logs stored in files.

    **This is not intended for direct instantiation.**
    '''
    def __init__(self, ctrl_be, log_file, pat, chunk_size, truncate_long_lines, append_gaps=True):
        """Constructor

        :param ctrl_be:  Control backend instance to retrieve root password if needed
        :param log_file: The path to the log file to read from or a file like instance to
                         read log entries from
        :type log_file: str/file
        :param pat: A regular expression pattern that matches a log entry
        :type pat: regular expression object
        :param chunk_size: The size in bytes of the chunks that are read from the log file
        :type chunk_size: int
        :param truncate_long_lines: Whether the log entries that are long should be abbreviated
        :type truncate_long_lines: bool
        :param append_gaps: Whether the data between the end of the record regex and the start
                            of the next record regex should be added to the previous entry
        :type append_gaps: bool
        """

        self.pat = pat  # the regular expression that identifies a record
        self.append_gaps = append_gaps  # if characters between the occurrences of the
                                        # regex are considered to belong to the last field of the record
        self.truncate_long_lines = truncate_long_lines
        self.ctrl_be = ctrl_be

        self.is_local = self.ctrl_be.server_profile.is_local
        self.not_readable = False
        self.partial_support = False
        self.mtime = None

        if isinstance(log_file, (file, StringIO.StringIO)):
            self.log_file = log_file
            if hasattr(log_file, 'name'):
                self.log_file_name = log_file.name
                self.mtime = os.stat(self.log_file_name).st_mtime
            else:
                self.log_file_name = None
        else:
            # If there isn't a directory component in the path, use @@datadir as the directory for the log file:
            log_file = log_file.strip(' "')
            ospath = server_os_path(self.ctrl_be.server_profile)
            datadir = self.ctrl_be.server_profile.datadir
            if not datadir and ctrl_be.is_sql_connected():
                datadir = self.ctrl_be.get_server_variable('datadir')
            self.log_file_name = log_file if ospath.isabs(log_file) else ospath.join(datadir, log_file)
            if self.is_local:
                try:
                    self.mtime = os.stat(self.log_file_name).st_mtime
                    self.log_file = open(self.log_file_name, 'rb')
                except IOError, e:
                    if self.ctrl_be.server_profile.target_is_windows:
                        raise LogFileAccessError('Cannot read from %s. Check permissions and retry.' %
                                                 self.log_file_name)
                    if os.path.isfile(self.log_file_name):
                        self.not_readable = True
                        self.last_known_size = os.path.getsize(self.log_file_name)
                        self.password = ctrl_be.password_handler.get_password_for('file')
                        try:
                            self.tail_data = ctrl_be.execute_filtered_command('tail -c %d %s' % (chunk_size,
                                                                                                 self.log_file_name),
                                                                              as_user = Users.ADMIN,
                                                                              user_password = self.password)[0]
                        except InvalidPasswordError:
                            ctrl_be.password_handler.reset_password_for('file')
                            raise

                        self.log_file = StringIO.StringIO(self.tail_data)
                        self.partial_support = 'The current user has no permission to read %s. Reading it with superuser privileges. Workbench has only limited support for this.' % log_file
                    else:
                        raise IOError(e)
                except OSError, e:
                    raise LogFileAccessError('''An error appeared when looking for the log file "%s". Please verify that you can access the directory
where the log file is placed ("%s") and that the log file is actually there. Try again when done.''' % (self.log_file_name, os.path.dirname(self.log_file_name)))

            else:  # Remote server
                if not self.ctrl_be.server_profile.remote_admin_enabled:
                    raise LogFileAccessError('''You have not enabled remote administration for this server. Without it this log file cannot be shown.
Please enable remote administration in this server instance and try again.''')
                if not self.ctrl_be.server_profile.uses_ssh:
                    raise LogFileAccessError('''Remote log files are only supported for SSH connection.
Please configure an SSH connection and try again.''')

                if self.ctrl_be.ssh:
                    self.ssh = self.ctrl_be.ssh
                else:
                    self.ssh = WbAdminSSH()
                    while True:
                        try:  # Repeat get password while password is misspelled. Re-raise other exceptions
                            self.ssh.wrapped_connect(self.ctrl_be.server_profile,
                                                     PasswordHandler(self.ctrl_be.server_profile))
                        except ConnectionError, error:
                            if not str(error).startswith('Could not establish SSH connection: Authentication failed'):
                                raise
                        else:
                            break
                if not self.ssh.is_connected():
                    raise LogFileAccessError('Could not connect to remote server')
                self.sftp = self.ssh.client.open_sftp()
                try:
                    self.log_file = self.sftp.open(self.log_file_name)
                    self.mtime = self.sftp.stat(self.log_file_name).st_mtime
                except IOError, e:
                    raise LogFileAccessError('Could not read file %s in remote server. Please verify path and permissions' % self.log_file_name)

        self.log_file.seek(0, 2)  # Move to EOF
        self.file_size = self.log_file.tell()
        self.chunk_size = chunk_size
        self.chunk_start = self.file_size

        # reuse self._adjust_chunk_end to find first record in the file:
        self.chunk_end = 0
        self._adjust_chunk_end()
        self.first_record_pos = self.chunk_end

        self.chunk_end = self.file_size



    def has_previous(self):
        '''
        If there is a previous chunk that can be read.
        '''
        return self.chunk_start > self.first_record_pos

    def has_next(self):
        '''
        If there is a next chunk that can be read.
        '''
        return self.chunk_end != self.file_size

    def range_text(self):
        if not self.not_readable:
            return 'Log file size: %s' % self._format_size(self.file_size)
        else:
            return 'Log file size: %s. (Reading last %s)' % (self._format_size(self.last_known_size),
                                                             self._format_size(self.file_size))

    def _format_size(self, bytes):
        '''
        Returns a string with a human friendly representation of a file size
        '''
        if bytes <= 0:
            return '0 B'
        units = (
            (1., 'B'),
            (1024., 'kB'),
            (1024*1024., 'MB'),
            (1024*1024*1024., 'GB'),
                )
        for idx, unit in enumerate(units):
            if bytes < unit[0]:
                return '%.1f %s' % (bytes/units[idx-1][0], units[idx-1][1])
        return '%.1f %s' % (bytes/units[-1][0], units[-1][1])

    def _read_previous_chunk(self):
        '''
        Reads the previous chunk.
        '''
        if self.chunk_start <= self.first_record_pos:
            raise IndexError('No more data to read from log file')
        self.chunk_end = self.chunk_start
        self._adjust_chunk_end()
        self.chunk_start = max(self.chunk_start - self.chunk_size, self.first_record_pos)
        self._adjust_chunk_start()
        self.log_file.seek(self.chunk_start)
        return self._read_chunk()

    def _read_next_chunk(self):
        '''
        Reads the next chunk.
        '''
        if self.chunk_end == self.file_size:
            raise IndexError('No more data to read from log file')
        self.chunk_start = self.chunk_end
        self.chunk_end = min(self.chunk_end + self.chunk_size - 1, self.file_size)
        self._adjust_chunk_end()
        self._adjust_chunk_start()
        return self._read_chunk()

    def _read_chunk(self):
        '''
        Reads the current chunk.
        '''
        bytes = self.chunk_end - self.chunk_start
        self.log_file.seek(self.chunk_start)
        data = self.log_file.read(bytes)
        return data

    def _adjust_chunk_start(self):
        '''
        Puts the chunk start marker at the beginning of a record. If a record starts within
        the range [self.chunk_start, self.chunk_end] the chunk start marker will point to it.
        If there's no record in the range, move backwards until there's at least one record
        in the chunk.
        Precondition: the chunk end marker must be set to delimit the end of the chunk.
        '''
        if self.chunk_end > self.chunk_start:
            if self.chunk_start <= self.first_record_pos:
                self.chunk_start = self.first_record_pos
                return
            data = ''
            bytes = self.chunk_end - self.chunk_start
            while True:
                self.log_file.seek(self.chunk_start)
                data = self.log_file.read(bytes) + data
                pat_occurrence = self.pat.search(data)
                if pat_occurrence:
#                    self.chunk_start += pat_occurrence.start()
                    break
                if self.chunk_start <= self.first_record_pos:
                    raise IndexError('No more data to read from log file')
                bytes = min(self.chunk_size/4, self.chunk_start - self.first_record_pos)
                self.chunk_start -= bytes

    def _adjust_chunk_end(self):
        '''
        Moves the chunk termination marker forward to just before the start of the next record
        or to the EOF if not next record.
        '''
        if self.chunk_end != self.file_size:
            trailing_data = ''
            self.log_file.seek(self.chunk_end)
            bytes = self.chunk_size/4  # TODO check this value
            while True:
                trailing_data += self.log_file.read(bytes)
                pat_occurrence = self.pat.search(trailing_data)
                if pat_occurrence or self.log_file.tell()==self.file_size:
                    break
            self.chunk_end = self.chunk_end + pat_occurrence.start() if pat_occurrence else self.file_size

    def _parse_chunk(self, data):
        '''
        Extracts the records from a chunk of data.
        '''
        records = []
        found = self.pat.search(data)
        if found:
            end = found.start()
            if self.chunk_start > self.first_record_pos:  # optional?
                self.chunk_start += end
        while found:
            start = found.start()
            if start-end > 1 and self.append_gaps:  # there's a gap between occurrences of the pattern
                records[-1][-1] += data[end:start]  # append the gap to previous record
            records.append( list(found.groups()) )
            end = found.end()
            found = self.pat.search(data, end)
            if found and self.truncate_long_lines:  # shorten all but the last record
                records[-1][-1] = self._shorten_query_field(records[-1][-1])
        if records:
            if self.append_gaps:
                records[-1][-1] += data[end:]  # add what remains in data
            if self.truncate_long_lines:
                records[-1][-1] = self._shorten_query_field(records[-1][-1])  # now shorten the last record

        return records

    def _shorten_query_field(self, data):
        '''
        Receives a query stored in a log file and prepares it for the output in
        the log viewer shortening to 256 characters and taking care of encoding issues
        '''
        l = len(data)
        try:
            abbr = data[:256].encode('utf-8')
        except ValueError:
            abbr = data[:256].decode('latin1').encode('utf-8')
        size = '%d bytes' % l if l < 1024 else '%.1f KB' % (l / 1024.0)
        return abbr if l <= 256 else abbr + ' [truncated, %s total]' % size

    def current(self):
        '''
        Returns a list with the records in the current chunk.
        Each record is a list with the values for each column of
        the corresponding log entry.
        '''
        try:
            data = self._read_chunk()
        except IndexError:
            return []
        return self._parse_chunk(data)

    def previous(self):
        '''
        Returns a list with the records in the previous chunk.
        Each record is a list with the values for each column of
        the corresponding log entry.
        '''
        try:
            data = self._read_previous_chunk()
        except IndexError:
            return []
        return self._parse_chunk(data)

    def next(self):
        '''
        Returns a list with the records in the next chunk.
        Each record is a list with the values for each column of
        the corresponding log entry.
        '''
        try:
            data = self._read_next_chunk()
        except IndexError:
            return []
        return self._parse_chunk(data)

    def first(self):
        '''
        Returns a list with the records in the first chunk
        '''
        self.chunk_end = self.first_record_pos
        return self.next()

    def last(self):
        '''
        Returns a list with the records in the first chunk
        '''
        self.chunk_start = self.file_size
        self.chunk_end = self.file_size
        return self.previous()

    def log_file_changed(self):
        '''
        If the log file has grown since the time self.file_size was
        computed.
        '''
        self.log_file.seek(0, 2)  # Move to EOF
        return self.log_file.tell() != self.file_size

    def refresh(self):
        '''
        Checks if the log file has been updated since it was opened and if so
        reopen the file again to keep going with the changes.
        Warning: this function only supports appending to the log file.
        '''
        if self.log_file_name:
            if self.is_local:
                mtime = os.stat(self.log_file_name).st_mtime
                if mtime != self.mtime:
                    if self.not_readable:
                        if self.ctrl_be.server_profile.target_is_windows:
                            return  #TODO: Add support for not readable files in Windows
                        size = os.path.getsize(self.log_file_name)
                        bytes = size - self.last_known_size
                        # Read new data (capped at chunk_size bytes) from the end of the log file:
                        new_data = self.ctrl_be.execute_filtered_command('tail -c %d %s' % (min(bytes, self.chunk_size), self.log_file_name),
                                                      as_user = Users.ADMIN,
                                                      user_password = self.password)[0]
                        if len(new_data) < self.chunk_size:  # Proceed to complete using what was stored in tail_data
                            self.tail_data = self.tail_data[-min( len(self.tail_data), self.chunk_size - len(new_data) ) : ] + new_data
                        else:
                            self.tail_data = new_data

                        self.log_file = StringIO.StringIO(self.tail_data)

                        # Reuse _adjust_chunk_end to set self.first_record_pos
                        chunk_end = self.chunk_end
                        self.chunk_end = 0
                        self._adjust_chunk_end()
                        self.first_record_pos = self.chunk_end
                        self.chunk_end = chunk_end

                        self.last_known_size = size
                    else:
                        self.log_file.close()
                        self.log_file = open(self.log_file_name, 'rb')

            else:  # Remote file
                mtime = self.sftp.stat(self.log_file_name).st_mtime
                if mtime != self.mtime:
                    self.log_file.close()
                    self.log_file = self.sftp.open(self.log_file_name, 'rb')

            self.log_file.seek(0, 2)  # Move to EOF
            self.file_size = self.log_file.tell()
            self.mtime = mtime

#==============================================================================
class ErrorLogFileReader(BaseLogFileReader):
    '''
    This class enables the retrieval of log entries in a MySQL error
    log file.
    '''
    def __init__(self, ctrl_be, file_name, chunk_size=4 * 1024, truncate_long_lines=False):
        pat = re.compile(r'^(\d{6} {1,2}\d{1,2}:\d{2}:\d{2}) (.*?)$', re.M)
        super(ErrorLogFileReader, self).__init__(ctrl_be, file_name, pat, chunk_size, truncate_long_lines)
        self.column_specs = (
                ('Time', 150),
                ('Details', 500),
                            )
        self.detail_column = 1

#==============================================================================
class GeneralLogFileReader(BaseLogFileReader):
    '''
    This class enables the retrieval of log entries in a MySQL general query
    log file.
    '''
    def __init__(self, ctrl_be, file_name, chunk_size=4 * 1024, truncate_long_lines=True):
        pat = re.compile(r'^(\d{6} {1,2}\d{1,2}:\d{2}:\d{2}[\t ]+|[\t ]+)(\s*\d+)(\s*.*?)(?:\t+| {2,})(.*?)$', re.M)
        super(GeneralLogFileReader, self).__init__(ctrl_be, file_name, pat, chunk_size, truncate_long_lines)
        self.column_specs = (
                ('Time', 150),
                ('Thread', 80),
                ('Command Type', 80),
                ('Detail', 500),
                            )
        self.detail_column = 3


#==============================================================================
class SlowLogFileReader(BaseLogFileReader):
    '''
    This class enables the retrieval of log entries in a MySQL slow query
    log file.
    '''
    def __init__(self, ctrl_be, file_name, chunk_size=4 * 1024, truncate_long_lines=False, append_gaps=False):
        pat = re.compile(r'(?:^|\n)# Time: (\d{6} {1,2}\d{1,2}:\d{2}:\d{2}).*?\n# User@Host: (.*?)\n# Query_time: +([0-9.]+) +Lock_time: +([\d.]+) +Rows_sent: +(\d+) +Rows_examined: +(\d+)\n(.*?)(?=\n# |\n[^\n]+, Version: |$)', re.S)
        super(SlowLogFileReader, self).__init__(ctrl_be, file_name, pat, chunk_size, truncate_long_lines, append_gaps)
        self.column_specs = (
                ('Start Time', 150),
                ('User@Host', 80),
                ('Query Time', 80),
                ('Lock Time', 80),
                ('Rows Sent', 80),
                ('Rows Examined', 80),
                ('Detail', 500),
                            )
        self.detail_column = 6
