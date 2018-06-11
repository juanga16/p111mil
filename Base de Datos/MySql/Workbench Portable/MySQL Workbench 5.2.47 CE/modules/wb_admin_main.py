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

from __future__ import with_statement

import platform
import threading
import time
import os
import sys
import ConfigParser

from grt import log_info, log_error

from mforms import App, Utilities, newBox, newPanel, newButton, newLabel, newTabView, newTabSwitcher, newTextEntry, newSelector
from mforms import newTaskSidebar
import mforms

import wb_admin_monitor
import wb_admin_config_file_be

from wb_admin_configuration_startup import WbAdminConfigurationStartup
from wb_admin_config_file_ui import WbAdminConfigFileUI
from wb_admin_connections import WbAdminConnections
from wb_admin_variables import WbAdminVariables
from wb_admin_security import WbAdminSecurity
from wb_admin_logs import WbAdminLogs
from wb_admin_export import WbAdminExport, WbAdminImport
from wb_admin_utils import MySQLConnection, MySQLError, weakcb, no_remote_admin_warning_label, dprint_ex
from wb_server_management import wbaOS
from wb_admin_ui_profile import UIProfile

import new


#-------------------------------------------------------------------------------
#def add_top_spacer(panel):
#    box = newBox(False)
#    spacer = newPanel(mforms.TransparentPanel)
#    spacer.set_size(100, 10)
#    box.add(spacer, False, True)
#    box.add(panel, True, True)
#    return box

#-------------------------------------------------------------------------------
def newHeaderLabel(text):
    widget = newPanel(mforms.StyledHeaderPanel)
    label = newLabel(text)
    widget.add(label)
    widget.set_text  = new.instancemethod(mforms.Label.set_text,  label, mforms.Label)
    widget.set_color = new.instancemethod(mforms.Label.set_color, label, mforms.Label)
    widget.set_style = new.instancemethod(mforms.Label.set_style, label, mforms.Label)
    widget.set_text_align = new.instancemethod(mforms.Label.set_text_align, label, mforms.Label)
    return widget


#===============================================================================
#
#===============================================================================
class ServerStatusPage(mforms.Box):
    status      = None
    connections = None

    #---------------------------------------------------------------------------
    def __init__(self, server_profile, ctrl_be, main_view):
        mforms.Box.__init__(self, False) # Make vertical box
        main_view.ui_profile.apply_style(self, 'page')
        self.set_managed()
        self.set_release_on_add()

        self.ctrl_be = ctrl_be
        self.main_view = main_view

        self.status = wb_admin_monitor.WbAdminMonitor(server_profile, self.ctrl_be)
        self.add(self.status, False, False)

        vbox = newBox(False)
        vbox.set_spacing(2)
        label = newLabel("CONNECTIONS")#newHeaderLabel(" Connections")
        main_view.ui_profile.apply_style(label, 'subsection-label')
        vbox.add(label, False, False)

        self.connections = WbAdminConnections(server_profile, self.ctrl_be)
        main_view.ui_profile.apply_style(self.connections, "page")
        vbox.add(self.connections, True, True)

        self.add(vbox, True, True)

        self.main_view.add_content_page(self, "MANAGEMENT", "Server Status", "admin_server_status_win")

    #---------------------------------------------------------------------------
    def refresh(self, status):
        self.status.refresh_status(status)

    #---------------------------------------------------------------------------
    def page_activated(self):
        self.main_view.set_content_label(" Server Status")
        self.connections.page_activated()

    #---------------------------------------------------------------------------
    def page_deactivated(self):
        self.connections.page_deactivated()


