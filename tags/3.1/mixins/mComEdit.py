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
#	$Id: mComEdit.py 176 2005-11-22 02:46:37Z limodou $

__doc__ = 'Common edit menu. Redo, Undo, Cut, Paste, Copy'

from modules import Mixin
import wx
from modules import common

popmenulist = [ (None, #parent menu id
	[
		(100, 'IDPM_UNDO', tr('Undo') + '\tCtrl+Z', wx.ITEM_NORMAL, 'OnUndo', tr('Reverse previous editing operation')),
		(110, 'IDPM_REDO', tr('Redo') + '\tCtrl+Y', wx.ITEM_NORMAL, 'OnRedo', tr('Reverse previous undo operation')),
		(120, '', '-', wx.ITEM_SEPARATOR, None, ''),
		(130, 'IDPM_CUT', tr('Cut') + '\tCtrl+X', wx.ITEM_NORMAL, 'OnPopupEdit', tr('Deletes text from the document and moves it to the clipboard')),
		(140, 'IDPM_COPY', tr('Copy') + '\tCtrl+C', wx.ITEM_NORMAL, 'OnPopupEdit', tr('Copies text from the document to the clipboard')),
		(150, 'IDPM_PASTE', tr('Paste') + '\tCtrl+V', wx.ITEM_NORMAL, 'OnPopupEdit', tr('Pastes text from the clipboard into the document')),
		(160, '', '-', wx.ITEM_SEPARATOR, None, ''),
		(170, 'IDPM_SELECTION', tr('Selection'), wx.ITEM_NORMAL, None, ''),

	]),
	('IDPM_SELECTION',
	[
		(100, 'IDPM_SELECTION_SELECT_WORD', tr('Select Word') + '\tCtrl+W', wx.ITEM_NORMAL, 'OnSelectionWord', tr('Selects current word')),
		(200, 'IDPM_SELECTION_SELECT_WORD_EXTENT', tr('Select Word Extent') + '\tCtrl+Shift+W', wx.ITEM_NORMAL, 'OnSelectionWordExtent', tr('Selects current word include "."')),
		(300, 'IDPM_SELECTION_SELECT_PHRASE', tr('Match Select (Left First)') + '\tCtrl+E', wx.ITEM_NORMAL, 'OnSelectionMatchLeft', tr('Selects the text encluded by (){}[]<>""\'\', matching left first')),
		(400, 'IDPM_SELECTION_SELECT_PHRASE_RIGHT', tr('Match Select (Right First)') + '\tCtrl+Shift+E', wx.ITEM_NORMAL, 'OnSelectionMatchRight', tr('Selects the text encluded by (){}[]<>""\'\', matching right first')),
		(500, 'IDPM_SELECTION_SELECT_ENLARGE', tr('Enlarge Selection') + '\tCtrl+Alt+E', wx.ITEM_NORMAL, 'OnSelectionEnlarge', tr('Enlarges selection')),
		(600, 'IDPM_SELECTION_SELECT_LINE', tr('Select Line') + '\tCtrl+R', wx.ITEM_NORMAL, 'OnSelectionLine', tr('Select current phrase')),
		(700, 'IDPM_SELECTION_SELECT_ALL', tr('Select All') + '\tCtrl+A', wx.ITEM_NORMAL, 'OnPopupEdit', tr('Selects the entire document')),
	]),
]
Mixin.setMixin('editor', 'popmenulist', popmenulist)

imagelist = {
	'IDPM_UNDO':common.unicode_abspath('images/undo.gif'),
	'IDPM_REDO':common.unicode_abspath('images/redo.gif'),
	'IDPM_CUT':common.unicode_abspath('images/cut.gif'),
	'IDPM_COPY':common.unicode_abspath('images/copy.gif'),
	'IDPM_PASTE':common.unicode_abspath('images/paste.gif'),
}
Mixin.setMixin('editor', 'imagelist', imagelist)

def OnUndo(win, event):
	win.Undo()
Mixin.setMixin('editor', 'OnUndo', OnUndo)

def OnRedo(win, event):
	win.Redo()
Mixin.setMixin('editor', 'OnRedo', OnRedo)

