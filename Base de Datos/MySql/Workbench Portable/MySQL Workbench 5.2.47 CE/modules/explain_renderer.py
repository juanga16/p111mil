#!/usr/bin/python
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

import cairo

import cairo_utils
from cairo_utils import Context, ImageSurface, Pattern
from cairo_utils import VBoxNode, TextRectangle, intersect_lines, draw_arrow_head



class TreeNode(VBoxNode):
    def __init__(self, parent, name, title, data):
        VBoxNode.__init__(self)
        self.padding = (0, 0, 0, 0)
        self.expand_to_fill = False
        self.name = name
        self.parent = parent
        self.data = data
        self.children = []
        self.content = TextRectangle(title)
        self.content.set_fill_color(0.83137254901960789, 0.92941176470588238, 0.99215686274509807, 1)
        self.items.append(self.content)
        self.extra_bottom_space = 0

    def __repr__(self):
        return "<node %s>"%self.content.text

    def get_flags(self, data = None):
        if not data:
            data = self.data
        flags = []
        for f in ["using_temporary_table", "dependent", "using_filesort", "cacheable"]:
            if data.get(f, False):
                flags.append(f)
        return flags


    def process(self):
        for ch in self.children:
            ch.process()

    def do_render(self, c):
        VBoxNode.do_render(self, c)
        self.render_shadow(c)

    def minimal_space_required_space_for_ref_to(self, c, ch):
        return 0


class OperationNode(TreeNode):
    def __init__(self, parent, name, title, data):
        TreeNode.__init__(self, parent, name, title, data)
        self.flags = TextRectangle("\n".join(self.get_flags()))
        self.content.border_color = None
        self.flags.border_color = None
        self.flags.font_size = 10
        self.flags.padding = 0, 5, 5, 5
        self.items.append(self.flags)
        self.set_fill_color(0.92941176470588238, 0.99215686274509807,0.83137254901960789,  1)

    def do_render(self, c):
        TreeNode.do_render(self, c)
        self.apply_attributes(c)
        x, y = self.pos
        w, h = self.size
        c.rectangle(x+0.5, y+0.5, w, h)
        c.stroke()


class SubqueryNode(TreeNode):
    def __init__(self, parent, name, data):
        TreeNode.__init__(self, parent, name, "SUBQUERY", data)
        self.padding = (0, 10, 25, 10)
        self.expand_to_fill = True
        self.content.border_color = None
        self.content.fill_color = (0.8, 0.8, 0.8, 0.5)
        self.content.line_spacing = 0
        self.content.padding = 5, 10, 5, 10

        self.subtitle = TextRectangle("\n".join(self.get_flags()))
        self.subtitle.border_color = None
        self.subtitle.fill_color = (0.8, 0.8, 0.8, 0.3)
        self.subtitle.line_spacing = 0
        self.subtitle.padding = 2, 10, 5, 10
        self.subtitle.font_size = 10
        self.items.append(self.subtitle)

    def __repr__(self):
        return "<subquery %s>"%self.name

    def process(self):
        TreeNode.process(self)
        tmp_table = None
        query_block = None
        #return
        for ch in self.children:
            if ch.name == "query_block":
                query_block = ch
            elif isinstance(ch, TableTreeNode):
                tmp_table = ch
            else:
                print "Unexpected child type in subquery:", ch.name, ch
        if tmp_table and query_block:
            self.children.remove(query_block)
            query_block.parent = tmp_table
            tmp_table.children.append(query_block)


    def do_render(self, c):
        def leftmost(node):
            x = node.pos[0]
            for ch in node.children:
                x = min(x, leftmost(ch))
            return x
        
        self.apply_attributes(c)
        x, y = self.pos
        w, h = self.gsize
        xx = leftmost(self)
        VBoxNode.do_render(self, c)
        c.save()
        c.set_source_rgba(1, 0, 0, 1)                           
        c.set_source_rgba(0.7, 0.7, 0.7, 1)
        c.set_dash([2.0, 2.0], 0)
        c.rectangle(xx+0.5, y+0.5, w, h)
        c.stroke()
        c.restore()


