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

from wb_admin_utils import not_running_warning_label, weakcb


from mforms import newBox, newTreeNodeView, newButton, newTabView, newTextEntry
import mforms

import wb_admin_variable_list

class VariablesViewer(mforms.Box):
    def __init__(self, ctrl_be, variables, command):
        mforms.Box.__init__(self, False)
        self.set_managed()
        self.set_release_on_add()

        self.suspend_layout()

        self.command = command
        self.ctrl_be = ctrl_be

        box = newBox(True)
        box.set_spacing(12)
        self.add(box, True, True)
        self.tree = newTreeNodeView(mforms.TreeFlatList)
        self.tree.set_selection_mode(mforms.TreeSelectMultiple)
        self.tree.set_size(180, -1)

        sidebox = newBox(False)

        box.add(sidebox, False, True)

        self.searchEntry = newTextEntry(mforms.SearchEntry)

        sidebox.set_spacing(12)
        sidebox.add(self.searchEntry, False, True)
        sidebox.add(self.tree, True, True)

        self.searchEntry.add_changed_callback(self.filterOutput)

        self.tree.add_column(mforms.StringColumnType, "Category", 160, False)
        self.tree.end_columns()
        self.tree.add_changed_callback(weakcb(self, "refresh"))

        self.values = newTreeNodeView(mforms.TreeFlatList)
        self.values.set_selection_mode(mforms.TreeSelectMultiple)
        box.add(self.values, True, True)

        self.values.add_column(mforms.StringColumnType, "Name", 200, False)
        self.values.add_column(mforms.StringColumnType, "Value", 120, True)
        self.values.add_column(mforms.StringColumnType, "Description", 1000, False)
        self.values.end_columns()
        self.values.set_allow_sorting(True)
        self.values.set_cell_edited_callback(self.edit_variable)
        self.values.add_changed_callback(weakcb(self, "value_selection_changed"))

        box = newBox(True)
        box.set_spacing(8)
        copy_all_button = newButton()
        copy_all_button.set_text('Copy Global Status and Variables to Clipboard')
        copy_all_button.add_clicked_callback(self.copy_status_to_clipboard)
        box.add(copy_all_button, False, False)
        copy_shown_button = newButton()
        copy_shown_button.set_text('Copy Selected to Clipboard')
        copy_shown_button.add_clicked_callback(self.copy_selected_to_clipboard)
        box.add(copy_shown_button, False, False)
        self.copy_selected_to_clipboard_button = copy_shown_button
        button = newButton()
        box.add_end(button, False, True)
        button.set_text("Refresh")
        box.set_padding(12)

        button.add_clicked_callback(weakcb(self, "refresh"))

        self.add(box, False, True)

        row = self.tree.add_node()
        row.set_string(0, "All")
        row = self.tree.add_node()
        row.set_string(0, "Filtered")
        self.resume_layout()


        variables_in_server = []
        result = self.ctrl_be.exec_query(self.command)
        if result is not None:
            while result.nextRow():
                name = result.stringByName("Variable_name")
                variables_in_server.append(name)

  
        self.variable_info = {}
        self.variables_in_group = {"Other":[]}
        
        existing_groups = set()
        for name, description, editable, groups in variables:
            self.variable_info[name.replace("-", "_")] = (description, editable)
            existing_groups = existing_groups.union(set(groups))
            for group in groups:
                if group not in self.variables_in_group:
                    self.variables_in_group[group] = []
                self.variables_in_group[group].append(name.replace("-", "_"))
            if not groups:
                self.variables_in_group["Other"].append(name.replace("-", "_"))

        for group_name in sorted(existing_groups):
            row = self.tree.add_node()
            row.set_string(0, group_name)
            row.set_tag(group_name)

        if self.variables_in_group["Other"]:
            row = self.tree.add_node()
            row.set_string(0, "Other")
            row.set_tag("Other")

        self.copy_selected_to_clipboard_button.set_enabled(len(self.values.get_selection()) > 0)


    def edit_variable(self, node, column, value):
        name = node.get_string(0)
        if name and self.variable_info.has_key(name) and self.variable_info[name][1]:
            try:
                int(value)
                self.ctrl_be.exec_sql("SET GLOBAL %s=%s" % (name, value))
            except:
                self.ctrl_be.exec_sql("SET GLOBAL %s='%s'" % (name, value.replace("'", "''")))

            value = self.ctrl_be.exec_query("%s LIKE '%s'" % (self.command, value))
            node.set_string(column, value)

          
    def value_selection_changed(self):
        self.copy_selected_to_clipboard_button.set_enabled(len(self.values.get_selection()) > 0)



    def refresh(self):
        if not self.ctrl_be.is_sql_connected():
            return

        rows = self.tree.get_selection()
        if not rows:
            self.values.clear()
            return

        filter = []
        search = None
        for row in rows:
            if self.tree.row_for_node(row) == 0:
                filter = None
                search = None
                break
            elif self.tree.row_for_node(row) == 1:
                filter = None
                search = self.searchEntry.get_string_value().replace("-", "_")
            else:
                tag = row.get_tag()
                if tag and filter is not None:
                    filter += self.variables_in_group.get(tag, [])
        if filter:
            filter = set(filter)

        result = self.ctrl_be.exec_query(self.command)

        self.values.freeze_refresh()
        self.values.clear()

        if result is not None:
            while result.nextRow():
                name = result.stringByName("Variable_name")

                if filter is not None and name.replace("-", "_") not in filter:
                    continue

                if search is not None and search.lower() not in name.lower():
                    continue

                value = result.stringByName("Value")
                r = self.values.add_node()
                r.set_string(0, name)
                r.set_string(1, value)
                if name.replace("-", "_") not in self.variable_info:
                    r.set_string(2, "")
                else:
                    editable = self.variable_info[name.replace("-", "_")][1] and "[rw] " or ""
                    r.set_string(2, editable + self.variable_info[name.replace("-", "_")][0])

        self.values.thaw_refresh()

          
    def filterOutput(self):
        self.tree.select_node(self.tree.node_at_row(1))
        self.refresh()

    def copy_status_to_clipboard(self):
        if not self.ctrl_be.is_sql_connected():
            mforms.Utilities.show_error('Connection error',
                                        'Cannot query the server for variables',
                                        'OK', '', '')
            return

        global_status = []
        result = self.ctrl_be.exec_query('SHOW GLOBAL STATUS')
        if result:
            while result.nextRow():
                var_name  = result.stringByName('Variable_name')
                var_value = result.stringByName('Value')
                global_status.append( (var_name, var_value) )

        global_variables = []
        result = self.ctrl_be.exec_query('SHOW GLOBAL VARIABLES')
        if result:
            while result.nextRow():
                var_name  = result.stringByName('Variable_name')
                var_value = result.stringByName('Value')
                global_variables.append( (var_name, var_value) )

        max_length = max( len(name) for name, val in global_status + global_variables ) + 5
        status = 'GLOBAL STATUS:\n'
        status += '\n'.join( [var_name.ljust(max_length, '.') + ' ' + var_value for var_name, var_value in global_status] )
        status += '\n\nGLOBAL VARIABLES:\n'
        status += '\n'.join( [var_name.ljust(max_length, '.') + ' ' + var_value for var_name, var_value in global_variables] )
        mforms.Utilities.set_clipboard_text(status)


    def copy_selected_to_clipboard(self):
        selection = []
        selected_vars = self.values.get_selection()
        if not selected_vars:
            return
        for node in selected_vars:
            selection.append((node.get_string(0), node.get_string(1)))
        max_length = max( len(name) for name, val in selection ) + 5
        status = '\n'.join( [var_name.ljust(max_length, '.') + ' ' + var_value for var_name, var_value in selection] )
        mforms.Utilities.set_clipboard_text(status)



