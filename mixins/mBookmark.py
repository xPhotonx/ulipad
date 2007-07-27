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
#	$Id: mBookmark.py 176 2005-11-22 02:46:37Z limodou $

from modules import Mixin
import wx
import wx.stc

def init(win):
	win.SetMarginWidth(0, 20)
	win.SetMarginType(0, wx.stc.STC_MARGIN_SYMBOL)

	win.SetMarginMask(0, ~wx.stc.STC_MASK_FOLDERS)
	win.MarkerDefine(0, wx.stc.STC_MARK_SHORTARROW, "blue", "blue")
	win.bookmarks = []
Mixin.setPlugin('editor', 'init', init)

menulist = [ ('IDM_SEARCH',
	[
		(180, '', '-', wx.ITEM_SEPARATOR, None, ''),
		(190, 'IDM_SEARCH_BOOKMARK_TOGGLE', tr('Toggle Marker') + '\tF9', wx.ITEM_NORMAL, 'OnSearchBookmarkToggle', tr('Set and clear marker at current line')),
		(200, 'IDM_SEARCH_BOOKMARK_CLEARALL', tr('Clear All Marker') + '\tCtrl+Shift+F9', wx.ITEM_NORMAL, 'OnSearchBookmarkClearAll', tr('Clears all marker from the active document')),
		(210, 'IDM_SEARCH_BOOKMARK_NEXT', tr('Next Marker') + '\tF5', wx.ITEM_NORMAL, 'OnSearchBookmarkNext', tr('Goes to next marker position')),
		(220, 'IDM_SEARCH_BOOKMARK_PREVIOUS', tr('Previous Marker') + '\tShift+F5', wx.ITEM_NORMAL, 'OnSearchBookmarkPrevious', tr('Goes to previous marker position')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

def OnSearchBookmarkToggle(win, event):
	line = win.document.GetCurrentLine()
	marker = win.document.MarkerGet(line)
	if marker:
		win.document.MarkerDelete(line, 0)
	else:
		win.document.MarkerAdd(line, 0)
Mixin.setMixin('mainframe', 'OnSearchBookmarkToggle', OnSearchBookmarkToggle)

def OnSearchBookmarkClearAll(win, event):
	win.document.MarkerDeleteAll(0)
Mixin.setMixin('mainframe', 'OnSearchBookmarkClearAll', OnSearchBookmarkClearAll)

def OnSearchBookmarkNext(win, event):
	line = win.document.GetCurrentLine()
	marker = win.document.MarkerGet(line)
	if marker:
		line += 1
	f = win.document.MarkerNext(line, 1)
	if f > -1:
		win.document.goto(f + 1)
	else:
		f = win.document.MarkerNext(0, 1)
		if f > -1:
			win.document.goto(f + 1)
Mixin.setMixin('mainframe', 'OnSearchBookmarkNext', OnSearchBookmarkNext)

def OnSearchBookmarkPrevious(win, event):
	line = win.document.GetCurrentLine()
	marker = win.document.MarkerGet(line)
	if marker:
		line -= 1
	f = win.document.MarkerPrevious(line, 1)
	if f > -1:
		win.document.goto(f + 1)
	else:
		f = win.document.MarkerPrevious(win.document.GetLineCount()-1, 1)
		if f > -1:
			win.document.goto(f + 1)
Mixin.setMixin('mainframe', 'OnSearchBookmarkPrevious', OnSearchBookmarkPrevious)