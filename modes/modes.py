import wx
from calc import calc
from config.config import conf
from abc import ABC, abstractmethod


class AbstractMode(ABC):
    """Abstract class for modes"""

    @abstractmethod
    def on_enter(self, event):
        """Abstract method for Enter key event processing
        :param event: - event object of wxPython module
        """
        assert NotImplementedError(f"method must be implemented")

    @abstractmethod
    def on_clear(self, event):
        """Abstract method for clearing input
        :param event: - event object of wxPython module
        """
        assert NotImplementedError(f"method must be implemented")

    @abstractmethod
    def on_button_click(self, event):
        """Abstract method for processing button events
        :param event: - event object of wxPython module
        """
        assert NotImplementedError(f"method must be implemented")

    @abstractmethod
    def i_o_labels(self, panel):
        """Abstract method for creating input and output fields
        :param panel: - panel object of wxPython module
        """
        assert NotImplementedError(f"method must be implemented")

    @abstractmethod
    def func_button(self, panel):
        """Abstract method for creating function buttons"""
        assert NotImplementedError(f"method must be implemented")


class BaseMode:

    def __init__(self, main_box):
        self.input = None
        self.output = None
        self.clear_input_if_checked = None
        main_box.Clear(True)

    def load_o_to_i(self, event):
        self.input.SetValue(self.output.GetValue())

    def on_delete(self, event):
        self.input.Remove(self.input.GetLastPosition()-1, self.input.GetLastPosition())

    def on_button_click(self, event):
        self.input.AppendText(event.EventObject.LabelText)
        if event.EventObject.LabelText in ('sin', 'cos', '\u221A', 'abs', 'log'):
            self.input.AppendText('(')

    def func_button(self, panel):
        bbox = wx.BoxSizer(wx.VERTICAL)
        rxbox = []
        for i in range(0, 2):
            rxbox.append(wx.BoxSizer(wx.HORIZONTAL))

        labels = ['sin', 'log']
        for i in range(len(labels)):
            b = wx.Button(panel, label=labels[i], size=(int(conf.get('button_params', 'w')),
                                                        int(conf.get('button_params', 'h'))
                                                        )
                          )
            b.Bind(wx.EVT_BUTTON, self.on_button_click)
            font = b.GetFont()
            font.PointSize += 5
            b.SetFont(font)
            rxbox[i].Add(b)

        return bbox, rxbox


