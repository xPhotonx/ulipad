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
#   $Id: PrefDialog.py 1886 2007-02-01 12:58:18Z limodou $

import wx
import Preference
import types
from modules import Mixin
from modules.Debug import error

class PrefDialog(wx.Dialog, Mixin.Mixin):
    __mixinname__ = 'prefdialog'

    def __init__(self, parent):
        self.initmixin()

        wx.Dialog.__init__(self, parent, -1, title=tr("Preference..."), size=wx.Size(600, 400), style=wx.DEFAULT_DIALOG_STYLE)

        self.items = {}

        self.parent = parent
        self.pref = self.parent.pref
        self.default_pref = Preference.Preference()
        self.box1 = wx.BoxSizer(wx.VERTICAL)
        self.notebook = wx.Notebook(self, -1)
        self.addPages(self.notebook)
        self.box1.Add(self.notebook, 1, wx.EXPAND|wx.ALL, 3)

        self.box2 = wx.BoxSizer(wx.HORIZONTAL)

        self.btnok = wx.Button(self, wx.ID_OK, tr("OK"))
        self.btnok.SetDefault()
        self.box2.Add(self.btnok, 0, wx.ALIGN_CENTRE|wx.ALL, 3)
        self.btncancel = wx.Button(self, wx.ID_CANCEL, tr("Cancel"))
        self.box2.Add(self.btncancel, 0, wx.ALIGN_CENTRE|wx.ALL, 3)

        self.box1.Add(self.box2, 0, wx.ALIGN_CENTER|wx.ALL, 3)

        self.SetSizer(self.box1)
        self.SetAutoLayout(True)
        wx.EVT_BUTTON(self, wx.ID_OK, self.OnOk)

        self.callplugin('initpreference', self)

    def addPages(self, notebook):
        pages = []
        for v in self.pref.preflist:
            pagename, order, kind, prefname, message, extern = v
            if not hasattr(self.pref, prefname):
                prefvalue = None
            else:
                prefvalue = getattr(self.parent.pref, prefname)
            if pages.count(pagename)==0:
#                               page = wx.Panel(notebook, -1)
                page = wx.ScrolledWindow(notebook, -1)
                page.EnableScrolling(False, True)
                page.SetScrollbars(10, 10, 30, 30)
                notebook.AddPage(page, pagename)
                pages.append(pagename)
                page.box = wx.BoxSizer(wx.VERTICAL)
                page.SetSizer(page.box)
                page.SetAutoLayout(True)
            else:
                page = notebook.GetPage(pages.index(pagename))
            value = self.validate(prefname, kind, prefvalue)
            self.addItem(page, kind, prefname, prefvalue, message, extern)

    def addItem(self, page, kind, prefname, prefvalue, message, extern):
        if self.execplugin("additem", self, page, kind, prefname, prefvalue, message, extern):
            return
        if kind == 'check':
            obj = wx.CheckBox(page, -1, message)
            obj.SetValue(prefvalue)
            self.items[prefname] = (obj, obj.GetValue)
        elif kind == 'num':
            obj = wx.BoxSizer(wx.HORIZONTAL)
            obj.Add(wx.StaticText(page, -1, message), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 10)
            nc = wx.SpinCtrl(page, min=1, max=100000, size=(60, 22))
            nc.SetValue(prefvalue)
            obj.Add(nc, 0)
            self.items[prefname] = (nc, nc.GetValue)
        elif kind == 'int':
            obj = wx.BoxSizer(wx.HORIZONTAL)
            obj.Add(wx.StaticText(page, -1, message), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 10)
            from wx.lib.intctrl import IntCtrl
            nc = IntCtrl(page)
            nc.SetValue(prefvalue)
            obj.Add(nc, 0)
            self.items[prefname] = (nc, nc.GetValue)
        elif kind == 'choice':
            obj = wx.BoxSizer(wx.HORIZONTAL)
            obj.Add(wx.StaticText(page, -1, message), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 10)
            cb = wx.ComboBox(page, -1, '', choices = extern, style = wx.CB_DROPDOWN|wx.CB_READONLY )
            obj.Add(cb, 0)
            if types.IntType == type(prefvalue):
                cb.SetSelection(prefvalue)
                self.items[prefname] = (cb, cb.GetSelection)
            else:
                cb.SetValue(prefvalue)
                self.items[prefname] = (cb, cb.GetValue)
        elif kind == 'text':
            obj = wx.BoxSizer(wx.HORIZONTAL)
            obj.Add(wx.StaticText(page, -1, message), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 10)
            tc = wx.TextCtrl(page, -1, prefvalue)
            obj.Add(tc, 0)
            self.items[prefname] = (tc, tc.GetValue)
        elif kind == 'password':
            obj = wx.BoxSizer(wx.HORIZONTAL)
            obj.Add(wx.StaticText(page, -1, message), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 10)
            tc = wx.TextCtrl(page, -1, prefvalue, style=wx.TE_PASSWORD)
            obj.Add(tc, 0)
            self.items[prefname] = (tc, tc.GetValue)
        elif kind == 'button':
            #message is button's label
            #extern is button event handler function
            button_id = wx.NewId()
            obj = wx.Button(page, button_id, message)
            func = getattr(self, extern)
            wx.EVT_BUTTON(obj, button_id, func)
        page.box.Add(obj, 0, wx.LEFT|wx.TOP|wx.RIGHT, 5)

    def validate(self, name, kind, value):
        if kind == 'check':
            return bool(value)
        elif kind == 'num' or kind == 'int':
            try:
                value = int(value)
            except:
                error.traceback()
                error.info((name, kind, value))
                return getattr(self.default_pref, name)
        else:
            return value

    def getObj(self, name):
        v = self.items[name]
        return v[0]

    def OnOk(self, event):
        for name, v in self.items.items():
            obj, func = v
            setattr(self.parent.pref, name, func())
        self.parent.pref.save()

        #self.parent = mainframe
        self.callplugin('savepreference', self.parent, self.parent.pref)
        event.Skip()