class WbAdminVariables(mforms.Box):
    ui_created = False
    def __init__(self, ctrl_be, server_profile, main_view):
        mforms.Box.__init__(self, False)
        main_view.ui_profile.apply_style(self, 'page')
        self.set_managed()
        self.set_release_on_add()
        self.ctrl_be = ctrl_be
        self.main_view = main_view
        self.main_view.add_content_page(self, "MANAGEMENT", "Status and System Variables", "admin_status_vars_win")


    def create_ui(self):
        self.warning = not_running_warning_label()
        self.add(self.warning, False, True)

        self.tab = newTabView(False)
        self.add(self.tab, True, True)

        self.status = VariablesViewer(self.ctrl_be, wb_admin_variable_list.status_variable_list, "SHOW GLOBAL STATUS")
        self.status.set_padding(6)
        self.tab.add_page(self.status, "Status Variables")

        self.server = VariablesViewer(self.ctrl_be, wb_admin_variable_list.system_variable_list, "SHOW GLOBAL VARIABLES")
        self.server.set_padding(6)
        self.tab.add_page(self.server, "System Variables")
  

    def page_activated(self):
        self.main_view.set_content_label(" Status and System Variables")
        if not self.ui_created:
            self.create_ui()
            self.ui_created = True

        if self.ctrl_be.is_sql_connected():
            self.warning.show(False)
            self.tab.show(True)
        else:
            self.warning.show(True)
            self.tab.show(False)

        self.status.refresh()
        self.server.refresh()
