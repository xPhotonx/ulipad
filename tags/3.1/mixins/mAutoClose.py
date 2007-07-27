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
#	$Id: mAutoClose.py 93 2005-10-11 02:51:02Z limodou $

__doc__ = "Auto close"

from modules import Mixin
import wx.stc

def init(win):
	wx.stc.EVT_STC_CHARADDED(win, win.GetId(), win.OnCharAdded)
Mixin.setPlugin('editor', 'init', init)

preflist = [
	(tr('Document'), 220, 'check', 'auto_close', tr('Auto close enclosing char, like: (, [, {'), None),
	(tr('Document'), 230, 'check', 'auto_close_ext', tr('Auto close enclosing char, like: \', ", <'), None),
]
Mixin.setMixin('preference', 'preflist', preflist)

def init(pref):
	pref.auto_close = True
	pref.auto_close_ext = False
Mixin.setPlugin('preference', 'init', init)

charlist = dict(zip([ord(i) for i in ['(', '[', '{', '\'', '"', '<']], [')', ']', '}', '\'', '"', '>']))

def OnCharAdded(win, event):
	chars = []
	if win.pref.auto_close:
		chars += [ord(i) for i in ['(', '[', '{'] ]
	if win.pref.auto_close_ext:
		chars += [ord(i) for i in ['\'', '"', '<'] ]

	ch = event.GetKey()
	pos = win.GetCurrentPos()
	chnext = win.GetCharAt(pos)
	if (ch in chars) and (chnext < 127) and (not chnext or not (ord('0') <= chnext <= ord('9') or ord('a') <= chnext <= ord('z') or chnext == ord('_') or ord('A') <= chnext <= ord('Z'))):
		win.AddText(charlist[ch])
		win.GotoPos(pos)
Mixin.setMixin('editor', 'OnCharAdded', OnCharAdded)

