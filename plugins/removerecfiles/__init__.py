#	Programmer:	tianyu263
#	E-mail:		tianyu263@163.com
#
#	Copyleft 2004 tianyu263
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
#	$Id: RemoveAllRecentFiles.py,v 1.0 2004/10/16 08:05:28 tianyu Studio WorkShop $
__doc__	= 'Plugin: Remove All Recent Files'

from modules import	Mixin
import wx
import os
import os.path
import sys
from modules import	makemenu


menulist = [('IDM_FILE_RECENTFILES', #parent menu id
	[
		(105, 'IDM_REMOVE_RECENTFILES',	tr('Remove All Recent Files'), wx.ITEM_NORMAL, 'OnDelRecentMenus', tr('Remove All Recent Files.')),
		(106, '', '-', wx.ITEM_SEPARATOR, None,	''),
	]),
]

Mixin.setMixin('mainframe',	'menulist',	menulist)

def	del_recent_menu(win):
	menu=makemenu.findmenu(win.menuitems, 'IDM_FILE_RECENTFILES')

	id=wx.NewId()
	win.recentmenu_ids.append(id)
	menu.Append(id,tr('Remove All Recent Files'))
	wx.EVT_MENU(win,id,win.OnDelRecentMenus)

	wmi	= menu.AppendSeparator()
	win.recentmenu_ids.append(wmi.GetId());

###########################
# add by tianyu
###########################
def	OnDelRecentMenus(win, event):
	menu=makemenu.findmenu(win.menuitems, 'IDM_FILE_RECENTFILES')
	for	id in win.recentmenu_ids:
		menu.Delete(id)
	win.recentmenu_ids = []

	fileCount =	len(win.pref.recent_files)
	for	i in range(0,fileCount):
		del	win.pref.recent_files[0]
	win.pref.recent_files=[]

#	id=wx.NewId()
#	win.recentmenu_ids.append(id)
#	menu.Append(id,tr('Remove All Recent Files'))
#	wx.EVT_MENU(win,id,win.OnDelRecentMenus)

#	wmi	= menu.AppendSeparator()
#	win.recentmenu_ids.append(wmi.GetId());

	id = win.IDM_FILE_RECENTFILES_ITEMS
	menu.Append(id,	tr('(empty)'))
	menu.Enable(id,	False)
	win.recentmenu_ids.append(id)

Mixin.setMixin('mainframe',	'OnDelRecentMenus',	OnDelRecentMenus)
###########################
##	tianyu add over
###########################