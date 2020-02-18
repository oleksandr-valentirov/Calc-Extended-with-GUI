import wx
from config.config import conf
from modes.modes import CalcMode, EquationsMode
# from modes.equations import EquationsMode


class MainFrame(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs)

        self.panel = wx.Panel(self)  # main panel
        self.main_box = wx.BoxSizer(wx.VERTICAL)  # main sizer
        CalcMode(self.panel, self.main_box)
        self.create_menu()  # creating menu bar. ToDo - why I shall create it after all inner content ?

    def equation_mode(self, event):
        EquationsMode(self.panel, self.main_box)

    def calc_mode(self, event):
        CalcMode(self.panel, self.main_box)

    def create_menu(self):
        menu_bar = wx.MenuBar()  # row under the top border of application

        file_section = wx.Menu()
        mode_section = wx.Menu()

        # forming file section
        about_item = file_section.Append(wx.ID_ABOUT)
        # ToDo - create action for ABOUT
        file_section.AppendSeparator()
        exit_item = file_section.Append(wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)

        # forming mode selection section
        calc_item = mode_section.AppendRadioItem(-1, '&Calculator')
        self.Bind(wx.EVT_MENU, self.calc_mode, calc_item)
        equation_item = mode_section.AppendRadioItem(-1, '&Equations')
        self.Bind(wx.EVT_MENU, self.equation_mode, equation_item)
        functions = mode_section.AppendRadioItem(-1, '&Functions')
        # ToDo - create action for radio buttons
        mode_section.AppendSeparator()

        menu_bar.Append(file_section, '&File')
        menu_bar.Append(mode_section, '&Mode')
        self.SetMenuBar(menu_bar)

    def on_exit(self, event):
        self.Close(True)


if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame(None, -1, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER,  # making fixed-size frame
                      title="Input testing", size=(int(conf.get('window_params', 'max_w')),
                                                   int(conf.get('window_params', 'max_h'))
                                                   )
                      )
    frame.Show()
    app.MainLoop()