class TableTreeNode(TreeNode):
    def __init__(self, parent, name, title, data):
        TreeNode.__init__(self, parent, name, title, data)
        self.border_color = 125.0/255, 125.0/255, 125.0/255, 1
        self.heading = self.content
        self.heading.border_color = None
        self.references = {}
        self.heading.set_icon("../../images/grt/structs/db.Table.16x16.png")
        self.heading.set_color(1, 1, 1, 1)
        self.body = None
        self.flags_box = None
        flags = []
        if data.has_key("using_join_buffer"):
            flags.append("join buf (%s)" % data["using_join_buffer"])
        if flags:
            self.flags_box = TextRectangle("\n".join(flags))
            self.flags_box.set_color(*self.heading.color)
            self.items.append(self.flags_box)
    
    def __repr__(self):
        return "<table: %s>"%self.heading.text

    def set_body_text(self, body):
        if self.body:
            self.body.text = body
        else:
            self.body = TextRectangle(body)
            r, g, b, a = self.heading.fill_color
            self.body.set_fill_color(r, g, b, 0.7)
            self.body.set_color(*self.heading.color)
            self.body.border_color = self.border_color
            if self.flags_box:
                self.body.draw_vertices = False, False, True, False
            else:
                self.body.draw_vertices = None
            self.body.padding = 3, 5, 5, 5
            self.items.append(self.body)

    def set_fill_color(self, r, g, b, a = 1.0):
        self.heading.set_fill_color(r, g, b, a)
        if self.body:
            self.body.set_fill_color(r, g, b, 0.7)
        if self.flags_box:
            self.flags_box.set_fill_color(r, g, b, 0.7)

    def stroke_line_to_parent(self, c, node, vertical):
        if vertical:
            p1, p2 = TreeNode.stroke_line_to_parent_v(self, c, node)
        else:
            p1, p2 = TreeNode.stroke_line_to_parent_h(self, c, node)
        filtered = self.data.get("filtered", None)
        rows = self.data.get("rows", None)
        if filtered is not None and rows is not None:
            c.set_source_rgb(0.1, 0.5, 0.1)
            total = str(int(filtered*rows/100.0))
            x, y = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
            cairo_utils.show_centered_text_with_background(c, x, y, total, (1,1,1))

 
    def do_render_attachments(self, c):
        c.set_line_width(self.line_width)
        c.save()
        c.set_source_rgba(0.1, 0.1, 0.5, 1)
        x, y = self.pos
        w, h = self.size
        if self.data.has_key("rows"):
            cairo_utils.show_centered_text_with_background(c, self.center()[0], y-12, str(self.data["rows"]), (1,1,1))
        cond = self.data.get("attached_condition", None)
        if cond:
            c.set_font_size(9)
            suffix = ""
            while len(cond) > 10:
                ext = c.text_extents(cond)
                if ext.width > self.gsize[0]*1.2:
                    cond = cond[:-1]
                    suffix = "..."
                else:
                    break
            ext = c.text_extents(cond+suffix)
            padding = 4
            c.set_source_rgba(0xcc/255.0, 0xcc/255.0, 0xcc/255.0, 1)
            c.rounded_rect(x + 10, y + self.gsize[1], ext.width + 2*padding, ext.height + 2*padding, 7)
            c.stroke_preserve()
            c.set_source_rgba(0xeb/255.0, 0xeb/255.0, 0xeb/255.0, 1)
            c.fill()

            c.set_source_rgba(0x30/255.0, 0x30/255.0, 0x30/255.0, 1)
            c.move_to(int(x + 10 + padding) + 0.5, int(y+self.gsize[1] + ext.height - (ext.height + ext.y_bearing) + padding) + 0.5)
            c.show_text(cond+suffix)

        c.restore()


    def do_render(self, c):
        self.do_render_attachments(c)

        x, y = self.pos
        w, h = self.size

        c.set_source_rgba(*self.border_color)
        c.rectangle(x+0.5, y+0.5, w, h)
        c.stroke()

        self.render_shadow(c)


    def minimal_space_required_space_for_ref_to(self, c, ch):
        if ch not in self.references:
            return 0
        ref_cols = self.references[ch]
        l = None
        for r in ref_cols:
            if len(r) > l:
                l = r
        c.set_font_size(11)
        ext = c.text_extents(l)
        return ext.width+10+10

    def calc(self, c):
        TreeNode.calc(self, c)
        if self.references:
            self.extra_bottom_space = 50

    def stroke_ref_to(self, c, ch):
        p1 = ch.center()
        p2 = self.center()
        d = self.parent.children.index(self) - self.parent.children.index(ch)
        if d < 0:
            p1s, p1e = self.right_vertex()
            p2s, p2e = ch.left_vertex()
        else:
            p1s, p1e = self.left_vertex()
            p2s, p2e = ch.right_vertex()
        e = intersect_lines(p2s, p2e, p1, p2)
        s = intersect_lines(p1s, p1e, p1, p2)
        if s and e:
            self.stroke_ref(c, s, e, d, self.references[ch])
        else:
            print s, e


    def stroke_ref(self, c, p1, p2, d, columns):
        def px(p1, p2, d):
            return (int(p1[0]+(p2[0]-p1[0])/4)+0.5, int(p1[1]+d*25)+0.5)

        c.set_line_width(1)
        c.move_to(p1[0], int(p1[1])+0.5)
        if d > 1:
            p11 = px(p1, p2, d)
            p22 = px(p2, p1, d)
            text_y = (p2[1]+p1[1])/2 + 20*d
            c.curve_to(p11[0], p11[1], p22[0], p22[1], p2[0], p2[1])
        else:
            text_y = (p2[1]+p1[1])/2
            c.line_to(p2[0], int(p2[1])+0.5)
        c.stroke()
        if columns:
            c.save()
            c.set_font_size(11)
            ext = c.text_extents(columns[0])
            x = p2[0] + ((p1[0]-p2[0]) - ext.width)/2
            y = text_y
            c.set_source_rgba(0.1, 0.1, 0.1, 1)
            cairo_utils.show_text_lines_with_border(c, int(x), int(y), "\n".join(columns), 0)
            c.restore()
        if d > 1:
            draw_arrow_head(c, p2, p22)
        else:
            draw_arrow_head(c, p2, p1)


