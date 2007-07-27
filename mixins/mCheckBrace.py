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
#	$Id: mCheckBrace.py 93 2005-10-11 02:51:02Z limodou $

from modules import Mixin
import wx
import wx.stc

def init(win):
	wx.EVT_UPDATE_UI(win, win.GetId(), win.OnUpdateUI)
Mixin.setPlugin('editor', 'init', init)

def OnUpdateUI(win, event):
	# check for matching braces
	braceAtCaret = -1
	braceOpposite = -1
	charBefore = None
	caretPos = win.GetCurrentPos()
	if caretPos > 0:
		charBefore = win.GetCharAt(caretPos - 1)
		styleBefore = win.GetStyleAt(caretPos - 1)

	# check before
	if charBefore and chr(charBefore) in "[]{}()" and styleBefore == wx.stc.STC_P_OPERATOR:
		braceAtCaret = caretPos - 1

	# check after
	if braceAtCaret < 0:
		charAfter = win.GetCharAt(caretPos)
		styleAfter = win.GetStyleAt(caretPos)
		if charAfter and chr(charAfter) in "[]{}()" and styleAfter == wx.stc.STC_P_OPERATOR:
			braceAtCaret = caretPos

	if braceAtCaret >= 0:
		braceOpposite = win.BraceMatch(braceAtCaret)

	if braceAtCaret != -1  and braceOpposite == -1:
		win.BraceBadLight(braceAtCaret)
	else:
		win.BraceHighlight(braceAtCaret, braceOpposite)
Mixin.setPlugin('editor', 'on_update_ui', OnUpdateUI)

