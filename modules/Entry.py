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
#   $Id: Entry.py 1783 2006-12-20 13:33:46Z limodou $

import wx

class MyTextEntry(wx.Dialog):
    def __init__(self, parent, title, message, defaultvalue):
        wx.Dialog.__init__(self, parent, -1, style = wx.DEFAULT_DIALOG_STYLE, title = title)

        box = wx.BoxSizer(wx.VERTICAL)
        stext = wx.StaticText(self, -1, label=message)
        box.Add(stext, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        self.text = wx.TextCtrl(self, -1, defaultvalue)
        self.text.SetSelection(-1, -1)
        box.Add(self.text, 1, wx.EXPAND|wx.ALL, 5)
        box2 = wx.BoxSizer(wx.HORIZONTAL)
        btnOK = wx.Button(self, wx.ID_OK, tr("OK"))
        btnOK.SetDefault()
        box2.Add(btnOK, 0, wx.ALIGN_RIGHT|wx.RIGHT, 5)
        btnCancel = wx.Button(self, wx.ID_CANCEL, tr("Cancel"))
        box2.Add(btnCancel, 0, wx.ALIGN_LEFT|wx.LEFT, 5)
        box.Add(box2, 0, wx.ALIGN_CENTER|wx.BOTTOM, 5)

        self.SetSizer(box)
        self.SetAutoLayout(True)

        box.Fit(self)

        self.value = defaultvalue

    def GetValue(self):
        return self.text.GetValue()

class MyFileEntry(wx.Dialog):
    def __init__(self, parent, title, message, defaultvalue):
        wx.Dialog.__init__(self, parent, -1, style = wx.DEFAULT_DIALOG_STYLE, title = title)

        box = wx.BoxSizer(wx.VERTICAL)
        stext = wx.StaticText(self, -1, label=message)
        box.Add(stext, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        self.text = wx.TextCtrl(self, -1, defaultvalue)
        self.text.SetSelection(-1, -1)
        box1.Add(self.text, 1, wx.EXPAND|wx.ALL, 5)
        self.ID_BROWSER = wx.NewId()
        self.btnBrowser = wx.Button(self, self.ID_BROWSER, tr("Browser"), size=(50, -1))
        box1.Add(self.btnBrowser, 0, wx.ALL, 5)
        box.Add(box1, 1, wx.EXPAND, 5)
        box2 = wx.BoxSizer(wx.HORIZONTAL)
        btnOK = wx.Button(self, wx.ID_OK, tr("OK"))
        btnOK.SetDefault()
        box2.Add(btnOK, 0, wx.ALIGN_RIGHT|wx.RIGHT, 5)
        btnCancel = wx.Button(self, wx.ID_CANCEL, tr("Cancel"))
        box2.Add(btnCancel, 0, wx.ALIGN_LEFT|wx.LEFT, 5)
        box.Add(box2, 0, wx.ALIGN_CENTER|wx.BOTTOM, 5)

        wx.EVT_BUTTON(self.btnBrowser, self.ID_BROWSER, self.OnBrowser)

        self.SetSizer(box)
        self.SetAutoLayout(True)
        box.Fit(self)

        self.value = defaultvalue

    def GetValue(self):
        return self.text.GetValue()

    def OnBrowser(self, event):
        dlg = wx.FileDialog(self, tr("Select A File"), "", "", tr("All file (*.*)|*.*"), wx.OPEN|wx.HIDE_READONLY)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            self.text.SetValue('%s' % filename)