class IndexedTableTreeNode(TableTreeNode):
    def __init__(self, parent, name, title, data):
        TableTreeNode.__init__(self, parent, name, title, data)


    def process(self):
        TableTreeNode.process(self)

        parent = self.parent
        tables = {}
        if parent.name == "nested_loop":
            for ch in parent.children:
                if ch.data.has_key("table_name"):
                    tables[ch.data["table_name"]] = ch

        if self.data.has_key("ref"):
            columns = []
            for ref in self.data["ref"]:
                if ref.count(".") == 2:
                    schema, table, column = ref.split(".")
                    columns.append(column)
            if columns: # schema and table must be the same for all refs
                if tables.has_key(table):
                    self.references[tables[table]] = columns
                else:
                    print "reference target for %s not found" % ref
                self.set_is_key_ref(True)
            else:
                self.set_is_key_ref(False)
        else:
            self.set_is_key_ref(False)


    def set_is_key_ref(self, flag):
        self.is_key_ref = flag
        key = self.data["key"]
        keys = self.data.get("possible_keys", [])
        key_length = self.data.get("key_length", "")
        if key_length:
            key_length = "[%s]"%key_length
        # if ref is not an external column name, then we add the ref value next to the key
        if flag or not self.data.has_key("ref"):
            if key in keys:
                keys.remove(key)
            keys.append("* %s%s"%(key, key_length))
        else:
            if key in keys:
                keys.remove(key)
            keys.append("* %s%s -> %s"%(key, key_length, ", ".join(self.data["ref"])))
        self.set_body_text("\n".join(keys))



