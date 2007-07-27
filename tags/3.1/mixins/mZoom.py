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
#	$Id: mZoom.py 176 2005-11-22 02:46:37Z limodou $

from modules import Mixin
import wx
import wx.stc
import os.path
from modules import common

menulist = [
	('IDM_VIEW', #parent menu id
	[
		(170, '', '-', wx.ITEM_SEPARATOR, None, ''),
		(185, 'IDM_VIEW_ZOOM_IN', tr('Zoom In'), wx.ITEM_NORMAL, 'OnViewZoomIn', tr('Increases the font size of the document')),
		(190, 'IDM_VIEW_ZOOM_OUT', tr('Zoom Out'), wx.ITEM_NORMAL, 'OnViewZoomOut', tr('Decreases the font size of the document')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

imagelist = {
	'IDM_VIEW_ZOOM_IN':'images/large.gif',
	'IDM_VIEW_ZOOM_OUT':'images/small.gif',
}
Mixin.setMixin('mainframe', 'imagelist', imagelist)

def OnViewZoomIn(win, event):
	win.document.ZoomIn()
Mixin.setMixin('mainframe', 'OnViewZoomIn', OnViewZoomIn)

def OnViewZoomOut(win, event):
	win.document.ZoomOut()
Mixin.setMixin('mainframe', 'OnViewZoomOut', OnViewZoomOut)

toollist = [
	(820, 'zoomin'),
	(830, 'zoomout'),
]
Mixin.setMixin('mainframe', 'toollist', toollist)

#order, IDname, imagefile, short text, long text, func
toolbaritems = {
	'zoomin':(wx.ITEM_NORMAL, 'IDM_VIEW_ZOOM_IN', common.unicode_abspath('images/large.gif'), tr('zoom in'), tr('Increases the font size of the document'), 'OnViewZoomIn'),
	'zoomout':(wx.ITEM_NORMAL, 'IDM_VIEW_ZOOM_OUT', common.unicode_abspath('images/small.gif'), tr('zoom out'), tr('Decreases the font size of the document'), 'OnViewZoomOut'),
}
Mixin.setMixin('mainframe', 'toolbaritems', toolbaritems)