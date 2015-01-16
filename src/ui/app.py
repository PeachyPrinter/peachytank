import wx
import wx.lib.newevent
import logging
from gl import Canvas
from domain.objects import Tank, Printer, PeachySetup
import random
from api.printer_model import PrinterModelApi


class TankInfoPanel(wx.Panel):
    def __init__(self, parent, api):
        wx.Panel.__init__(self, parent=parent)
        self.api = api
        self.sizer = wx.FlexGridSizer(20, 3, 10, 10)
        self.SetSizer(self.sizer)
        self.load_data()

    def load_data(self):
        self._remove_old_widgets()
        self.sizer.AddMany([(0, 10), (0, 10), (0, 10)])
        for (k, v) in self.api.get_tank_info().iteritems():
            key = wx.StaticText(self, label=k)
            if type(v[0]) == type(''):
                text_data = v[0]
            else:
                text_data = '{:5,.2f}'.format(v[0])
            text = wx.StaticText(self, label=text_data)
            unit = wx.StaticText(self, label=v[1])
            self.sizer.Add(key, 0, wx.EXPAND)
            self.sizer.Add(text, 1, wx.EXPAND)
            self.sizer.Add(unit, 0)
            self.Layout()

    def _remove_old_widgets(self):
        children = self.sizer.GetChildren()
        if children:
            for child in children:
                self.sizer.Hide(0)
                self.sizer.Remove(0)
            self.sizer.Layout()


class PrinterInfoPanel(wx.Panel):
    def __init__(self, parent, api):
        wx.Panel.__init__(self, parent=parent)
        self.api = api
        self.sizer = wx.FlexGridSizer(20, 2, 10, 10)
        self.SetSizer(self.sizer)
        self.load_data()

    def load_data(self):
        self._remove_old_widgets()
        self.sizer.AddMany([(0, 10), (0, 10), (0, 10)])
        for (k, v) in self.api.get_tank_info().iteritems():
            key = wx.StaticText(self, label=k)
            if type(v[0]) == type(''):
                text_data = v[0]
            else:
                text_data = '{:5,.2f}'.format(v[0])
            text = wx.StaticText(self, label=text_data)
            unit = wx.StaticText(self, label=v[1])
            self.sizer.Add(key, 0, wx.EXPAND)
            self.sizer.Add(text, 1, wx.EXPAND)
            self.sizer.Add(unit, 0)
            self.Layout()

    def _remove_old_widgets(self):
        children = self.sizer.GetChildren()
        if children:
            for child in children:
                self.sizer.Hide(0)
                self.sizer.Remove(0)
            self.sizer.Layout()