class MaterializedTableTreeNode(TableTreeNode):
    def __init__(self, parent, name, title, data):
        TableTreeNode.__init__(self, parent, name, title, data)
        self.expand_to_fill = True
        self.padding = 0, 10, 10, 10
        self.set_body_text("SUBQUERY, materialized from")
        self.body.set_fill_color(0.8, 0.8, 0.8, 0.5)
        self.body.set_color(0, 0, 0, 1)
        
        flags = self.get_flags()
        self.subtitle = TextRectangle("\n".join(flags))
        self.subtitle.border_color = None
        self.subtitle.set_fill_color(0.8, 0.8, 0.8, 0.3)
        self.subtitle.line_spacing = 0
        self.subtitle.padding = 2, 10, 5, 10
        self.subtitle.font_size = 10
        self.items.append(self.subtitle)


    def set_fill_color(self, r, g, b, a):
        self.heading.set_fill_color(r, g, b, 0.6)


    def process(self):
        for ch in self.children:
            if ch.name == "materialized_from_subquery":
                self.subquery_info = ch.data
                # remove the subquery node
                for cch in ch.children:
                    cch.parent = self
                self.children.remove(ch)
                self.children.extend(ch.children)
                break
        self.subtitle.text = "\n".join(self.get_flags(self.subquery_info))
        TableTreeNode.process(self)


    def do_render(self, c):
        def leftmost(node):
            x = node.pos[0]
            for ch in node.children:
                x = min(x, leftmost(ch))
            return x
 
        self.do_render_attachments(c)

        self.apply_attributes(c)
        x, y = self.pos
        w, h = self.gsize
        xx = leftmost(self)
        VBoxNode.do_render(self, c)
        c.save()
        c.set_source_rgba(1, 0, 0, 1)                           
        c.set_source_rgba(0.7, 0.7, 0.7, 1)
        c.set_dash([3.0, 2.0], 0)
        c.rectangle(xx+0.5, y+0.5, w, h)
        c.stroke()
        c.restore()



# Layouter

class TreeLayouter:
    def __init__(self, root, options):
        self.root = root
        self.yspacing = options.get("yspacing", 60)
        self.xspacing = options.get("xspacing", 30)
        self.vertical = options.get("vertical", True)

    
    def layout(self, ctx, node, x = 0, y = 0):
        t, l, b, r = node.padding
        
        if self.vertical:
            spacing = self.xspacing
        else:
            spacing = self.yspacing

        spacings = [spacing] * (len(node.children)-1)
        spacings.append(0) # no space after last item

        if node.children:
            # calculate the amount of horizontal space needed between each item
            
            # 1st calculate needed between adjacent items
            for i in range(len(node.children)):
                ch = node.children[i]
                if i > 0:
                    prev = node.children[i-1]
                    lspace = ch.minimal_space_required_space_for_ref_to(ctx, prev)
                    spacings[i-1] = max(spacings[i-1], int(lspace))

                if i < len(node.children)-1:
                    next = node.children[i+1]
                    rspace = ch.minimal_space_required_space_for_ref_to(ctx, next)
                    spacings[i] = max(spacings[i], int(rspace))

        #
        width, height = node.size
    
        if self.vertical:
            total_width = 0
            max_height = 0
            xx = x
            for i, ch in enumerate(node.children):
                w, h = self.layout(ctx, ch, xx, y + self.yspacing + height + t)
                xx  += w + spacings[i]
                total_width += w
                max_height = max(max_height, h)
            twidth = max(width, total_width + sum(spacings))
            if max_height > 0:
                theight = height + self.yspacing + max_height
            else:
                theight = height

            twidth += l + r
            theight += t + b + node.extra_bottom_space

            node.pos = x+(twidth)/2-node.size[0]/2, y
            node.gsize = twidth, theight
            if node.expand_to_fill:
                node.pos = x, y
                node.size = twidth, height

            node.layout_internal()
            # if child nodes are narrower than parent nodes, then offset them
            if total_width <= width:
                self.adjust_child_layout_v(node, l+(width-total_width)/2)
            else:
                self.adjust_child_layout_v(node, l)
        else:
            total_height = 0
            max_width = 0
            yy = y
            for i, ch in enumerate(node.children):
                w, h = self.layout(ctx, ch, x + self.xspacing + width + t, yy)
                yy  += h + spacings[i]
                total_height += h
                max_width = max(max_width, w)
            theight = max(height, total_height + sum(spacings))
            if max_width > 0:
                twidth = width + self.xspacing + max_width
            else:
                twidth = width
            
            theight += l + r
            twidth += t + b + node.extra_bottom_space

            node.pos = x, y+(theight)/2-node.size[1]/2
            node.gsize = twidth, theight
            if node.expand_to_fill:
                node.pos = x, y
                node.size = twidth, height
            
            node.layout_internal()
            # if child nodes are narrower than parent nodes, then offset them
            if total_height <= height:
                self.adjust_child_layout_h(node, l+(height-total_height)/2)
            else:
                self.adjust_child_layout_h(node, l)
        

        return twidth, theight


    def adjust_child_layout_v(self, node, offset):
        for ch in node.children:
            cx, cy = ch.pos
            ch.pos = int(cx + offset), int(cy)
            self.adjust_child_layout_v(ch, offset)


    def adjust_child_layout_h(self, node, offset):
        for ch in node.children:
            cx, cy = ch.pos
            ch.pos = int(cx), int(cy + offset)
            self.adjust_child_layout_h(ch, offset)


    def get_total_size(self, ctx):
        def calc_all(c, node):
            node.calc(c)
            for ch in node.children:
                calc_all(c, ch)
        calc_all(ctx, self.root)
 
        return self.layout(ctx, self.root, 0, 0)


    def render(self, c, x, y):
        def calc_all(c, node):
            node.calc(c)
            for ch in node.children:
                calc_all(c, ch)
        calc_all(c, self.root)
        self.layout(c, self.root, x, y)
        self.do_render(c, self.root)
        self.do_render_lines(c, self.root)

    def do_render_lines(self, c, node):
        for ch in node.children:
            ch.stroke_line_to_parent(c, node, self.vertical)

        for ch in node.children:
            self.do_render_lines(c, ch)

        c.set_source_rgba(0.7, 0.4, 0.0, 0.5)
        for ch in node.children:
            if hasattr(ch, "references"):
                for ref in ch.references.keys():
                    ch.stroke_ref_to(c, ref)


    def do_render(self, c, node):
        node.render(c)
        for ch in node.children:
            self.do_render(c, ch)



