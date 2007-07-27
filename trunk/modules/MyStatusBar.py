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
#   $Id: MyStatusBar.py 1457 2006-08-23 02:12:12Z limodou $

import wx

class MyStatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, -1)

        if wx.Platform == '__WXMSW__':
            self.SetFieldsCount(6)
            self.SetStatusWidths([-1, 70, 60, 30, 60, 40])
        else:
            self.SetFieldsCount(5)
            self.SetStatusWidths([-1, 70, 60, 40, 60])

        self.g1 = wx.Gauge(self, -1, 100, (1, 3), (105, 16))
        self.g1.SetBezelFace(1)
        self.g1.SetShadowWidth(1)

        self.slashtext = wx.StaticText(self, -1, style=wx.ST_NO_AUTORESIZE)
        self.slashtext.Hide()
        self.active = False

        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.g1.Hide()
        self.autohide = True

    def OnIdle(self, evt):
        if self.autohide:
            if self.g1.GetValue() == 0:
                if self.g1.IsShown():
                    self.g1.Hide()
            else:
                if not self.g1.IsShown():
                    self.g1.Show()

    def show(self, text, color='RED'):
        self.slashtext.SetBackgroundColour(color)
        self.slashtext.SetLabel(text)
        self.slashtext.Show()
        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start(2000)

    def note(self, text):
        self.show(text, color='GREEN')

    def warn(self, text):
        self.show(text)

    def Notify(self):
        wx.CallAfter(self.slashtext.Hide)

    def OnSize(self, evt):
        self.Reposition()  # for normal size events

    def Reposition(self):
        rect = self.GetFieldRect(0)
        self.slashtext.SetPosition((rect.x+1, rect.y+1))
        self.slashtext.SetSize((rect.width-2, rect.height-2))
