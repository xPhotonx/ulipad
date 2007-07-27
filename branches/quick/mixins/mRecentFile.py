#	Programmer:	limodou
#	E-mail:		limodou@gmail.com
#
#	Copyleft 2006 limodou
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
#	$Id: mRecentFile.py 475 2006-01-16 09:50:28Z limodou $

import wx
import os
from modules import Mixin
from modules import makemenu
from modules import common

def add_mainframe_menu(menulist):
    menulist.extend([('IDM_FILE',
        [
            (130, 'IDM_FILE_RECENTFILES', tr('Open Recent File'), wx.ITEM_NORMAL, None, ''),
            (135, 'IDM_FILE_RECENTPATHS', tr('Open Recent Path'), wx.ITEM_NORMAL, None, ''),
        ]),
        ('IDM_FILE_RECENTFILES',
        [
            (100, 'IDM_FILE_RECENTFILES_ITEMS', tr('(empty)'), wx.ITEM_NORMAL, 'OnOpenRecentFiles', ''),
        ]),
        ('IDM_FILE_RECENTPATHS',
        [
            (100, 'IDM_FILE_RECENTPATHS_ITEMS', tr('(empty)'), wx.ITEM_NORMAL, 'OnOpenRecentPaths', ''),
        ]),
    ])
Mixin.setPlugin('mainframe', 'add_menu', add_mainframe_menu)

def beforeinit(win):
	win.recentmenu_ids = [win.IDM_FILE_RECENTFILES_ITEMS]
	win.recentpathmenu_ids = [win.IDM_FILE_RECENTPATHS_ITEMS]
	create_recent_menu(win)
	create_recent_path_menu(win)
Mixin.setPlugin('mainframe', 'beforeinit', beforeinit)

def add_pref(preflist):
    preflist.extend([
        (tr('General'), 100, 'num', 'recent_files_num', tr('Max number of recent files:'), None),
        (tr('General'), 110, 'num', 'recent_paths_num', tr('Max number of recent paths:'), None),
    ])
Mixin.setPlugin('preference', 'add_pref', add_pref)

def pref_init(pref):
	pref.recent_files = []
	pref.recent_files_num = 10
	pref.recent_paths = []
	pref.recent_paths_num = 10
Mixin.setPlugin('preference', 'init', pref_init)

def afteropenfile(win, filename):
	if filename:
		#deal recent files
		if filename in win.pref.recent_files:
			win.pref.recent_files.remove(filename)
		win.pref.recent_files.insert(0, filename)
		win.pref.recent_files = win.pref.recent_files[:win.pref.recent_files_num]
		win.pref.last_dir = os.path.dirname(filename)

		#deal recent path
		path = os.path.dirname(filename)
		if path in win.pref.recent_paths:
			win.pref.recent_paths.remove(path)
		win.pref.recent_paths.insert(0, path)
		win.pref.recent_paths = win.pref.recent_paths[:win.pref.recent_paths_num]

		#save pref
		win.pref.save()

		#create menus
		create_recent_menu(win.mainframe)
		create_recent_path_menu(win.mainframe)
Mixin.setPlugin('editor', 'afteropenfile', afteropenfile)
Mixin.setPlugin('editor', 'aftersavefile', afteropenfile)

def create_recent_menu(win):
	menu = makemenu.findmenu(win.menuitems, 'IDM_FILE_RECENTFILES')

	for id in win.recentmenu_ids:
		menu.Delete(id)

	win.recentmenu_ids = []
	if len(win.pref.recent_files) == 0:
		id = win.IDM_FILE_RECENTFILES_ITEMS
		menu.Append(id, tr('(empty)'))
		menu.Enable(id, False)
		win.recentmenu_ids = [id]
	else:
		for i, filename in enumerate(win.pref.recent_files):
			id = wx.NewId()
			win.recentmenu_ids.append(id)
			menu.Append(id, "%d %s" % (i+1, filename))
			wx.EVT_MENU(win, id, win.OnOpenRecentFiles)

def create_recent_path_menu(win):
	menu = makemenu.findmenu(win.menuitems, 'IDM_FILE_RECENTPATHS')

	for id in win.recentpathmenu_ids:
		menu.Delete(id)

	win.recentpathmenu_ids = []
	if len(win.pref.recent_paths) == 0:
		id = win.IDM_FILE_RECENTPATHS_ITEMS
		menu.Append(id, tr('(empty)'))
		menu.Enable(id, False)
		win.recentpathmenu_ids = [id]
	else:
		for i, path in enumerate(win.pref.recent_paths):
			id = wx.NewId()
			win.recentpathmenu_ids.append(id)
			menu.Append(id, "%d %s" % (i+1, path))
			wx.EVT_MENU(win, id, win.OnOpenRecentPaths)

def OnOpenRecentFiles(win, event):
	eid = event.GetId()
	index = win.recentmenu_ids.index(eid)
	filename = win.pref.recent_files[index]
	try:
		f = file(filename)
		f.close()
	except:
		common.showerror(win, tr("Can't open the file [%s]!") % filename)
		del win.pref.recent_files[index]
		win.pref.save()
		create_recent_menu(win)
		return
	win.editctrl.new(filename)
Mixin.setMixin('mainframe', 'OnOpenRecentFiles', OnOpenRecentFiles)

def OnOpenRecentPaths(win, event):
	eid = event.GetId()
	index = win.recentpathmenu_ids.index(eid)
	path = win.pref.recent_paths[index]
	if os.path.exists(path) and os.path.isdir(path):
		dlg = wx.FileDialog(win, tr("Open"), path, "", '|'.join(win.filewildchar), wx.OPEN|wx.HIDE_READONLY|wx.MULTIPLE)
		dlg.SetFilterIndex(win.getFilterIndex())
		if dlg.ShowModal() == wx.ID_OK:
			encoding = win.execplugin('getencoding', win, win)
			for filename in dlg.GetPaths():
				win.editctrl.new(filename, encoding)
			dlg.Destroy()
	else:
		common.showerror(win, tr("Can't open the path [%s]!") % path)
		del win.pref.recent_paths[index]
		win.pref.save()
		create_recent_path_menu(win)
		return
Mixin.setMixin('mainframe', 'OnOpenRecentPaths', OnOpenRecentPaths)

def add_tool_list(toollist, toolbaritems):
    toollist.extend([
        (115, 'openpath'),
    ])
    
    #order, IDname, imagefile, short text, long text, func
    toolbaritems.update({
        'openpath':(wx.ITEM_NORMAL, 'IDM_FILE_OPEN_PATH', common.unicode_abspath('images/paths.gif'), tr('open path'), tr('Open path'), 'OnFileOpenPath'),
    })
Mixin.setPlugin('mainframe', 'add_tool_list', add_tool_list)

def OnFileOpenPath(win, event):
	eid = event.GetId()
	size = win.toolbar.GetToolSize()
	pos = win.toolbar.GetToolPos(eid)
	menu = wx.Menu()

	if len(win.pref.recent_paths) == 0:
		id = win.IDM_FILE_RECENTPATHS_ITEMS
		menu.Append(id, tr('(empty)'))
		menu.Enable(id, False)
	else:
		for i, path in enumerate(win.pref.recent_paths):
			id = win.recentpathmenu_ids[i]
			menu.Append(id, "%d %s" % (i+1, path))
#			wx.EVT_MENU(win, id, win.OnOpenRecentPaths)
	win.PopupMenu(menu, (size[0]*pos, size[1]))
	menu.Destroy()
Mixin.setMixin('mainframe', 'OnFileOpenPath', OnFileOpenPath)