import datetime
import keyword
import os
import traceback

import wx
import gettext
import wx.lib.agw.flatnotebook as fnb
import wx.stc as stc

domain = 'wxnote'
locale_dir = 'locale'
lang = 'zh_CN'
gettext.bindtextdomain(domain, locale_dir)
gettext.textdomain(domain)
gettext.install(domain, localedir=locale_dir, names=('ngettext',))

COLOR_FG = (0,0,0)
COLOR_BG = (255, 255, 255)

COLOR_CUR_TAB = (51, 204, 51)
COLOR_OTHER_TAB = (102, 153, 153)
class FlatNotebook(fnb.FlatNotebook):
    def __init__(self, parent):
        fnb.FlatNotebook.__init__(
            self,
            parent=parent,
            id=wx.ID_ANY,
            agwStyle=(
                fnb.FNB_NO_TAB_FOCUS |
                fnb.FNB_X_ON_TAB |
                fnb.FNB_NAV_BUTTONS_WHEN_NEEDED |
                fnb.FNB_COLOURFUL_TABS
            )
        )
        self.SetTabAreaColour((255,255,255))
        self.SetActiveTabColour(COLOR_CUR_TAB)
        self.SetNonActiveTabTextColour(COLOR_OTHER_TAB)

        self.right_click_menu()
        self.custom_page()

    def right_click_menu(self):
        menu = wx.Menu()
        self.SetRightClickMenu(menu)
        menu.Append(wx.ID_CLOSE, 'Close', 'Close')
        self.Bind(wx.EVT_MENU, self.close, id=wx.CLOSE)
    def close(self, event):
        self.DeletePage(self.GetSelection())

    def custom_page(self):
        panel = wx.Panel(self)
        font = wx.Font(9, wx.TELETYPE, wx.NORMAL, wx.NORMAL)
        panel.SetFont(font)
        panel.SetBackgroundColour(COLOR_BG)
        panel.SetForegroundColour(COLOR_FG)
        self.SetCustomPage(panel)

class TxtCtrl(stc.StyledTextCtrl):
    def __init__(self, parent, text, readonly):
        stc.StyledTextCtrl.__init__(self, parent, wx.ID_ANY)
        self.SetText(text)
        self.SetReadOnly(readonly)
        self.Bind(stc.EVT_STC_MARGINCLICK, self.margin_click)

    def margin_click(self, event):
        if event.GetMargin() == 2:
            if event.GetShift() and event.GetCtrl():
                self.fold_all()
            else:
                line_clicked = self.LineFromPosition(event.GetPosition())
                if (
                    self.GetFoldLevel(line_clicked) and
                    stc.STC_FOLDLEVELHEADERFLAG
                ):
                    if event.GetShift():
                        self.SetFoldExpanded(line_clicked, True)
                        self.expand(line_clicked, True, True, 1)
                    elif event.GetCtrl():
                        pass
                    else:
                        self.ToggleFold(line_clicked)
        else:
            event.Skip()

    def fold_all(self):
        line_count = self.GetLineCount()
        expanding = True
        # TODO

    def expand(self, line, doexpand, force=False, vis_levels=0, level=-1):
        pass



