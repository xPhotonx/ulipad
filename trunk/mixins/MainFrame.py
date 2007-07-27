#coding=utf-8
#   Programmer: limodou
#   E-mail:     limodou@gmail.com
#
#   Copyleft 2006 limodou
#
#   Distributed under the terms of the GPL (GNU Public License)
#
#   NewEdit is free software; you can redistribute it and/or modify
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
#   $Id: MainFrame.py 501 2006-01-18 08:00:32Z limodou $

import wx
import copy
#import locale
from modules import Mixin
from modules import makemenu
from modules import Accelerator
from modules import MyStatusBar
#from modules import common

class MainFrame(wx.Frame, Mixin.Mixin):

    __mixinname__ = 'mainframe'
    menulist = [ (None, #parent menu id
        [
            (100, 'IDM_FILE', tr('File'), wx.ITEM_NORMAL, None, ''),
            (900, 'IDM_HELP', tr('Help'), wx.ITEM_NORMAL, None, ''),
        ]),
        ('IDM_FILE',
        [
            (900, '', '-', wx.ITEM_SEPARATOR, None, ''),
            (910, 'IDM_FILE_EXIT', tr('Exit\tAlt+X'),wx. ITEM_NORMAL, 'OnExit', tr('Exit Program')),
        ]),
    ]
    accellist = {}
    default_accellist = {}
    editoraccellist = {}
    default_editoraccellist = {}
    imagelist = {}
    filewildchar = [
        tr('All files (*.*)|*'),
    ]
    toollist = []
    toolbaritems = {}
    filenewtypes = []

    def __init__(self, app, filenames):
        self.initmixin()
        self.app = app
        self.pref = app.pref
        self.filenames = filenames

        self.callplugin_once('start', self)

        wx.Frame.__init__(self, None, -1, self.app.appname, size=wx.Size(600, 400), name=self.app.appname)

        #@add_menu menulist
        self.callplugin_once('add_menu', MainFrame.menulist)
        #@add_menu_image_list
        self.callplugin_once('add_menu_image_list', MainFrame.imagelist)
        #@add_filewildchar filewildchar
        self.callplugin_once('add_filewildchar', MainFrame.filewildchar)
        #@add_tool_list
        self.callplugin_once('add_tool_list', MainFrame.toollist, MainFrame.toolbaritems)
        #@add_new_files
        self.callplugin_once('add_new_files', MainFrame.filenewtypes)
        
        self.id = self.GetId()
        self.menubar=makemenu.makemenu(self, self.menulist, MainFrame.accellist, MainFrame.editoraccellist, MainFrame.imagelist)
        self.SetMenuBar(self.menubar)

        a = {}
        self.callplugin_once('init_accelerator', self, MainFrame.accellist, MainFrame.editoraccellist)
        a.update(MainFrame.accellist)
        a.update(MainFrame.editoraccellist)
        MainFrame.default_accellist = copy.deepcopy(MainFrame.accellist)
        MainFrame.default_editoraccellist = copy.deepcopy(MainFrame.editoraccellist)

        self.editorkeycodes = {}
        Accelerator.getkeycodes(self.editoraccellist, self.editorkeycodes)

        makemenu.setmenutext(self, a)
        Accelerator.initaccelerator(self, MainFrame.accellist)

        self.statusbar = MyStatusBar.MyStatusBar(self)
        self.SetStatusBar(self.statusbar)
        self.progressbar = self.statusbar.g1

        self.callplugin('beforeinit', self)
        self.callplugin('init', self)
        self.callplugin('show', self)
        wx.EVT_IDLE(self, self.OnIdle)
        wx.EVT_CLOSE(self, self.OnClose)
        
    def afterinit(self):
        self.callplugin('afterinit', self)

    def OnExit(self, event):
#        self.callplugin('on_close', self)
        self.Close()

    def OnUpdateUI(self, event):
        self.callplugin('on_update_ui', self, event)

    def OnIdle(self, event):
        if wx.Platform == '__WXMSW__':
            self.SetStatusText("%dM" % (wx.GetFreeMemory()/1024/1024), 5)
        self.callplugin('on_idle', self, event)
        
    def OnClose(self, event):
        if not self.execplugin('on_close', self, event):
            self.callplugin('afterclosewindow', self)
            event.Skip()
        
    def removeAccel(self):
        MainFrame.accellist = copy.deepcopy(MainFrame.default_accellist)
        MainFrame.editoraccellist = copy.deepcopy(MainFrame.default_editoraccellist)
        self.editorkeycodes = {}
        Accelerator.getkeycodes(self.editoraccellist, self.editorkeycodes)
        Accelerator.initaccelerator(self, MainFrame.accellist)

    def insertAccel(self, accel, editoraccel):
        MainFrame.accellist.update(accel)
        MainFrame.editoraccellist.update(editoraccel)
        self.editorkeycodes = {}
        Accelerator.getkeycodes(self.editoraccellist, self.editorkeycodes)
        Accelerator.initaccelerator(self, MainFrame.accellist)
        