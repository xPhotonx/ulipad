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
from modules import Mixin
from modules.Debug import error
from modules import common
from modules import meide as ui

CONFIG_PREFIX = '_config_'

class PrefDialog(wx.Dialog, Mixin.Mixin):
    __mixinname__ = 'prefdialog'

    def __init__(self, parent):
        self.initmixin()

        #config.ini
        self.ini = common.get_config_file_obj()
        
        wx.Dialog.__init__(self, parent, -1, title=tr("Preference..."), size=wx.Size(600, 400), style=wx.DEFAULT_DIALOG_STYLE)

        self.value_set = []

        self.parent = parent
        self.pref = self.parent.pref
        self.default_pref = Preference.Preference()
        
        self.box = box = ui.VBox()
        self.notebook = wx.Notebook(self, -1)
        self.addPages(self.notebook)
        
        box.add(self.notebook, proportion=1, flag=wx.EXPAND|wx.ALL, border=3)

        box.add(ui.simple_buttons(), flag=wx.ALIGN_CENTER|wx.BOTTOM)
        box.bind('btnOk', 'click', self.OnOk)
        
        self.callplugin('initpreference', self)
        ui.create(self, box, 0)
        box.find('btnOk').get_obj().SetDefault()
        
    def addPages(self, notebook):
        pages = []
        for v in self.pref.preflist:
            pagename, order, kind, prefname, message, extern = v
            #add config options process
            prefvalue = None
            if prefname.startswith(CONFIG_PREFIX):
                section, key = prefname[len(CONFIG_PREFIX):].split('_')
                if self.ini.has_key(section) and self.ini[section].has_key(key):
                    prefvalue = self.ini[section][key]
            else:
                prefvalue = getattr(self.parent.pref, prefname, prefvalue)
            if pages.count(pagename)==0:
                page = wx.ScrolledWindow(notebook, -1)
                page.EnableScrolling(False, True)
                page.SetScrollbars(10, 10, 30, 30)
                notebook.AddPage(page, pagename)
                pages.append(pagename)
                page.box = ui.SimpleGrid().create(page).auto_layout()
                self.value_set.append(page.box)
            else:
                page = notebook.GetPage(pages.index(pagename))
            value = self.validate(prefname, kind, prefvalue)
            self.addItem(page, kind, prefname, prefvalue, message, extern)

    def addItem(self, page, kind, prefname, prefvalue, message, extern):
        if self.execplugin("additem", self, page, kind, prefname, prefvalue, message, extern):
            return
        
        obj = None
        label = message
        kwargs = None
        if not isinstance(kind, str):
            obj = kind
            kwargs = extern
        else:
            if kind == 'check':
                obj = ui.Check(prefvalue, label=message)
                label = ''
            elif kind == 'num':
                obj = ui.IntSpin(prefvalue, max=100000, min=1, size=(60, -1))
            elif kind == 'int':
                obj = ui.Int(prefvalue)
            elif kind == 'choice':
                obj = ui.SingleChoice(prefvalue, choices=extern)
            elif kind == 'text':
                obj = ui.Text(prefvalue)
            elif kind == 'password':
                obj = ui.Password(prefvalue)
            elif kind == 'openfile':
                obj = ui.OpenFile(prefvalue)
            elif kind == 'button':
                label = ''
                func = getattr(self, extern)
                obj = ui.Button(message).bind('click', func)
                
        if not kwargs:
            if label:
                span = False
            else:
                span = True
            page.box.add(label, obj, name=prefname, span=span)
        else:
            page.box.add(label, obj, name=prefname, **kwargs)

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

    def OnOk(self, event):
        values = {}
        config = []
        for b in self.value_set:
            values.update(b.GetValue())
        for name, v in values.items():
            #if a name starts with CONFIG_PREFIX, so this value should be saved
            #in config.ini file, but not preference file
            if name.startswith(CONFIG_PREFIX):
                config.append((name, v))
            else:
                setattr(self.parent.pref, name, v)
        self.parent.pref.save()
        
        #process config options
        for name, v in config:
            section, key = name[len(CONFIG_PREFIX):].split('_')
            self.ini[section][key] = v
        self.ini.save()

        #self.parent = mainframe
        self.callplugin('savepreference', self.parent, self.parent.pref)
        event.Skip()