def OnPopupEdit(win, event):
	eid = event.GetId()
	if eid == win.IDPM_CUT:
		win.Cut()
	elif eid == win.IDPM_COPY:
		win.Copy()
	elif eid == win.IDPM_PASTE:
		win.Paste()
	elif eid == win.IDPM_SELECTION_SELECT_ALL:
		win.SelectAll()
Mixin.setMixin('editor', 'OnPopupEdit', OnPopupEdit)

menulist = [ (None, #parent menu id
	[
		(200, 'IDM_EDIT', tr('Edit'), wx.ITEM_NORMAL, None, ''),
	]),
	('IDM_EDIT', #parent menu id
	[
		(201, 'IDM_EDIT_UNDO', tr('Undo') +'\tE=Ctrl+Z', wx.ITEM_NORMAL, 'OnEditUndo', tr('Reverse previous editing operation')),
		(202, 'IDM_EDIT_REDO', tr('Redo') +'\tE=Ctrl+Y', wx.ITEM_NORMAL, 'OnEditRedo', tr('Reverse previous undo operation')),
		(203, '', '-', wx.ITEM_SEPARATOR, None, ''),
		(204, 'IDM_EDIT_CUT', tr('Cut') + '\tE=Ctrl+X', wx.ITEM_NORMAL, 'DoSTCBuildIn', tr('Deletes text from the document and moves it to the clipboard')),
		(205, 'IDM_EDIT_COPY', tr('Copy') + '\tE=Ctrl+C', wx.ITEM_NORMAL, 'DoSTCBuildIn', tr('Copies text from the document to the clipboard')),
		(206, 'IDM_EDIT_PASTE', tr('Paste') + '\tE=Ctrl+V', wx.ITEM_NORMAL, 'DoSTCBuildIn', tr('Pastes text from the clipboard into the document')),
		(210, '', '-', wx.ITEM_SEPARATOR, None, ''),
		(215, 'IDM_EDIT_SELECTION', tr('Selection'), wx.ITEM_NORMAL, None, ''),

	]),
	('IDM_EDIT_SELECTION',
	[
		(100, 'IDM_EDIT_SELECTION_SELECT_WORD', tr('Select Word') + '\tCtrl+W', wx.ITEM_NORMAL, 'OnEditSelectionWord', tr('Selects current word')),
		(200, 'IDM_EDIT_SELECTION_SELECT_WORD_EXTENT', tr('Select Word Extent') + '\tCtrl+Shift+W', wx.ITEM_NORMAL, 'OnEditSelectionWordExtent', tr('Selects current word include "."')),
		(300, 'IDM_EDIT_SELECTION_SELECT_PHRASE', tr('Match Select (Left First)') + '\tCtrl+E', wx.ITEM_NORMAL, 'OnEditSelectionMatchLeft', tr('Selects the text encluded by (){}[]<>""\'\', matching left first')),
		(400, 'IDM_EDIT_SELECTION_SELECT_PHRASE_RIGHT', tr('Match Select (Right First)') + '\tCtrl+Shift+E', wx.ITEM_NORMAL, 'OnEditSelectionMatchRight', tr('Selects the text encluded by (){}[]<>""\'\', matching right first')),
		(500, 'IDM_EDIT_SELECTION_SELECT_ENLARGE', tr('Enlarge Selection') + '\tCtrl+Alt+E', wx.ITEM_NORMAL, 'OnEditSelectionEnlarge', tr('Enlarges selection')),
		(600, 'IDM_EDIT_SELECTION_SELECT_LINE', tr('Select Line') + '\tCtrl+R', wx.ITEM_NORMAL, 'OnEditSelectionLine', tr('Select current phrase')),
		(700, 'IDM_EDIT_SELECTION_SELECT_ALL', tr('Select All') + '\tE=Ctrl+A', wx.ITEM_NORMAL, 'DoSTCBuildIn', tr('Selects the entire document')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

imagelist = {
	'IDM_EDIT_UNDO':common.unicode_abspath('images/undo.gif'),
	'IDM_EDIT_REDO':common.unicode_abspath('images/redo.gif'),
	'IDM_EDIT_CUT':common.unicode_abspath('images/cut.gif'),
	'IDM_EDIT_COPY':common.unicode_abspath('images/copy.gif'),
	'IDM_EDIT_PASTE':common.unicode_abspath('images/paste.gif'),
}
Mixin.setMixin('mainframe', 'imagelist', imagelist)

def OnEditUndo(win, event):
	win.document.Undo()
Mixin.setMixin('mainframe', 'OnEditUndo', OnEditUndo)

def OnEditRedo(win, event):
	win.document.Redo()
Mixin.setMixin('mainframe', 'OnEditRedo', OnEditRedo)

def DoSTCBuildIn(win, event):
	eid = event.GetId()
	if eid == win.IDM_EDIT_CUT:
		win.document.Cut()
	elif eid == win.IDM_EDIT_COPY:
		win.document.Copy()
	elif eid == win.IDM_EDIT_PASTE:
		win.document.Paste()
	elif eid == win.IDM_EDIT_SELECTION_SELECT_ALL:
		win.document.SelectAll()
Mixin.setMixin('mainframe', 'DoSTCBuildIn', DoSTCBuildIn)

def afterinit(win):
	wx.EVT_UPDATE_UI(win, win.IDM_EDIT_CUT, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDM_EDIT_COPY, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDM_EDIT_PASTE, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDM_EDIT_UNDO, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDM_EDIT_REDO, win.OnUpdateUI)
Mixin.setPlugin('mainframe', 'afterinit', afterinit)

def OnUpdateUI(win, event):
	eid = event.GetId()
	if hasattr(win, 'document') and win.document:
		if eid in [win.IDM_EDIT_CUT, win.IDM_EDIT_COPY]:
			event.Enable(win.document.GetSelectedText and len(win.document.GetSelectedText()) > 0)
		elif eid == win.IDM_EDIT_PASTE:
			event.Enable(bool(win.document.CanPaste()))
		elif eid == win.IDM_EDIT_UNDO:
			event.Enable(bool(win.document.CanUndo()))
		elif eid == win.IDM_EDIT_REDO:
			event.Enable(bool(win.document.CanRedo()))
Mixin.setPlugin('mainframe', 'on_update_ui', OnUpdateUI)

def init(win):
	wx.EVT_UPDATE_UI(win, win.IDPM_CUT, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDPM_COPY, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDPM_PASTE, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDPM_UNDO, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDPM_REDO, win.OnUpdateUI)
	wx.EVT_LEFT_DCLICK(win, win.OnDClick)
	wx.EVT_LEFT_DCLICK(win, win.OnDClick)
Mixin.setPlugin('editor', 'init', init)

def OnUpdateUI(win, event):
	eid = event.GetId()
	if eid in [win.IDPM_CUT, win.IDPM_COPY]:
		event.Enable(len(win.GetSelectedText()) > 0)
	elif eid == win.IDPM_PASTE:
		event.Enable(win.CanPaste())
	elif eid == win.IDPM_UNDO:
		event.Enable(win.CanUndo())
	elif eid == win.IDPM_REDO:
		event.Enable(win.CanRedo())
Mixin.setPlugin('editor', 'on_update_ui', OnUpdateUI)

def OnDClick(win, event):
	if event.ControlDown():
		win.mainframe.OnEditSelectionWordExtent(event)
	else:
		event.Skip()
Mixin.setMixin('editor', 'OnDClick', OnDClick)

def OnSelectionWord(win, event):
	win.mainframe.OnEditSelectionWord(event)
Mixin.setMixin('editor', 'OnSelectionWord', OnSelectionWord)

def OnEditSelectionWord(win, event):
	pos = win.document.GetCurrentPos()
	start = win.document.WordStartPosition(pos, True)
	end = win.document.WordEndPosition(pos, True)
	win.document.SetSelection(start, end)
Mixin.setMixin('mainframe', 'OnEditSelectionWord', OnEditSelectionWord)

def OnSelectionWordExtent(win, event):
	win.mainframe.OnEditSelectionWordExtent(event)
Mixin.setMixin('editor', 'OnSelectionWordExtent', OnSelectionWordExtent)

def OnEditSelectionWordExtent(win, event):
	pos = win.document.GetCurrentPos()
	start = win.document.WordStartPosition(pos, True)
	end = win.document.WordEndPosition(pos, True)
	if end > start:
		i = start - 1
		while i >= 0:
			if win.document.getChar(i) in win.getWordChars() + '.':
				start -= 1
				i -= 1
			else:
				break
		i = end
		length = win.document.GetLength()
		while i < length:
			if win.document.getChar(i) in win.getWordChars()+ '.':
				end += 1
				i += 1
			else:
				break
	win.document.SetSelection(start, end)
Mixin.setMixin('mainframe', 'OnEditSelectionWordExtent', OnEditSelectionWordExtent)

def OnEditSelectionLine(win, event):
	win.document.SetSelection(*win.document.getLinePositionTuple())
Mixin.setMixin('mainframe', 'OnEditSelectionLine', OnEditSelectionLine)

def OnSelectionLine(win, event):
	win.mainframe.OnEditSelectionLine(event)
Mixin.setMixin('editor', 'OnSelectionLine', OnSelectionLine)

def OnEditSelectionMatchLeft(win, event):
	pos = win.document.GetCurrentPos()
	text = win.document.getRawText()

	token = [('\'', '\''), ('"', '"'), ('(', ')'), ('[', ']'), ('{', '}'), ('<', '>')]
	start, match = findLeft(text, pos, token)
	if start > -1:
		end, match = findRight(text, pos, token, match)
		if end > -1:
			win.document.SetSelection(start, end)
Mixin.setMixin('mainframe', 'OnEditSelectionMatchLeft', OnEditSelectionMatchLeft)

def OnSelectionMatchLeft(win, event):
	event.SetId(win.mainframe.IDM_EDIT_SELECTION_SELECT_PHRASE)
	win.mainframe.OnEditSelectionMatchLeft(event)
Mixin.setMixin('editor', 'OnSelectionMatchLeft', OnSelectionMatchLeft)

def OnEditSelectionMatchRight(win, event):
	pos = win.document.GetCurrentPos()
	text = win.document.getRawText()

	token = [('\'', '\''), ('"', '"'), ('(', ')'), ('[', ']'), ('{', '}'), ('<', '>')]
	end, match = findRight(text, pos, token)
	if end > -1:
		start, match = findLeft(text, pos, token, match)
		if start > -1:
			win.document.SetSelection(end, start)
Mixin.setMixin('mainframe', 'OnEditSelectionMatchRight', OnEditSelectionMatchRight)

def OnSelectionMatchRight(win, event):
	win.mainframe.OnEditSelectionMatchRight(event)
Mixin.setMixin('editor', 'OnSelectionMatchRight', OnSelectionMatchRight)

def findLeft(text, pos, token, match=None):
	countleft = {}
	countright = {}
	leftlens = {}
	rightlens = {}
	for left, right in token:
		countleft[left] = 0
		countright[right] = 0
		leftlens[left] = len(left)
		rightlens[right] = len(right)
	i = pos
	while i >= 0:
		for left, right in token:
			if text.endswith(left, 0, i):
				if countright[right] == 0:
					if (not match) or (match and (match == right)):
						return i, left
					else:
						i -= leftlens[left]
						break
				else:
					countright[right] -= 1
					i -= leftlens[left]
					break
			elif text.endswith(right, 0, i):
				countright[right] += 1
				i -= rightlens[right]
				break
		else:
			i -= 1
	return -1, ''

def findRight(text, pos, token, match=None):
	countleft = {}
	countright = {}
	leftlens = {}
	rightlens = {}
	for left, right in token:
		countleft[left] = 0
		countright[right] = 0
		leftlens[left] = len(left)
		rightlens[right] = len(right)
	i = pos
	length = len(text)
	while i < length:
		for left, right in token:
			if text.startswith(right, i):
				if countleft[left] == 0:
					if (not match) or (match and (match == left)):
						return i, right
					else:
						i += rightlens[right]
						break
				else:
					countleft[left] -= 1
					i += rightlens[right]
					break
			elif text.startswith(left, i):
				countleft[left] += 1
				i += leftlens[left]
				break
		else:
			i += 1
	return -1, ''

def OnEditSelectionEnlarge(win, event):
	start, end = win.document.GetSelection()
	if end - start > 0:
		if win.document.GetCharAt(start-1) < 127:
			start -= 1
		if win.document.GetCharAt(end + 1) < 127:
			end += 1
		win.document.SetSelection(start, end)
Mixin.setMixin('mainframe', 'OnEditSelectionEnlarge', OnEditSelectionEnlarge)

def OnSelectionEnlarge(win, event):
	win.mainframe.OnEditSelectionEnlarge(event)
Mixin.setMixin('editor', 'OnSelectionEnlarge', OnSelectionEnlarge)