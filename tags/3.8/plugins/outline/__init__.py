#   Programmer: limodou
#   E-mail:     limodou@gmail.coms
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
#   $Id$

import wx
from modules import Mixin
from modules import common

def add_mainframe_menu(menulist):
    menulist.extend([
        ('IDM_WINDOW',
        [
            (220, 'IDM_WINDOW_OUTLINE', tr('Open Outline Window'), wx.ITEM_NORMAL, 'OnWindowOutline', tr('Opens outline window.'))
        ]),
    ])
Mixin.setPlugin('mainframe', 'add_menu', add_mainframe_menu)

def add_notebook_menu(popmenulist):
    popmenulist.extend([(None,
        [
            (200, 'IDPM_OUTLINEWINDOW', tr('Open Outline Window'), wx.ITEM_NORMAL, 'OnOutlineWindow', tr('Opens outline window.')),
        ]),
    ])
Mixin.setPlugin('notebook', 'add_menu', add_notebook_menu)

def add_images(images):
    images.update({
        'close': 'images/folderclose.png',
        'open': 'images/folderopen.png',
        'item': 'images/file.gif',
        })
Mixin.setPlugin('outline', 'add_images', add_images)

#toollist = [
#   (550, 'outline'),
#]
#Mixin.setMixin('mainframe', 'toollist', toollist)
#
##order, IDname, imagefile, short text, long text, func
#toolbaritems = {
#   'dirbrowser':(wx.ITEM_NORMAL, 'IDM_WINDOW_OUTLINE', images.getWizardBitmap(), tr('outline'), tr('Opens outline window.'), 'OnWindowOutline'),
#}
#Mixin.setMixin('mainframe', 'toolbaritems', toolbaritems)

def createOutlineWindow(win):
    if not win.panel.getPage(tr('Outline')):
        from Outline import OutlineWindow

        page = OutlineWindow(win.panel.createNotebook('left'), win)
        win.panel.addPage('left', page, tr('Outline'))
Mixin.setMixin('mainframe', 'createOutlineWindow', createOutlineWindow)

def OnWindowOutline(win, event):
    win.createShareWindow()
    win.panel.showPage(tr('Outline'))
Mixin.setMixin('mainframe', 'OnWindowOutline', OnWindowOutline)

def OnOutlineWindow(win, event):
    win.mainframe.createOutlineWindow()
    win.panel.showPage(tr('Outline'))
Mixin.setMixin('notebook', 'OnOutlineWindow', OnOutlineWindow)

def close_page(page, name):
    if name == tr('Outline'):
        page.OnCloseWin()
Mixin.setPlugin('notebook', 'close_page', close_page)

def pref_init(pref):
    pref.recent_outlines = []
    pref.recent_outlines_num = 10
Mixin.setPlugin('preference', 'init', pref_init)

def createOutlineEditWindow(win):
    page = win.panel.getPage('Outline Edit')
    if not page:
        page = wx.TextCtrl(win.panel.createNotebook('bottom'), -1, style=wx.TE_MULTILINE)
        win.panel.addPage('bottom', page, 'Outline Edit')
Mixin.setMixin('mainframe', 'createOutlineEditWindow', createOutlineEditWindow)

from OutlinePanel import OutlinePanel

panellist = {'outlineedit':OutlinePanel}
Mixin.setMixin('editctrl', 'panellist', panellist)

def on_modified(win, event):
    if win.documenttype == 'outlineedit':
        outline = win.outline
        outline.update_node(win.outline_node, newcontent=win.GetText())
Mixin.setPlugin('editor', 'on_modified', on_modified)