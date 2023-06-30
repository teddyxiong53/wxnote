import wx
import gettext

domain = 'wxnote'
locale_dir = 'locale'
lang = 'zh_CN'
gettext.bindtextdomain(domain, locale_dir)
gettext.textdomain(domain)
gettext.install(domain, localedir=locale_dir, names=('ngettext',))


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        self._init_ui()
    def _init_ui(self):
        # add menubar
        self._add_menubar()
        # add toolbar
        self._add_toolbar()
        # add statusbar
        self._add_status_bar()

    def _add_file_menu(self):
        self.file_menu = wx.Menu()
        self.menubar.Append(self.file_menu, '&File')

    def _add_file_menu(self):
        self.file_menu = wx.Menu()
        self.menubar.Append(self.file_menu, '&File')

    def _add_edit_menu(self):
        self.edit_menu = wx.Menu()
        self.menubar.Append(self.edit_menu, '&Edit')

    def _add_search_menu(self):
        self.search_menu = wx.Menu()
        self.menubar.Append(self.search_menu, '&Search')

    def _add_view_menu(self):
        self.view_menu = wx.Menu()
        self.menubar.Append(self.view_menu, '&View')

    def _add_encoding_menu(self):
        self.encoding_menu = wx.Menu()
        self.menubar.Append(self.encoding_menu, 'E&ncoding')

    def _add_language_menu(self):
        self.language_menu = wx.Menu()
        self.menubar.Append(self.language_menu, '&Language')

    def _add_settings_menu(self):
        self.settings_menu = wx.Menu()
        self.menubar.Append(self.settings_menu, 'Se&ttings')

    def _add_tools_menu(self):
        self.tools_menu = wx.Menu()
        self.menubar.Append(self.tools_menu, 'To&ols')

    def _add_macro_menu(self):
        self.macro_menu = wx.Menu()
        self.menubar.Append(self.macro_menu, '&Macro')

    def _add_run_menu(self):
        self.run_menu = wx.Menu()
        self.menubar.Append(self.run_menu, '&Run')

    def _add_plugins_menu(self):
        self.plugins_menu = wx.Menu()
        self.menubar.Append(self.plugins_menu, '&Plugins')

    def _add_window_menu(self):
        self.window_menu = wx.Menu()
        self.menubar.Append(self.window_menu, '&Window')

    def _add_help_menu(self):
        self.help_menu = wx.Menu()
        self.menubar.Append(self.help_menu, '&Help')

    def _add_menubar(self):
        self.menubar = wx.MenuBar()
        self.SetMenuBar(self.menubar)
        self._add_file_menu()
        self._add_edit_menu()
        self._add_search_menu()
        self._add_view_menu()

        self._add_encoding_menu()
        self._add_language_menu()
        self._add_settings_menu()
        self._add_tools_menu()

        self._add_macro_menu()
        self._add_run_menu()
        self._add_plugins_menu()
        self._add_window_menu()
        self._add_help_menu()

    def _add_toolbar(self):
        pass
    def _add_status_bar(self):
        pass
class WXNote(wx.App):
    def OnInit(self):
        frame = MainFrame(None, -1, title=_("WXNote"))
        frame.Show()
        return True

if __name__ == '__main__':
    app = WXNote()
    app.MainLoop()
