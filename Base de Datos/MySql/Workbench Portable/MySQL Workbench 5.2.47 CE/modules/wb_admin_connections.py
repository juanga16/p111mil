# Copyright (c) 2009, 2013, Oracle and/or its affiliates. All rights reserved.
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

from mforms import newTreeNodeView, newButton, newBox, newSelector, newLabel, Utilities
import mforms

from functools import partial

from wb_admin_utils import not_running_warning_label, weakcb, dprint_ex

class WbAdminConnections(mforms.Box):
    ui_created = False
    serial = 0
    
    def __init__(self, instance_info, ctrl_be):
        mforms.Box.__init__(self, False)
        self.set_managed()
        self.set_release_on_add()
        self.instance_info = instance_info
        self.ctrl_be = ctrl_be
        self.page_active = False
    
    
    def create_ui(self):
        dprint_ex(4, "Enter")
        self.suspend_layout()
        
        self.warning = not_running_warning_label()
        self.add(self.warning, False, True)
        
        self.connection_list = newTreeNodeView(mforms.TreeDefault|mforms.TreeFlatList)
        self.connection_list.add_column(mforms.LongIntegerColumnType, "Id", 50, False)
        self.connection_list.add_column(mforms.StringColumnType, "User", 80, False)
        self.connection_list.add_column(mforms.StringColumnType, "Host", 120, False)
        self.connection_list.add_column(mforms.StringColumnType, "DB", 100, False)
        self.connection_list.add_column(mforms.StringColumnType, "Command", 80, False)
        self.connection_list.add_column(mforms.IntegerColumnType, "Time", 60, False)
        self.connection_list.add_column(mforms.StringColumnType, "State", 80, False)
        self.info_column = self.connection_list.add_column(mforms.StringColumnType, "Info", 300, False)
        self.connection_list.end_columns()
        self.connection_list.set_allow_sorting(True)
        
        self.connection_list.add_changed_callback(weakcb(self, "connection_selected"))
        
        #self.set_padding(8)
        self.add(self.connection_list, True, True)
        
        self.button_box = box = newBox(True)
        
        box.set_spacing(12)
        box.set_padding(12)
        
        refresh_button = newButton()
        refresh_button.set_text("Refresh")
        box.add_end(refresh_button, False, True)
        refresh_button.add_clicked_callback(weakcb(self, "refresh"))

        copy_button = newButton()
        copy_button.set_text("Copy Selected")
        box.add_end(copy_button, False, True)
        copy_button.add_clicked_callback(weakcb(self, "copy_selected"))

        self.kill_button = newButton()
        self.kill_button.set_text("Kill Connection")
        box.add_end(self.kill_button, False, True)
        self.kill_button.add_clicked_callback(weakcb(self, "kill_connection"))
        
        self.killq_button = newButton()
        self.killq_button.set_text("Kill Query")
        box.add_end(self.killq_button, False, True)
        self.killq_button.add_clicked_callback(weakcb(self, "kill_query"))
        
        refresh_label = newLabel("Refresh Rate:")
        box.add(refresh_label, False, True)
        
        self.refresh_values = [0.5,1,2,3,4,5,10,15,30]
        self.refresh_values_size = len(self.refresh_values)
        
        self.refresh_selector = newSelector()
        self.refresh_selector.set_size(100,-1)
        
        for s in self.refresh_values:
            self.refresh_selector.add_item(str(s) + " seconds")
        
        self.refresh_selector.add_item("Don't Refresh")
        
        self.refresh_selector.set_selected(9)
        box.add(self.refresh_selector, False, True)
        self.refresh_selector.add_changed_callback(weakcb(self, "update_refresh_rate"))
        
        self.add(box, False, True)
        
        self.resume_layout()
        
        self.connection_selected()
        dprint_ex(4, "Leave")
    
    
    def connection_selected(self):
        dprint_ex(4, "Enter")
        if not self.connection_list.get_selected_node():
            self.kill_button.set_enabled(False)
            self.killq_button.set_enabled(False)
        else:
            self.kill_button.set_enabled(True)
            self.killq_button.set_enabled(True)
        dprint_ex(4, "Leave")
    
    def page_activated(self):
        if not self.ui_created:
            self.create_ui()
            self.ui_created = True
        
        self.page_active = True
        if self.ctrl_be.is_sql_connected():
            self.warning.show(False)
            self.connection_list.show(True)
            self.button_box.show(True)
        else:
            self.warning.show(True)
            self.connection_list.show(False)
            self.button_box.show(False)
        
        self.refresh()
    
    def page_deactivated(self):
        self.page_active = False
    
    def get_process_list(self):
        fields = ["Id", "User", "Host", "db", "Command", "Time", "State", "Info"]
        result = self.ctrl_be.exec_query("SHOW FULL PROCESSLIST")
        if result is not None:
            result_rows = []
            while result.nextRow():
                row = []
                for field in fields:
                    value = result.stringByName(field)
                    row.append(value)
                result_rows.append(row)
            return result_rows
        
        return None
    
    
    def update_refresh_rate(self):
        index = int(self.refresh_selector.get_selected_index())
        self.serial += 1
        if (index < self.refresh_values_size):
            Utilities.add_timeout(self.refresh_values[index], partial(self.refresh, my_serial = self.serial))
    
    def copy_selected(self):
        sel = self.connection_list.get_selected_node()
        if not sel:
            return
        
        info = sel.get_string(self.info_column)
        mforms.Utilities.set_clipboard_text(info)


    def refresh(self, query_result = None, my_serial = 0):
        if not self.ctrl_be.is_sql_connected():
            dprint_ex(2, "Leave. SQL connection is offline")
            return False
        
        if not self.page_active:
            dprint_ex(2, "Leave. Page is inactive")
            return False
        
        node = self.connection_list.get_selected_node()
        if node:
            old_selected = node.get_long(0)
        else:
            old_selected = None
        old_selected_node = None
        
        if query_result is None:
            query_result = self.get_process_list()
        
        if query_result is not None:
            self.connection_list.freeze_refresh()
            self.connection_list.clear()
            id_width = 0
            try:
                for row in query_result:
                    r = self.connection_list.add_node()
                    for c, field in enumerate(row):
                        if c == 0:
                            try:
                                field= long(field)
                            except:
                                field= 0
                            r.set_long(c, field)
                        elif c == 5:
                            try:
                                field= int(field)
                            except:
                                field= 0
                            r.set_int(c, field)
                        else:
                            field = str(field)
                            if c == 0:
                                id_width = max(id_width, len(field))
                            r.set_string(c, field)
                        if c == 0 and field == old_selected:
                            old_selected_node = r
            
            finally:
                self.connection_list.thaw_refresh()
            
            if old_selected_node:
                self.connection_list.select_node(old_selected_node)
            
            self.connection_selected()
        
        return (my_serial == self.serial)
    
    
    
    def kill_connection(self):
        if not self.ctrl_be.is_sql_connected():
            return
        
        sel = self.connection_list.get_selected_node()
        if not sel:
            return
        
        connid = sel.get_long(0)
        try:
            self.ctrl_be.exec_sql("KILL CONNECTION %s"%connid)
        except Exception, e:
            raise Exception("Error executing KILL CONNECTION: %s" % e)
        
        self.refresh()
    
    
    def kill_query(self):
        if not self.ctrl_be.is_sql_connected():
            return
        
        sel = self.connection_list.get_selected_node()
        if not sel:
            return
        
        connid = sel.get_long(0)
        try:
            self.ctrl_be.exec_sql("KILL QUERY %s"%connid)
        except Exception, e:
            raise Exception("Error executing KILL QUERY: %s" % e)
        
        self.refresh()