class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        self.init_ui()

    def init_ui(self):
        # add menubar
        self.add_menubar()
        # add toolbar
        self.add_toolbar()
        # add statusbar
        self.add_status_bar()
        # container for text content
        panel = wx.Panel(self)
        panel.SetBackgroundColour(COLOR_BG)
        # create container for all tabs
        self.pages = []
        self.notebook = FlatNotebook(panel)
        first_page = self.new_file()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, wx.ALL|wx.EXPAND, 0)
        panel.SetSizerAndFit(sizer)
        panel.Layout()

    def new_file(self):
        self.show_notebook_if_not_shown()

    def new_file_event(self, event):
        if event.GetId() == wx.ID_NEW:
            self.new_file()
        else:
            event.Skip()

    def save_file_event(self, event):
        pass
    def add_file_menu(self):
        self.file_menu = wx.Menu()
        self.menubar.Append(self.file_menu, '&File')
        # add menuitem
        # New
        self.file_menu.Append(wx.ID_NEW, '&New', 'New a file')
        self.Bind(wx.EVT_MENU, self.new_file_event, id=wx.ID_NEW)

        # Open
        self.file_menu.Append(wx.ID_OPEN, '&Open file\tCtrl+O', 'Open a file')
        self.Bind(wx.EVT_MENU, self.open_file_event, id=wx.ID_OPEN)
        # Save
        self.file_menu.Append(wx.ID_SAVE, 'Save\tCtrl+S', 'Save current file')
        self.Bind(wx.EVT_MENU, self.save_file_event, id=wx.ID_SAVE)
        # Save as
        self.file_menu.Append(wx.ID_SAVEAS, 'Save as', 'Save using a different name')
        self.Bind(wx.EVT_MENU, self.save_file_event, id=wx.ID_SAVEAS)
        # Save all
        # TODO
        self.file_menu.Append(wx.ID_SAVEAS, 'Save as', 'Save using a different name')
        self.Bind(wx.EVT_MENU, self.save_file_event, id=wx.ID_SAVEAS)
        # Close
        self.file_menu.Append(wx.ID_CLOSE, 'Close', 'Close current file')
        self.Bind(wx.EVT_MENU, self.close_file_event, id=wx.ID_CLOSE)
        # Close All
        self.file_menu.Append(wx.ID_CLOSE_ALL, 'Close all', 'Close all file')
        self.Bind(wx.EVT_MENU, self.close_all_event, id=wx.ID_CLOSE_ALL)

    def close_file_event(self, event):
        pass
    def close_all_event(self, event):
        pass
    def add_edit_menu(self):
        self.edit_menu = wx.Menu()
        self.menubar.Append(self.edit_menu, '&Edit')

    def add_search_menu(self):
        self.search_menu = wx.Menu()
        self.menubar.Append(self.search_menu, '&Search')

    def add_view_menu(self):
        self.view_menu = wx.Menu()
        self.menubar.Append(self.view_menu, '&View')

    def add_encoding_menu(self):
        self.encoding_menu = wx.Menu()
        self.menubar.Append(self.encoding_menu, 'E&ncoding')

    def add_language_menu(self):
        self.language_menu = wx.Menu()
        self.menubar.Append(self.language_menu, '&Language')

    def add_settings_menu(self):
        self.settings_menu = wx.Menu()
        self.menubar.Append(self.settings_menu, 'Se&ttings')

    def add_tools_menu(self):
        self.tools_menu = wx.Menu()
        self.menubar.Append(self.tools_menu, 'To&ols')

    def add_macro_menu(self):
        self.macro_menu = wx.Menu()
        self.menubar.Append(self.macro_menu, '&Macro')

    def add_run_menu(self):
        self.run_menu = wx.Menu()
        self.menubar.Append(self.run_menu, '&Run')

    def add_plugins_menu(self):
        self.plugins_menu = wx.Menu()
        self.menubar.Append(self.plugins_menu, '&Plugins')

    def add_window_menu(self):
        self.window_menu = wx.Menu()
        self.menubar.Append(self.window_menu, '&Window')

    def add_help_menu(self):
        self.help_menu = wx.Menu()
        self.menubar.Append(self.help_menu, '&Help')
    def open_file_event(self, event):
        if event.GetId() == wx.ID_OPEN:
            self.open_file()
        else:
            event.Skip()
    def show_notebook_if_not_shown(self):
        if not self.notebook.IsShown():
            self.notebook_visible_toggle_action()

    def notebook_visible_toggle_action(self):
        self.notebook.Show(not self.notebook.IsShown())
        # self.view_menu.Check()
        self.SendSizeEvent()

    def set_styles_default(self):
        '''
        Set page default style
        :return: None
        '''
        page = self.notebook.GetCurrentPage()
        page.ClearDocumentStyle()

        page.SetUseTabs(False)
        page.SetTabWidth(4)
        page.SetViewWhiteSpace(True)
        page.SetViewEOL(False)

        font = wx.Font(12, wx.TELETYPE, wx.NORMAL, wx.NORMAL)
        page.StyleSetFont(stc.STC_STYLE_DEFAULT, font)

        page.StyleSetForeground(stc.STC_STYLE_DEFAULT, COLOR_FG)
        page.StyleSetBackground(stc.STC_STYLE_DEFAULT, COLOR_BG)
        page.SetSelForeground(True, (255,255,255))
        page.SetSelBackground(True, (68,68,68))
        page.SetCaretForeground((0,255,0))

        page.StyleClearAll()

        # below is non-basic style
        # set line number style
        page.StyleSetForeground(stc.STC_STYLE_LINENUMBER, (151, 151, 151))
        page.StyleSetBackground(stc.STC_STYLE_LINENUMBER, (51,51,51))

        # set null lexer for default text file
        page.SetLexer(stc.STC_LEX_NULL)
        # set python keyword
        page.SetKeyWords(0, " ".join(keyword.kwlist))
        page.SetFoldMarginColour(True, (41,41,41))
        page.SetFoldMarginHiColour(True, (51,51,51))
        page.SetMarginSensitive(2, False)

    def open_file(self):
        self.show_notebook_if_not_shown()
        dlg = wx.FileDialog(
            parent=self,
            message=_('Select a file to open'),
            defaultDir=os.getcwd(),
            defaultFile=_('New'),
            wildcard='All files (*.*) |*.*',
            style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_MULTIPLE
        )
        result = dlg.ShowModal()
        # dlg.Destroy()
        if result == wx.ID_OK:
            paths = dlg.GetPaths()
            filenames = dlg.GetFilenames()
            for index, filename in enumerate(filenames):
                path = paths[index]
                try:
                    f = open(path, 'r')
                    text = f.read()
                    f.close()

                    if (
                            (len(self.pages) == 1) and
                            (self.pages[0].filename == 'New') and
                            (self.pages[0].GetModify() == False)
                    ):
                        self.notebook.DeletePage(0)
                        self.pages = []

                    page = TxtCtrl(self, text, False)
                    self.pages.append(page)
                    page.SetUndoCollection(True)
                    page.SetBufferedDraw(True)

                    page.python_syntax = False
                    page.folding_symbols = False
                    page.line_numbers = False
                    page.word_wrap = True
                    page.path = path
                    page.filename = filename
                    page.datetime = str(datetime.datetime.now())

                    page.SetMarginLeft(6)
                    page.SetMarginWidth(0, 0)
                    page.SetMarginWidth(1, 0)
                    page.SetMarginWidth(2, 0)

                    self.notebook.AddPage(page=page, text=page.filename, select=True)

                    self.set_styles_default()
                    page.SetFocus()
                    page.SetSavePoint()

                    self.statusbar.SetStatusText(_('You opened {}').format(filename), 0)
                    self.statusbar.SetStatusText(filename, 1)
                except (IOError, UnicodeDecodeError) as error:
                    error_dlg = wx.MessageDialog(
                        parent=self,
                        message=_('Fail to open {}, reason {}').format(filename, error),
                        caption=_('Error'),
                        style=wx.ICON_EXCLAMATION
                    )
                    error_dlg.ShowModal()
                    error_dlg.Destroy()
                except Exception as e:
                    traceback.print_exc()
                    error_dlg = wx.MessageDialog(
                        parent=self,
                        message=_('Fail to open {}').format(filename),
                        caption=_('Error'),
                        style=wx.ICON_EXCLAMATION
                    )
                    error_dlg.ShowModal()
                    error_dlg.Destroy()
            else:
                self.statusbar.SetStatusText(_('The file is not opend'), 0)






    def add_menubar(self):
        self.menubar = wx.MenuBar()
        self.SetMenuBar(self.menubar)
        self.add_file_menu()
        self.add_edit_menu()
        self.add_search_menu()
        self.add_view_menu()

        self.add_encoding_menu()
        self.add_language_menu()
        self.add_settings_menu()
        self.add_tools_menu()

        self.add_macro_menu()
        self.add_run_menu()
        self.add_plugins_menu()
        self.add_window_menu()
        self.add_help_menu()

    def add_toolbar(self):
        pass
    def add_status_bar(self):
        self.statusbar = self.CreateStatusBar()
        # two part
        # left: update status
        # right: current filename
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-2, -1])
        self.statusbar.SetStatusText(_('Welcome to WXNote'), 0)
        self.statusbar.SetStatusText(_('No opened file'), 1)
        self.statusbar.Show()

class WXNote(wx.App):
    def OnInit(self):
        frame = MainFrame(None, -1, title=_("WXNote"), size=(800,600))
        frame.Centre()
        frame.Show()
        return True

if __name__ == '__main__':
    app = WXNote()
    app.MainLoop()
