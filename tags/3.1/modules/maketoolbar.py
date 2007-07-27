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
#	$Id: maketoolbar.py 176 2005-11-22 02:46:37Z limodou $

import wx
import Id
from Debug import debug
import common

class EUnknowStyleType(Exception): pass


def addtools(win, toolbar, toollist, toolbaritems):
	#judge image size by the first item of the toolbar item list
	imagefile = toolbaritems.values()[0][2]
	image = common.getpngimage(imagefile)
	size = wx.Size(image.GetWidth(), image.GetHeight())
	toolbar.SetToolBitmapSize(size)

	toollist.sort()
	debug.info('[addtools] toolbar list...')
	for order, name in toollist:
		if name == '|':
			toolbar.AddSeparator()
			debug.info('\t%d -' % order)
		else:
			style, idname, imagefile, shorttext, longtext, func = toolbaritems[name]
			image = common.getpngimage(imagefile)
			id = Id.makeid(win, idname)
			if style == wx.ITEM_NORMAL:
				toolbar.AddSimpleTool(id, image, shorttext, longtext)
			elif style == wx.ITEM_CHECK:
				toolbar.AddCheckTool(id, image, shortHelp=shorttext, longHelp=longtext)
#			elif style == wx.ITEM_RADIO:
#				toolbar.AddRadioTool(id, image, shortHelp=shorttext, longHelp=longtext)
			else:
				raise EUnknowStyleType
			if func:
				try:
					f = getattr(win, func)
					wx.EVT_TOOL(win, id, f)
				except:
					debug.info("[addtools] Can't find function [%s] in class %s" % (func, win.__class__.__name__))
	toolbar.Realize()

def makebasetoolbar(win, toollist, toolbaritems):
	toolbar = wx.ToolBar(win, -1, style=wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)
	addtools(win, toolbar, toollist, toolbaritems)
	return toolbar

def maketoolbar(win, toollist, toolbaritems):
	win.toolbar = win.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)
	addtools(win, win.toolbar, toollist, toolbaritems)
	return win.toolbar

def inserttookbar(win, oldtoollist, toollist, toolbaritems):
	if len(toollist) == 0:
		return

	tl = oldtoollist[:]
	newtl = toollist[:]
	newtl.sort()
	tl.extend(newtl)
	tl.sort()

	for v in newtl:
		i = tl.index(v)
		order, name = v
		if name == '|':
			win.toolbar.InsertSeparator(i)
		else:
			style, idname, imagefile, shorttext, longtext, func = toolbaritems[name]
			image = common.getpngimage(imagefile)
			id = Id.makeid(win, idname)
			if style == wx.ITEM_NORMAL:
				win.toolbar.InsertSimpleTool(i, id, image, shorttext, longtext)
			elif style == wx.ITEM_CHECK:
				win.toolbar.InsertTool(i, id, image, isToggle = True, shortHelpString=shorttext, longHelpString=longtext)
#			elif style == wx.ITEM_RADIO:
#				win.toolbar.InsertRadioTool(i, id, image, shortHelp=shorttext, longHelp=longtext)
			else:
				raise EUnknowStyleType
			if func:
				try:
					f = getattr(win, func)
					wx.EVT_TOOL(win, id, f)
				except:
					debug.info("[maketoolbar] Can't find function [%s] in class %s" % (func, win.__class__.__name__))
	win.toolbar.Realize()

def removetoolbar(win, oldtoollist, toollist, toolbaritems):
	if len(toollist) == 0:
		return

	tl = oldtoollist[:]
	newtl = toollist[:]
	newtl.sort()
	newtl.reverse()
	tl.extend(newtl)
	tl.sort()

	for v in newtl:
		i = tl.index(v)
		win.toolbar.DeleteToolByPos(i)