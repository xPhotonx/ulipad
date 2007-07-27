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
#   $Id$

import wx
from modules import Mixin

def add_mainframe_menu(menulist):
    menulist.extend([('IDM_WINDOW', #parent menu id
        [
            (210, 'IDM_WINDOW_TODO', tr('Open TODO Window')+u'\tCtrl+T', wx.ITEM_NORMAL, 'OnWindowTODO', tr('Open the TODO window.')),
        ]),
    ])
Mixin.setPlugin('mainframe', 'add_menu', add_mainframe_menu)

def add_notebook_menu(popmenulist):
    popmenulist.extend([ (None,
        [
            (190, 'IDPM_TODOWINDOW', tr('Open TODO Window'), wx.ITEM_NORMAL, 'OnNTodoWindow', tr('Opens the TODO window.')),
        ]),
    ])
Mixin.setPlugin('notebook', 'add_menu', add_notebook_menu)

def pref_init(pref):
    pref.auto_todo = True
Mixin.setPlugin('preference', 'init', pref_init)

def add_pref(preflist):
    preflist.extend([
        (tr('Document'), 270, 'check', 'auto_todo', tr('Auto show TODO window if TODO window already opened.'), None),
    ])
Mixin.setPlugin('preference', 'add_pref', add_pref)

def createtodowindow(win):
    if not win.panel.getPage(tr('TODO')):
        from TodoWindow import TodoWindow

        page = TodoWindow(win.panel.createNotebook('bottom'), win)
        win.panel.addPage('bottom', page, tr('TODO'))
    win.todowindow = win.panel.getPage(tr('TODO'))
Mixin.setMixin('mainframe', 'createtodowindow', createtodowindow)

def OnWindowTODO(win, event):
    win.createtodowindow()
    win.panel.showPage(tr('TODO'))
    win.todowindow.show(win.document)
Mixin.setMixin('mainframe', 'OnWindowTODO', OnWindowTODO)

def OnNTodoWindow(win, event):
    win.mainframe.createtodowindow()
    win.showPage(tr('TODO'))
    win.mainframe.todowindow.show(win.mainframe.document)
Mixin.setMixin('notebook', 'OnNTodoWindow', OnNTodoWindow)

def aftersavefile(win, filename):
    if win.mainframe.panel.getPage(tr('TODO')):
        win.mainframe.todowindow.show(win)
Mixin.setPlugin('editor', 'aftersavefile', aftersavefile)

def on_document_enter(win, editor):
    if win.pref.auto_todo and win.mainframe.panel.getPage(tr('TODO')):
        win.mainframe.todowindow.show(win.document)
Mixin.setPlugin('editctrl', 'on_document_enter', on_document_enter)
