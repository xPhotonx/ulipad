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
#	$Id: mSession.py 93 2005-10-11 02:51:02Z limodou $

from modules import Mixin
import wx
import wx.stc

def init(pref):
	pref.load_session = True
	pref.sessions = []
	pref.last_tab_index = -1
	pref.screen_lines = 0
Mixin.setPlugin('preference', 'init', init)

preflist = [
	(tr('General'), 130, 'check', 'load_session', tr('Auto load the files of last session'), None),
]
Mixin.setMixin('preference', 'preflist', preflist)

def afterclosewindow(win):
	win.pref.sessions = []
	win.pref.last_tab_index = -1
	if win.pref.load_session:
		for document in win.editctrl.getDocuments():
			if document.documenttype != 'edit':
				continue
			win.pref.screen_lines = document.LinesOnScreen()
			if document.filename and document.savesession:
				win.pref.sessions.append(getStatus(document))
		win.pref.last_tab_index = win.editctrl.GetSelection()
	win.pref.save()
Mixin.setPlugin('mainframe', 'afterclosewindow', afterclosewindow)

def getStatus(document):
	"""filename, pos, bookmarks"""
	row = document.GetCurrentLine()
	col = document.GetColumn(document.GetCurrentPos())
	bookmarks = []
	start = 0
	line = document.MarkerNext(start, 1)
	while line > -1:
		bookmarks.append(line)
		start = line + 1
		line = document.MarkerNext(start, 1)
	return document.filename, row, col, bookmarks

def setStatus(document, row, col, bookmarks):
	document.GotoLine(row)
	for line in bookmarks:
		document.MarkerAdd(line, 0)

def openPage(win):
	n = 0
	if win.mainframe.pref.load_session and not win.mainframe.app.skipsessionfile:
		for filename, row, col, bookmarks in win.mainframe.pref.sessions:
			document = win.new(filename, delay=True)
			if document:
				setStatus(document, row, col, bookmarks)
				n += 1
		index = win.mainframe.pref.last_tab_index
		if index > -1 and index < len(win.list):
			wx.CallAfter(win.switch, win.list[index], delay=False)
# 			while 1:
# 				try:
# 					win.switch(win.list[index], delay=False)
# 					break
# 				except:
# 					index=len(win.list)-1
					
	return n > 0
Mixin.setPlugin('editctrl', 'openpage', openPage)

