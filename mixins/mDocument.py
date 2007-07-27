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
#	$Id: mDocument.py 176 2005-11-22 02:46:37Z limodou $

from modules import Mixin
import wx
import wx.stc
from modules import common

menulist = [ (None,
	[
		(500, 'IDM_DOCUMENT', tr('Document'), wx.ITEM_NORMAL, None, ''),
	]),
	('IDM_DOCUMENT', #parent menu id
	[
		(100, 'IDM_DOCUMENT_WORDWRAP', tr('Word-wrap'), wx.ITEM_CHECK, 'OnDocumentWordWrap', tr('Toggles the word wrap feature of the active document')),
		(110, 'IDM_DOCUMENT_AUTOINDENT', tr('Auto Indent'), wx.ITEM_CHECK, 'OnDocumentAutoIndent', tr('Toggles the auto-indent feature of the active document')),
		(115, 'IDM_DOCUMENT_TABINDENT', tr('Use Tab Indent'), wx.ITEM_CHECK, 'OnDocumentTabIndent', tr('Uses tab as indent char or uses space as indent char.')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

imagelist = {
	'IDM_DOCUMENT_WORDWRAP':common.unicode_abspath('images/wrap.gif'),
}
Mixin.setMixin('mainframe', 'imagelist', imagelist)

def init(pref):
	pref.autoindent = True
	pref.usetabs = True
	pref.wordwrap = False
Mixin.setPlugin('preference', 'init', init)

preflist = [
	(tr('Document'), 150, 'check', 'autoindent', tr('Auto indent'), None),
	(tr('Document'), 160, 'check', 'usetabs', tr('Use Tabs'), None),
	(tr('Document'), 170, 'check', 'wordwrap', tr('Auto word-wrap'), None),
]
Mixin.setMixin('preference', 'preflist', preflist)

def savepreference(mainframe, pref):
	for document in mainframe.editctrl.list:
		if mainframe.pref.wordwrap:
			document.SetWrapMode(wx.stc.STC_WRAP_WORD)
		else:
			document.SetWrapMode(wx.stc.STC_WRAP_NONE)
Mixin.setPlugin('prefdialog', 'savepreference', savepreference)

toollist = [
	(805, 'wrap'),
]
Mixin.setMixin('mainframe', 'toollist', toollist)

#order, IDname, imagefile, short text, long text, func
toolbaritems = {
	'wrap':(wx.ITEM_CHECK, 'IDM_DOCUMENT_WORDWRAP', common.unicode_abspath('images/wrap.gif'), tr('wrap'), tr('Toggles the word wrap feature of the active document'), 'OnDocumentWordWrap'),
}
Mixin.setMixin('mainframe', 'toolbaritems', toolbaritems)

def init(win):
	win.SetUseTabs(win.mainframe.pref.usetabs)
	win.usetab = win.mainframe.pref.usetabs
Mixin.setPlugin('editor', 'init', init)

def OnKeyDown(win, event):
	if event.GetKeyCode() == wx.WXK_RETURN:
		if win.GetSelectedText():
			win.CmdKeyExecute(wx.stc.STC_CMD_NEWLINE)
			return True
		if win.pref.autoindent:
			line = win.GetCurrentLine()
			text = win.GetTextRange(win.PositionFromLine(line), win.GetCurrentPos())
			if text.strip() == '':
				win.AddText(win.getEOLChar() + text)
				return True

			n = win.GetLineIndentation(line) / win.GetTabWidth()
			win.AddText(win.getEOLChar() + win.getIndentChar() * n)
			return True
		else:
			win.AddText(win.getEOLChar())
			return True
Mixin.setPlugin('editor', 'on_key_down', OnKeyDown, Mixin.LOW)

def OnDocumentWordWrap(win, event):
	mode = win.document.GetWrapMode()
	if mode == wx.stc.STC_WRAP_NONE:
		win.document.SetWrapMode(wx.stc.STC_WRAP_WORD)
	else:
		win.document.SetWrapMode(wx.stc.STC_WRAP_NONE)
Mixin.setMixin('mainframe', 'OnDocumentWordWrap', OnDocumentWordWrap)

def OnDocumentAutoIndent(win, event):
	win.pref.autoindent = not win.pref.autoindent
	win.pref.save()
Mixin.setMixin('mainframe', 'OnDocumentAutoIndent', OnDocumentAutoIndent)

def afterinit(win):
	wx.EVT_UPDATE_UI(win, win.IDM_DOCUMENT_WORDWRAP, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDM_DOCUMENT_AUTOINDENT, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDM_DOCUMENT_TABINDENT, win.OnUpdateUI)
Mixin.setPlugin('mainframe', 'afterinit', afterinit)

def OnUpdateUI(win, event):
	eid = event.GetId()
	if hasattr(win, 'document') and win.document:
		if eid == win.IDM_DOCUMENT_WORDWRAP:
			if win.document.GetWrapMode:
				event.Enable(True)
				mode = win.document.GetWrapMode()
				if mode == wx.stc.STC_WRAP_NONE:
					event.Check(False)
				else:
					event.Check(True)
			else:
				event.Enable(False)
		elif eid == win.IDM_DOCUMENT_AUTOINDENT:
			if win.document.canedit:
				event.Enable(True)
				event.Check(win.pref.autoindent)
			else:
				event.Enable(False)
		elif eid == win.IDM_DOCUMENT_TABINDENT:
			if win.document.canedit:
				event.Enable(True)
				event.Check(win.document.usetab)
			else:
				event.Enable(False)
Mixin.setPlugin('mainframe', 'on_update_ui', OnUpdateUI)

def openfiletext(win, stext):
	pos = 0
	text = stext[0]
	while pos < len(text) - 1:
		if text[pos] == ' ':
			win.SetUseTabs(False)
			win.usetab = False
			return
		elif text[pos] == '\t':
			win.SetUseTabs(True)
			win.usetab = True
			return
		else:
			pos = text.find('\n', pos + 1)
			if pos > -1:
				pos += 1
			else:
				break
	win.SetUseTabs(win.mainframe.pref.usetabs)
	win.usetab = win.mainframe.pref.usetabs
Mixin.setPlugin('editor', 'openfiletext', openfiletext)

def OnDocumentTabIndent(win, event):
	win.document.usetab = not win.document.usetab
	win.document.SetUseTabs(win.document.usetab)
	from modules import makemenu
	menu = makemenu.findmenu(win.menuitems, 'IDM_DOCUMENT_TABINDENT')
	if win.document.usetab:
		menu.SetText(tr('Use Tab Indent'))
	else:
		menu.SetText(tr('Use Space Indent'))
Mixin.setMixin('mainframe', 'OnDocumentTabIndent', OnDocumentTabIndent)