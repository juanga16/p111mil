from wb import DefineModule, wbinputs
import grt
import mforms

from cairo_utils import Context
from explain_renderer import render_json_data, render_json_data_to_file, decode_json
from performance_charting import TreePieChart, event_waits_summary_by_thread_by_event_name_to_tree

ModuleInfo = DefineModule(name= "SQLIDEQueryAnalysis", author= "Oracle Corp.", version= "1.0")


class JSONTreeViewer(mforms.TreeNodeView):
    def __init__(self):
        mforms.TreeNodeView.__init__(self, mforms.TreeAltRowColors|mforms.TreeShowColumnLines|mforms.TreeShowRowLines)
        self.add_column(mforms.StringColumnType, "Key", 200)
        self.add_column(mforms.StringColumnType, "Value", 300)
        self.end_columns()

    def display_data(self, data):
        def add_nodes(node, create_node, data):
            if type(data) is dict:
                if node:
                    node.set_string(1, "<dict>")
                for key, value in data.items():
                    ch = create_node()
                    ch.set_string(0, key)
                    add_nodes(ch, ch.add_child, value)
            elif type(data) is list:
                if node:
                    node.set_string(1, "<list>")
                for i, value in enumerate(data):
                    ch = create_node()
                    ch.set_string(0, str(i))
                    add_nodes(ch, ch.add_child, value)
            else:
                if not node:
                    node = create_node()
                if type(data) is bool:
                    node.set_string(1, "true" if data else "false")
                else:
                    node.set_string(1, str(data))
    
        data = decode_json(data)
        self.clear()
        add_nodes(None, self.add_node, data)

class RenderBox(mforms.PyDrawBox):
    def __init__(self):
        mforms.PyDrawBox.__init__(self)
        
        self.set_instance(self)
        self.repaint_callback = None
        self.size = None
    
    def repaint(self, cr, x, y, w, h):
        c = Context(cr)
        w, h = self.repaint_callback(c)
        if self.size != (w, h):
            self.set_size(w, h)
            self.size = (w, h)

class VisualExplainViewer(mforms.AppView):
    def __init__(self):
        VisualExplainViewer.__init__(self, False, "QueryEditorExplain", False)
        #tree = JSONTreeViewer()
        #tree.display_data(json)
        #view.add(tree, False, True)
        #tree.set_size(400, -1)

        self.toolbar = mforms.newToolbar(mforms.SecondaryToolBar)
        self.add(self.toolbar, False, True)

        self.scroll = mforms.newScrollPanel(mforms.ScrollPanelNoFlags)
        self.scroll.set_visible_scrollers(True, True)
        self.add(self.scroll, True, True)

    def set_image(self, image):
        self.scroll.add(image)

def newToolBarItem(*args):
    item = mforms.ToolBarItem(*args)
    item.set_managed()
    return item


class ExplainTab(mforms.AppView):
    node_spacing = 30
    vertical = True

    def __init__(self, json):
        mforms.AppView.__init__(self, False, "QueryExplain", False)

        self.json_data = json
        self.toolbar = mforms.newToolBar(mforms.SecondaryToolBar)

        get_resource_path = mforms.App.get().get_resource_path

      
        #btn = newToolBarItem(mforms.SegmentedToggleItem)
        #btn.set_icon(get_resource_path("qe_resultset-tb-switcher_grid_off_mac.png"))
        #btn.set_alt_icon(get_resource_path("qe_resultset-tb-switcher_grid_on_mac.png"))
        #self.toolbar.add_item(btn)

        #btn = newToolBarItem(mforms.SegmentedToggleItem)
        #btn.set_icon(get_resource_path("qe_resultset-tb-switcher_explain_off.png"))
        #btn.set_alt_icon(get_resource_path("qe_resultset-tb-switcher_explain_on.png"))
        #self.toolbar.add_item(btn)

        #s = newToolBarItem(mforms.SeparatorItem)
        #self.toolbar.add_item(s)

        l = newToolBarItem(mforms.LabelItem)
        l.set_text("Spacing:")
        self.toolbar.add_item(l)
          
        btn = newToolBarItem(mforms.TextActionItem)
        btn.set_icon(get_resource_path("tiny_more_space.png"))
        btn.set_tooltip("Increase spacing between nodes.")
        btn.add_activated_callback(self.spacing_inc)
        self.toolbar.add_item(btn)

        btn = newToolBarItem(mforms.TextActionItem)
        btn.set_icon(get_resource_path("tiny_less_space.png"))
        btn.set_tooltip("Decrease spacing between nodes.")
        btn.add_activated_callback(self.spacing_dec)
        self.toolbar.add_item(btn)

        #s = newToolBarItem(mforms.SeparatorItem)
        #self.toolbar.add_item(s)
      
        #l = newToolBarItem(mforms.LabelItem)
        #l.set_text("Layout:")
        #self.toolbar.add_item(l)

        #btn = newToolBarItem(mforms.ToggleItem)
        #btn.set_icon(get_resource_path("tiny_align_h_middle.png"))
        #btn.add_activated_callback(lambda x:self.change_layout(True))
        #self.toolbar.add_item(btn)

        #btn = newToolBarItem(mforms.ToggleItem)
        #btn.set_icon(get_resource_path("tiny_align_v_middle.png"))
        #btn.add_activated_callback(lambda x:self.change_layout(False))
        #self.toolbar.add_item(btn)

        s = newToolBarItem(mforms.SeparatorItem)
        self.toolbar.add_item(s)
        
        btn = newToolBarItem(mforms.ActionItem)
        btn.set_icon(get_resource_path("tiny_saveas.png"))
        btn.add_activated_callback(self.save)
        btn.set_tooltip("Save image to an external file.")
        self.toolbar.add_item(btn)
        
    
        self.add(self.toolbar, False, True)
      
        self.scroll = mforms.newScrollPanel(mforms.ScrollPanelNoFlags)
        self.scroll.set_back_color("#ffffff")
        self.scroll.set_visible_scrollers(True, True)

        self.img = mforms.newImageBox()
        self.scroll.add(self.img)
            
        self.add(self.scroll, True, True)

          
    def spacing_inc(self, item):
        self.node_spacing += 5
        self.render()
  
  
    def spacing_dec(self, item):
        self.node_spacing -= 5
        if self.node_spacing < 0:
            self.node_spacing = 0
        self.render()


    def change_layout(self, vertical):
        self.vertical = vertical
        self.render()


    def save(self, item):
        ch = mforms.FileChooser(mforms.SaveFile)
        ch.set_extensions("PNG image (*.png)|*.png", "png")
        ch.set_title("Save Image As")
        ch.set_path("explain.png")
        if ch.run_modal():
            self.render(ch.get_path())


    def render(self, path=None):
        options = {}
        if self.vertical:
            options["yspacing"] = self.node_spacing * 2
            options["xspacing"] = self.node_spacing
        else:
            options["yspacing"] = self.node_spacing
            options["xspacing"] = self.node_spacing * 2
        options["vertical"] = self.vertical

        if not path:
            path = mforms.App.get().get_user_data_folder()+"/explain.png"
        w, h = render_json_data_to_file(self.json_data, None, path, options)
        self.img.set_image(path)
        self.img.set_size(w, h)



