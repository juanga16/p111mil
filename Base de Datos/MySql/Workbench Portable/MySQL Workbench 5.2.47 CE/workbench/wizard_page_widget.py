# Copyright (c) 2012, 2013, Oracle and/or its affiliates. All rights reserved.
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

class WizardPage(mforms.Box):
    def __init__(self, main, header_label, wide=False, no_buttons= False):
        mforms.Box.__init__(self, False)
        self.set_managed()
        self.set_release_on_add()

        self.ui_created = False
        self.main = main

        self._identifier = "    "+header_label

        self.set_back_color("") # Make the page transparent.
        self.container = mforms.newBox(True)

        # Main content
        self.content = mforms.newBox(False)
        self.content.set_spacing(12)
        self.content.set_padding(24)
        if not wide:
            self.content.set_size(800, -1)
            self.container.add(self.content, False, True)
        else:
            self.container.add(self.content, True, True)
        
        self.add(self.container, True, True)

        if not no_buttons:
            # Buttons at the bottom of the page:
            button_box = mforms.newBox(True)
            button_box.set_spacing(8)
            button_box.set_padding(16)

            if hasattr(self, "go_advanced"):
                self.advanced_button = mforms.newButton()
                self.advanced_button.set_text('Advanced >>')
                self.advanced_button.add_clicked_callback(self.go_advanced)
                button_box.add(self.advanced_button, False, True)

            self.cancel_button = mforms.newButton()
            self.cancel_button.set_text('Cancel')
            button_box.add_end(self.cancel_button, False, True)
            if hasattr(self, "go_cancel"):
                self.cancel_button.add_clicked_callback(self.go_cancel)
            else:
                self.cancel_button.set_enabled(False)

            self.next_button = mforms.newButton()
            self.next_button.set_text('Next >')
            self.next_button.add_clicked_callback(self.go_next)
            button_box.add_end(self.next_button, False, True)

            self.back_button = mforms.newButton()
            self.back_button.set_text('< Back')
            self.back_button.add_clicked_callback(self.go_back)
            button_box.add_end(self.back_button, False, True)

            self.add_end(button_box, False, True)


    def identifier(self):
        return self._identifier

    def go_back(self):
        self.main.go_previous_page()

    def go_next(self):
        self.main.go_next_page()

    #def go_cancel(self):
    #    pass

    #def go_advanced(self):
    #    pass

    def page_activated(self, advancing):
        if hasattr(self.main, 'header'):
            self.main.header.set_text(self._identifier.strip())
        if self.main.background: # this probably should be deleted (check migration in all platforms 1st)
            self.main.background.set_title(self._identifier.strip())
        if not self.ui_created:
            self.create_ui()
            self.ui_created = True

    def create_ui(self):
        pass