def decode_json(text):
    return eval(text, {"false":False, "true":True})



def process_table(parent, table):
    # Possible col_join_types (access_type) according to mysql 5.6.5 sources
    col_join_types = [
    ("UNKNOWN",         (1, 0, 0, 1),           TableTreeNode),
    ("system",          None,                   TableTreeNode),
    ("const",           None,                   TableTreeNode),
    ("eq_ref",          (0.25, 0.5, 0.75, 1),   IndexedTableTreeNode),
    ("index",           (1, 0.5, 0, 1),         IndexedTableTreeNode),
    ("ALL",             (0.75, 0.25, 0.25, 1),  TableTreeNode),
    ("range",           (0.0, 0.5, 0.25, 1),    IndexedTableTreeNode),
    ("ref",             (0.0, 0.5, 0.25, 1),      IndexedTableTreeNode),
    ("fulltext",        (1, 0.5, 0, 1),         TableTreeNode),
    ("ref_or_null",     None,                   TableTreeNode),
    ("unique_subquery", None,                   TableTreeNode),
    ("index_subquery",  None,                   TableTreeNode),
    ("index_merge",     None,                   TableTreeNode),
    ]

    access_type = table.get("access_type", None)
    table_name = table.get("table_name", "")

    if not access_type:
        node = TableTreeNode(parent, table_name, table.get("message", "???"), table)
        node.set_fill_color(0.25, 0.5, 0.75, 1)
        return node

    tableClass = TableTreeNode
    tableColor = 0.5, 0.5, 0.5, 1
    for join_type, color, class_ in col_join_types:
        if join_type == access_type:
            if color:
                tableColor = color
            tableClass = class_

    if table.has_key("materialized_from_subquery"):
      tableClass = MaterializedTableTreeNode

    node = tableClass(parent, table_name, table_name+"  (%s)"%access_type, table)
    node.set_fill_color(*tableColor)
    return node


def process_subquery(parent, data):
    node = SubqueryNode(parent, parent.name.replace("_subqueries", "_subquery"), data)
    return node

def process_node(parent, name, data):
    if type(data) is not dict:
        return None
    oper = name
    if oper.endswith("_operation"):
        oper = oper[0:-len("_operation")]
        if oper.endswith("ing"):
            oper = oper[0:-3]
        node = OperationNode(parent, name, oper.upper(), data)
    elif oper == "query_block":
        oper = "query_block #%s" % data.get("select_id")
        node = TreeNode(parent, name, oper, data)
        node.set_fill_color(0.83137254901960789, 0.92941176470588238, 0.99215686274509807, 1)
    else:
        node = TreeNode(parent, name, oper, data)
        node.set_fill_color(0.83137254901960789, 0.92941176470588238, 0.99215686274509807, 1)
    
    return node