@ModuleInfo.plugin("wb.sqlide.visual_explain", caption="Visual Explain", input=[wbinputs.currentQueryEditor()])
@ModuleInfo.export(grt.INT, grt.classes.db_query_QueryEditor)
def visualExplain(editor):
    version = editor.owner.serverVersion
    if version.majorNumber < 5 or version.minorNumber < 6:
        # explain format=json only supported in 5.6+
        mforms.Utilities.show_message("Visual Explain", "Visual Explain is supported in MySQL servers 5.6 or newer, but the one you are connected to is %s.%s.%s." % (version.majorNumber, version.minorNumber, version.releaseNumber), "OK", "", "")
    else:
        statement = editor.currentStatement
        if statement:
            rset = editor.owner.executeScript("EXPLAIN FORMAT=JSON %s" % statement)
            if rset:
                json = rset[0].stringFieldValue(0)

                view = ExplainTab(json)
                
                #bgpattern = mforms.App.get().get_resource_path("background_stripes_light.png")
                dock = mforms.fromgrt(editor.resultDockingPoint)
                dock.dock_view(view, "", 0)
                dock.set_view_title(view, "Explain")
              
                view.render()

                rset[0].reset_references()
                
    return 0


@ModuleInfo.plugin("wb.sqlide.wait_summary", caption="P_S / Wait Summary", input=[wbinputs.currentQueryEditor()])
@ModuleInfo.export(grt.INT, grt.classes.db_query_QueryEditor)
def waitSummary(editor):
    statement = editor.currentStatement
    if statement:
        before_rows = []
        after_rows = []

        rset = editor.owner.executeScript("select * from performance_schema.events_waits_summary_by_thread_by_event_name as e join performance_schema.threads as t on e.thread_id=t.thread_id where t.processlist_id=connection_id()")
        if rset:
            while rset[0].nextRow():
                row = []
                for i in range(7):
                    if i == 1:
                        row.append(rset[0].stringFieldValue(i))
                    else:
                        row.append(rset[0].intFieldValue(i))
                before_rows.append(row)

        editor.owner.executeScriptAndOutputToGrid(statement)

        rset = editor.owner.executeScript("select * from performance_schema.events_waits_summary_by_thread_by_event_name as e join performance_schema.threads as t on e.thread_id=t.thread_id where t.processlist_id=connection_id()")
        if rset:
            while rset[0].nextRow():
                row = []
                for i in range(7):
                    if i == 1:
                        row.append(rset[0].stringFieldValue(i))
                    else:
                        row.append(rset[0].intFieldValue(i))
                after_rows.append(row)
        tree = event_waits_summary_by_thread_by_event_name_to_tree(before_rows, after_rows)
        print tree
        import cairo
        import cairo_utils
        surf = cairo_utils.ImageSurface(cairo.CAIRO_FORMAT_ARGB32, 800, 800)
        c = cairo_utils.Context(surf)
        c.set_source_rgb(0,0,0)
        c.paint()
        chart = TreePieChart(tree, c)
        chart.plot()
        surf.write_to_png("/tmp/explain.png")

        view = mforms.newAppView(True, "QueryEditorView", False)
        scroll = mforms.newScrollPanel(mforms.ScrollPanelNoFlags)
        scroll.set_visible_scrollers(True, True)
        image = mforms.newImageBox()
        image.set_size(800, 800)
        scroll.add(image)
        image.set_image("/tmp/explain.png")
        view.add(scroll, True, True)
        dock = mforms.fromgrt(editor.resultDockingPoint)
        dock.dock_view(view, "", 0)
        dock.set_view_title(view, "Explain")
            
    return 0

