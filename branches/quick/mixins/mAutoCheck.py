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
#	$Id: mAutoCheck.py 475 2006-01-16 09:50:28Z limodou $

__doc__ = 'Auto check if the file is modified'

import wx
import os
import stat
from modules import Mixin

def add_pref(preflist):
    preflist.extend([
        (tr('Document'), 210, 'check', 'auto_check', tr('Auto check if there are some opened files were modified by others'), None)
    ])
Mixin.setPlugin('preference', 'add_pref', add_pref)

def pref_init(pref):
	pref.auto_check  = False
Mixin.setPlugin('preference', 'init', pref_init)

def on_idle(win, event):
	if win.pref.auto_check:
		for document in win.editctrl.list:
			if document.filename and document.documenttype == 'edit' and document.opened:
				if os.path.exists(document.filename) and not checkFilename(win, document) and win.editctrl.filetimes.has_key(document.filename):
					if getModifyTime(document.filename) > win.editctrl.filetimes[document.filename]:
						dlg = wx.MessageDialog(win, tr("This file [%s] has been modified by others,\ndo you like reload it?") % document.filename, tr("Check"), wx.YES_NO | wx.ICON_QUESTION)
						answer = dlg.ShowModal()
						if answer == wx.ID_YES:
							document.openfile(document.filename)
							document.editctrl.switch(document)
						win.editctrl.filetimes[document.filename] = getModifyTime(document.filename)
Mixin.setPlugin('mainframe', 'on_idle', on_idle)

def editctrl_init(win):
	win.filetimes = {}
Mixin.setPlugin('editctrl', 'init', editctrl_init)

def afteropenfile(win, filename):
	if filename and win.documenttype == 'edit':
		win.editctrl.filetimes[filename] = getModifyTime(filename)
Mixin.setPlugin('editor', 'afteropenfile', afteropenfile)

def aftersavefile(win, filename):
	if win.documenttype == 'edit':
		win.editctrl.filetimes[filename] = getModifyTime(filename)
Mixin.setPlugin('editor', 'aftersavefile', aftersavefile)

def closefile(win, filename):
	if filename and win.document.documenttype == 'edit':
		if win.editctrl.filetimes.has_key(filename):
			del win.editctrl.filetimes[filename]
Mixin.setPlugin('mainframe', 'closefile', closefile)

def getModifyTime(filename):
	try:
		ftime = os.stat(filename)[stat.ST_MTIME]
	except:
		ftime = 0
	return ftime

def checkFilename(win, document):
	if not document.needcheck():
		return True
	if not os.path.exists(document.filename) and win.editctrl.filetimes[document.filename] != 'NO':
		dlg = wx.MessageDialog(win, tr("This file [%s] has been removed by others,\nDo you like save it?") % document.filename, tr("Check"), wx.YES_NO | wx.ICON_QUESTION)
		answer = dlg.ShowModal()
		if answer == wx.ID_YES:
			document.savefile(document.filename, document.locale)
			document.editctrl.switch(document)
			win.editctrl.filetimes[document.filename] = getModifyTime(document.filename)
		else:
			win.editctrl.filetimes[document.filename] = 'NO'
		return True
	else:
		return False