#   Programmer:     limodou
#   E-mail:         limodou@gmail.com
#   
#   Copyleft 2006 limodou
#   
#   Distributed under the terms of the GPL (GNU Public License)
#   
#   UliPad is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#   $Id: Calltip.py 2055 2007-04-21 15:53:00Z limodou $
   
import wx
import inspect




        
#class MyCallTip(wx.PopupWindow):
class MyCallTip(wx.PopupTransientWindow):
    def __init__(self, parent):
        #wx.PopupWindow.__init__(self,parent)
        wx.PopupTransientWindow.__init__(self,parent)
        self.parent = parent
        self.scroll_win = wx.ScrolledWindow(self,-1, style=wx.SIMPLE_BORDER |wx.NO_3D)
##        self.scroll_win.EnableScrolling(False, True)
        self.text = wx.StaticText(self.scroll_win, -1, label='')
        self.text_fixed_font = wx.Font(10, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)
        self.text_default_font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
        self.text.Bind(wx.EVT_LEFT_DCLICK, self.open_source_file, id=self.text.GetId())
        self.bgcolor = '#FFFFE1'

        self.active = False
        self.Hide()

    def show(self, pos, text):
        if  self.parent.pref.inputass_calltip_including_source_code:
            self.text.SetFont(self.text_fixed_font)
        else:
            self.text.SetFont(self.text_default_font)
        self.text.SetLabel(text.strip())
        self.active = True
        self.SetBackgroundColour(self.bgcolor)
        self.text.SetBackgroundColour(self.bgcolor)
        self.move(pos)
        self.Show()
        self.parent.SetFocus()
            
    def move(self, pos):    
        cw = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        ch = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)
        dh = self.parent.TextHeight(self.parent.LineFromPosition(pos))
        xx, yy = self.parent.PointFromPosition(pos)
        screen_pos = x,y = self.parent.ClientToScreen((xx, yy))
        w, h = self.text.GetBestSize()
        bar = wx.SystemSettings.GetMetric(wx.SYS_HSCROLL_Y) 
        fw = w
        if  ch - y - dh >ch*0.5:
            fh = ch -y -dh
        else:
            fh = y
        if  fh > h:
            fh = h
        if  w > cw:
            text_width = cw-bar
        elif w == cw:
            text_width = w-bar
        else:
            text_width = w 
        
        self.text.Wrap(text_width)
        self.SetSize((text_width + bar,fh))
        self.scroll_win.SetSize(self.GetClientSize())
        if  h > fh:
            self.scroll_win.SetScrollbars(0, 20, 0, (h+19)/20)
        else:
            self.scroll_win.SetScrollbars(0, 0, 0, 0)
        if y + dh + fh > ch:
            if y - fh>= 0:
                y -= fh
            else:
                y += dh
        else:
            y += dh
        if x + fw > cw:
            x -= fw
            if x < 0:
                x = 0
        self.Move((x, y))
        
    def cancel(self):
        if self.active:
            self.scroll_win.Scroll(0, 0)
            self.Hide()
            self.active = False

    def setHightLight(self, start, end):
        pass

    def open_source_file(self, event):
        self.cancel()
        obj = self.parent.calltip_obj
        # built-in,extension,no source available.
        try:
            filename = inspect.getsourcefile(obj)
        except:
            return 
        if  filename is None:
            return
        else:
            doc = self.parent.mainframe.editctrl.new(filename)
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