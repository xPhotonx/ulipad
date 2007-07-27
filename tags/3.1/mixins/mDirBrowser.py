#   Programmer: limodou
#   E-mail:     limodou@gmail.coms
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
#   $Id: mDirBrowser.py 176 2005-11-22 02:46:37Z limodou $

from modules import Mixin
import wx
import os.path
from modules import common

menulist = [
    ('IDM_FILE',
    [
        (138, 'IDM_WINDOW_DIRBROWSER', tr('Directory Browser')+'\tF2', wx.ITEM_NORMAL, 'OnWindowDirBrowser', tr('Opens directory browser window.'))
    ]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

popmenulist = [ (None,
    [
        (170, 'IDPM_DIRBROWSERWINDOW', tr('Directory Browser'), wx.ITEM_NORMAL, 'OnDirBrowserWindow', tr('Opens directory browser window.')),
    ]),
]
Mixin.setMixin('notebook', 'popmenulist', popmenulist)

dirbrowser_imagelist = {
	'close':common.unicode_abspath('images/folderclose.gif'),
	'open':common.unicode_abspath('images/folderopen.gif'),
	'item':common.unicode_abspath('images/file.gif'),
}

def afterinit(win):
	win.dirbrowser_imagelist = dirbrowser_imagelist
Mixin.setPlugin('mainframe', 'afterinit', afterinit)

#toollist = [
#	(550, 'dirbrowser'),
#]
#Mixin.setMixin('mainframe', 'toollist', toollist)
#
##order, IDname, imagefile, short text, long text, func
#toolbaritems = {
#	'dirbrowser':(wx.ITEM_NORMAL, 'IDM_WINDOW_DIRBROWSER', images.getWizardBitmap(), tr('dir browser'), tr('Opens directory browser window.'), 'OnWindowDirBrowser'),
#}
#Mixin.setMixin('mainframe', 'toolbaritems', toolbaritems)

def createDirBrowserWindow(win):
    if not win.panel.getPage(tr('Dir Browser')):
        from DirBrowser import DirBrowser

        page = DirBrowser(win.panel.createNotebook('left'), win)
        win.panel.addPage('left', page, tr('Dir Browser'))
Mixin.setMixin('mainframe', 'createDirBrowserWindow', createDirBrowserWindow)

def OnWindowDirBrowser(win, event):
    win.createDirBrowserWindow()
    win.panel.showPage(tr('Dir Browser'))
Mixin.setMixin('mainframe', 'OnWindowDirBrowser', OnWindowDirBrowser)

def OnDirBrowserWindow(win, event):
    win.mainframe.createDirBrowserWindow()
    win.panel.showPage(tr('Dir Browser'))
Mixin.setMixin('notebook', 'OnDirBrowserWindow', OnDirBrowserWindow)

def init(pref):
    pref.recent_dir_paths = []
    pref.recent_dir_paths_num = 10
Mixin.setPlugin('preference', 'init', init)