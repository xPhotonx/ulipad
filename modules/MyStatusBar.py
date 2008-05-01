#   Programmer: limodou
#   E-mail:     limodou@gmail.com
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
#   $Id: MyStatusBar.py 1736 2006-11-27 13:01:19Z limodou $
import wx
import wx.stc
import common





class Vim_pad(wx.stc.StyledTextCtrl):
    def __init__(self, parent, id=-1):
        wx.stc.StyledTextCtrl.__init__(self, parent, id,style = wx.FULL_REPAINT_ON_RESIZE
##                    |wx.ST_NO_AUTORESIZE
                    |wx.NO_BORDER)

        self.SetMarginWidth(0,0)
        self.SetMarginWidth(1,0)
        self.SetMarginWidth(2,0)
        self.MarkerDefine(0,wx.stc.STC_MARK_ARROWS,'red','grey')
##        self.CmdKeyExecute(wx.stc.STC_CMD_NEWLINE)
        self.MarkerAdd(0, 0)
        if wx.Platform == '__WXMSW__':
            self.faces = { 'times': 'Courier New',
                      'mono' : 'Courier New',
                      'helv' : 'Courier New',
                      'other': 'Courier New',
                      'size' : 12.5,
                      'size2': 11,
                     }
        elif  wx.Platform == '__WXMAC__':
            self.faces = { 'times': 'Times',
                      'mono' : 'Courier',
                      'helv' : 'Courier',
                      'other': 'Courier',
                      'size' : 12,
                      'size2': 10,
                     }
        else:
            self.faces = { 'times': 'Times',
                      'mono' : 'Courier',
                      'helv' : 'Courier',
                      'other': 'Courier',
                      'size' : 10,
                      'size2': 10,
                     }

        self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,
                          "face:%(mono)s,size:%(size)d" % self.faces)








class MyStatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, -1)
        if wx.Platform == '__WXGTK__':
            imgWidth = 21
        else:
            imgWidth = 16
        temp = ['icon:%d' % imgWidth, 'status:-1', 'line:60', 'col:60', 'eolmode:40', 'coding:86',
                # 'progress:86',
                #'vim_pad:180',
                ]
        temp1 = [x.split(':')[0] for x in temp]
        stbar_widths = [int(x.split(':')[1]) for x in temp]
        t = enumerate(temp1)
        count = len(temp)
        self.sbpos = dict([(x[1],x[0]) for x in t])
        if wx.Platform == '__WXMSW__':
            self.SetFieldsCount(count)
            self.SetStatusWidths(stbar_widths)
        elif wx.Platform == '__WXGTK__':
            self.SetFieldsCount(count)
            self.SetStatusWidths(stbar_widths)
        else:
            self.SetFieldsCount(count)
            self.SetStatusWidths(stbar_widths)
        self.slashtext = wx.StaticText(self, -1, style=wx.ST_NO_AUTORESIZE)
        self.slashtext.Hide()
        self.vim_pad = Vim_pad(self, -1)
        self.vim_pad.Hide()
        self.g1 = wx.Gauge(self, -1, 100, (1, 3), (105, 16))
        self.g1.SetBezelFace(1)
        self.g1.SetShadowWidth(1)
        self.linkProgressToStatusBar()

        rect = self.GetFieldRect(self.sbpos['icon'])
        self.img = wx.StaticBitmap(self, -1,
            common.getpngimage('images/Info.png'),
            (rect.x+1, rect.y+1), (16, 16))

#        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.g1.Hide()
        self.images = {'Info': common.getpngimage('Images/Info.png'),
                       'Warning': common.getpngimage('Images/Warning.png'),
                       'Error': common.getpngimage('Images/Error.png')}

        self.autohide = True
        self.showing = False
        self.active = False
        self.text = ''

    def OnIdle(self, evt):
        if self.autohide:
            if self.g1.GetValue() == 0:
                if self.g1.IsShown():
                    self.g1.Hide()
            else:
                if not self.g1.IsShown():
                    self.g1.Show()

    def show_panel(self, text, color='RED', font=None):
        self.slashtext.SetBackgroundColour(color)
        if font:
            self.slashtext.SetFont(font)
        self.slashtext.SetLabel(text)
        self.slashtext.Show()

    def note(self, text):
        if not self.showing:
            self.showing = True
            wx.CallAfter(self.show_panel, text, color='GREEN')
            wx.FutureCall(2000, self.Notify)

    def warn(self, text):
        if not self.showing:
            self.showing = True
            wx.CallAfter(self.show_panel, text)
            wx.FutureCall(2000, self.Notify)

    def hide_panel(self):
        wx.CallAfter(self.slashtext.Hide)

    def Notify(self):
        def f():
            self.slashtext.Hide()
            self.showing = False
        wx.CallAfter(f)

    def OnSize(self, evt):
        self.Reposition()  # for normal size events

    def Reposition(self):
        rect = self.GetFieldRect(self.sbpos['icon'])
        self.img.SetPosition((rect.x+1, rect.y+1))
        self.img.SetSize((16, 16))
        rect = self.GetFieldRect(self.sbpos['status'])
        self.slashtext.SetPosition((rect.x+1, rect.y+1))
        self.slashtext.SetSize((rect.width-2, rect.height-2))
        rect = self.GetFieldRect(self.sbpos['status'])
        self.vim_pad.SetPosition((rect.x+1, rect.y+1))
        self.vim_pad.SetSize((rect.width - 2, rect.height +  2))
        rect = self.GetFieldRect(self.sbpos['coding'])
##        self.g1.SetPosition((rect.x+1, rect.y+1))
        self.g1.SetDimensions(rect.x+1, rect.y+1, rect.width -2, rect.height -2)

    def linkProgressToStatusBar(self):
        rect = self.GetFieldRect(self.sbpos['coding'])
##        self.g1.SetPosition((rect.x+1, rect.y+1))
        self.g1.SetDimensions(rect.x+1, rect.y+1, rect.width -2, rect.height -2)

    def SetStatusText(self,text, type='status'):
        if type == 'status':
            self.text = text
        pos = self.sbpos.get(type)
        if pos:
            wx.StatusBar.SetStatusText(self, text, pos)

    def setHint(self, hint, msgType='Info', ringBell=False):
        """ Show a status message in the statusbar, optionally rings a bell.

        msgType can be 'Info', 'Warning' or 'Error'
        """
        if not self.images:
            return
        #self.SetStatusText(hint, 'status')
        wx.StatusBar.SetStatusText(self, hint, self.sbpos['status'])
        self.img.SetToolTipString(hint)
        self.img.SetBitmap(self.images[msgType])
        if ringBell: wx.Bell()
