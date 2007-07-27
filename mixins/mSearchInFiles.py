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
#	$Id: mSearchInFiles.py 176 2005-11-22 02:46:37Z limodou $

from modules import Mixin
import wx
import os.path, sys

menulist = [
	('IDM_SEARCH', #parent menu id
	[
		(145, 'IDM_SEARCH_FIND_IN_FILES', tr('Find In Files...'), wx.ITEM_NORMAL, 'OnSearchFindInFiles', tr('Find text in files')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

def OnSearchFindInFiles(win, event):
	import FindInFiles

	dlg = FindInFiles.FindInFiles(win, win.pref)
	dlg.Show()
Mixin.setMixin('mainframe', 'OnSearchFindInFiles', OnSearchFindInFiles)

def init(pref):
	pref.searchinfile_searchlist = []
	pref.searchinfile_dirlist = []
	pref.searchinfile_extlist = []
	pref.searchinfile_case = False
	pref.searchinfile_subdir = False
	pref.searchinfile_regular = False
	pref.searchinfile_defaultpath = os.path.dirname(sys.argv[0])
Mixin.setPlugin('preference', 'init', init)