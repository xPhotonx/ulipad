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
#   $Id: mWindow.py 1839 2007-01-19 12:15:56Z limodou $

import wx
from modules import Mixin

def add_mainframe_menu(menulist):
    menulist.extend([(None,
        [
            (890, 'IDM_WINDOW', tr('Window'), wx.ITEM_NORMAL, '', ''),
        ]),
        ('IDM_WINDOW',
        [
            (100, 'IDM_WINDOW_LEFT', tr('Left Window')+'\tAlt+Z', wx.ITEM_CHECK, 'OnWindowLeft', tr('Shows or hides the left Window')),
            (110, 'IDM_WINDOW_BOTTOM', tr('Bottom Window'), wx.ITEM_CHECK, 'OnWindowBottom', tr('Shows or hides the bottom Window')),
            (120, '-', '', wx.ITEM_SEPARATOR, '', ''),
            (130, 'IDM_WINDOW_SHELL', tr('Open Shell Window')+'\tAlt+X', wx.ITEM_NORMAL, 'OnWindowShell', tr('Opens shell window.')),
            (140, 'IDM_WINDOW_MESSAGE', tr('Open Messages Window'), wx.ITEM_NORMAL, 'OnWindowMessage', tr('Opens messages window.')),
        ]),
        ('IDM_EDIT',
        [
            (280, '-', '', wx.ITEM_SEPARATOR, '', ''),
            (290, 'IDM_EDIT_CLEARSHELL', tr('Clear Shell Window') + '\tCtrl+Alt+R', wx.ITEM_NORMAL, 'OnEditClearShell', tr('Clears content of shell window.')),
        ]),
    ])
Mixin.setPlugin('mainframe', 'add_menu', add_mainframe_menu)


def OnWindowLeft(win, event):
    flag = not win.panel.LeftIsVisible

#    if flag:
#        win.createSnippetWindow()
#
    win.panel.showWindow('left', flag)
Mixin.setMixin('mainframe', 'OnWindowLeft', OnWindowLeft)

def OnWindowBottom(win, event):
    flag = not win.panel.BottomIsVisible
    if flag:
        win.createShellWindow()
#        win.createMessageWindow()

    win.panel.showWindow('bottom', flag)
    if flag:
        win.panel.showPage(tr('Shell'))
Mixin.setMixin('mainframe', 'OnWindowBottom', OnWindowBottom)

def on_mainframe_updateui(win, event):
    eid = event.GetId()
    if eid == win.IDM_WINDOW_LEFT:
        event.Check(win.panel.LeftIsVisible)
    elif eid == win.IDM_WINDOW_BOTTOM:
        event.Check(win.panel.BottomIsVisible)
Mixin.setPlugin('mainframe', 'on_update_ui', on_mainframe_updateui)

def afterinit(win):
    wx.EVT_UPDATE_UI(win, win.IDM_WINDOW_LEFT, win.OnUpdateUI)
    wx.EVT_UPDATE_UI(win, win.IDM_WINDOW_BOTTOM, win.OnUpdateUI)
    win.messagewindow = None
    win.shellwindow = None
Mixin.setPlugin('mainframe', 'afterinit', afterinit)

def add_tool_list(toollist, toolbaritems):
    toollist.extend([
        (450, 'left'),
        (500, 'bottom'),
    ])

    #order, IDname, imagefile, short text, long text, func
    toolbaritems.update({
        'left':(wx.ITEM_CHECK, 'IDM_WINDOW_LEFT', 'images/left.gif', tr('Toggle Left Window'), tr('Shows or hides the left Window'), 'OnWindowLeft'),
        'bottom':(wx.ITEM_CHECK, 'IDM_WINDOW_BOTTOM', 'images/bottom.gif', tr('Toggle Bottom Window'), tr('Shows or hides the bottom Window'), 'OnWindowBottom'),
    })
Mixin.setPlugin('mainframe', 'add_tool_list', add_tool_list)

def createShellWindow(win):
    if not win.panel.getPage(tr('Shell')):
        from ShellWindow import ShellWindow

        page = ShellWindow(win.panel.createNotebook('bottom'), win)
        win.panel.addPage('bottom', page, tr('Shell'))
    win.shellwindow = win.panel.getPage(tr('Shell'))
Mixin.setMixin('mainframe', 'createShellWindow', createShellWindow)

def createMessageWindow(win):
    if not win.panel.getPage(tr('Messages')):
        from MessageWindow import MessageWindow

        page = MessageWindow(win.panel.createNotebook('bottom'), win)
        win.panel.addPage('bottom', page, tr('Messages'))
    win.messagewindow = win.panel.getPage(tr('Messages'))
Mixin.setMixin('mainframe', 'createMessageWindow', createMessageWindow)

def OnWindowShell(win, event):
    win.createShellWindow()
    win.panel.showPage(tr('Shell'))
Mixin.setMixin('mainframe', 'OnWindowShell', OnWindowShell)

def OnWindowMessage(win, event):
    win.createMessageWindow()
    win.panel.showPage(tr('Messages'))
Mixin.setMixin('mainframe', 'OnWindowMessage', OnWindowMessage)

def add_editor_menu(popmenulist):
    popmenulist.extend([ (None,
        [
            (120, 'IDPM_SHELLWINDOW', tr('Open Shell Window'), wx.ITEM_NORMAL, 'OnShellWindow', tr('Opens shell window.')),
            (130, 'IDPM_MESSAGEWINDOW', tr('Open Messages Window'), wx.ITEM_NORMAL, 'OnMessageWindow', tr('Opens messages window.')),
        ]),
    ])
Mixin.setPlugin('notebook', 'add_menu', add_editor_menu)

def OnShellWindow(win, event):
    win.mainframe.createShellWindow()
    win.panel.showPage(tr('Shell'))
Mixin.setMixin('notebook', 'OnShellWindow', OnShellWindow)

def OnMessageWindow(win, event):
    win.mainframe.createMessageWindow()
    win.panel.showPage(tr('Messages'))
Mixin.setMixin('notebook', 'OnMessageWindow', OnMessageWindow)

def OnEditClearShell(win, event):
    shellwin = win.panel.getPage(tr('Shell'))
    if shellwin:
        shellwin.clear()
        shellwin.prompt()
Mixin.setMixin('mainframe', 'OnEditClearShell', OnEditClearShell)