class DisplayPanel(wx.Panel):
    def __init__(self, parent, api):
        self.parent = parent
        self.api = api
        wx.Panel.__init__(self, self.parent, -1, style=wx.RAISED_BORDER)

        self.SetFocus()
        self.canvas = Canvas(self)
        info_sizer = self.setup_info_panel()
        sizer_display_control = wx.BoxSizer(wx.HORIZONTAL)
        sizer_display_control.Add(info_sizer, 1, wx.EXPAND, 5)
        sizer_display_control.Add(self.canvas, 5, wx.ALL | wx.EXPAND, 5)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_display_control)

        self.setup_events()
        wx.PostEvent(self.GetEventHandler(), self.UpdateEvent())

    def setup_info_panel(self):
        info_sizer = wx.BoxSizer(wx.VERTICAL)
        control_sizer = self.setup_controls()
        info_pages = self.setup_info_pages()
        info_sizer.Add(control_sizer, 0, wx.EXPAND)
        info_sizer.Add(info_pages, 1, wx.EXPAND)
        return info_sizer

    def setup_events(self):
        self.UpdateEvent, EVT_UPDATE = wx.lib.newevent.NewEvent()
        self.Bind(EVT_UPDATE, self.update_display)
        self.Bind(wx.EVT_SLIDER, self.update_tank)
        self.Bind(wx.EVT_RADIOBUTTON, self.update_tank)

    def setup_controls(self):
        control_sizer = wx.FlexGridSizer(11, 1, 5, 5)

        printer_height_label = wx.StaticText(self, label="Printer Height Above Tank mm")
        self.printer_height_value_label = wx.StaticText(self, label="250", style=wx.ALIGN_RIGHT)
        printer_height_sizer = wx.BoxSizer(wx.HORIZONTAL)
        printer_height_sizer.AddMany([(printer_height_label, 1, wx.EXPAND), (self.printer_height_value_label, 1, wx.EXPAND)])
        self.printer_height_slider = wx.Slider(self, value=100, minValue=1, maxValue=3000)

        tank_height_label = wx.StaticText(self, label="Tank Height mm")
        self.tank_height_value_label = wx.StaticText(self, label="200", style=wx.ALIGN_RIGHT)
        tank_height_sizer = wx.BoxSizer(wx.HORIZONTAL)
        tank_height_sizer.AddMany([(tank_height_label, 1, wx.EXPAND), (self.tank_height_value_label, 1, wx.EXPAND)])
        self.tank_height_slider = wx.Slider(self, value=200, minValue=100, maxValue=3000)

        printer_width_label = wx.StaticText(self, label="Tank Width mm")
        self.printer_width_value_label = wx.StaticText(self, label="100", style=wx.ALIGN_RIGHT)
        printer_width_sizer = wx.BoxSizer(wx.HORIZONTAL)
        printer_width_sizer.AddMany([(printer_width_label, 1, wx.EXPAND), (self.printer_width_value_label, 1, wx.EXPAND)])
        self.printer_width_slider = wx.Slider(self, value=100, minValue=40, maxValue=1000)

        material_width_label = wx.StaticText(self, label="Material Width mm")
        self.material_width_value_label = wx.StaticText(self, label="3", style=wx.ALIGN_RIGHT)
        material_width_sizer = wx.BoxSizer(wx.HORIZONTAL)
        material_width_sizer.AddMany([(material_width_label, 1, wx.EXPAND), (self.material_width_value_label, 1, wx.EXPAND)])
        self.material_width_slider = wx.Slider(self, value=3, minValue=0.1, maxValue=20)

        self.shape_cylinder = wx.RadioButton(self, -1, 'Cylinder', (10, 10), style=wx.RB_GROUP)
        self.shape_box = wx.RadioButton(self, -1, 'Box', (10, 30))

        control_sizer.Add(printer_height_sizer, 1, wx.EXPAND)
        control_sizer.Add(self.printer_height_slider, 1, wx.EXPAND)
        control_sizer.Add(tank_height_sizer, 1, wx.EXPAND)
        control_sizer.Add(self.tank_height_slider, 1, wx.EXPAND)
        control_sizer.Add(printer_width_sizer, 1, wx.EXPAND)
        control_sizer.Add(self.printer_width_slider, 1, wx.EXPAND)
        control_sizer.Add(material_width_sizer, 1, wx.EXPAND)
        control_sizer.Add(self.material_width_slider, 1, wx.EXPAND)
        control_sizer.Add(self.shape_cylinder)
        control_sizer.Add(self.shape_box)
        control_sizer.Add((0, 10))

        control_sizer.AddGrowableCol(0)
        return control_sizer

    def setup_info_pages(self):
        notebook = wx.Notebook(self)
        self.tankInfo = TankInfoPanel(notebook, self.api)
        notebook.AddPage(self.tankInfo, "Tank")
        tabTwo = PrinterInfoPanel(notebook, self.api)
        notebook.AddPage(tabTwo, "Printer")
        return notebook

    def shutdown(self):
        pass

    def update_display(self, message):
        logging.info('Updating display')
        self.update_tank(None)

    def update_tank(self, message):
        logging.info('Updating tank')
        self.printer_height_value_label.SetLabel(str(self.printer_height_slider.GetValue()))
        self.tank_height_value_label.SetLabel(str(self.tank_height_slider.GetValue()))
        self.printer_width_value_label.SetLabel(str(self.printer_width_slider.GetValue()))
        self.material_width_value_label.SetLabel(str(self.material_width_slider.GetValue()))

        if self.shape_cylinder.GetValue():
            shape = 'Cylinder'
        else:
            shape = 'Box'

        tank = Tank(
            self.tank_height_slider.GetValue(),
            self.material_width_slider.GetValue(),
            self.printer_width_slider.GetValue(),
            1199.8,
            shape
            )
        printer = Printer(self.tank_height_slider.GetValue() + self.printer_height_slider.GetValue())
        peachy_setup = PeachySetup(tank, printer)
        self.api.set_tank(tank)

        self.tankInfo.load_data()
        self.canvas.peachy_setup = peachy_setup
        self.canvas.OnDraw()

class ViewerApp(wx.App):
    def __init__(self, path):
        logging.info('Starting Application')
        self.frame = None
        self.api = PrinterModelApi()
        wx.App.__init__(self, redirect=False)
        logging.info("Started Application")
        

    def setup_menu(self):
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        menu_exit_item = menu.Append(wx.ID_EXIT, "E&xit\tCtrl-Q", "Exit")

        self.Bind(wx.EVT_MENU, self.OnExitApp, menu_exit_item)

        menuBar.Append(menu, "&File")
        self.frame.SetMenuBar(menuBar)

    def OnInit(self):
        logging.debug("Initting")
        self.frame = wx.Frame(None,
                              id=-1,
                              title="Tank Builder",
                              pos=(0, 0),
                              style=wx.DEFAULT_FRAME_STYLE,
                              )

        self.frame.CreateStatusBar()
        self.setup_menu()
        self.frame.Show(True)
        self.frame.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
        sizer = wx.BoxSizer(wx.VERTICAL)
        logging.debug("Starting display panel")
        display_panel = DisplayPanel(self.frame, self.api)
        logging.debug("Display panel started")
        sizer.Add(display_panel, 1, wx.EXPAND | wx.ALL)
        self.frame.SetSizer(sizer)
        logging.info("Display Size: %s,%s" % wx.DisplaySize())
        self.frame.SetSize(wx.DisplaySize())
        display_panel.SetFocus()
        self.window = display_panel
        self.SetTopWindow(self.frame)
        return True

    def OnExitApp(self, evt):
        self.frame.Close(True)

    def OnCloseFrame(self, evt):
        if hasattr(self, "window") and hasattr(self.window, "shutdown"):
            self.window.shutdown()
        evt.Skip()
