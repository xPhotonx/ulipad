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
#	$Id: mDClickCloseFile.py 176 2005-11-22 02:46:37Z limodou $

from modules import Mixin
import wx

def init(pref):
	pref.dclick_close_file = True
Mixin.setPlugin('preference', 'init', init)

preflist = [
	(tr('Document'), 100, 'check', 'dclick_close_file', tr('Double click will close the selected document'), None)
]
Mixin.setMixin('preference', 'preflist', preflist)

def savepreference(mainframe, pref):
	if pref.dclick_close_file:
		wx.EVT_LEFT_DCLICK(mainframe.editctrl, mainframe.editctrl.OnDClick)
	else:
		wx.EVT_LEFT_DCLICK(mainframe.editctrl, None)
Mixin.setPlugin('prefdialog', 'savepreference', savepreference)

def OnDClick(win, event):
	if wx.NB_HITTEST_NOWHERE == win.HitTest(event.GetPosition())[1]:
		event.Skip()
		return
	win.mainframe.CloseFile(win.document)
	if len(win.list) == 0:
		win.new()
Mixin.setMixin('editctrl', 'OnDClick', OnDClick)

def init(win):
	if win.pref.dclick_close_file:
		wx.EVT_LEFT_DCLICK(win, win.OnDClick)
	else:
		wx.EVT_LEFT_DCLICK(win, None)
Mixin.setPlugin('editctrl', 'init', init)