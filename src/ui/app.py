import wx
import wx.lib.newevent
import logging
from gl import Canvas


class DisplayPanel(wx.Panel):
    def __init__(self, parent):
        self.parent = parent
        wx.Panel.__init__(self, self.parent, -1, style=wx.RAISED_BORDER)

        self.SetFocus()
        self.canvas = Canvas(self)

        sizer_display_control = wx.BoxSizer(wx.HORIZONTAL)
        self.control_sizer = wx.FlexGridSizer(6, 1, 5, 5)
        sizer_display_control.Add(self.control_sizer, 1, wx.EXPAND, 5)
        sizer_display_control.Add(self.canvas, 5, wx.ALL | wx.EXPAND, 5)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_display_control)

        self.setup_controls()
        self.setup_events()

    def setup_events(self):
        self.UpdateEvent, EVT_UPDATE = wx.lib.newevent.NewEvent()
        self.Bind(EVT_UPDATE, self.update_display)
        self.Bind(wx.EVT_SLIDER, self.update_tank)

    def setup_controls(self):
        tank_height_label = wx.StaticText(self, label="Tank Height mm")
        printer_height_label = wx.StaticText(self, label="Printer Height mm")
        printer_width_label = wx.StaticText(self, label="Tank Width mm")

        self.tank_height_slider = wx.Slider(self, value=200, minValue=100, maxValue=3000)
        self.printer_height_slider = wx.Slider(self, value=250, minValue=120, maxValue=3500)
        self.printer_width_slider = wx.Slider(self, value=100, minValue=40, maxValue=1000)

        self.control_sizer.Add(tank_height_label)
        self.control_sizer.Add(self.tank_height_slider, 1, wx.EXPAND)
        self.control_sizer.Add(printer_height_label)
        self.control_sizer.Add(self.printer_height_slider, 1, wx.EXPAND)
        self.control_sizer.Add(printer_width_label)
        self.control_sizer.Add(self.printer_width_slider, 1, wx.EXPAND)
        self.control_sizer.AddGrowableCol(0)

    def shutdown(self):
        pass

    def update_display(self, message):
        logging.info('Updating display')

    def update_tank(self, message):
        pass


class ViewerApp(wx.App):
    def __init__(self, path):
        logging.info('Starting Application')
        self.frame = None
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
        display_panel = DisplayPanel(self.frame)
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