class CalcMode(AbstractMode, BaseMode):

    def __init__(self, panel, main_box):
        super().__init__(main_box)

        self.panel = panel
        # I/O is decimal by default
        self.input_type = 0
        self.default_input = ''
        self.output_type = 0

        self.gui_box = wx.BoxSizer(wx.HORIZONTAL)  # GUI handler
        options_box = wx.BoxSizer(wx.HORIZONTAL)  # option box above left and right GUI
        left_box = wx.BoxSizer(wx.VERTICAL)  # left part of the GUI
        right_box = wx.BoxSizer(wx.VERTICAL)  # right part of the GUI

        obox = self.calc_options_buttons(panel)  # options
        options_box.Add(obox, wx.SizerFlags().Border(wx.TOP, 5))

        lbox = self.i_o_labels(panel)  # I/O labels
        fbox = self.func_button(panel)  # function buttons
        right_box.Add(lbox)  # I/O should be from right
        right_box.Add(fbox, wx.SizerFlags().Border(wx.TOP, 5))  # functions should be under I/O

        bbox = self.num_buttons(panel)  # number buttons
        left_box.Add(bbox)  # numbers should be from left

        self.gui_box.Add(left_box, wx.SizerFlags().Border(wx.LEFT, 10))
        self.gui_box.Add(right_box, wx.SizerFlags().Border(wx.LEFT, 10))

        main_box.Add(options_box, wx.SizerFlags().Border(wx.LEFT | wx.TOP, 10))
        main_box.Add(self.gui_box, wx.SizerFlags().Border(wx.TOP, 10))
        main_box.Layout()
        panel.SetSizer(main_box)

    def i_o_labels(self, panel):
        lbox = wx.BoxSizer(wx.VERTICAL)  # I/O sizer
        # I/O definitions
        self.input = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER, size=(int(conf.get('calc_label_params', 'w')),
                                                                         int(conf.get('calc_label_params', 'h'))
                                                                         )
                                 )
        font = self.input.GetFont()
        font.PointSize = 15
        self.input.SetFont(font)

        self.output = wx.TextCtrl(panel, style=wx.TE_READONLY, size=(int(conf.get('calc_label_params', 'w')),
                                                                     int(conf.get('calc_label_params', 'h'))
                                                                     )
                                  )
        font = self.output.GetFont()
        font.PointSize = 15
        self.output.SetFont(font)

        # input event handler
        self.input.Bind(wx.EVT_TEXT_ENTER, self.on_enter)
        # I/O sizers
        lbox.Add(self.input)
        lbox.Add(self.output, wx.SizerFlags().Border(wx.TOP, 5))
        return lbox

    def bin_num_buttons(self, panel):
        bbox = wx.BoxSizer(wx.VERTICAL)
        rxbox = []

        for i in range(0, 3):
            rxbox.append(wx.BoxSizer(wx.HORIZONTAL))

        labels = ['0', '+', '^']
        for i in range(1, 4):
            b = wx.Button(panel, label=labels[i - 1], size=(int(conf.get('button_params', 'w')),
                                                            int(conf.get('button_params', 'h'))
                                                            )
                          )
            b.Bind(wx.EVT_BUTTON, self.on_button_click)
            font = b.GetFont()
            font.PointSize += 5
            b.SetFont(font)
            rxbox[i - 1].Add(b)

        sizers = [0, 0, 1, 1, 1, 2, 2, 2]
        for i in ('1', '(/)', '-', '|', '&&', '<<', '>>'):
            if i == '(/)':
                b = wx.Choice(panel, name=i, choices=['(', ')'], size=(int(conf.get('button_params', 'w')),
                                                                       int(conf.get('button_params', 'h')))
                              )
                b.Bind(wx.EVT_CHOICE, self.on_parenthesis)
            else:
                b = wx.Button(panel, label=i, size=(int(conf.get('button_params', 'w')),
                                                    int(conf.get('button_params', 'h')))
                              )
                b.Bind(wx.EVT_BUTTON, self.on_button_click)
            font = b.GetFont()
            font.PointSize += 5
            b.SetFont(font)
            rxbox[sizers.pop(0)].Add(b, wx.SizerFlags().Border(wx.LEFT, 5))

        bbox.Add(rxbox.pop(0))
        for i in rxbox:
            bbox.Add(i, wx.SizerFlags().Border(wx.TOP, 5))
        return bbox

    def num_buttons(self, panel):
        bbox = wx.BoxSizer(wx.VERTICAL)
        rxbox = []

        for i in range(0, 4):
            rxbox.append(wx.BoxSizer(wx.HORIZONTAL))

        labels = ['1', '4', '7', '.']
        for i in range(1, 5):
            b = wx.Button(panel, label=labels[i - 1], size=(int(conf.get('button_params', 'w')),
                                                            int(conf.get('button_params', 'h'))
                                                            )
                          )
            b.Bind(wx.EVT_BUTTON, self.on_button_click)
            font = b.GetFont()
            font.PointSize += 5
            b.SetFont(font)
            rxbox[i - 1].Add(b)

        sizers = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]
        for i in ('2', '3', '+', '5', '6', '-', '8', '9', '*', '0', '(/)', '/'):
            if i == '(/)':
                b = wx.Choice(panel, name=i, choices=['(', ')'], size=(int(conf.get('button_params', 'w')),
                                                                       int(conf.get('button_params', 'h')))
                              )
                b.Bind(wx.EVT_CHOICE, self.on_parenthesis)
            else:
                b = wx.Button(panel, label=i, size=(int(conf.get('button_params', 'w')),
                                                    int(conf.get('button_params', 'h')))
                              )
                b.Bind(wx.EVT_BUTTON, self.on_button_click)
            font = b.GetFont()
            font.PointSize += 5
            b.SetFont(font)
            rxbox[sizers.pop(0)].Add(b, wx.SizerFlags().Border(wx.LEFT, 5))

        bbox.Add(rxbox.pop(0))
        for i in rxbox:
            bbox.Add(i, wx.SizerFlags().Border(wx.TOP, 5))
        return bbox

    def hex_buttons(self, panel):
        bbox = wx.BoxSizer(wx.VERTICAL)
        rxbox = []

        for i in range(0, 6):
            rxbox.append(wx.BoxSizer(wx.HORIZONTAL))

        labels = ['1', '4', '7', '.', 'A', 'D']
        for i in range(1, 7):
            b = wx.Button(panel, label=labels[i - 1], size=(int(conf.get('button_params', 'w')),
                                                            int(conf.get('button_params', 'h'))
                                                            )
                          )
            b.Bind(wx.EVT_BUTTON, self.on_button_click)
            font = b.GetFont()
            font.PointSize += 5
            b.SetFont(font)
            rxbox[i - 1].Add(b)

        sizers = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5]
        for i in ('2', '3', '+', '5', '6', '-', '8', '9', '*', '0', '(/)', '/', 'B', 'C', 'D', 'E'):
            if i == '(/)':
                b = wx.Choice(panel, name=i, choices=['(', ')'], size=(int(conf.get('button_params', 'w')),
                                                                       int(conf.get('button_params', 'h')))
                              )
                b.Bind(wx.EVT_CHOICE, self.on_parenthesis)
            else:
                b = wx.Button(panel, label=i, size=(int(conf.get('button_params', 'w')),
                                                    int(conf.get('button_params', 'h')))
                              )
                b.Bind(wx.EVT_BUTTON, self.on_button_click)
            font = b.GetFont()
            font.PointSize += 5
            b.SetFont(font)
            rxbox[sizers.pop(0)].Add(b, wx.SizerFlags().Border(wx.LEFT, 5))

        bbox.Add(rxbox.pop(0))
        for i in range(len(rxbox)):
            bbox.Add(rxbox[i], wx.SizerFlags().Border(wx.TOP, 5))
        return bbox

    def calc_options_buttons(self, panel):
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        i = wx.RadioBox(panel, label="Input", choices=('dec', 'bin', 'hex'))
        o = wx.RadioBox(panel, label="Output", choices=('dec', 'bin', 'hex'))
        i.Bind(wx.EVT_RADIOBOX, self.set_input_type)
        o.Bind(wx.EVT_RADIOBOX, self.set_output_type)

        enter = wx.Button(panel, label="-->", size=(int(conf.get('button_params', 'w')),
                                                    int(conf.get('button_params', 'h'))
                                                    )
                          )
        enter.Bind(wx.EVT_BUTTON, self.on_enter)
        font = enter.GetFont()
        font.PointSize += 5
        enter.SetFont(font)

        clear = wx.Button(panel, label="X", size=(int(conf.get('button_params', 'w')),
                                                  int(conf.get('button_params', 'h'))
                                                  )
                          )
        clear.Bind(wx.EVT_BUTTON, self.on_clear)
        font = clear.GetFont()
        font.PointSize += 5
        clear.SetFont(font)

        delete = wx.Button(panel, label="<--", size=(int(conf.get('button_params', 'w')),
                                                     int(conf.get('button_params', 'h'))
                                                     )
                           )
        delete.Bind(wx.EVT_BUTTON, self.on_delete)
        font = delete.GetFont()
        font.PointSize += 5
        delete.SetFont(font)

        self.clear_input_if_checked = wx.CheckBox(panel, label='\nClear on Enter', size=(100, 40))

        hbox.Add(i)
        hbox.Add(o, wx.SizerFlags().Border(wx.LEFT, 10))
        hbox.Add(delete, wx.SizerFlags().Border(wx.LEFT, 10))
        hbox.Add(clear, wx.SizerFlags().Border(wx.LEFT, 10))
        hbox.Add(enter, wx.SizerFlags().Border(wx.LEFT, 10))
        hbox.Add(self.clear_input_if_checked, wx.SizerFlags().Border(wx.LEFT, 10))

        return hbox

    def func_button(self, panel):
        bbox, rxbox = BaseMode.func_button(self, panel)
        sizers = [0, 0, 0, 0, 0, 1, 1]
        for label in ('cos', '\u221A', 'pi', 'abs', '^', 'e', 'load output\nto input'):
            if len(label) == 20:
                b = wx.Button(panel, label=label, size=(105, int(conf.get('button_params', 'h'))))
                b.Bind(wx.EVT_BUTTON, self.load_o_to_i)
            else:
                b = wx.Button(panel, label=label, size=(int(conf.get('button_params', 'w')),
                                                        int(conf.get('button_params', 'h'))
                                                        )
                              )
                b.Bind(wx.EVT_BUTTON, self.on_button_click)
            font = b.GetFont()
            font.PointSize += 5
            b.SetFont(font)
            rxbox[sizers.pop(0)].Add(b, wx.SizerFlags().Border(wx.LEFT, 5))

        bbox.Add(rxbox.pop(0))
        for row in rxbox:
            bbox.Add(row, wx.SizerFlags().Border(wx.TOP, 5))

        return bbox

    def set_output_type(self, event):
        self.output_type = event.GetSelection()

    def set_input_type(self, event):
        self.destroy_nums(None)
        choice = event.GetSelection()
        if choice == 0:
            self.gui_box.Insert(0, self.num_buttons(self.panel), wx.SizerFlags().Border(wx.LEFT, 10))
            self.default_input = ''
        elif choice == 1:
            self.gui_box.Insert(0, self.bin_num_buttons(self.panel), wx.SizerFlags().Border(wx.LEFT, 10))
            self.default_input = '0b'
        else:
            self.gui_box.Insert(0, self.hex_buttons(self.panel), wx.SizerFlags().Border(wx.LEFT, 10))
            self.default_input = '0x'
        self.input.SetValue(self.default_input)
        self.panel.Layout()

    def on_button_click(self, event):
        BaseMode.on_button_click(self, event)
        if event.EventObject.LabelText in ('+', '-', '*', '/', '|', '&', '^', '<<', '>>'):
            self.input.AppendText(self.default_input)

    def destroy_nums(self, event):
        self.gui_box.Children[0].Sizer.Clear(True)
        self.gui_box.Remove(0)

    def on_parenthesis(self, event):
        self.input.AppendText(['(', ')'][event.GetSelection()])

    def on_clear(self, event):
        self.input.SetValue(self.default_input)

    def on_enter(self, event):
        text = self.input.GetValue()
        output_type = [None, bin, hex]
        if self.clear_input_if_checked.GetValue():
            self.input.SetValue(self.default_input)
        self.output.SetValue(str(calc.evaluate(text, output_type[self.output_type])))


