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
#	$Id: mSetScrollWidth.py 475 2006-01-16 09:50:28Z limodou $

import wx
from modules import Mixin

def editor_init(win):
	win.SetScrollWidth(1)
	win.maxline = 'WWWW'
Mixin.setPlugin('editor', 'init', editor_init)

def OnModified(win, event):
	if win.GetWrapMode() == wx.stc.STC_WRAP_NONE:
		win.setWidth(win.GetCurLine()[0])
Mixin.setPlugin('editor', 'on_modified', OnModified)

def openfiletext(win, stext):
	lines = stext[0].splitlines()
	lens = [len(text) for text in lines]
	if lens:
		maxlen = max(lens)
		line = lines[lens.index(maxlen)]
		win.setWidth(line)
	else:
		win.setWidth('')
Mixin.setPlugin('editor', 'openfiletext', openfiletext)

def setWidth(win, text=''):
	if not text:
		text = win.maxline
	if win.GetWrapMode() == wx.stc.STC_WRAP_NONE:
		ll = win.TextWidth(wx.stc.STC_STYLE_DEFAULT, "W")*4
		line = text.expandtabs(win.GetTabWidth())
		current_width = win.GetScrollWidth()
		width = win.TextWidth(wx.stc.STC_STYLE_DEFAULT, line)
		if width>current_width:
			win.maxline = line
			win.SetScrollWidth(width + ll)
Mixin.setMixin('editor', 'setWidth', setWidth)