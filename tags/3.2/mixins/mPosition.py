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
#	$Id: mPosition.py 481 2006-01-17 05:54:13Z limodou $

import wx
from modules import Mixin

def editor_init(win):
	wx.EVT_KEY_UP(win, win.OnKeyUp)
	wx.EVT_LEFT_UP(win, win.OnMouseUp)
Mixin.setPlugin('editor', 'init', editor_init)

def OnKeyUp(win, event):
	win.mainframe.SetStatusText(tr("Line: %d") % (win.GetCurrentLine()+1), 1)
	win.mainframe.SetStatusText(tr("Col: %d") % (win.GetColumn(win.GetCurrentPos())+1), 2)
	if not win.callplugin('on_key_up', win, event):
		event.Skip()
Mixin.setMixin('editor', 'OnKeyUp', OnKeyUp)

def OnMouseUp(win, event):
	win.mainframe.SetStatusText(tr("Line: %d") % (win.GetCurrentLine()+1), 1)
	win.mainframe.SetStatusText(tr("Col: %d") % (win.GetColumn(win.GetCurrentPos())+1), 2)
	event.Skip()
Mixin.setMixin('editor', 'OnMouseUp', OnMouseUp)

def on_document_enter(win, document):
	if document.documenttype == 'edit':
		win.mainframe.SetStatusText(tr("Line: %d") % (document.GetCurrentLine()+1), 1)
		win.mainframe.SetStatusText(tr("Col: %d") % (document.GetColumn(document.GetCurrentPos())+1), 2)
Mixin.setPlugin('editctrl', 'on_document_enter', on_document_enter)