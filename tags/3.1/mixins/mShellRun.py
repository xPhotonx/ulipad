#	Programmer:	limodou
#	E-mail:		chatme@263.net
#
#	Copyleft 2004 limodou
#
#	Distributed under the terms of the GPL (GNU Public License)
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
#	$Id: mShellRun.py 176 2005-11-22 02:46:37Z limodou $

__doc__ = 'run shell command'

from modules import Mixin
import wx
from modules import makemenu
import sys
import os.path
import wx.lib.dialogs
import traceback
from modules import Entry

def init(pref):
	pref.shells = []
Mixin.setPlugin('preference', 'init', init)

menulist = [('IDM_TOOL',
	[
		(100, 'IDM_SHELL', tr('Shell Command'), wx.ITEM_NORMAL, None, ''),
	]),
	('IDM_SHELL', #parent menu id
	[
		(100, 'IDM_SHELL_MANAGE', tr('Shell Command Manage...'), wx.ITEM_NORMAL, 'OnShellManage', tr('Shell command manage')),
		(110, '', '-', wx.ITEM_SEPARATOR, None, ''),
		(120, 'IDM_SHELL_ITEMS', tr('(empty)'), wx.ITEM_NORMAL, 'OnShellItems', tr('Execute an shell command')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

def OnShellManage(win, event):
	from ShellDialog import ShellDialog

	dlg = ShellDialog(win, win.pref)
	answer = dlg.ShowModal()
	if answer == wx.ID_OK:
		makeshellmenu(win, win.pref)
Mixin.setMixin('mainframe', 'OnShellManage', OnShellManage)

def beforeinit(win):
	win.shellmenu_ids=[win.IDM_SHELL_ITEMS]
	makeshellmenu(win, win.pref)
Mixin.setPlugin('mainframe', 'beforeinit', beforeinit)

def makeshellmenu(win, pref):
	menu = makemenu.findmenu(win.menuitems, 'IDM_SHELL')

	for id in win.shellmenu_ids:
		menu.Delete(id)

	win.shellmenu_ids = []
	if len(win.pref.shells) == 0:
		id = win.IDM_SHELL_ITEMS
		menu.Append(id, tr('(empty)'))
		menu.Enable(id, False)
		win.shellmenu_ids=[id]
	else:
		for description, filename in win.pref.shells:
			id = wx.NewId()
			win.shellmenu_ids.append(id)
			menu.Append(id, description)
			wx.EVT_MENU(win, id, win.OnShellItems)

def OnShellItems(win, event):
	win.createMessageWindow()

	eid = event.GetId()
	index = win.shellmenu_ids.index(eid)
	command = win.pref.shells[index][1]
	command = command.replace('$path', os.path.dirname(win.document.filename))
	command = command.replace('$file', win.document.filename)
	wx.Execute(command)
Mixin.setMixin('mainframe', 'OnShellItems', OnShellItems)