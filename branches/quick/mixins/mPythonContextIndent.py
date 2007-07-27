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
#   This function is referenced with DrPython.
#
#	$Id: mPythonContextIndent.py 475 2006-01-16 09:50:28Z limodou $

__doc__ = 'Context indent'

from modules import Mixin
import wx
import re

def OnKeyDown(win, event):
	if event.GetKeyCode() == wx.WXK_RETURN:
		if win.GetSelectedText():
			return False
		if win.pref.autoindent and win.pref.python_context_indent and win.languagename == 'python':
			pythonContextIndent(win)
			return True
Mixin.setPlugin('editor', 'on_key_down', OnKeyDown, Mixin.HIGH)

def add_pref(preflist):
    preflist = [
        ('Python', 110, 'check', 'python_context_indent', tr('Use context sensitive indent'), None)
    ]
Mixin.setPlugin('preference', 'add_pref', add_pref)

def pref_init(pref):
	pref.python_context_indent = True
Mixin.setPlugin('preference', 'init', pref_init)

def pythonContextIndent(win):
	pos = win.GetCurrentPos()
	if win.languagename == 'python':
		linenumber = win.GetCurrentLine()
		numtabs = win.GetLineIndentation(linenumber) / win.GetTabWidth()
		text = win.GetTextRange(win.PositionFromLine(linenumber), win.GetCurrentPos())
		if text.strip() == '':
			win.AddText(win.getEOLChar()+text)
			return
		if win.pref.python_context_indent:
			linetext = win.GetLine(linenumber).rstrip()
			if linetext:
				if linetext[-1] == ':':
					numtabs = numtabs + 1
				else:
					#Remove Comment:
					comment = linetext.find('#')
					if comment > -1:
						linetext = linetext[:comment]
					#Keyword Search.
					keyword = re.compile(r"(\sreturn\b)|(\sbreak\b)|(\spass\b)|(\scontinue\b)|(\sraise\b)", re.MULTILINE)
					slash = re.compile(r"\\\Z")

					if slash.search(linetext.rstrip()) is None:
						if keyword.search(linetext) is not None:
							numtabs = numtabs - 1
		#Go to current line to add tabs
		win.AddText(win.getEOLChar())
		for i in range(numtabs):
			win.AddText(win.getIndentChar())