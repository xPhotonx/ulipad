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
#	$Id: mCase.py 93 2005-10-11 02:51:02Z limodou $

__doc__ = 'uppercase and lowercase processing'

from modules import Mixin
import wx
import wx.stc

menulist = [ ('IDM_EDIT',
	[
		(260, 'IDM_EDIT_CASE', tr('Case'), wx.ITEM_NORMAL, None, ''),
	]),
	('IDM_EDIT_CASE',
	[
		(100, 'IDM_EDIT_CASE_UPPER_CASE', tr('Upper Case') + '\tE=Ctrl+U', wx.ITEM_NORMAL, 'OnEditCaseUpperCase', tr('Changes the selected text to upper case')),
		(200, 'IDM_EDIT_CASE_LOWER_CASE', tr('Lower Case') + '\tE=Ctrl+Shift+U', wx.ITEM_NORMAL, 'OnEditCaseLowerCase', tr('Changes the selected text to lower case')),
		(300, 'IDM_EDIT_CASE_INVERT_CASE', tr('Invert Case'), wx.ITEM_NORMAL, 'OnEditCaseInvertCase', tr('Inverts the case of the selected text')),
		(400, 'IDM_EDIT_CASE_CAPITALIZE', tr('Capitalize'), wx.ITEM_NORMAL, 'OnEditCaseCapitalize', tr('Capitalizes all words of the selected text')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

popmenulist = [ (None, #parent menu id
	[
		(230, 'IDPM_CASE', tr('Case'), wx.ITEM_NORMAL, None, ''),
	]),
	('IDPM_CASE',
	[
		(100, 'IDPM_CASE_UPPER_CASE', tr('Upper Case') + '\tCtrl+U', wx.ITEM_NORMAL, 'OnCaseUpperCase', tr('Changes the selected text to upper case')),
		(200, 'IDPM_CASE_LOWER_CASE', tr('Lower Case') + '\tCtrl+Shift+U', wx.ITEM_NORMAL, 'OnCaseLowerCase', tr('Changes the selected text to lower case')),
		(300, 'IDPM_CASE_INVERT_CASE', tr('Invert Case'), wx.ITEM_NORMAL, 'OnCaseInvertCase', tr('Inverts the case of the selected text')),
		(400, 'IDPM_CASE_CAPITALIZE', tr('Capitalize'), wx.ITEM_NORMAL, 'OnCaseCapitalize', tr('Capitalizes all words of the selected text')),
	]),
]
Mixin.setMixin('editor', 'popmenulist', popmenulist)

def OnEditCaseUpperCase(win, event):
	win.document.CmdKeyExecute(wx.stc.STC_CMD_UPPERCASE)
Mixin.setMixin('mainframe', 'OnEditCaseUpperCase', OnEditCaseUpperCase)

def OnEditCaseLowerCase(win, event):
	win.document.CmdKeyExecute(wx.stc.STC_CMD_LOWERCASE)
Mixin.setMixin('mainframe', 'OnEditCaseLowerCase', OnEditCaseLowerCase)

def OnEditCaseInvertCase(win, event):
	text = win.document.GetSelectedText()
	if len(text) == 0:
		text = win.document.GetCharAt(win.document.GetCurrentPos())
	text = text.swapcase()
	win.document.CmdKeyExecute(wx.stc.STC_CMD_CLEAR)
	win.document.AddText(text)
Mixin.setMixin('mainframe', 'OnEditCaseInvertCase', OnEditCaseInvertCase)

def OnEditCaseCapitalize(win, event):
	text = win.document.GetSelectedText()
	if len(text) > 0:
		s=[]
		word = False
		for ch in text:
			if 'a' <= ch.lower() <= 'z':
				if word == False:
					ch = ch.upper()
					word = True
			else:
				if word == True:
					word = False
			s.append(ch)
		text = ''.join(s)
		win.document.ReplaceSelection(text)
Mixin.setMixin('mainframe', 'OnEditCaseCapitalize', OnEditCaseCapitalize)

def OnCaseUpperCase(win, event):
	event.SetId(win.mainframe.IDM_EDIT_CASE_UPPER_CASE)
	OnEditCaseUpperCase(win.mainframe, event)
Mixin.setMixin('editor', 'OnCaseUpperCase', OnCaseUpperCase)

def OnCaseLowerCase(win, event):
	event.SetId(win.mainframe.IDM_EDIT_CASE_LOWER_CASE)
	OnEditCaseLowerCase(win.mainframe, event)
Mixin.setMixin('editor', 'OnCaseLowerCase', OnCaseLowerCase)

def OnCaseInvertCase(win, event):
	event.SetId(win.mainframe.IDM_EDIT_CASE_INVERT_CASE)
	OnEditCaseInvertCase(win.mainframe, event)
Mixin.setMixin('editor', 'OnCaseInvertCase', OnCaseInvertCase)

def OnCaseCapitalize(win, event):
	event.SetId(win.mainframe.IDM_EDIT_CASE_CAPITALIZE)
	OnEditCaseCapitalize(win.mainframe, event)
Mixin.setMixin('editor', 'OnCaseCapitalize', OnCaseCapitalize)

def init(win):
	wx.EVT_UPDATE_UI(win, win.IDM_EDIT_CASE_CAPITALIZE, win.OnUpdateUI)
Mixin.setPlugin('mainframe', 'init', init)

def OnUpdateUI(win, event):
	eid = event.GetId()
	if eid == win.IDM_EDIT_CASE_CAPITALIZE:
		event.Enable(win.document.GetSelectedText and len(win.document.GetSelectedText()) > 0)
Mixin.setPlugin('mainframe', 'on_update_ui', OnUpdateUI)

def init(win):
	wx.EVT_UPDATE_UI(win, win.IDPM_CASE_CAPITALIZE, win.OnUpdateUI)
Mixin.setPlugin('editor', 'init', init)

def OnUpdateUI(win, event):
	eid = event.GetId()
	if eid == win.IDPM_CASE_CAPITALIZE:
		event.Enable(len(win.GetSelectedText()) > 0)
Mixin.setPlugin('editor', 'on_update_ui', OnUpdateUI)