def tree_from_json(parent, name, json):
    if name == "table":
        node = process_table(parent, json)
    elif name.endswith("_subqueries item"):
        node = process_subquery(parent, json)
    else:
        node = process_node(parent, name, json)
    if not node:
        return None
    for key, value in json.items():
        if key in ["possible_keys", "ref"]:
            continue
        if type(value) is dict:
            ch = tree_from_json(node, key, value)
            if ch:
                node.children.append(ch)
        elif type(value) is list:
            if value and type(value[0]) == dict and value[0].keys() == ["table"]:
                interm = TreeNode(node, key, key, {})
                interm.set_fill_color(0.83137254901960789, 0.92941176470588238, 0.99215686274509807, 1)
                node.children.append(interm)
                for item in value:
                    ch = tree_from_json(interm, "table", item["table"])
                    if ch:
                        interm.children.append(ch)
            else:
                interm = TreeNode(node, key, key, {})
                node.children.append(interm)
                for item in value:
                    ch = tree_from_json(interm, key+" item", item)
                    if ch:
                        interm.children.append(ch)
    return node


def strip_useless_nodes(tree):
    def is_useless(node):
        if node.name in ["query_specification", "nested_loop_item", "query_block"]:
            return True
        return False

    if is_useless(tree) and len(tree.children) == 1:
        tree = tree.children[0]
        tree.parent = None

    for i, ch in enumerate(tree.children):
        if is_useless(ch) and len(ch.children) == 1:
            tree.children[i] = ch.children[0]
            ch.children[0].parent = tree

        strip_useless_nodes(ch)

    return tree


def render_json_data(ctx, json_text, background_image, options):
    padding = 50

    json = decode_json(json_text)
    tree = tree_from_json(None, "query_block", json["query_block"])
    tree.process()
    tree = strip_useless_nodes(tree)
    layout = TreeLayouter(tree, options)
    w, h = layout.get_total_size(ctx)
    ctx.set_font_size(12)
    if background_image:
        bgimage = ImageSurface.from_png(background_image)
    else:
        bgimage = None
    if bgimage and bgimage.status() == cairo.CAIRO_STATUS_SUCCESS:
        ctx.save()
        pat = Pattern(bgimage)
        pat.set_extend(cairo.CAIRO_EXTEND_REPEAT)
        ctx.set_source(pat)
        ctx.paint()
        ctx.restore()
    else:
        ctx.set_source_rgb(1,1,1)
        ctx.paint()
    layout.render(ctx, padding, padding)

    return w+padding*2, h+padding*2


def render_json_data_to_file(json_text, background_image, png_file, options):
    padding = 50

    json = decode_json(json_text)
    tree = tree_from_json(None, "query_block", json["query_block"])
    tree.process()
    tree = strip_useless_nodes(tree)
    layout = TreeLayouter(tree, options)
    img = ImageSurface(cairo.CAIRO_FORMAT_ARGB32, 10, 100)
    ctx = Context(img)
    w, h = layout.get_total_size(ctx)
    img = ImageSurface(cairo.CAIRO_FORMAT_ARGB32, w+padding*2, h+padding*2)
    ctx = Context(img)
    ctx.set_font_size(12)
    if background_image:
        bgimage = ImageSurface.from_png(background_image)
    else:
        bgimage = None
    if bgimage and bgimage.status() == cairo.CAIRO_STATUS_SUCCESS:
        ctx.save()
        pat = Pattern(bgimage)
        pat.set_extend(cairo.CAIRO_EXTEND_REPEAT)
        ctx.set_source(pat)
        ctx.paint()
        ctx.restore()
    else:
        ctx.set_source_rgb(1,1,1)
        ctx.paint()
    layout.render(ctx, padding, padding)
    img.write_to_png(png_file)

    return w+padding*2, h+padding*2

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        sys.stdin.readline()
        render_json_data_to_file(sys.stdin.read().replace(r"\n", ""), None, "explain.png")
    else:
        f = sys.argv[1]
        render_json_data_to_file(open(f).read(), None, f+".png")
