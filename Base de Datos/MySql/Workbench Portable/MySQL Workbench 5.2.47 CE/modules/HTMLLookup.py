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

from HTMLParser import HTMLParser, HTMLParseError

class HTMLLookup(HTMLParser):
    def __init__(self):
        self.reset();

    def reset(self):
        HTMLParser.reset(self)

        # Used as a tag stack as teh document is being parsed
        self.stack = []

        # Stores tupes of (tag, condition) to be searched,
        # Condition a list of tuples (attribute, value)
        self.path = []

        # Is a record of the depth at which each tag in the path
        # was found, used for tag matching when finding closing tags
        self.found_path_depth = []

        # Stores the next item in the path to be searched
        self.path_index = 0

        # Maintains a count of the items in the stack
        self.stack_index = 0

        # Flag to publish found data, publishing occurs on all data items
        # found after the path has been found
        self.found_target = False

        # Flag to indicate to quit once the processing has been completed
        self.quit_on_done = False

    def feed(self, data):
        try:
            quit_on_done_backup = self.quit_on_done
            path_backup = self.path
            self.reset()
            self.path = path_backup
            self.quit_on_done = quit_on_done_backup
            HTMLParser.feed(self, data)
        except HTMLParseError, msg:
            if not self.quit_on_done or not "DONE PROCESSING" in msg.msg:
                raise HTMLParseError(msg.msg, self.getpos())
            

    def add_path_node(self, tag):
        self.path.append((tag,[]))

    def add_path_conditioned_node(self, tag, attrs):
        self.path.append((tag, attrs))

    # Matches a tag with the following tag to be searched on
    # the path attribute
    def match_tag(self, tag, attrs):
        ret_val = True;

        # Gets the next path tuple
        next_tuple = self.path[self.path_index]

        # Splits the tuple in Tag and Attributes
        next_tag = next_tuple[0]
        next_attrs = next_tuple[1]

        # Compares the next and found tags
        if next_tag == tag:

            # Ensures all the Attribute tuples in the next path tag
            # exists on the found tag attributes
            for i in range(len(next_attrs)):
                if attrs.count(next_attrs[i]) == 0:
                    ret_val = False

        else:
            ret_val = False

        return ret_val
        
    def handle_starttag(self, tag, attrs):
        # The path index controls the number of items in
        # the search path that have been found
        if self.path_index < len(self.path):
            if self.match_tag(tag, attrs):
                self.found_path_depth.append(self.stack_index)
                self.path_index = self.path_index + 1

            
            if self.path_index == len(self.path):
                self.found_target = True
                self.handle_path_entry(tag, attrs)

        # Any tag is stacked and changes the stack index 
        self.stack.append(tag)
        self.stack_index = self.stack_index + 1

    def handle_endtag(self, tag):
        self.stack_index = self.stack_index - 1

        # Ensures the closing tag matches the one in the stack
        if self.stack[self.stack_index] == tag:
            self.stack.pop()

            # If any path item has been found
            if self.path_index > 0:

                # Verifies if the depth of the closing tag matches with the depth of
                # the last path found item
                if self.stack_index == self.found_path_depth[self.path_index - 1]:

                    # Verifies the closing tag is the same as the last found path item
                    if self.path[self.path_index -1][0] == tag:

                        # Positions the found cursors an item back
                        self.path_index = self.path_index - 1
                        self.found_path_depth.pop()

                        # If the found path is incomplete, stops publishing
                        if self.found_target and self.path_index < len(self.path):
                            self.found_target = False
                            self.handle_path_exit(tag)
                            if self.quit_on_done:
                                self.error("DONE PROCESSING")
                    else:
                        print "Error: end tag not matching tag in search path!"
        else:
            print "Error: end tag not matching start tag : ", tag

    def handle_data(self, data):
        if self.found_target:
            self.handle_found_data(data)

    # Function to handle data found after the complete path has been found
    # An inheriting class should do something with this
    def handle_found_data(self, data):
        pass

    # Function to handle the exact moment where the path being searched has been found
    # An inheriting class should do something with this
    def handle_path_entry(self, tag, attrs):
        pass

    def handle_path_exit(self, tag):
        pass
