#   Programmer: limodou
#   E-mail:     chatme@263.net
#
#   Copyleft 2004 limodou
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
#   $Id: mModuleFile.py 93 2005-10-11 02:51:02Z limodou $

from modules import Mixin
import wx
import wx.stc
import os.path
from modules import common

menulist = [
    ('IDM_VIEW', #parent menu id
    [
        (200, '', '-', wx.ITEM_SEPARATOR, None, ''),
        (210, 'IDM_VIEW_OPEN_MODULE', tr('Open Module File\tE=F6'), wx.ITEM_NORMAL, 'OnViewOpenModuleFile', tr('Open current word as Python module file')),
    ]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

popmenulist = [
    (None, #parent menu id
    [
        (165, 'IDPM_OPEN_MODULE', tr('Open Module File\tF6'), wx.ITEM_NORMAL, 'OnOpenModuleFile', tr('Open current word as Python module file')),
        (166, '', '-', wx.ITEM_SEPARATOR, None, ''),
    ]),
]
Mixin.setMixin('editor', 'popmenulist', popmenulist)

def OnViewOpenModuleFile(win, event):
    openmodulefile(win, getword(win))
Mixin.setMixin('mainframe', 'OnViewOpenModuleFile', OnViewOpenModuleFile)

def OnOpenModuleFile(win, event):
    openmodulefile(win.mainframe, getword(win.mainframe))
Mixin.setMixin('editor', 'OnOpenModuleFile', OnOpenModuleFile)

def openmodulefile(mainframe, module):
    try:
        mod = my_import(module)
        f, ext = os.path.splitext(mod.__file__)
        filename = f + '.py'
        if os.path.exists(filename):
            mainframe.editctrl.new(filename)
    except:
        pass

def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def getword(mainframe):
    pos = mainframe.document.GetCurrentPos()
    start = mainframe.document.WordStartPosition(pos, True)
    end = mainframe.document.WordEndPosition(pos, True)
    if end > start:
        i = start - 1
        while i >= 0:
            if mainframe.document.getChar(i) in mainframe.getWordChars() + '.':
                start -= 1
                i -= 1
            else:
                break
        i = end
        length = mainframe.document.GetLength()
        while i < length:
            if mainframe.document.getChar(i) in mainframe.getWordChars()+ '.':
                end += 1
                i += 1
            else:
                break
    return mainframe.document.GetTextRange(start, end)

def init(win):
	wx.EVT_UPDATE_UI(win, win.IDM_VIEW_OPEN_MODULE, win.OnUpdateUI)
Mixin.setPlugin('mainframe', 'init', init)

def OnUpdateUI(win, event):
	eid = event.GetId()
	if eid == win.IDM_VIEW_OPEN_MODULE:
		event.Enable(win.document.languagename == 'python' and win.document.documenttype == 'edit')
Mixin.setPlugin('mainframe', 'on_update_ui', OnUpdateUI)

def init(win):
	wx.EVT_UPDATE_UI(win, win.IDPM_OPEN_MODULE, win.OnUpdateUI)
Mixin.setPlugin('editor', 'init', init)

def OnUpdateUI(win, event):
	eid = event.GetId()
	if eid == win.IDPM_OPEN_MODULE:
		event.Enable(win.languagename == 'python' and win.documenttype == 'edit')
Mixin.setPlugin('editor', 'on_update_ui', OnUpdateUI)

