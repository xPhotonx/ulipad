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
#	$Id: mView.py 93 2005-10-11 02:51:02Z limodou $

from modules import Mixin
import wx
import wx.stc
import os.path
from modules import common

menulist = [ (None,
	[
		(300, 'IDM_VIEW', tr('View'), wx.ITEM_NORMAL, None, ''),
	]),
	('IDM_VIEW', #parent menu id
	[
		(100, 'IDM_VIEW_TAB', tr('Tabs And Spaces'), wx.ITEM_CHECK, 'OnViewTab', tr('Shows or hides space and tab marks')),
		(110, 'IDM_VIEW_INDENTATION_GUIDES', tr('Indentation Guides'), wx.ITEM_CHECK, 'OnViewIndentationGuides', tr('Shows or hides indentation guides')),
		(120, 'IDM_VIEW_RIGHT_EDGE', tr('Right edge indicator'), wx.ITEM_CHECK, 'OnViewRightEdge', tr('Shows or hides right edge indicator')),
		(130, 'IDM_VIEW_ENDOFLINE_MARK', tr('End-of-line marker'), wx.ITEM_CHECK, 'OnViewEndOfLineMark', tr('Shows or hides end-of-line marker')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

def afterinit(win):
	wx.EVT_UPDATE_UI(win, win.IDM_VIEW_TAB, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDM_VIEW_INDENTATION_GUIDES, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDM_VIEW_RIGHT_EDGE, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDM_VIEW_ENDOFLINE_MARK, win.OnUpdateUI)
Mixin.setPlugin('mainframe', 'afterinit', afterinit)

def init(win):
	#show long line indicator
	if win.mainframe.pref.startup_show_longline:
		win.SetEdgeMode(wx.stc.STC_EDGE_LINE)
	else:
		win.SetEdgeMode(wx.stc.STC_EDGE_NONE)
#	win.SetEdgeColour(wx.Colour(200,200,200))

	#long line width
	win.SetEdgeColumn(win.mainframe.pref.edge_column_width)

	#show tabs
	if win.mainframe.pref.startup_show_tabs:
		win.SetViewWhiteSpace(wx.stc.STC_WS_VISIBLEALWAYS)
	else:
		win.SetViewWhiteSpace(wx.stc.STC_WS_INVISIBLE)

	#show indentation guides
	win.SetIndentationGuides(win.mainframe.pref.startup_show_indent_guide)
Mixin.setPlugin('editor', 'init', init)

def OnViewTab(win, event):
	stat = win.document.GetViewWhiteSpace()
	if stat == wx.stc.STC_WS_INVISIBLE:
		win.document.SetViewWhiteSpace(wx.stc.STC_WS_VISIBLEALWAYS)
	elif stat == wx.stc.STC_WS_VISIBLEALWAYS:
		win.document.SetViewWhiteSpace(wx.stc.STC_WS_INVISIBLE)
Mixin.setMixin('mainframe', 'OnViewTab', OnViewTab)

def OnViewIndentationGuides(win, event):
	win.document.SetIndentationGuides(not win.document.GetIndentationGuides())
Mixin.setMixin('mainframe', 'OnViewIndentationGuides', OnViewIndentationGuides)

def init(pref):
	pref.edge_column_width = 100
	pref.startup_show_tabs = False
	pref.startup_show_indent_guide = False
	pref.startup_show_longline = False
Mixin.setPlugin('preference', 'init', init)

preflist = [
	(tr('Document'), 110, 'check', 'startup_show_tabs', tr('Whitespace is visible on startup'), None),
	(tr('Document'), 115, 'check', 'startup_show_indent_guide', tr('Indentation guides is visible on startup'), None),
	(tr('Document'), 120, 'check', 'startup_show_longline', tr('Long line indicator is visible on startup'), None),
	(tr('Document'), 130, 'num', 'edge_column_width', tr('Long line indicator column'), None),
]
Mixin.setMixin('preference', 'preflist', preflist)

def savepreference(mainframe, pref):
	for document in mainframe.editctrl.list:
		if document.CanView():
			document.SetEdgeColumn(mainframe.pref.edge_column_width)
Mixin.setPlugin('prefdialog', 'savepreference', savepreference)

def OnViewRightEdge(win, event):
	flag = win.document.GetEdgeMode()
	if flag == wx.stc.STC_EDGE_NONE:
		k = wx.stc.STC_EDGE_LINE
	else:
		k = wx.stc.STC_EDGE_NONE
	win.document.SetEdgeMode(k)
Mixin.setMixin('mainframe', 'OnViewRightEdge', OnViewRightEdge)

def OnViewEndOfLineMark(win, event):
	win.document.SetViewEOL(not win.document.GetViewEOL())
Mixin.setMixin('mainframe', 'OnViewEndOfLineMark', OnViewEndOfLineMark)

def OnUpdateUI(win, event):
	eid = event.GetId()
	if hasattr(win, 'document') and win.document and win.document.CanView():
		event.Enable(True)
		if eid == win.IDM_VIEW_TAB:
			stat = win.document.GetViewWhiteSpace()
			if stat == wx.stc.STC_WS_INVISIBLE:
				event.Check(False)
			elif stat == wx.stc.STC_WS_VISIBLEALWAYS:
				event.Check(True)
		elif eid == win.IDM_VIEW_INDENTATION_GUIDES:
			event.Check(win.document.GetIndentationGuides())
		elif eid == win.IDM_VIEW_RIGHT_EDGE:
			flag = win.document.GetEdgeMode()
			if flag == wx.stc.STC_EDGE_NONE:
				event.Check(False)
			else:
				event.Check(True)
		elif eid == win.IDM_VIEW_ENDOFLINE_MARK:
			event.Check(win.document.GetViewEOL())
	else:
		if eid in [win.IDM_VIEW_TAB, win.IDM_VIEW_INDENTATION_GUIDES, win.IDM_VIEW_RIGHT_EDGE, win.IDM_VIEW_ENDOFLINE_MARK]:
			event.Enable(False)
Mixin.setPlugin('mainframe', 'on_update_ui', OnUpdateUI)

toollist = [
	(800, '|'),
	(810, 'viewtab'),
]
Mixin.setMixin('mainframe', 'toollist', toollist)

#order, IDname, imagefile, short text, long text, func
toolbaritems = {
	'viewtab':(wx.ITEM_CHECK, 'IDM_VIEW_TAB', common.unicode_abspath('images/format.gif'), tr('toggle white space'), tr('Shows or hides space and tab marks'), 'OnViewTab'),
}
Mixin.setMixin('mainframe', 'toolbaritems', toolbaritems)