#===============================================================================
#
#===============================================================================
class WbAdminMainView(mforms.Box):
    last_server_status = None

    def __init__(self, server_profile, ctrl_be, monitor):
        mforms.Box.__init__(self, True) # True - vertical layout
        self.tasks_side                 = newTaskSidebar()
        self.content_box                = newBox(False)

        self.tasks_side.set_selection_color(mforms.SystemColorHighlight)

        self.tabs                       = []
        self.name2page                  = {}
        self.config_ui                  = None
        self.closing                    = False
        self.tabview                    = newTabView(True)
        self.ctrl_be                    = ctrl_be
        self.old_active_tab             = None
        self.server_profile             = server_profile

        self.refresh_tasks_sleep_time   = 2

        self.ui_profile = UIProfile(server_profile)

        # Setup self
        self.set_managed()
        self.set_release_on_add()
        self.ui_profile.apply_style(self, "main")

        if server_profile.host_os == wbaOS.windows:
            side_panel = newPanel(mforms.StyledHeaderPanel)
            side_panel.set_title(" Task and Object Browser")
            side_panel.add(self.tasks_side)
            self.add(side_panel, False, True)

            self.content_panel = newPanel(mforms.StyledHeaderPanel)
            self.content_panel.set_title(" Task and Object Browser")
            self.content_panel.add(self.content_box)
            self.add(self.content_panel, True, True)
        else:
            vbox  = newBox(False)
            vbox.add(self.tasks_side, True, True)
            self.add(vbox, False, False)

            vbox  = newBox(False)
            self.content_label = newHeaderLabel("")
            self.ui_profile.apply_style(self.content_label, 'content-label')
            vbox.add(self.content_label, False, False)
            vbox.add(self.content_box, True, True)
            self.add(vbox, True, True)

        self.ctrl_be.add_me_for_event("server_started", self)
        self.ctrl_be.add_me_for_event("server_stopped", self)

        # Setup tasks sidebar
        self.fill_task_sidebar()
        self.tasks_side.add_on_section_command_callback(self.section_clicked)
        self.tasks_side.show()
        self.tasks_side.set_size(220, -1)

        # Setup content box
        self.content_box.add(self.tabview, True, True)

        # Retrieve from server the log file paths if exist
        status = self.ctrl_be.is_server_running(verbose=0)
        if status in ['stopped', 'unknown'] and not all(
                [ self.server_profile.general_log_file_path,  # only proceed to parse the config file if
                  self.server_profile.slow_log_file_path,     # any of these is missing
                  self.server_profile.error_log_file_path,
                  self.server_profile.log_output ] ):

            cfg_be = wb_admin_config_file_be.WbAdminConfigFileBE(self.server_profile, self.ctrl_be)
            cfg_be.open_configuration_file(self.server_profile.config_file_path)
            options = dict(cfg_be.get_options(self.server_profile.config_file_section))

            if not self.server_profile.log_output and options.has_key('log-output'):
                self.server_profile.log_ouput = options['log-output']

            if not self.server_profile.general_log_file_path:
                path = options['general_log_file'] if options.has_key('general_log_file') else (
                       options['log'] if options.has_key('log') else '')  # the 'log' option is deprecated but still allowed
                if path:
                    self.server_profile.general_log_file_path = path.strip('"')

            if not self.server_profile.slow_log_file_path:
                path = options['slow_query_log_file'] if options.has_key('slow_query_log_file') else (
                       options['log-slow-queries'] if options.has_key('log-slow-queries') else '')  # the 'log-slow-queries' option is deprecated but still allowed
                if path:
                    self.server_profile.slow_log_file_path = path.strip('"')

            if not self.server_profile.error_log_file_path and options.has_key('log-error'):
                self.server_profile.error_log_file_path = options['log-error'].strip('"')

        # Create content pages
        self.server_status_page = ServerStatusPage(server_profile, ctrl_be, self)
        self.config_ui = WbAdminConfigFileUI(server_profile = server_profile, ctrl_be = ctrl_be, main_view = self)
        self.startup = WbAdminConfigurationStartup(ctrl_be, server_profile, self)
        self.security = WbAdminSecurity(self.ctrl_be, server_profile, self)
        self.variables = WbAdminVariables(self.ctrl_be, server_profile, self)
        self.logs = WbAdminLogs(self.ctrl_be, server_profile, self)
        self.dump = WbAdminExport(server_profile, self.ctrl_be, self)
        self.restore = WbAdminImport(server_profile, self.ctrl_be, self)

        self.init_extensions(server_profile, self.ctrl_be)

        Utilities.add_timeout(0.5, weakcb(self, "timeout"))
        self.timeout_thread = threading.Thread(target = self.refresh_tasks_thread)
        self.timeout_thread.setDaemon(True)
        self.timeout_thread.start()
        self.tabview.add_tab_changed_callback(self.tab_changed)

        self.timeout() # will call self.connect_mysql() and check if mysql is running

        self.ctrl_be.continue_events() # Process events which are queue during init
        dprint_ex(1, "WBA init complete")

        self.tasks_side.select_entry("MANAGEMENT", "Server Status")
        self.server_status_page.page_activated()

    #---------------------------------------------------------------------------
    def set_content_label(self, text):
        if hasattr(self, "content_label"):
            self.content_label.set_text(text)
        else:
            self.content_panel.set_title(text)

    #---------------------------------------------------------------------------
    def add_taskbar_section(self, name):
        i = self.tasks_side.add_section(name)
        #self.sections_list.append(name)
        return i

    #---------------------------------------------------------------------------
    def fill_task_sidebar(self):
        self.add_taskbar_section("MANAGEMENT")
        self.add_taskbar_section("CONFIGURATION")
        self.add_taskbar_section("SECURITY")
        self.add_taskbar_section("DATA EXPORT / RESTORE")
        #self.add_taskbar_section("ENTERPRISE BACKUP")

    #---------------------------------------------------------------------------
    def section_clicked(self, section):
        i, content = self.name2page.get(section, (None, None))
        #print section, i, content
        if i is not None:
            self.tabview.set_active_tab(i)
            #set_active_tab() already triggers a tab_changed event
            #self.tab_changed()

    #---------------------------------------------------------------------------
    def switch_to(self, section, task):
        self.tasks_side.select_entry(section, task)
        self.tab_changed()

    #---------------------------------------------------------------------------
    def tab_changed(self):
        if self.old_active_tab and hasattr(self.old_active_tab, "page_deactivated"):
            self.old_active_tab.page_deactivated()

        i = self.tabview.get_active_tab()
        panel = self.tabs[i]
        if panel is not None:
            panel.page_activated()
        self.old_active_tab = panel

    #---------------------------------------------------------------------------
    def shutdown(self):
        dprint_ex(2, " closing")
        self.closing = True
        for tab in self.tabs:
            if hasattr(tab, "shutdown"):
                res = tab.shutdown()
                if res is False:  # It has to explicitely return False to cancel shutdown
                    self.closing = False

    #---------------------------------------------------------------------------
    def shutdown_event(self):
        self.shutdown()

    #---------------------------------------------------------------------------
    def server_started_event(self):
        dprint_ex(1, "Handling start event")
        if len(self.tabs) > 0 and hasattr(self.tabs[0], 'print_output'):
            self.ctrl_be.uitask(self.tabs[0].print_output, "Server is running")
        ###self.connect_mysql()
        #if None == self.connect_mysql():
        self.refresh_tasks_sleep_time = 2
        dprint_ex(1, "Done handling start event")

    #---------------------------------------------------------------------------
    def server_stopped_event(self):
        dprint_ex(1, "Handling stop event")
        if len(self.tabs) > 0 and hasattr(self.tabs[0], "print_output"):
            self.ctrl_be.uitask(self.tabs[0].print_output, "Server is stopped")

        self.refresh_tasks_sleep_time = 3
        dprint_ex(1, "Done handling stop event")

    #---------------------------------------------------------------------------
    def refresh_tasks_thread(self):
        dprint_ex(2, "Entering refresh tasks thread")
        number_of_wakes_between_refreshes = 3
        cnt = 0

        only_status_check = 0

        while not self.closing:
            status = "unknown"

            try:
                status = self.ctrl_be.is_server_running(verbose=0)
            except Exception, exc:
                import traceback
                traceback.print_exc()
                print "exception getting server status: %s" % exc

            control_event = None
            if self.last_server_status != status:
                if status == "running":
                    control_event = "server_started"
                elif status == "stopped":
                    control_event = "server_stopped"

            if control_event:
                self.ctrl_be.event_from_main(control_event)

            dprint_ex(3, "server running", status, ", self.closing =", self.closing)
            if self.last_server_status != status or only_status_check == 0:
                dprint_ex(2, "Performing extra actions")
                if self.server_status_page:
                    self.server_status_page.refresh(status)

            self.last_server_status = status


            time.sleep(self.refresh_tasks_sleep_time)
            cnt += 1
            only_status_check = cnt % number_of_wakes_between_refreshes

        dprint_ex(2, "Leaving refresh tasks thread")

    #---------------------------------------------------------------------------
    def timeout(self):
        if not self.closing:
            self.ctrl_be.process_ui_task_queue()
        return not self.closing


    #---------------------------------------------------------------------------
    def add_content_page(self, content, section_name, item_name, icon_name_as_cmd, return_content_container = False):
            # strip _win prefix for osx icons, because we do not install _win icons in osx
        import sys
        if sys.platform == "darwin":
            if icon_name_as_cmd[-4:] == "_win":
                icon_name_as_cmd = icon_name_as_cmd[:-4]

        container = content
        if return_content_container:
            container = newBox(False)
            container.add_end(content, True, True)

        self.tasks_side.add_section_entry(section_name, item_name, icon_name_as_cmd + ".png", icon_name_as_cmd, False)
        i = self.tabview.add_page(container, "")
        #content.set_padding(8)
        self.tabs.append(content)
        self.name2page[icon_name_as_cmd] = (i, content)

        return container

    #---------------------------------------------------------------------------
    def init_extensions(self, server_profile, ctrl_be):
        log_info("WBA", "Initializing extension modules for WBA...\n")

        init_count = 0
        # search in the same dir where the WBA code itself is located
        for location in [os.path.dirname(__file__)]:
            try:
                folders = [f for f in os.listdir(location) if f.startswith("wba_") and os.path.isdir(os.path.join(location, f))]
            except:
                continue

            sys.path.append(location)

            for candidate in folders:
                if os.path.exists(os.path.join(location, candidate, "__init__.py")):
                    mod = __import__(candidate)
                    if hasattr(mod, "wba_register"):
                        log_info("WBA", "Registering WBA extension module %s/%s...\n" % (location, candidate))
                        try:
                            mod.wba_register(server_profile, ctrl_be, self)
                            init_count += 1
                            log_info("WBA", "WBA extension module %s/%s registered OK\n" % (location, candidate))
                        except:
                            import traceback
                            traceback.print_exc()
                            log_error("WBA", "Exception caught while loading WBA extension module %s/%s\n" % (location, candidate))
                            del sys.modules[mod.__name__]
                            del mod
                    else:
                        # unload the module
                        del sys.modules[mod.__name__]
                        del mod

            sys.path.pop()

        log_info("WBA", "%i extension modules initialized\n" % init_count)

