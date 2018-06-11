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
from wb_common import PermissionDeniedError, InvalidPasswordError, OperationCancelledError, parentdir


class BackupContentViewer(mforms.Box):
    def __init__(self, owner, context, backup_file):
        mforms.Box.__init__(self, False)
        self.set_managed()
        self.set_release_on_add()
        self._owner = owner
        self._context = context




class BackupLogViewer(mforms.Box):
    def __init__(self, context, profile):
        mforms.Box.__init__(self, False)
        self.set_managed()
        self.set_release_on_add()
        self._context = context
        self._profile = profile

        self.set_spacing(12)

        self.text = mforms.newTextBox(mforms.VerticalScrollBar)
        self.add(self.text, True, True)


    def load(self, backup_path):
        # get the backup logs
        try:
            data = self._context.server_interface.get_file_content(backup_path+".log")
            self.text.set_value(data)
        except Exception, e:
            self.text.set_value("Could not load log file for backup %s:\n%s" % (backup_path, e))



class BackupLogViewerDialog(mforms.Form):
    def __init__(self, context, profile, backup_path):
        mforms.Form.__init__(self, None, 0)

        box = mforms.newBox(False)
        box.set_padding(12)
        box.set_spacing(12)
        self.set_content(box)

        self.set_title("mysqlbackup logs for %s" % backup_path)

        self.viewer = BackupLogViewer(context, profile)
        box.add(self.viewer, True, True)

        self.viewer.load(backup_path)

        bbox = mforms.newBox(True)
        bbox.set_spacing(12)

        close = mforms.newButton()
        close.set_text("Close")
        bbox.add_end(close, False, True)
        close.add_clicked_callback(self.close)

        box.add_end(bbox, False, True)


        self.set_size(800, 600)
        self.center()

