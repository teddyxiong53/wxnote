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

class WXNote(wx.App):
    def OnInit(self):
        frame = MainFrame(None, -1, title=_("WXNote"))
        frame.Show()
        return True

if __name__ == '__main__':
    app = WXNote()
    app.MainLoop()
