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

from HTMLGetData import HTMLGetData

class MySQLGetRequestResult(HTMLGetData):
    def __init__(self):
        self.reset()

    def reset(self):
        HTMLGetData.reset(self)
        self.found_root_path = False
        self.result_type = ''
        self.add_path_node('html')
        self.add_path_node('body')
        self.add_path_conditioned_node("div",[('id','content')])

    def handle_path_entry(self, tag, attrs):
        if self.result_type == '':
            self.found_root_path = True

            # Disabling publishing after finding the root node
            self.found_target = False

    def handle_starttag(self, tag, attrs):
        # Injects the needed tags to find the right result when it identifies
        # The type of result being handled
        if self.found_root_path and tag == 'div':
            for attr in attrs:
                if attr[0] == 'class':
                    if attr[1] == 'thanks':
                        self.add_path_conditioned_node("table",[('id','bugheader')])
                        self.add_path_conditioned_node("tr",[('id','title')])
                        self.found_root_path = False
                        self.quit_on_done = True
                        self.result_type = 'success'
                    elif attr[1] == 'error':
                        self.add_path_conditioned_node("div",[('class','error')])
                        self.found_root_path = False
                        self.quit_on_done = True
                        self.result_type = 'error'
                    elif attr[1] == 'warning':
                        self.add_path_conditioned_node("div",[('class','warning')])
                        self.found_root_path = False
                        self.quit_on_done = True
                        self.result_type = 'warning'

        HTMLGetData.handle_starttag(self, tag, attrs)


    def handle_endtag(self, tag):
        HTMLGetData.handle_endtag(self, tag)