class EquationsMode(AbstractMode, BaseMode):

    def __init__(self, panel, main_box):
        super().__init__(main_box)

        gui_box = wx.BoxSizer(wx.VERTICAL)  # GUI handler
        i_o_box = wx.BoxSizer(wx.VERTICAL)  # left part of the GUI
        func_box = wx.BoxSizer(wx.VERTICAL)  # right part of the GUI

        lbox = self.i_o_labels(panel)  # types and I/O in left part
        i_o_box.Add(lbox)

        fbox = self.func_button(panel)  # function buttons in right part
        func_box.Add(fbox)

        gui_box.Add(i_o_box, wx.SizerFlags().Border(wx.LEFT, 10))
        gui_box.Add(func_box, wx.SizerFlags().Border(wx.LEFT | wx.TOP, 10))
        main_box.Add(gui_box, wx.SizerFlags().Border(wx.TOP, 10))
        main_box.Layout()
        panel.SetSizer(main_box)

    def i_o_labels(self, panel):
        ibox = wx.BoxSizer(wx.HORIZONTAL)
        lbox = wx.BoxSizer(wx.VERTICAL)
        types = wx.RadioBox(panel, label="Type of equation", choices=('Linear', 'Diff'))
        # ToDo - actions for types radiobox

        # I/O definitions
        self.input = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER, size=(int(conf.get('equ_label_params', 'w')),
                                                                         int(conf.get('equ_label_params', 'h'))
                                                                         )
                                 )
        font = self.input.GetFont()
        font.PointSize = 15
        self.input.SetFont(font)
        self.input.Bind(wx.EVT_TEXT_ENTER, self.on_enter)

        text = wx.StaticText(panel, label=" = 0")
        font = text.GetFont()
        font.PointSize = 20
        text.SetFont(font)

        self.output = wx.TextCtrl(panel, style=wx.TE_READONLY, size=(int(conf.get('equ_label_params', 'w')),
                                                                     int(conf.get('equ_label_params', 'h'))
                                                                     )
                                  )
        font = self.output.GetFont()
        font.PointSize = 15
        self.output.SetFont(font)

        lbox.Add(types)
        ibox.Add(self.input)
        ibox.Add(text)
        lbox.Add(ibox, wx.SizerFlags().Border(wx.TOP, 5))
        lbox.Add(self.output, wx.SizerFlags().Border(wx.TOP, 5))
        return lbox

    def on_button_click(self, event):
        BaseMode.on_button_click(self, event)

    def on_enter(self, event):
        text = self.input.GetValue()
        self.output.SetValue(str(calc.solve_equation(text)))

    def on_clear(self, event):
        self.input.SetValue('')

    def func_button(self, panel):
        bbox, rxbox = BaseMode.func_button(self, panel)
        sizers = [0, 0, 0, 0, 0, 1]
        for label in ('cos', '\u221A', 'pi', 'abs', '^', 'e'):
            b = wx.Button(panel, label=label, size=(int(conf.get('button_params', 'w')),
                                                    int(conf.get('button_params', 'h'))
                                                    )
                          )
            b.Bind(wx.EVT_BUTTON, self.on_button_click)
            font = b.GetFont()
            font.PointSize += 5
            b.SetFont(font)
            rxbox[sizers.pop(0)].Add(b, wx.SizerFlags().Border(wx.LEFT, 5))

        bbox.Add(rxbox.pop(0))
        for row in rxbox:
            bbox.Add(row, wx.SizerFlags().Border(wx.TOP, 5))

        return bbox
