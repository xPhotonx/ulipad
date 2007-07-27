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
#	$Id: PyBlosxom.py 42 2005-09-28 05:19:21Z limodou $

from modules import Mixin
import wx

def init(win):
	#pyblosxom button
	win.ID_PYBLOSXOM= wx.NewId()
	win.btnPyblosxom = wx.Button(win, win.ID_PYBLOSXOM, tr('PyBlosxom'), size=(70, 22))
	win.box1.Add(win.btnPyblosxom, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 2)

	wx.EVT_BUTTON(win.btnPyblosxom, win.ID_PYBLOSXOM, win.OnPyblosxom)
Mixin.setPlugin('blogmanagewindow', 'init', init)

def OnPyblosxom(win, event):
	menulist = [
		(tr("Categories"), win.OnPyblosxomCategories),
		(tr("Edit Config File"), win.OnPyblosxomEditFile),
		(tr("Upload File"), win.OnPyblosxomUploadFile),
		(tr("Get File List"), win.OnPyblosxomGetFileList),
	]
	menu = wx.Menu()
	
	for caption, func in menulist:
		id = wx.NewId()
		menu.Append(id, caption)
		wx.EVT_MENU(win, id, func)
	win.PopupMenu(menu, win.btnPyblosxom.GetPosition() + (0, win.btnPyblosxom.GetSize()[1]))
	menu.Destroy()
Mixin.setMixin('blogmanagewindow', 'OnPyblosxom', OnPyblosxom)

def OnPyblosxomCategories(win, event):
	from PyBlosxomPlugin import PyBlosxomCategories
	
	dlg = PyBlosxomCategories(win)
	ans = dlg.ShowModal()
Mixin.setMixin('blogmanagewindow', 'OnPyblosxomCategories', OnPyblosxomCategories)

def OnPyblosxomEditFile(win, event):
	from PyBlosxomPlugin import PyBlosxomEditFile
	
	dlg = PyBlosxomEditFile(win)
	ans = dlg.ShowModal()
Mixin.setMixin('blogmanagewindow', 'OnPyblosxomEditFile', OnPyblosxomEditFile)

def OnPyblosxomUploadFile(win, event):
	from PyBlosxomPlugin import uploadFile
	
	uploadFile(win)
Mixin.setMixin('blogmanagewindow', 'OnPyblosxomUploadFile', OnPyblosxomUploadFile)

def OnPyblosxomGetFileList(win, event):
	from PyBlosxomPlugin import getFileLists
	
	getFileLists(win)
Mixin.setMixin('blogmanagewindow', 'OnPyblosxomGetFileList', OnPyblosxomGetFileList)
