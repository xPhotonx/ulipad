#   Programmer: limodou
#   E-mail:     limodou@gmail.coms
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
#   $Id: mDirBrowser.py 184 2005-11-23 14:16:08Z limodou $

import wx
from modules import Mixin

def add_mainframe_menu(menulist):
    menulist.extend([
        ('IDM_WINDOW',
        [
            (200, 'IDM_WINDOW_SHARE', tr('Open Share Resouce Window'), wx.ITEM_NORMAL, 'OnWindowShare', tr('Opens share resouce window.'))
        ]),
    ])
Mixin.setPlugin('mainframe', 'add_menu', add_mainframe_menu)

def add_notebook_menu(popmenulist):
    popmenulist.extend([(None,
        [
            (180, 'IDPM_SHAREWINDOW', tr('Open Share Resouce Window'), wx.ITEM_NORMAL, 'OnShareWindow', tr('Opens share resouce window.')),
        ]),
    ])
Mixin.setPlugin('notebook', 'add_menu', add_notebook_menu)

def afterinit(win):
    win.share_imagelist = {
        'close':'images/folderclose.gif',
        'open':'images/folderopen.gif',
        'item':'images/file.gif',
    }
Mixin.setPlugin('mainframe', 'afterinit', afterinit)

#toollist = [
#   (550, 'dirbrowser'),
#]
#Mixin.setMixin('mainframe', 'toollist', toollist)
#
##order, IDname, imagefile, short text, long text, func
#toolbaritems = {
#   'dirbrowser':(wx.ITEM_NORMAL, 'IDM_WINDOW_DIRBROWSER', images.getWizardBitmap(), tr('dir browser'), tr('Opens directory browser window.'), 'OnWindowDirBrowser'),
#}
#Mixin.setMixin('mainframe', 'toolbaritems', toolbaritems)

def createShareWindow(win):
    if not win.panel.getPage(tr('Share Resouce')):
        from ShareWindow import ShareWindow

        page = ShareWindow(win.panel.createNotebook('left'), win)
        win.panel.addPage('left', page, tr('Share Resouce'))
Mixin.setMixin('mainframe', 'createShareWindow', createShareWindow)

def OnWindowShare(win, event):
    win.createShareWindow()
    win.panel.showPage(tr('Share Resouce'))
Mixin.setMixin('mainframe', 'OnWindowShare', OnWindowShare)

def OnShareWindow(win, event):
    win.mainframe.createShareWindow()
    win.panel.showPage(tr('Share Resouce'))
Mixin.setMixin('notebook', 'OnShareWindow', OnShareWindow)

def close_page(page, name):
    if name == tr('Share Resouce'):
        page.OnCloseWin()
Mixin.setPlugin('notebook', 'close_page', close_page)
