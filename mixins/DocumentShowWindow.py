
import sys
import inspect
import wx


from modules import common
from modules.Debug import error
from modules.Mixin import Mixin


class DocumentShowWindow(wx.Panel, Mixin):
    __mixinname__ = 'docuwindow'
    
    def __init__(self, parent, mainframe):
        self.initmixin()
        
        wx.Panel.__init__(self, parent, -1)
        self.parent = parent
        self.mainframe = mainframe
        self.pref = mainframe.pref

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.scroll_win = wx.ScrolledWindow(self,-1, size=self.parent.GetSize(), style=wx.SIMPLE_BORDER |wx.NO_3D)
        self.text = wx.StaticText(self.scroll_win, -1, label='')
        self.text_fixed_font = wx.Font(10, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)
        self.text_default_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
        self.bgcolor = '#FFFFE1'
        
        self.text.Bind(wx.EVT_LEFT_DCLICK, self.open_source_file, id=self.text.GetId())
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.active = False
        self.Show()
        
    def show(self, text):
        
        if  self.mainframe.pref.inputass_calltip_including_source_code:
            self.text.SetFont(self.text_fixed_font)
        else:
            self.text.SetFont(self.text_default_font)
        self.text.SetLabel(text.strip())
        self.active = True
        self.SetBackgroundColour(self.bgcolor)
        self.text.SetBackgroundColour(self.bgcolor)
        self._set_scroll_bar()
        self.Show()
        if hasattr(self.mainframe,'document'):
            self.mainframe.document.SetFocus()
            
    def _set_scroll_bar(self):
        self.scroll_win.Scroll(0, 0)
        cw, ch = self.parent.GetClientSize()
        w, h = self.text.GetBestSize()
        self.scroll_win.SetSize(self.GetClientSize())
        if h > ch:
            self.scroll_win.SetScrollbars(wx.VERTICAL, 20, 0, h/20)
        else:
            self.scroll_win.SetScrollbars(wx.VERTICAL, 0, 0, 0)
        # todo don't how to set horizontal bar 2008:01:17 by ygao
        #if  w > cw :
            #self.scroll_win.SetScrollbars(wx.HORIZONTAL, cw, 0, (w+cw/cw))
        

    def OnSize(self,event):
        self._set_scroll_bar()
        

        
    def open_source_file(self, event):
        obj = self.mainframe.document.calltip_obj
        # built-in,extension,no source available.
        try:
            filename = inspect.getsourcefile(obj)
        except:
            return 
        if  filename is None:
            return
        else:
            doc = self.mainframe.editctrl.new(filename)
        lnum = None
        try:
            s, lnum = inspect.findsource(obj)
        except:
            pass
        if  lnum:
            del s
            doc.GotoLine(lnum)
            doc.EnsureCaretVisible()
        event.Skip()        

    def canClose(self):
        self.mainframe.panel.showWindow("right",False)
        
        return False