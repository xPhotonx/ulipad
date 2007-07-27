
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
#	$Id: Import.py 176 2005-11-22 02:46:37Z limodou $


#-----------------------  mMainframe.py ------------------

from modules import Mixin
import wx

def getmainframe(app, filenames):
    from MainFrame import MainFrame

    app.mainframe = frame = MainFrame(app, filenames)
    frame.workpath = app.workpath
    frame.userpath = app.userpath
    frame.afterinit()
    frame.editctrl.openPage()
    return frame
Mixin.setPlugin('app', 'getmainframe', getmainframe)



#-----------------------  mPreference.py ------------------

from modules import Mixin
import wx

menulist = [ (None,
	[
		(600, 'IDM_OPTION', tr('Option'), wx.ITEM_NORMAL, None, ''),
	]),
	('IDM_OPTION',
	[
		(100, 'IDM_OPTION_PREFERENCE', tr('Preference...'), wx.ITEM_NORMAL, 'OnOptionPreference', tr('Setup program preferences')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

def beforegui(win):
	import Preference

	win.pref = Preference.Preference()
	win.pref.load()
	win.pref.printValues()
Mixin.setPlugin('app', 'beforegui', beforegui, Mixin.HIGH)

def OnOptionPreference(win, event):
	import PrefDialog

	dlg = PrefDialog.PrefDialog(win)
	dlg.ShowModal()
Mixin.setMixin('mainframe', 'OnOptionPreference', OnOptionPreference)



#-----------------------  mMainSubFrame.py ------------------

from modules import Mixin
import wx
import MyPanel

class MainSubFrame(MyPanel.SashPanel, Mixin.Mixin):

	__mixinname__ = 'mainsubframe'

	def __init__(self, parent, mainframe):
		self.initmixin()
		self.parent = parent
		self.mainframe = mainframe
		self.mainframe.panel = self

		MyPanel.SashPanel.__init__(self, parent, ['left', 'right', 'bottom'])

		self.callplugin('init', self)

def init(win):
	return MainSubFrame(win, win)
Mixin.setPlugin('mainframe', 'init', init)



#-----------------------  mEditorCtrl.py ------------------

from modules import Mixin
import wx
import os.path
import EncodingDialog
from MyUnicodeException import MyUnicodeException
from modules.Debug import error

menulist = [ ('IDM_FILE',
	[
		(100, 'IDM_FILE_NEW', tr('New') + '\tCtrl+N', wx.ITEM_NORMAL, 'OnFileNew', tr('Creates a new document')),
		(110, 'IDM_FILE_OPEN', tr('Open') + '\tCtrl+O', wx.ITEM_NORMAL, 'OnFileOpen', tr('Opens an existing document')),
		(120, 'IDM_FILE_REOPEN', tr('Reopen') + '\tCtrl+Shift+O', wx.ITEM_NORMAL, 'OnFileReOpen', tr('Reopens an existing document')),
		(140, 'IDM_FILE_CLOSE', tr('Close') + '\tCtrl+F4', wx.ITEM_NORMAL, 'OnFileClose', tr('Closes an opened document')),
		(150, 'IDM_FILE_CLOSE_ALL', tr('Close All'), wx.ITEM_NORMAL, 'OnFileCloseAll', tr('Closes all document windows')),
		(160, '', '-', wx.ITEM_SEPARATOR, None, ''),
		(170, 'IDM_FILE_SAVE', tr('Save') + '\tCtrl+S', wx.ITEM_NORMAL, 'OnFileSave', tr('Saves an opened document using the same filename')),
		(180, 'IDM_FILE_SAVE_AS', tr('Save As'), wx.ITEM_NORMAL, 'OnFileSaveAs', tr('Saves an opened document to a specified filename')),
		(190, 'IDM_FILE_SAVE_ALL', tr('Save All'), wx.ITEM_NORMAL, 'OnFileSaveAll', tr('Saves all documents')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

popmenulist = [ (None,
	[
		(100, 'IDPM_FILE_CLOSE', tr('Close') + '\tCtrl+F4', wx.ITEM_NORMAL, 'OnPopUpMenu', tr('Closes an opened document')),
		(200, 'IDPM_FILE_CLOSE_ALL', tr('Close All'), wx.ITEM_NORMAL, 'OnPopUpMenu', tr('Closes all document windows')),
		(250, '', '-', wx.ITEM_SEPARATOR, None, ''),
		(300, 'IDPM_FILE_SAVE', tr('Save') + '\tCtrl+S', wx.ITEM_NORMAL, 'OnPopUpMenu', tr('Saves an opened document using the same filename')),
		(400, 'IDPM_FILE_SAVE_AS', tr('Save As'), wx.ITEM_NORMAL, 'OnPopUpMenu', 'tr(Saves an opened document to a specified filename)'),
		(500, 'IDPM_FILE_SAVE_ALL', tr('Save All'), wx.ITEM_NORMAL, 'OnPopUpMenu', tr('Saves all documents')),
	]),
]
Mixin.setMixin('editctrl', 'popmenulist', popmenulist)

imagelist = {
	'IDM_FILE_NEW':'images/new.gif',
	'IDM_FILE_OPEN':'images/open.gif',
	'IDM_FILE_CLOSE':'images/close.gif',
	'IDM_FILE_SAVE':'images/save.gif',
	'IDM_FILE_SAVEALL':'images/saveall.gif',
}
Mixin.setMixin('mainframe', 'imagelist', imagelist)

imagelist = {
	'IDPM_FILE_CLOSE':'images/close.gif',
	'IDPM_FILE_SAVE':'images/save.gif',
	'IDPM_FILE_SAVEALL':'images/saveall.gif',
}
Mixin.setMixin('editctrl', 'imagelist', imagelist)

def neweditctrl(win):
	from EditorFactory import EditorFactory

	win.notebook = EditorFactory(win.top, win.mainframe)
Mixin.setPlugin('mainsubframe', 'init', neweditctrl)

filewildchar = [
	tr('All files (*.*)|*'),
]
Mixin.setMixin('mainframe', 'filewildchar', filewildchar)

def init(win):
	wx.EVT_CLOSE(win, win.OnClose)
Mixin.setPlugin('mainframe', 'init', init)

def OnClose(win, event):
	if event.CanVeto():
		for document in win.editctrl.list:
			r = win.CloseFile(document, True)
			if r == wx.ID_CANCEL:
				return
		if win.execplugin('closewindow', win) == wx.ID_CANCEL:
			return
	win.callplugin('afterclosewindow', win)
	event.Skip()
Mixin.setMixin('mainframe', 'OnClose', OnClose)

def OnFileNew(win, event):
	win.editctrl.new()
Mixin.setMixin('mainframe', 'OnFileNew', OnFileNew)

def OnFileOpen(win, event):
	dlg = wx.FileDialog(win, tr("Open"), win.pref.last_dir, "", '|'.join(win.filewildchar), wx.OPEN|wx.HIDE_READONLY|wx.MULTIPLE)
	dlg.SetFilterIndex(getFilterIndex(win))
	if dlg.ShowModal() == wx.ID_OK:
		encoding = win.execplugin('getencoding', win, win)
		for filename in dlg.GetPaths():
			win.editctrl.new(filename, encoding)
		dlg.Destroy()
Mixin.setMixin('mainframe', 'OnFileOpen', OnFileOpen)

def getFilterIndex(win):
	if len(win.pref.recent_files) > 0:
		filename = win.pref.recent_files[0]
		ext = os.path.splitext(filename)[1]
		for i, v in enumerate(win.filewildchar):
			s = v.split('|')[1]
			for wildchar in s.split(';'):
				if wildchar.endswith(ext):
					return i
			else:
				continue
	return 0

def OnFileReOpen(win, event):
	if win.document.isModified():
		dlg = wx.MessageDialog(win, tr("This document has been modified,\ndo you really want to reload the file?"), tr("Reopen file..."), wx.YES_NO|wx.ICON_QUESTION)
		answer = dlg.ShowModal()
		dlg.Destroy()
		if answer != wx.ID_YES:
			return
	win.document.openfile(win.document.filename)
	win.editctrl.switch(win.document)
Mixin.setMixin('mainframe', 'OnFileReOpen', OnFileReOpen)

def OnFileClose(win, event):
	win.CloseFile(win.document)
	if len(win.editctrl.list) == 0:
		win.editctrl.new()
Mixin.setMixin('mainframe', 'OnFileClose', OnFileClose)

def OnFileCloseAll(win, event):
	i = len(win.editctrl.list) - 1
	while i > -1:
		document = win.editctrl.list[i]
		if not document.opened:
			win.editctrl.DeletePage(i)
			del win.editctrl.list[i]
		i -= 1

	k = len(win.editctrl.list)
	for i in range(k):
		document = win.editctrl.list[0]
		r = win.CloseFile(document)
		if r == wx.ID_CANCEL:
			break
	if len(win.editctrl.list) == 0:
		win.editctrl.new()
Mixin.setMixin('mainframe', 'OnFileCloseAll', OnFileCloseAll)

def CloseFile(win, document, checkonly = False):
	answer = wx.ID_YES
	if document.isModified():
		d = wx.MessageDialog(win, tr("Would you like to save %s ?") % document.getFilename(),
			tr("Close File"), wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
		answer = d.ShowModal()
		d.Destroy()
		if answer == wx.ID_YES:
			win.SaveFile(document)
		elif answer == wx.ID_CANCEL:
			return answer

	if checkonly == False:
		win.editctrl.lastdocument = None
		win.callplugin('closefile', win, document.filename)
		win.editctrl.closefile(document)
	return answer
Mixin.setMixin('mainframe', 'CloseFile', CloseFile)

def OnFileSave(win, event):
	win.SaveFile(win.document)
Mixin.setMixin('mainframe', 'OnFileSave', OnFileSave)

def OnFileSaveAll(win, event):
	for ctrl in win.editctrl.list:
		if ctrl.opened:
			r = win.SaveFile(ctrl)
Mixin.setMixin('mainframe', 'OnFileSaveAll', OnFileSaveAll)

def OnFileSaveAs(win, event):
	win.SaveFile(win.document, True)
Mixin.setMixin('mainframe', 'OnFileSaveAs', OnFileSaveAs)

def SaveFile(win, ctrl, issaveas=False):
	encoding = None
	if not ctrl.cansavefile():
		return True

	if issaveas or len(ctrl.filename)<=0:
		encoding = win.execplugin('getencoding', win, win)
		dlg = wx.FileDialog(win, tr("Save File %s As") % ctrl.getFilename(), win.pref.last_dir, '', '|'.join(win.filewildchar), wx.SAVE|wx.OVERWRITE_PROMPT)
		dlg.SetFilterIndex(getFilterIndex(win))
		if (dlg.ShowModal() == wx.ID_OK):
			filename = dlg.GetPath()
			dlg.Destroy()

			#check if the filename has been openned, if openned then fail
			for document in win.editctrl.list:
				if (not ctrl is document ) and (filename == document.filename):
					wx.MessageDialog(win, tr("Ths file %s has been openned!\nCann't save new file to it.") % document.getFilename(),
						tr("Save As..."), wx.OK|wx.ICON_INFORMATION).ShowModal()
					return False
		else:
			return False
	else:
		filename = ctrl.filename

	return win.editctrl.savefile(ctrl, filename, encoding)
Mixin.setMixin('mainframe', 'SaveFile', SaveFile)

def init(pref):
	pref.last_dir = ''
Mixin.setPlugin('preference', 'init', init)



#-----------------------  mEditor.py ------------------

from modules import Mixin
from TextPanel import TextPanel

panellist = {'edit':TextPanel}
Mixin.setMixin('editctrl', 'panellist', panellist)



#-----------------------  mComEdit.py ------------------

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



#-----------------------  mToolbar.py ------------------

from modules import Mixin
import wx
from modules import maketoolbar
import os.path
from modules import common

toollist = [
	(100, 'new'),
	(110, 'open'),
	(120, 'save'),
	(130, '|'),
	(140, 'cut'),
	(150, 'copy'),
	(160, 'paste'),
	(170, '|'),
	(180, 'undo'),
	(190, 'redo'),
	(200, '|'),
	(400, 'preference'),
	(900, '|'),
]
Mixin.setMixin('mainframe', 'toollist', toollist)

toolbaritems = {
	'new':(wx.ITEM_NORMAL, 'IDM_FILE_NEW', common.unicode_abspath('images/new.gif'), tr('new'), tr('Creates a new document'), 'OnFileNew'),
	'open':(wx.ITEM_NORMAL, 'IDM_FILE_OPEN', common.unicode_abspath('images/open.gif'), tr('open'), tr('Opens an existing document'), 'OnFileOpen'),
	'save':(wx.ITEM_NORMAL, 'IDM_FILE_SAVE', common.unicode_abspath('images/save.gif'), tr('save'), tr('Saves an opened document using the same filename'), 'OnFileSave'),
	'cut':(wx.ITEM_NORMAL, 'IDM_EDIT_CUT', common.unicode_abspath('images/cut.gif'), tr('cut'), tr('Deletes text from the document and moves it to the clipboard'), 'DoSTCBuildIn'),
	'copy':(wx.ITEM_NORMAL, 'IDM_EDIT_COPY', common.unicode_abspath('images/copy.gif'), tr('copy'), tr('Copies text from the document to the clipboard'), 'DoSTCBuildIn'),
	'paste':(wx.ITEM_NORMAL, 'IDM_EDIT_PASTE', common.unicode_abspath('images/paste.gif'), tr('paste'), tr('Pastes text from the clipboard into the document'), 'DoSTCBuildIn'),
	'undo':(wx.ITEM_NORMAL, 'IDM_EDIT_UNDO', common.unicode_abspath('images/undo.gif'), tr('undo'), tr('Reverse previous editing operation'), 'OnEditUndo'),
	'redo':(wx.ITEM_NORMAL, 'IDM_EDIT_REDO', common.unicode_abspath('images/redo.gif'), tr('redo'), tr('Reverse previous undo operation'), 'OnEditRedo'),
	'preference':(wx.ITEM_NORMAL, 'IDM_OPTION_PREFERENCE', common.unicode_abspath('images/prop.gif'), tr('preference'), tr('Setup program preferences'), 'OnOptionPreference'),
}
Mixin.setMixin('mainframe', 'toolbaritems', toolbaritems)

def beforeinit(win):
	maketoolbar.maketoolbar(win, win.toollist, win.toolbaritems)
Mixin.setPlugin('mainframe', 'beforeinit', beforeinit)



#-----------------------  mIcon.py ------------------

import wx
import os
from modules import Mixin
from modules import common

iconfile = common.unicode_abspath(os.path.abspath('newedit.ico'))
def init(win):
	icon = wx.EmptyIcon()
	icon.LoadFile(iconfile, wx.BITMAP_TYPE_ICO)
	win.SetIcon(icon)
Mixin.setPlugin('mainframe', 'init', init)



#-----------------------  mRecentFile.py ------------------

from modules import Mixin
import wx
import os.path
from modules import makemenu
from modules import common

menulist = [('IDM_FILE',
	[
		(130, 'IDM_FILE_RECENTFILES', tr('Open Recent File'), wx.ITEM_NORMAL, None, ''),
		(135, 'IDM_FILE_RECENTPATHS', tr('Open Recent Path'), wx.ITEM_NORMAL, None, ''),
	]),
	('IDM_FILE_RECENTFILES',
	[
		(100, 'IDM_FILE_RECENTFILES_ITEMS', tr('(empty)'), wx.ITEM_NORMAL, 'OnOpenRecentFiles', ''),
	]),
	('IDM_FILE_RECENTPATHS',
	[
		(100, 'IDM_FILE_RECENTPATHS_ITEMS', tr('(empty)'), wx.ITEM_NORMAL, 'OnOpenRecentPaths', ''),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

def beforeinit(win):
	win.recentmenu_ids = [win.IDM_FILE_RECENTFILES_ITEMS]
	win.recentpathmenu_ids = [win.IDM_FILE_RECENTPATHS_ITEMS]
	create_recent_menu(win)
	create_recent_path_menu(win)
Mixin.setPlugin('mainframe', 'beforeinit', beforeinit)

preflist = [
	(tr('General'), 100, 'num', 'recent_files_num', tr('Max number of recent files:'), None),
	(tr('General'), 110, 'num', 'recent_paths_num', tr('Max number of recent paths:'), None),
]
Mixin.setMixin('preference', 'preflist', preflist)

def init(pref):
	pref.recent_files = []
	pref.recent_files_num = 10
	pref.recent_paths = []
	pref.recent_paths_num = 10
Mixin.setPlugin('preference', 'init', init)

def afteropenfile(win, filename):
	if filename:
		#deal recent files
		if filename in win.pref.recent_files:
			win.pref.recent_files.remove(filename)
		win.pref.recent_files.insert(0, filename)
		while len(win.pref.recent_files) > win.pref.recent_files_num:
			win.pref.recent_files.pop(-1)
		win.pref.last_dir = os.path.dirname(filename)

		#deal recent path
		path = os.path.dirname(filename)
		if path in win.pref.recent_paths:
			win.pref.recent_paths.remove(path)
		win.pref.recent_paths.insert(0, path)
		while len(win.pref.recent_paths) > win.pref.recent_paths_num:
			win.pref.recent_paths.pop(-1)

		#save pref
		win.pref.save()

		#create menus
		create_recent_menu(win.mainframe)
		create_recent_path_menu(win.mainframe)
Mixin.setPlugin('editor', 'afteropenfile', afteropenfile)
Mixin.setPlugin('editor', 'aftersavefile', afteropenfile)

def create_recent_menu(win):
	menu = makemenu.findmenu(win.menuitems, 'IDM_FILE_RECENTFILES')

	for id in win.recentmenu_ids:
		menu.Delete(id)

	win.recentmenu_ids = []
	if len(win.pref.recent_files) == 0:
		id = win.IDM_FILE_RECENTFILES_ITEMS
		menu.Append(id, tr('(empty)'))
		menu.Enable(id, False)
		win.recentmenu_ids = [id]
	else:
		for i, filename in enumerate(win.pref.recent_files):
			id = wx.NewId()
			win.recentmenu_ids.append(id)
			menu.Append(id, "%d %s" % (i+1, filename))
			wx.EVT_MENU(win, id, win.OnOpenRecentFiles)

def create_recent_path_menu(win):
	menu = makemenu.findmenu(win.menuitems, 'IDM_FILE_RECENTPATHS')

	for id in win.recentpathmenu_ids:
		menu.Delete(id)

	win.recentpathmenu_ids = []
	if len(win.pref.recent_paths) == 0:
		id = win.IDM_FILE_RECENTPATHS_ITEMS
		menu.Append(id, tr('(empty)'))
		menu.Enable(id, False)
		win.recentpathmenu_ids = [id]
	else:
		for i, path in enumerate(win.pref.recent_paths):
			id = wx.NewId()
			win.recentpathmenu_ids.append(id)
			menu.Append(id, "%d %s" % (i+1, path))
			wx.EVT_MENU(win, id, win.OnOpenRecentPaths)

def OnOpenRecentFiles(win, event):
	eid = event.GetId()
	index = win.recentmenu_ids.index(eid)
	filename = win.pref.recent_files[index]
	try:
		f = file(filename)
		f.close()
	except:
		common.showerror(win, tr("Can't open the file [%s]!") % filename)
		del win.pref.recent_files[index]
		win.pref.save()
		create_recent_menu(win)
		return
	win.editctrl.new(filename)
Mixin.setMixin('mainframe', 'OnOpenRecentFiles', OnOpenRecentFiles)

def OnOpenRecentPaths(win, event):
	eid = event.GetId()
	index = win.recentpathmenu_ids.index(eid)
	path = win.pref.recent_paths[index]
	if os.path.exists(path) and os.path.isdir(path):
		dlg = wx.FileDialog(win, tr("Open"), path, "", '|'.join(win.filewildchar), wx.OPEN|wx.HIDE_READONLY|wx.MULTIPLE)
		dlg.SetFilterIndex(getFilterIndex(win))
		if dlg.ShowModal() == wx.ID_OK:
			encoding = win.execplugin('getencoding', win, win)
			for filename in dlg.GetPaths():
				win.editctrl.new(filename, encoding)
			dlg.Destroy()
	else:
		common.showerror(win, tr("Can't open the path [%s]!") % path)
		del win.pref.recent_paths[index]
		win.pref.save()
		create_recent_path_menu(win)
		return
Mixin.setMixin('mainframe', 'OnOpenRecentPaths', OnOpenRecentPaths)

toollist = [
	(115, 'openpath'),
]
Mixin.setMixin('mainframe', 'toollist', toollist)

toolbaritems = {
	'openpath':(wx.ITEM_NORMAL, 'IDM_FILE_OPEN_PATH', common.unicode_abspath('images/paths.gif'), tr('open path'), tr('Open path'), 'OnFileOpenPath'),
}
Mixin.setMixin('mainframe', 'toolbaritems', toolbaritems)

def OnFileOpenPath(win, event):
	eid = event.GetId()
	size = win.toolbar.GetToolSize()
	pos = win.toolbar.GetToolPos(eid)
	menu = wx.Menu()

	if len(win.pref.recent_paths) == 0:
		id = win.IDM_FILE_RECENTPATHS_ITEMS
		menu.Append(id, tr('(empty)'))
		menu.Enable(id, False)
	else:
		for i, path in enumerate(win.pref.recent_paths):
			id = win.recentpathmenu_ids[i]
			menu.Append(id, "%d %s" % (i+1, path))
	win.PopupMenu(menu, (size[0]*pos, size[1]))
	menu.Destroy()
Mixin.setMixin('mainframe', 'OnFileOpenPath', OnFileOpenPath)



#-----------------------  mSearch.py ------------------

"""Search process"""

import wx
from modules import Mixin
import os.path
from modules import common

menulist = [ (None, #parent menu id
	[
		(400, 'IDM_SEARCH', tr('Search'), wx.ITEM_NORMAL, None, ''),
	]),
	('IDM_SEARCH', #parent menu id
	[
		(100, 'IDM_SEARCH_FIND', tr('Find...') + '\tE=Ctrl+F', wx.ITEM_NORMAL, 'OnSearchFind', tr('Find text')),
		(110, 'IDM_SEARCH_DIRECTFIND', tr('Direct Find') + '\tF4', wx.ITEM_NORMAL, 'OnSearchDirectFind', tr('Direct find selected text')),
		(120, 'IDM_SEARCH_REPLACE', tr('Replace...') + '\tE=Ctrl+H', wx.ITEM_NORMAL, 'OnSearchReplace', tr('Find and replace text')),
		(130, 'IDM_SEARCH_FIND_NEXT', tr('Find Next') + '\tF3', wx.ITEM_NORMAL, 'OnSearchFindNext', tr('Find next occurance of text')),
		(140, 'IDM_SEARCH_FIND_PREVIOUS', tr('Find Previous') + '\tShift+F3', wx.ITEM_NORMAL, 'OnSearchFindPrev', tr('Find previous occurance of text')),
		(150, '', '-', wx.ITEM_SEPARATOR, None, ''),
		(160, 'IDM_SEARCH_GOTO_LINE', tr('Go to Line...') + '\tE=Ctrl+G', wx.ITEM_NORMAL, 'OnSearchGotoLine', tr('Goes to specified line in the active document')),
		(170, 'IDM_SEARCH_LAST_MODIFY', tr('Go to Last Modify') + '\tE=Ctrl+B', wx.ITEM_NORMAL, 'OnSearchLastModify', tr('Goes to the last modify position')),

	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

imagelist = {
	'IDM_SEARCH_FIND':common.unicode_abspath('images/find.gif'),
	'IDM_SEARCH_REPLACE':common.unicode_abspath('images/replace.gif'),
	'IDM_SEARCH_FIND_NEXT':common.unicode_abspath('images/findnext.gif'),
}
Mixin.setMixin('mainframe', 'imagelist', imagelist)

toollist = [
	(220, 'find'),
	(230, 'replace'),
	(240, '|'),
]
Mixin.setMixin('mainframe', 'toollist', toollist)

toolbaritems = {
	'find':(wx.ITEM_NORMAL, 'IDM_SEARCH_FIND', common.unicode_abspath('images/find.gif'), tr('find'), tr('Find text'), 'OnSearchFind'),
	'replace':(wx.ITEM_NORMAL, 'IDM_SEARCH_REPLACE', common.unicode_abspath('images/replace.gif'), tr('replace'), tr('Find and replace text'), 'OnSearchReplace'),
}
Mixin.setMixin('mainframe', 'toolbaritems', toolbaritems)

def afterinit(win):
	import FindReplaceDialog

	win.finder = FindReplaceDialog.Finder()
Mixin.setPlugin('mainframe', 'afterinit', afterinit)

def on_document_enter(win, document):
	win.mainframe.finder.setWindow(document)
Mixin.setPlugin('editctrl', 'on_document_enter', on_document_enter)

findresfile = common.unicode_abspath('resources/finddialog.xrc')

def OnSearchFind(win, event):
	from modules import Resource
	from modules import i18n
	import FindReplaceDialog

	filename = i18n.makefilename(findresfile, win.app.i18n.lang)
	dlg = Resource.loadfromresfile(filename, win, FindReplaceDialog.FindDialog, 'FindDialog', win.finder)
	dlg.Show()
Mixin.setMixin('mainframe', 'OnSearchFind', OnSearchFind)

def OnSearchDirectFind(win, event):
	text = win.document.GetSelectedText()
	if len(text) > 0:
		win.finder.findtext = text
		win.finder.find(0)
Mixin.setMixin('mainframe', 'OnSearchDirectFind', OnSearchDirectFind)

def OnSearchReplace(win, event):
	from modules import Resource
	from modules import i18n
	import FindReplaceDialog

	filename = i18n.makefilename(findresfile, win.app.i18n.lang)
	filename = i18n.makefilename(findresfile, win.app.i18n.lang)
	dlg = Resource.loadfromresfile(filename, win, FindReplaceDialog.FindReplaceDialog, 'FindReplaceDialog', win.finder)
	dlg.Show()
Mixin.setMixin('mainframe', 'OnSearchReplace', OnSearchReplace)

def OnSearchFindNext(win, event):
	win.finder.find(0)
Mixin.setMixin('mainframe', 'OnSearchFindNext', OnSearchFindNext)

def OnSearchFindPrev(win, event):
	win.finder.find(1)
Mixin.setMixin('mainframe', 'OnSearchFindPrev', OnSearchFindPrev)

preflist = [
	(tr('General'), 120, 'num', 'max_number', tr('Max number of saved items:'), None)
]
Mixin.setMixin('preference', 'preflist', preflist)

def init(pref):
	pref.max_number  = 20
	pref.findtexts = []
	pref.replacetexts = []
Mixin.setPlugin('preference', 'init', init)

def OnSearchGotoLine(win, event):
	from modules import Entry

	line = win.document.GetCurrentLine() + 1
	dlg = Entry.MyTextEntry(win, tr("Go to Line..."), tr("Enter the Line Number:"), str(line))
	answer = dlg.ShowModal()
	if answer == wx.ID_OK:
		try:
			line = int(dlg.GetValue())
		except:
			return
		else:
			win.document.GotoLine(line-1)
Mixin.setMixin('mainframe', 'OnSearchGotoLine', OnSearchGotoLine)

def init(win):
	win.lastmodify = -1
Mixin.setPlugin('editor', 'init', init, Mixin.HIGH)

def OnSearchLastModify(win, event):
	if win.document.lastmodify > -1:
		win.document.GotoPos(win.document.lastmodify)
Mixin.setMixin('mainframe', 'OnSearchLastModify', OnSearchLastModify)

def OnModified(win, event):
	for flag in (wx.stc.STC_MOD_INSERTTEXT, wx.stc.STC_MOD_DELETETEXT,
		wx.stc.STC_PERFORMED_UNDO,
		wx.stc.STC_PERFORMED_REDO):
		if event.GetModificationType() & flag:
			win.lastmodify = event.GetPosition()
			return
Mixin.setPlugin('editor', 'on_modified', OnModified)



#-----------------------  mPosition.py ------------------

from modules import Mixin
import wx
import wx.stc

def init(win):
	wx.EVT_KEY_UP(win, win.OnKeyUp)
	wx.EVT_LEFT_UP(win, win.OnMouseUp)
Mixin.setPlugin('editor', 'init', init)

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



#-----------------------  mLineending.py ------------------

from modules import Mixin
import wx
import wx.stc

eolmess = [tr(r"Unix Mode ('\n')"), tr(r"DOS/Windows Mode ('\r\n')"), tr(r"Mac Mode ('\r')")]

def beforeinit(win):
	win.lineendingsaremixed = False
	win.eolmode = win.pref.default_eol_mode
	win.eols = {0:wx.stc.STC_EOL_LF, 1:wx.stc.STC_EOL_CRLF, 2:wx.stc.STC_EOL_CR}
	win.eolstr = {0:'UNIX', 1:'WIN', 2:'MAC'}
	win.eolmess = eolmess
	win.SetEOLMode(win.eols[win.eolmode])
Mixin.setPlugin('editor', 'init', beforeinit)

preflist = [
	(tr('Document'), 190, 'choice', 'default_eol_mode', tr('Default line ending used in document:'), eolmess)
]
Mixin.setMixin('preference', 'preflist', preflist)

def init(pref):
	if wx.Platform == '__WXMSW__':
		pref.default_eol_mode = 1
	else:
		pref.default_eol_mode = 0
Mixin.setPlugin('preference', 'init', init)

menulist = [ ('IDM_DOCUMENT',
	[
		(120, 'IDM_DOCUMENT_EOL_CONVERT', tr('Convert Line Ending'), wx.ITEM_NORMAL, None, ''),
	]),
	('IDM_DOCUMENT_EOL_CONVERT',
	[
		(100, 'IDM_DOCUMENT_EOL_CONVERT_PC', tr('Convert to Windows Format'), wx.ITEM_NORMAL, 'OnDocumentEolConvertWin', tr('Convert line ending to windows format')),
		(200, 'IDM_DOCUMENT_EOL_CONVERT_UNIX', tr('Convert to Unix Format'), wx.ITEM_NORMAL, 'OnDocumentEolConvertUnix', tr('Convert line ending to unix format')),
		(300, 'IDM_DOCUMENT_EOL_CONVERT_MAX', tr('Convert to MAC Format'), wx.ITEM_NORMAL, 'OnDocumentEolConvertMac', tr('Convert line ending to mac format')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

def setEOLMode(win, mode):
	win.lineendingsaremixed = False
	win.eolmode = mode
	win.ConvertEOLs(win.eols[mode])
	win.SetEOLMode(win.eols[mode])
	win.mainframe.SetStatusText(win.eolstr[mode], 3)

def OnDocumentEolConvertWin(win, event):
	setEOLMode(win.document, 1)
Mixin.setMixin('mainframe', 'OnDocumentEolConvertWin', OnDocumentEolConvertWin)

def OnDocumentEolConvertUnix(win, event):
	setEOLMode(win.document, 0)
Mixin.setMixin('mainframe', 'OnDocumentEolConvertUnix', OnDocumentEolConvertUnix)

def OnDocumentEolConvertMac(win, event):
	setEOLMode(win.document, 2)
Mixin.setMixin('mainframe', 'OnDocumentEolConvertMac', OnDocumentEolConvertMac)

def fileopentext(win, stext):
	text = stext[0]

	win.lineendingsaremixed = False

	eollist = "".join(map(getEndOfLineCharacter, text))

	len_win = eollist.count('\r\n')
	len_unix = eollist.count('\n')
	len_mac = eollist.count('\r')
	if len_mac > 0 and len_unix == 0:
		win.eolmode = 2
	elif len_win == len_unix:
		win.eolmode = 1
	elif len_unix > 0 and len_win == 0 and len_mac == 0:
		win.eolmode = 0
	else:
		win.lineendingsaremixed = True
Mixin.setPlugin('editor', 'openfiletext', fileopentext)

def afteropenfile(win, filename):
	if win.lineendingsaremixed:
		eolmodestr = "MIX"
		d = wx.MessageDialog(win,
			tr('%s is currently Mixed.\nWould you like to change it to the default?\nThe Default is: %s')
			% (win.filename, win.eolmess[win.pref.default_eol_mode]),
			tr("Mixed Line Ending"), wx.YES_NO | wx.ICON_QUESTION)
		if d.ShowModal() == wx.ID_YES:
			setEOLMode(win, win.pref.default_eol_mode)
			win.savefile(win.filename, win.locale)
	if win.lineendingsaremixed == False:
		eolmodestr = win.eolstr[win.eolmode]
	win.mainframe.SetStatusText(eolmodestr, 3)
	win.SetEOLMode(win.eolmode)
Mixin.setPlugin('editor', 'afteropenfile', afteropenfile)

def savefile(win, filename):
	if not win.lineendingsaremixed:
		setEOLMode(win, win.eolmode)
Mixin.setPlugin('editor', 'savefile', savefile)

def on_document_enter(win, document):
	if document.documenttype == 'edit':
		if document.lineendingsaremixed:
			eolmodestr = "MIX"
		else:
			eolmodestr = document.eolstr[document.eolmode]
		win.mainframe.SetStatusText(eolmodestr, 3)
Mixin.setPlugin('editctrl', 'on_document_enter', on_document_enter)

def getEndOfLineCharacter(character):
	if character == '\r' or character == '\n':
		return character
	return ""



#-----------------------  mDClickCloseFile.py ------------------

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



#-----------------------  mSetScrollWidth.py ------------------

from modules import Mixin
import wx
import wx.stc

def init(win):
	win.SetScrollWidth(1)
	win.maxline = 'WWWW'
Mixin.setPlugin('editor', 'init', init)

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



#-----------------------  mView.py ------------------

from modules import Mixin
import wx
import wx.stc
import os.path
from modules import common

menulist = [ (None,
	[
		(300, 'IDM_VIEW', tr('View'), wx.ITEM_NORMAL, None, ''),
	]),
	('IDM_VIEW', #parent menu id
	[
		(100, 'IDM_VIEW_TAB', tr('Tabs And Spaces'), wx.ITEM_CHECK, 'OnViewTab', tr('Shows or hides space and tab marks')),
		(110, 'IDM_VIEW_INDENTATION_GUIDES', tr('Indentation Guides'), wx.ITEM_CHECK, 'OnViewIndentationGuides', tr('Shows or hides indentation guides')),
		(120, 'IDM_VIEW_RIGHT_EDGE', tr('Right edge indicator'), wx.ITEM_CHECK, 'OnViewRightEdge', tr('Shows or hides right edge indicator')),
		(130, 'IDM_VIEW_ENDOFLINE_MARK', tr('End-of-line marker'), wx.ITEM_CHECK, 'OnViewEndOfLineMark', tr('Shows or hides end-of-line marker')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

def afterinit(win):
	wx.EVT_UPDATE_UI(win, win.IDM_VIEW_TAB, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDM_VIEW_INDENTATION_GUIDES, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDM_VIEW_RIGHT_EDGE, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDM_VIEW_ENDOFLINE_MARK, win.OnUpdateUI)
Mixin.setPlugin('mainframe', 'afterinit', afterinit)

def init(win):
	#show long line indicator
	if win.mainframe.pref.startup_show_longline:
		win.SetEdgeMode(wx.stc.STC_EDGE_LINE)
	else:
		win.SetEdgeMode(wx.stc.STC_EDGE_NONE)

	#long line width
	win.SetEdgeColumn(win.mainframe.pref.edge_column_width)

	#show tabs
	if win.mainframe.pref.startup_show_tabs:
		win.SetViewWhiteSpace(wx.stc.STC_WS_VISIBLEALWAYS)
	else:
		win.SetViewWhiteSpace(wx.stc.STC_WS_INVISIBLE)

	#show indentation guides
	win.SetIndentationGuides(win.mainframe.pref.startup_show_indent_guide)
Mixin.setPlugin('editor', 'init', init)

def OnViewTab(win, event):
	stat = win.document.GetViewWhiteSpace()
	if stat == wx.stc.STC_WS_INVISIBLE:
		win.document.SetViewWhiteSpace(wx.stc.STC_WS_VISIBLEALWAYS)
	elif stat == wx.stc.STC_WS_VISIBLEALWAYS:
		win.document.SetViewWhiteSpace(wx.stc.STC_WS_INVISIBLE)
Mixin.setMixin('mainframe', 'OnViewTab', OnViewTab)

def OnViewIndentationGuides(win, event):
	win.document.SetIndentationGuides(not win.document.GetIndentationGuides())
Mixin.setMixin('mainframe', 'OnViewIndentationGuides', OnViewIndentationGuides)

def init(pref):
	pref.edge_column_width = 100
	pref.startup_show_tabs = False
	pref.startup_show_indent_guide = False
	pref.startup_show_longline = False
Mixin.setPlugin('preference', 'init', init)

preflist = [
	(tr('Document'), 110, 'check', 'startup_show_tabs', tr('Whitespace is visible on startup'), None),
	(tr('Document'), 115, 'check', 'startup_show_indent_guide', tr('Indentation guides is visible on startup'), None),
	(tr('Document'), 120, 'check', 'startup_show_longline', tr('Long line indicator is visible on startup'), None),
	(tr('Document'), 130, 'num', 'edge_column_width', tr('Long line indicator column'), None),
]
Mixin.setMixin('preference', 'preflist', preflist)

def savepreference(mainframe, pref):
	for document in mainframe.editctrl.list:
		if document.CanView():
			document.SetEdgeColumn(mainframe.pref.edge_column_width)
Mixin.setPlugin('prefdialog', 'savepreference', savepreference)

def OnViewRightEdge(win, event):
	flag = win.document.GetEdgeMode()
	if flag == wx.stc.STC_EDGE_NONE:
		k = wx.stc.STC_EDGE_LINE
	else:
		k = wx.stc.STC_EDGE_NONE
	win.document.SetEdgeMode(k)
Mixin.setMixin('mainframe', 'OnViewRightEdge', OnViewRightEdge)

def OnViewEndOfLineMark(win, event):
	win.document.SetViewEOL(not win.document.GetViewEOL())
Mixin.setMixin('mainframe', 'OnViewEndOfLineMark', OnViewEndOfLineMark)

def OnUpdateUI(win, event):
	eid = event.GetId()
	if hasattr(win, 'document') and win.document and win.document.CanView():
		event.Enable(True)
		if eid == win.IDM_VIEW_TAB:
			stat = win.document.GetViewWhiteSpace()
			if stat == wx.stc.STC_WS_INVISIBLE:
				event.Check(False)
			elif stat == wx.stc.STC_WS_VISIBLEALWAYS:
				event.Check(True)
		elif eid == win.IDM_VIEW_INDENTATION_GUIDES:
			event.Check(win.document.GetIndentationGuides())
		elif eid == win.IDM_VIEW_RIGHT_EDGE:
			flag = win.document.GetEdgeMode()
			if flag == wx.stc.STC_EDGE_NONE:
				event.Check(False)
			else:
				event.Check(True)
		elif eid == win.IDM_VIEW_ENDOFLINE_MARK:
			event.Check(win.document.GetViewEOL())
	else:
		if eid in [win.IDM_VIEW_TAB, win.IDM_VIEW_INDENTATION_GUIDES, win.IDM_VIEW_RIGHT_EDGE, win.IDM_VIEW_ENDOFLINE_MARK]:
			event.Enable(False)
Mixin.setPlugin('mainframe', 'on_update_ui', OnUpdateUI)

toollist = [
	(800, '|'),
	(810, 'viewtab'),
]
Mixin.setMixin('mainframe', 'toollist', toollist)

toolbaritems = {
	'viewtab':(wx.ITEM_CHECK, 'IDM_VIEW_TAB', common.unicode_abspath('images/format.gif'), tr('toggle white space'), tr('Shows or hides space and tab marks'), 'OnViewTab'),
}
Mixin.setMixin('mainframe', 'toolbaritems', toolbaritems)



#-----------------------  mFormat.py ------------------

from modules import Mixin
import wx
import wx.stc
from modules import common

menulist = [ ('IDM_EDIT',
	[
		(250, 'IDM_EDIT_FORMAT', tr('Format'), wx.ITEM_NORMAL, None, ''),
	]),
	('IDM_EDIT_FORMAT',
	[
		(100, 'IDM_EDIT_FORMAT_CHOP', tr('Trim Trailing Spaces'), wx.ITEM_NORMAL, 'OnEditFormatChop', tr('Trims trailing white spaces')),
		(110, 'IDM_EDIT_FORMAT_SPACETOTAB', tr('Leading Spaces to Tabs'), wx.ITEM_NORMAL, 'OnEditFormatSpaceToTab', tr('Converts leading spaces to tabs')),
		(120, 'IDM_EDIT_FORMAT_TABTOSPACE', tr('Leading Tabs To Spaces'), wx.ITEM_NORMAL, 'OnEditFormatTabToSpace', tr('Converts leading tabs to spaces')),
		(125, 'IDM_EDIT_FORMAT_ALLTABTOSPACE', tr('ALL Tabs To Spaces'), wx.ITEM_NORMAL, 'OnEditFormatAllTabToSpace', tr('Converts all tabs to spaces')),
		(130, '', '-', wx.ITEM_SEPARATOR, None, ''),
		(140, 'IDM_EDIT_FORMAT_INDENT', tr('Increase Indent') + '\tE=Ctrl+I', wx.ITEM_NORMAL, 'OnEditFormatIndent', tr('Increases the indentation of current line or selected block')),
		(150, 'IDM_EDIT_FORMAT_UNINDENT', tr('Decrease Indent') + '\tE=Ctrl+Shift+I', wx.ITEM_NORMAL, 'OnEditFormatUnindent', tr('Decreases the indentation of current line or selected block')),
		(160, '', '-', wx.ITEM_SEPARATOR, None, ''),
		(170, 'IDM_EDIT_FORMAT_COMMENT', tr('Line Comment...') + '\tE=Ctrl+/', wx.ITEM_NORMAL, 'OnEditFormatComment', tr('Inserts comment sign at the beginning of line')),
		(180, 'IDM_EDIT_FORMAT_UNCOMMENT', tr('Line Uncomment...') + '\tE=Ctrl+\\', wx.ITEM_NORMAL, 'OnEditFormatUncomment', tr('Removes comment sign at the beginning of line')),
		(190, '', '-', wx.ITEM_SEPARATOR, None, ''),
		(200, 'IDM_EDIT_FORMAT_QUOTE', tr('Text Quote...') + '\tE=Ctrl+Q', wx.ITEM_NORMAL, 'OnEditFormatQuote', tr('Quote selected text')),
		(210, 'IDM_EDIT_FORMAT_UNQUOTE', tr('Text Unquote...') + '\tE=Ctrl+Shift+Q', wx.ITEM_NORMAL, 'OnEditFormatUnquote', tr('Unquote selected text')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

popmenulist = [ (None, #parent menu id
	[
		(220, 'IDPM_FORMAT', tr('Format'), wx.ITEM_NORMAL, None, ''),
	]),
	('IDPM_FORMAT',
	[
		(100, 'IDPM_FORMAT_CHOP', tr('Trim Trailing Spaces'), wx.ITEM_NORMAL, 'OnFormatChop', tr('Trims trailing white spaces')),
		(110, 'IDPM_FORMAT_SPACETOTAB', tr('Leading Spaces to Tabs'), wx.ITEM_NORMAL, 'OnFormatSpaceToTab', tr('Converts leading spaces to tabs')),
		(120, 'IDPM_FORMAT_TABTOSPACE', tr('Leading Tabs To Spaces'), wx.ITEM_NORMAL, 'OnFormatTabToSpace', tr('Converts leading tabs to spaces')),
		(125, 'IDPM_FORMAT_ALLTABTOSPACE', tr('ALL Tabs To Spaces'), wx.ITEM_NORMAL, 'OnFormatAllTabToSpace', tr('Converts all tabs to spaces')),
		(130, '', '-', wx.ITEM_SEPARATOR, None, ''),
		(140, 'IDPM_FORMAT_INDENT', tr('Increase Indent') + '\tCtrl+I', wx.ITEM_NORMAL, 'OnFormatIndent', tr('Increases the indentation of current line or selected block')),
		(150, 'IDPM_FORMAT_UNINDENT', tr('Decrease Indent') + '\tCtrl+Shift+I', wx.ITEM_NORMAL, 'OnFormatUnindent', tr('Decreases the indentation of current line or selected block')),
		(160, '', '-', wx.ITEM_SEPARATOR, None, ''),
		(170, 'IDPM_FORMAT_COMMENT', tr('Line Comment...') + '\tCtrl+/', wx.ITEM_NORMAL, 'OnFormatComment', tr('Inserts comment sign at the beginning of line')),
		(180, 'IDPM_FORMAT_UNCOMMENT', tr('Line Uncomment...') + '\tCtrl+\\', wx.ITEM_NORMAL, 'OnFormatUncomment', tr('Removes comment sign at the beginning of line')),
		(190, '', '-', wx.ITEM_SEPARATOR, None, ''),
		(200, 'IDPM_FORMAT_QUOTE', tr('Text Quote...') + '\tCtrl+Q', wx.ITEM_NORMAL, 'OnFormatQuote', tr('Quote selected text')),
		(210, 'IDPM_FORMAT_UNQUOTE', tr('Text Unquote...') + '\tCtrl+Shift+Q', wx.ITEM_NORMAL, 'OnFormatUnquote', tr('Unquote selected text')),
	]),
]
Mixin.setMixin('editor', 'popmenulist', popmenulist)

imagelist = {
	'IDM_EDIT_FORMAT_INDENT':common.unicode_abspath('images/indent.gif'),
	'IDM_EDIT_FORMAT_UNINDENT':common.unicode_abspath('images/unindent.gif'),
}
Mixin.setMixin('mainframe', 'imagelist', imagelist)

imagelist = {
	'IDPM_FORMAT_INDENT':common.unicode_abspath('images/indent.gif'),
	'IDPM_FORMAT_UNINDENT':common.unicode_abspath('images/unindent.gif'),
}
Mixin.setMixin('editor', 'imagelist', imagelist)


def OnEditFormatIndent(win, event):
	win.document.CmdKeyExecute(wx.stc.STC_CMD_TAB)
Mixin.setMixin('mainframe', 'OnEditFormatIndent', OnEditFormatIndent)

def OnEditFormatUnindent(win, event):
	win.document.CmdKeyExecute(wx.stc.STC_CMD_BACKTAB)
Mixin.setMixin('mainframe', 'OnEditFormatUnindent', OnEditFormatUnindent)

def OnFormatIndent(win, event):
	win.CmdKeyExecute(wx.stc.STC_CMD_TAB)
Mixin.setMixin('editor', 'OnFormatIndent', OnFormatIndent)

def OnFormatUnindent(win, event):
	win.CmdKeyExecute(wx.stc.STC_CMD_BACKTAB)
Mixin.setMixin('editor', 'OnFormatUnindent', OnFormatUnindent)

def OnFormatQuote(win, event):
	win.mainframe.OnEditFormatQuote(event)
Mixin.setMixin('editor', 'OnFormatQuote', OnFormatQuote)

def OnFormatUnquote(win, event):
	win.mainframe.OnEditFormatUnquote(event)
Mixin.setMixin('editor', 'OnFormatUnquote', OnFormatUnquote)

def init(pref):
	pref.tabwidth = 4
	pref.last_comment_chars = '#'
Mixin.setPlugin('preference', 'init', init)

preflist = [
	(tr('Document'), 140, 'num', 'tabwidth', tr('Tab width:'), None),
]
Mixin.setMixin('preference', 'preflist', preflist)

def init(win):
	#set tab width
	win.SetTabWidth(win.mainframe.pref.tabwidth)
Mixin.setPlugin('editor', 'init', init)

def savepreference(mainframe, pref):
	for document in mainframe.editctrl.list:
		document.SetTabWidth(mainframe.pref.tabwidth)
Mixin.setPlugin('prefdialog', 'savepreference', savepreference)

def OnEditFormatChop(win, event):
	win.document.BeginUndoAction()
	for i in win.document.getSelectionLines():
		text = win.document.getLineText(i)
		newtext = text.rstrip()
		win.document.replaceLineText(i, newtext)
	win.document.EndUndoAction()
Mixin.setMixin('mainframe', 'OnEditFormatChop', OnEditFormatChop)

def OnFormatChop(win, event):
	win.mainframe.OnEditFormatChop(event)
Mixin.setMixin('editor', 'OnFormatChop', OnFormatChop)

def OnEditFormatComment(win, event):
	from modules import Entry

	dlg = Entry.MyTextEntry(win, tr("Comment..."), tr("Comment Char:"), win.pref.last_comment_chars)
	answer = dlg.ShowModal()
	if answer == wx.ID_OK:
		commentchar = dlg.GetValue()
		if len(commentchar) == 0:
			return
		win.pref.last_comment_chars = commentchar
		win.pref.save()
		win.document.BeginUndoAction()
		for i in win.document.getSelectionLines():
			text = win.document.getLineText(i)
			win.document.replaceLineText(i, commentchar + text)
		win.document.EndUndoAction()
Mixin.setMixin('mainframe', 'OnEditFormatComment', OnEditFormatComment)

def OnFormatComment(win, event):
	win.mainframe.OnEditFormatComment(event)
Mixin.setMixin('editor', 'OnFormatComment', OnFormatComment)

def OnEditFormatUncomment(win, event):
	from modules import Entry

	dlg = Entry.MyTextEntry(win, tr("Comment..."), tr("Comment Char:"), win.pref.last_comment_chars)
	answer = dlg.ShowModal()
	if answer == wx.ID_OK:
		commentchar = dlg.GetValue()
		if len(commentchar) == 0:
			return
		win.pref.last_comment_chars = commentchar
		win.pref.save()
		win.document.BeginUndoAction()
		for i in win.document.getSelectionLines():
			text = win.document.getLineText(i)
			if text.startswith(commentchar):
				win.document.replaceLineText(i, text[len(commentchar):])
		win.document.EndUndoAction()
Mixin.setMixin('mainframe', 'OnEditFormatUncomment', OnEditFormatUncomment)

def OnFormatUncomment(win, event):
	win.mainframe.OnEditFormatUncomment(event)
Mixin.setMixin('editor', 'OnFormatUncomment', OnFormatUncomment)

def OnEditFormatSpaceToTab(win, event):
	win.document.BeginUndoAction()
	for i in win.document.getSelectionLines():
		tabwidth = win.document.GetTabWidth()
		text = win.document.getLineText(i).expandtabs(tabwidth)
		k = 0
		for ch in text:
			if ch == ' ':
				k += 1
			else:
				break
		n, m = divmod(k, tabwidth)
		newtext = '\t'*n + ' '*m + text[k:]
		win.document.replaceLineText(i, newtext)
	win.document.EndUndoAction()
Mixin.setMixin('mainframe', 'OnEditFormatSpaceToTab', OnEditFormatSpaceToTab)

def OnFormatSpaceToTab(win, event):
	win.mainframe.OnEditFormatSpaceToTab(event)
Mixin.setMixin('editor', 'OnFormatSpaceToTab', OnFormatSpaceToTab)

def OnEditFormatAllTabToSpace(win, event):
	win.document.BeginUndoAction()
	for i in win.document.getSelectionLines():
		tabwidth = win.document.GetTabWidth()
		text = win.document.getLineText(i).expandtabs(tabwidth)
		win.document.replaceLineText(i, text)
	win.document.EndUndoAction()
Mixin.setMixin('mainframe', 'OnEditFormatAllTabToSpace', OnEditFormatAllTabToSpace)

def OnFormatAllTabToSpace(win, event):
	win.mainframe.OnEditFormatAllTabToSpace(event)
Mixin.setMixin('editor', 'OnFormatAllTabToSpace', OnFormatAllTabToSpace)

def OnEditFormatTabToSpace(win, event):
	win.document.BeginUndoAction()
	for i in win.document.getSelectionLines():
		tabwidth = win.document.GetTabWidth()
		text = win.document.getLineText(i)
		k = 0
		for j, ch in enumerate(text):
			if ch == '\t':
				k += 1
			else:
				break
		text = ' '*k*tabwidth + text[j:]
		win.document.replaceLineText(i, text)
	win.document.EndUndoAction()
Mixin.setMixin('mainframe', 'OnEditFormatTabToSpace', OnEditFormatTabToSpace)

def OnFormatTabToSpace(win, event):
	win.mainframe.OnEditFormatTabToSpace(event)
Mixin.setMixin('editor', 'OnFormatTabToSpace', OnFormatTabToSpace)

def init(win):
	win.quote_user = False
	win.quote_index = 0
	win.quote_start = ''
	win.quote_end = ''
	win.quoteresfile = common.unicode_abspath('resources/quotedialog.xrc')
Mixin.setPlugin('mainframe', 'init', init)

def OnEditFormatQuote(win, event):
	from modules import Resource
	import QuoteDialog
	from modules import i18n

	text = win.document.GetSelectedText()
	if len(text) > 0:
		filename = i18n.makefilename(win.quoteresfile, win.app.i18n.lang)
		dlg = Resource.loadfromresfile(filename, win, QuoteDialog.MyQuoteDialog, 'QuoteDialog', win)
		answer = dlg.ShowModal()
		dlg.Destroy()
		if answer == wx.ID_OK:
			if win.quote_user:
				start = win.quote_start
				end = win.quote_end
			else:
				start, end = QuoteDialog.quote_string[win.quote_index]
			win.document.BeginUndoAction()
			win.document.ReplaceSelection(start + text + end)
			win.document.EndUndoAction()
Mixin.setMixin('mainframe', 'OnEditFormatQuote', OnEditFormatQuote)

def OnEditFormatUnquote(win, event):
	from modules import Resource
	import QuoteDialog
	from modules import i18n

	text = win.document.GetSelectedText()
	if len(text) > 0:
		filename = i18n.makefilename(win.quoteresfile, win.app.i18n.lang)
		dlg = Resource.loadfromresfile(filename, win, QuoteDialog.MyQuoteDialog, 'QuoteDialog', win)
		answer = dlg.ShowModal()
		dlg.Destroy()
		if answer == wx.ID_OK:
			if win.quote_user:
				start = win.quote_start
				end = win.quote_end
			else:
				start, end = QuoteDialog.quote_string[win.quote_index]
			win.document.BeginUndoAction()
			win.document.ReplaceSelection(text[len(start):-len(end)])
			win.document.EndUndoAction()
Mixin.setMixin('mainframe', 'OnEditFormatUnquote', OnEditFormatUnquote)

def init(win):
	wx.EVT_UPDATE_UI(win, win.IDM_EDIT_FORMAT_QUOTE, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDM_EDIT_FORMAT_UNQUOTE, win.OnUpdateUI)
Mixin.setPlugin('mainframe', 'init', init)

def OnUpdateUI(win, event):
	eid = event.GetId()
	if eid == win.IDM_EDIT_FORMAT_QUOTE:
		event.Enable(win.document and win.document.GetSelectedText and len(win.document.GetSelectedText()) > 0)
	elif eid == win.IDM_EDIT_FORMAT_UNQUOTE:
		event.Enable(win.document and win.document.GetSelectedText and len(win.document.GetSelectedText()) > 0)
Mixin.setPlugin('mainframe', 'on_update_ui', OnUpdateUI)

def init(win):
	wx.EVT_UPDATE_UI(win, win.IDPM_FORMAT_QUOTE, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDPM_FORMAT_UNQUOTE, win.OnUpdateUI)
Mixin.setPlugin('editor', 'init', init)

def OnUpdateUI(win, event):
	eid = event.GetId()
	if eid == win.IDPM_FORMAT_QUOTE:
		event.Enable(len(win.GetSelectedText()) > 0)
	elif eid == win.IDPM_FORMAT_UNQUOTE:
		event.Enable(len(win.GetSelectedText()) > 0)
Mixin.setPlugin('editor', 'on_update_ui', OnUpdateUI)



#-----------------------  mCase.py ------------------

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



#-----------------------  mDocument.py ------------------

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



#-----------------------  mUnicode.py ------------------

__doc__ = 'encoding selection and unicode support'

from modules import Mixin
import wx
import wx.stc
from MyUnicodeException import MyUnicodeException
from modules.Debug import error

def init(pref):
	pref.auto_detect_utf8 = True
Mixin.setPlugin('preference', 'init', init)

preflist = [
	(tr('Document'), 170, 'check', 'auto_detect_utf8', tr('Auto detect UTF-8 encoding'), None),
]
Mixin.setMixin('preference', 'preflist', preflist)

def init(win):
	win.locale = win.defaultlocale
Mixin.setPlugin('editor', 'init', init)

def openfileencoding(win, stext, encoding):
	text = stext[0]

	if not encoding:
		if win.mainframe.pref.auto_detect_utf8:
			encoding = 'utf-8'
		else:
			encoding = win.defaultlocale
	try:
		s = unicode(text, encoding)
		win.locale = encoding
	except:
		if win.mainframe.pref.auto_detect_utf8 and encoding == 'utf-8':
			encoding = win.defaultlocale
			try:
				s = unicode(text, encoding)
				win.locale = encoding
			except:
				error.traceback()
				raise MyUnicodeException(win, tr("Cann't convert file encoding [%s] to unicode!\nThe file cann't be openned!") % encoding,
					tr("Unicode Error"))
		else:
			error.traceback()
			raise MyUnicodeException(win, tr("Cann't convert file encoding [%s] to unicode!\nThe file cann't be openned!") % encoding,
				tr("Unicode Error"))
	stext[0] = s
Mixin.setPlugin('editor', 'openfileencoding', openfileencoding)

def savefileencoding(win, stext, encoding):
	text = stext[0]

	if not encoding:
		encoding = win.locale

	oldencoding = win.locale
	if encoding:
		try:
			s = text.encode(encoding)
			win.locale = encoding
		except:
			error.traceback()
			raise MyUnicodeException(win, tr("Cann't convert file to [%s] encoding!\nThe file cann't be saved!") % encoding,
				tr("Unicode Error"))
	else:
		s = text
	stext[0] = s
Mixin.setPlugin('editor', 'savefileencoding', savefileencoding)



#-----------------------  mBookmark.py ------------------

from modules import Mixin
import wx
import wx.stc

def init(win):
	win.SetMarginWidth(0, 20)
	win.SetMarginType(0, wx.stc.STC_MARGIN_SYMBOL)

	win.SetMarginMask(0, ~wx.stc.STC_MASK_FOLDERS)
	win.MarkerDefine(0, wx.stc.STC_MARK_SHORTARROW, "blue", "blue")
	win.bookmarks = []
Mixin.setPlugin('editor', 'init', init)

menulist = [ ('IDM_SEARCH',
	[
		(180, '', '-', wx.ITEM_SEPARATOR, None, ''),
		(190, 'IDM_SEARCH_BOOKMARK_TOGGLE', tr('Toggle Marker') + '\tF9', wx.ITEM_NORMAL, 'OnSearchBookmarkToggle', tr('Set and clear marker at current line')),
		(200, 'IDM_SEARCH_BOOKMARK_CLEARALL', tr('Clear All Marker') + '\tCtrl+Shift+F9', wx.ITEM_NORMAL, 'OnSearchBookmarkClearAll', tr('Clears all marker from the active document')),
		(210, 'IDM_SEARCH_BOOKMARK_NEXT', tr('Next Marker') + '\tF5', wx.ITEM_NORMAL, 'OnSearchBookmarkNext', tr('Goes to next marker position')),
		(220, 'IDM_SEARCH_BOOKMARK_PREVIOUS', tr('Previous Marker') + '\tShift+F5', wx.ITEM_NORMAL, 'OnSearchBookmarkPrevious', tr('Goes to previous marker position')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

def OnSearchBookmarkToggle(win, event):
	line = win.document.GetCurrentLine()
	marker = win.document.MarkerGet(line)
	if marker:
		win.document.MarkerDelete(line, 0)
	else:
		win.document.MarkerAdd(line, 0)
Mixin.setMixin('mainframe', 'OnSearchBookmarkToggle', OnSearchBookmarkToggle)

def OnSearchBookmarkClearAll(win, event):
	win.document.MarkerDeleteAll(0)
Mixin.setMixin('mainframe', 'OnSearchBookmarkClearAll', OnSearchBookmarkClearAll)

def OnSearchBookmarkNext(win, event):
	line = win.document.GetCurrentLine()
	marker = win.document.MarkerGet(line)
	if marker:
		line += 1
	f = win.document.MarkerNext(line, 1)
	if f > -1:
		win.document.goto(f + 1)
	else:
		f = win.document.MarkerNext(0, 1)
		if f > -1:
			win.document.goto(f + 1)
Mixin.setMixin('mainframe', 'OnSearchBookmarkNext', OnSearchBookmarkNext)

def OnSearchBookmarkPrevious(win, event):
	line = win.document.GetCurrentLine()
	marker = win.document.MarkerGet(line)
	if marker:
		line -= 1
	f = win.document.MarkerPrevious(line, 1)
	if f > -1:
		win.document.goto(f + 1)
	else:
		f = win.document.MarkerPrevious(win.document.GetLineCount()-1, 1)
		if f > -1:
			win.document.goto(f + 1)
Mixin.setMixin('mainframe', 'OnSearchBookmarkPrevious', OnSearchBookmarkPrevious)



#-----------------------  mFolder.py ------------------

from modules import Mixin
import wx
import wx.stc

def init(pref):
	pref.use_folder = False
Mixin.setPlugin('preference', 'init', init)

preflist = [
	(tr('Document'), 180, 'check', 'use_folder', tr('Use code fold'), None),
]
Mixin.setMixin('preference', 'preflist', preflist)

def savepreference(mainframe, pref):
	for document in mainframe.editctrl.list:
		if document.enablefolder:
			if pref.use_folder:
				document.SetMarginWidth(2, 16)
			else:
				document.SetMarginWidth(2, 0)
Mixin.setPlugin('prefdialog', 'savepreference', savepreference)

def init(win):
	win.enablefolder = False
	win.SetMarginType(2, wx.stc.STC_MARGIN_SYMBOL) #margin 2 for symbols
	win.SetMarginMask(2, wx.stc.STC_MASK_FOLDERS)  #set up mask for folding symbols
	win.SetMarginSensitive(2, True)           #this one needs to be mouse-aware


	#define folding markers
	win.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEREND,     wx.stc.STC_MARK_BOXPLUSCONNECTED,  "white", "black")
	win.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.stc.STC_MARK_BOXMINUSCONNECTED, "white", "black")
	win.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERMIDTAIL, wx.stc.STC_MARK_TCORNER,  "white", "black")
	win.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERTAIL,    wx.stc.STC_MARK_LCORNER,  "white", "black")
	win.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERSUB,     wx.stc.STC_MARK_VLINE,    "white", "black")
	win.MarkerDefine(wx.stc.STC_MARKNUM_FOLDER,        wx.stc.STC_MARK_BOXPLUS,  "white", "black")
	win.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPEN,    wx.stc.STC_MARK_BOXMINUS, "white", "black")
Mixin.setPlugin('editor', 'init', init)

def colourize(win):
	if win.enablefolder:
		if hasattr(win, 'pref'):
			if win.pref.use_folder:
				win.SetMarginWidth(2, 16)
				return
	win.SetMarginWidth(2, 0)	#used as folder

Mixin.setPlugin('lexerbase', 'colourize', colourize)

def OnMarginClick(win, event):
	# fold and unfold as needed
	if event.GetMargin() == 2:
		if event.GetControl() and event.GetShift():
			FoldAll(win)
		else:
			lineClicked = win.LineFromPosition(event.GetPosition())
			if win.GetFoldLevel(lineClicked) & wx.stc.STC_FOLDLEVELHEADERFLAG:
				if event.GetShift():
					win.SetFoldExpanded(lineClicked, True)
					Expand(win, lineClicked, True, True, 1)
				elif event.GetControl():
					if win.GetFoldExpanded(lineClicked):
						win.SetFoldExpanded(lineClicked, False)
						Expand(win, lineClicked, False, True, 0)
					else:
						win.SetFoldExpanded(lineClicked, True)
						Expand(win, lineClicked, True, True, 100)
				else:
					win.ToggleFold(lineClicked)
Mixin.setPlugin('editor', 'on_margin_click', OnMarginClick)

def FoldAll(win):
	lineCount = win.GetLineCount()
	expanding = True

	# find out if we are folding or unfolding
	for lineNum in range(lineCount):
		if win.GetFoldLevel(lineNum) & wx.stc.STC_FOLDLEVELHEADERFLAG:
			expanding = not win.GetFoldExpanded(lineNum)
			break;

	lineNum = 0
	while lineNum < lineCount:
		level = win.GetFoldLevel(lineNum)
		if level & wx.stc.STC_FOLDLEVELHEADERFLAG and \
		   (level & wx.stc.STC_FOLDLEVELNUMBERMASK) == wx.stc.STC_FOLDLEVELBASE:

			if expanding:
				win.SetFoldExpanded(lineNum, True)
				lineNum = win.Expand(lineNum, True)
				lineNum = lineNum - 1
			else:
				lastChild = win.GetLastChild(lineNum, -1)
				win.SetFoldExpanded(lineNum, False)
				if lastChild > lineNum:
					win.HideLines(lineNum+1, lastChild)

		lineNum = lineNum + 1

def Expand(win, line, doExpand, force=False, visLevels=0, level=-1):
	lastChild = win.GetLastChild(line, level)
	line = line + 1
	while line <= lastChild:
		if force:
			if visLevels > 0:
				win.ShowLines(line, line)
			else:
				win.HideLines(line, line)
		else:
			if doExpand:
				win.ShowLines(line, line)

		if level == -1:
			level = win.GetFoldLevel(line)

		if level & wx.stc.STC_FOLDLEVELHEADERFLAG:
			if force:
				if visLevels > 1:
					win.SetFoldExpanded(line, True)
				else:
					win.SetFoldExpanded(line, False)
				line = Expand(win, line, doExpand, force, visLevels-1)

			else:
				if doExpand and win.GetFoldExpanded(line):
					line = Expand(win, line, True, force, visLevels-1)
				else:
					line = Expand(win, line, False, force, visLevels-1)
		else:
			line = line + 1;

	return line



#-----------------------  mCheckBrace.py ------------------

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



#-----------------------  mZoom.py ------------------

from modules import Mixin
import wx
import wx.stc
import os.path
from modules import common

menulist = [
	('IDM_VIEW', #parent menu id
	[
		(170, '', '-', wx.ITEM_SEPARATOR, None, ''),
		(185, 'IDM_VIEW_ZOOM_IN', tr('Zoom In'), wx.ITEM_NORMAL, 'OnViewZoomIn', tr('Increases the font size of the document')),
		(190, 'IDM_VIEW_ZOOM_OUT', tr('Zoom Out'), wx.ITEM_NORMAL, 'OnViewZoomOut', tr('Decreases the font size of the document')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

imagelist = {
	'IDM_VIEW_ZOOM_IN':'images/large.gif',
	'IDM_VIEW_ZOOM_OUT':'images/small.gif',
}
Mixin.setMixin('mainframe', 'imagelist', imagelist)

def OnViewZoomIn(win, event):
	win.document.ZoomIn()
Mixin.setMixin('mainframe', 'OnViewZoomIn', OnViewZoomIn)

def OnViewZoomOut(win, event):
	win.document.ZoomOut()
Mixin.setMixin('mainframe', 'OnViewZoomOut', OnViewZoomOut)

toollist = [
	(820, 'zoomin'),
	(830, 'zoomout'),
]
Mixin.setMixin('mainframe', 'toollist', toollist)

toolbaritems = {
	'zoomin':(wx.ITEM_NORMAL, 'IDM_VIEW_ZOOM_IN', common.unicode_abspath('images/large.gif'), tr('zoom in'), tr('Increases the font size of the document'), 'OnViewZoomIn'),
	'zoomout':(wx.ITEM_NORMAL, 'IDM_VIEW_ZOOM_OUT', common.unicode_abspath('images/small.gif'), tr('zoom out'), tr('Decreases the font size of the document'), 'OnViewZoomOut'),
}
Mixin.setMixin('mainframe', 'toolbaritems', toolbaritems)



#-----------------------  mSession.py ------------------

from modules import Mixin
import wx
import wx.stc

def init(pref):
    pref.load_session = True
    pref.sessions = []
    pref.last_tab_index = -1
    pref.screen_lines = 0
Mixin.setPlugin('preference', 'init', init)

preflist = [
    (tr('General'), 130, 'check', 'load_session', tr('Auto load the files of last session'), None),
]
Mixin.setMixin('preference', 'preflist', preflist)

def afterclosewindow(win):
    win.pref.sessions = []
    win.pref.last_tab_index = -1
    if win.pref.load_session:
        for document in win.editctrl.getDocuments():
            if document.documenttype != 'edit':
                continue
            win.pref.screen_lines = document.LinesOnScreen()
            if document.filename and document.savesession:
                win.pref.sessions.append(getStatus(document))
        win.pref.last_tab_index = win.editctrl.GetSelection()
    win.pref.save()
Mixin.setPlugin('mainframe', 'afterclosewindow', afterclosewindow)

def getStatus(document):
    """filename, pos, bookmarks"""
    row = document.GetCurrentLine()
    col = document.GetColumn(document.GetCurrentPos())
    bookmarks = []
    start = 0
    line = document.MarkerNext(start, 1)
    while line > -1:
        bookmarks.append(line)
        start = line + 1
        line = document.MarkerNext(start, 1)
    return document.filename, row, col, bookmarks

def setStatus(document, row, col, bookmarks):
    document.GotoLine(row)
    for line in bookmarks:
        document.MarkerAdd(line, 0)

def openPage(win):
    n = 0
    if win.mainframe.pref.load_session and not win.mainframe.app.skipsessionfile:
        for filename, row, col, bookmarks in win.mainframe.pref.sessions:
            document = win.new(filename, delay=True)
            if document:
                setStatus(document, row, col, bookmarks)
                n += 1
        index = win.mainframe.pref.last_tab_index
        if index > -1 and index < len(win.list):
           wx.CallAfter(win.switch, win.list[index], delay=False)

    return n > 0
Mixin.setPlugin('editctrl', 'openpage', openPage)



#-----------------------  mLastStatus.py ------------------

__doc__ = "Saveing last window status, including position, size, and Maximized or Iconized."

from modules import Mixin
import wx
import wx.stc

def init(pref):
	pref.save_current_status = True
	pref.status_position = (0, 0)
	pref.status_size = (600, 400)
	pref.status = 3	#1 Iconized 2 Maximized 3 normal
Mixin.setPlugin('preference', 'init', init)

preflist = [
	(tr('General'), 140, 'check', 'save_current_status', tr('Saves current status when exit the program'), None),
]
Mixin.setMixin('preference', 'preflist', preflist)

def afterclosewindow(win):
	if win.pref.save_current_status:
		if win.IsMaximized():
			win.pref.status = 2
		else:
			win.pref.status = 3
			saveWindowPosition(win)
		win.pref.save()
Mixin.setPlugin('mainframe', 'afterclosewindow', afterclosewindow)

def init(win):
	if win.pref.save_current_status:
		win.Move(win.pref.status_position)
		win.SetSize(win.pref.status_size)
		if win.pref.status == 2:
			win.Maximize()
Mixin.setPlugin('mainframe', 'beforeinit', init)

def init(win):
	wx.EVT_MAXIMIZE(win, win.OnMaximize)
	wx.EVT_ICONIZE(win, win.OnIconize)
Mixin.setPlugin('mainframe', 'init', init)

def OnMaximize(win, event):
	saveWindowPosition(win)
	event.Skip()
Mixin.setMixin('mainframe', 'OnMaximize', OnMaximize)

def OnIconize(win, event):
	saveWindowPosition(win)
	event.Skip()
Mixin.setMixin('mainframe', 'OnIconize', OnIconize)

def saveWindowPosition(win):
	if win.IsIconized() == False and win.IsMaximized() == False:
		win.pref.status_position = win.GetPositionTuple()
		win.pref.status_size = win.GetSizeTuple()
		win.pref.save()



#-----------------------  mDuplicate.py ------------------

__doc__ = 'Duplicate char, word, line'

from modules import Mixin
import wx
import wx.stc
from modules import Calltip

CALLTIP_DUPLICATE = 1

def init(pref):
	pref.duplicate_extend_mode = True
Mixin.setPlugin('preference', 'init', init)

preflist = [
	(tr('General'), 150, 'check', 'duplicate_extend_mode', tr("Use duplication extend mode ('.' will be treated as word char)"), None)
]
Mixin.setMixin('preference', 'preflist', preflist)

popmenulist = [ (None,
	[
		(190, 'IDPM_DUPLICATE', tr('Duplication'), wx.ITEM_NORMAL, None, ''),
	]),
	('IDPM_DUPLICATE', #parent menu id
	[
		(90, 'IDPM_DUPLICATE_MODE', tr('Duplicate Extend Mode') + '\tF10', wx.ITEM_CHECK, 'OnDuplicateMode', tr('Toggle duplication extend mode')),
		(100, 'IDPM_DUPLICATE_CURRENT_LINE', tr('Duplicate Current Line') + '\tCtrl+J', wx.ITEM_NORMAL, 'OnDuplicateCurrentLine', tr('Duplicates current line')),
		(200, 'IDPM_DUPLICATE_CHAR', tr('Duplicate Previous Char') + '\tCtrl+M', wx.ITEM_NORMAL, 'OnDuplicateChar', tr('Copies a character from previous matched word')),
		(300, 'IDPM_DUPLICATE_NEXT_CHAR', tr('Duplicate Next Char') + '\tCtrl+Shift+M', wx.ITEM_NORMAL, 'OnDuplicateNextChar', tr('Copies a character from next matched word')),
		(400, 'IDPM_DUPLICATE_WORD', tr('Duplicate Previous Word') + '\tCtrl+P', wx.ITEM_NORMAL, 'OnDuplicateWord', tr('Copies a word from previous matched line')),
		(500, 'IDPM_DUPLICATE_NEXT_WORD', tr('Duplicate Next Word') + '\tCtrl+Shift+P', wx.ITEM_NORMAL, 'OnDuplicateNextWord', tr('Copies a word from next matched line')),
		(600, 'IDPM_DUPLICATE_LINE', tr('Duplicate Previous Line') + '\tCtrl+L', wx.ITEM_NORMAL, 'OnDuplicateLine', tr('Copies a line from next matched line')),
		(700, 'IDPM_DUPLICATE_NEXT_LINE', tr('Duplicate Next Line') + '\tCtrl+Shift+L', wx.ITEM_NORMAL, 'OnDuplicateNextLine', tr('Copies a line from next matched line')),
	]),
]
Mixin.setMixin('editor', 'popmenulist', popmenulist)

def init(win):
	win.calltip = Calltip.MyCallTip(win)
	win.calltip_type = -1
Mixin.setPlugin('editor', 'init', init)

def getWordChars(win):
	wordchars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
	if win.pref.duplicate_extend_mode:
		return wordchars + '.'
	else:
		return wordchars
Mixin.setMixin('mainframe', 'getWordChars', getWordChars)

def OnDuplicateCurrentLine(win, event):
	win.mainframe.OnEditDuplicateCurrentLine(event)
Mixin.setMixin('editor', 'OnDuplicateCurrentLine', OnDuplicateCurrentLine)

def OnDuplicateChar(win, event):
	win.mainframe.OnEditDuplicateChar(event)
Mixin.setMixin('editor', 'OnDuplicateChar', OnDuplicateChar)

def OnDuplicateNextChar(win, event):
	win.mainframe.OnEditDuplicateNextChar(event)
Mixin.setMixin('editor', 'OnDuplicateNextChar', OnDuplicateNextChar)

def OnDuplicateWord(win, event):
	win.mainframe.OnEditDuplicateWord(event)
Mixin.setMixin('editor', 'OnDuplicateWord', OnDuplicateWord)

def OnDuplicateNextWord(win, event):
	win.mainframe.OnEditDuplicateNextWord(event)
Mixin.setMixin('editor', 'OnDuplicateNextWord', OnDuplicateNextWord)

def OnDuplicateLine(win, event):
	win.mainframe.OnEditDuplicateLine(event)
Mixin.setMixin('editor', 'OnDuplicateLine', OnDuplicateLine)

def OnDuplicateNextLine(win, event):
	win.mainframe.OnEditDuplicateNextLine(event)
Mixin.setMixin('editor', 'OnDuplicateNextLine', OnDuplicateNextLine)

menulist = [ ('IDM_EDIT', #parent menu id
	[
		(230, 'IDM_EDIT_DUPLICATE', tr('Duplication'), wx.ITEM_NORMAL, None, ''),
	]),
	('IDM_EDIT_DUPLICATE', #parent menu id
	[
		(90, 'IDM_EDIT_DUPLICATE_MODE', tr('Duplicate Extend Mode') + '\tF10', wx.ITEM_CHECK, 'OnEditDuplicateMode', tr('Toggle duplication extend mode')),
		(100, 'IDM_EDIT_DUPLICATE_CURRENT_LINE', tr('Duplicate Current Line') + '\tE=Ctrl+J', wx.ITEM_NORMAL, 'OnEditDuplicateCurrentLine', tr('Duplicates current line')),
		(200, 'IDM_EDIT_DUPLICATE_CHAR', tr('Duplicate Previous Char') + '\tE=Ctrl+M', wx.ITEM_NORMAL, 'OnEditDuplicateChar', tr('Copies a character from previous matched word')),
		(300, 'IDM_EDIT_DUPLICATE_NEXT_CHAR', tr('Duplicate Next Char') + '\tE=Ctrl+Shift+M', wx.ITEM_NORMAL, 'OnEditDuplicateNextChar', tr('Copies a character from next matched word')),
		(400, 'IDM_EDIT_DUPLICATE_WORD', tr('Duplicate Previous Word') + '\tE=Ctrl+P', wx.ITEM_NORMAL, 'OnEditDuplicateWord', tr('Copies a word from previous matched line')),
		(500, 'IDM_EDIT_DUPLICATE_NEXT_WORD', tr('Duplicate Next Word') + '\tE=Ctrl+Shift+P', wx.ITEM_NORMAL, 'OnEditDuplicateNextWord', tr('Copies a word from next matched line')),
		(600, 'IDM_EDIT_DUPLICATE_LINE', tr('Duplicate Previous Line') + '\tE=Ctrl+L', wx.ITEM_NORMAL, 'OnEditDuplicateLine', tr('Copies a line from next matched line')),
		(700, 'IDM_EDIT_DUPLICATE_NEXT_LINE', tr('Duplicate Next Line') + '\tE=Ctrl+Shift+L', wx.ITEM_NORMAL, 'OnEditDuplicateNextLine', tr('Copies a line from next matched line')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

def init(win):
	wx.EVT_UPDATE_UI(win, win.IDPM_DUPLICATE_MODE, win.OnUpdateUI)
Mixin.setPlugin('editor', 'init', init)

def OnUpdateUI(win, event):
	eid = event.GetId()
	if eid == win.IDPM_DUPLICATE_MODE:
		event.Check(win.pref.duplicate_extend_mode)
Mixin.setPlugin('editor', 'on_update_ui', OnUpdateUI)

def init(win):
	wx.EVT_UPDATE_UI(win, win.IDM_EDIT_DUPLICATE_MODE, win.OnUpdateUI)
Mixin.setPlugin('mainframe', 'init', init)

def OnUpdateUI(win, event):
	eid = event.GetId()
	if eid == win.IDM_EDIT_DUPLICATE_MODE:
		event.Check(win.pref.duplicate_extend_mode)
Mixin.setPlugin('mainframe', 'on_update_ui', OnUpdateUI)

def OnDuplicateMode(win, event):
	win.mainframe.OnEditDuplicateMode(event)
Mixin.setMixin('editor', 'OnDuplicateMode', OnDuplicateMode)

def OnEditDuplicateMode(win, event):
	win.pref.duplicate_extend_mode = not win.pref.duplicate_extend_mode
	win.pref.save()
Mixin.setMixin('mainframe', 'OnEditDuplicateMode', OnEditDuplicateMode)

def OnEditDuplicateCurrentLine(win, event):
	line = win.document.GetCurrentLine()
	text = win.document.getLineText(line)
	pos = win.document.GetCurrentPos() - win.document.PositionFromLine(line)
	start = win.document.GetLineEndPosition(line)
	win.document.InsertText(start, win.document.getEOLChar() + text)
	win.document.GotoPos(win.document.PositionFromLine(line + 1) + pos)
Mixin.setMixin('mainframe', 'OnEditDuplicateCurrentLine', OnEditDuplicateCurrentLine)

def OnEditDuplicateChar(win, event):
	pos = win.document.GetCurrentPos()
	text = win.document.getRawText()
	word = findLeftWord(text, pos, win.getWordChars())
	length = len(word)
	if length > 0:
		findstart = pos - length - 1	#-1 means skip the char before the word
		if findstart > 0:
			start = findPreviousWordPos(text, findstart, word, win.getWordChars())
			if start > -1:
				start += length
				if text[start] in win.getWordChars():
					win.document.InsertText(pos, text[start])
					win.document.GotoPos(pos + 1)
Mixin.setMixin('mainframe', 'OnEditDuplicateChar', OnEditDuplicateChar)

def findPreviousWordPos(text, pos, word, word_chars):
	while pos >= 0:
		if pos == 0:
			ch = ''
		else:
			ch = text[pos - 1]
		if (not ch) or (not (ch in word_chars)):
			if text.startswith(word, pos):
				return pos
		pos -= 1
	return -1

def findLeftWord(text, pos, word_chars):
	"""if just left char is '.' or '(', etc. then continue to search, other case stop searching"""
	edge_chars = '.[('
	chars = []
	leftchar = text[pos - 1]
	if leftchar in edge_chars:
		chars.append(leftchar)
		pos -= 1

	while pos > 0:
		leftchar = text[pos - 1]
		if leftchar in word_chars:
			pos -= 1
			chars.append(leftchar)
		else:
			break
	chars.reverse()
	return ''.join(chars)

def OnEditDuplicateNextChar(win, event):
	pos = win.document.GetCurrentPos()
	text = win.document.getRawText()
	word = findLeftWord(text, pos, win.getWordChars())
	length = len(word)
	if length > 0:
		findstart = pos 	#-1 means skip the char before the word
		if findstart > 0:
			start = findNextWordPos(text, findstart, word, win.getWordChars())
			if start > -1:
				start += length
				if text[start] in win.getWordChars():
					win.document.InsertText(pos, text[start])
					win.document.GotoPos(pos + 1)
Mixin.setMixin('mainframe', 'OnEditDuplicateNextChar', OnEditDuplicateNextChar)

def findNextWordPos(text, pos, word, word_chars):
	length = len(text)
	while pos < length:
		if pos - 1 == 0:
			ch = ''
		else:
			ch = text[pos - 1]
		if (not ch) or (not (ch in word_chars)):
			if text.startswith(word, pos):
				return pos
		pos += 1
	return -1

def OnKeyDown(win, event):
	if win.findflag:
		key = event.GetKeyCode()
		if key in (wx.WXK_RETURN, wx.WXK_SPACE):
			win.calltip.cancel()
			win.findflag = 0
			if win.calltip_type == CALLTIP_DUPLICATE:#duplicate mode
				win.AddText(win.duplicate_match_text)
		elif key == wx.WXK_ESCAPE:
			win.calltip.cancel()
			win.findflag = 0
		elif key in ('L', 'P') and event.ControlDown():
			return False
		return True
Mixin.setPlugin('editor', 'on_key_down', OnKeyDown, Mixin.HIGH, 0)

def getMatchWordPos(text, start, word, word_chars):
	pos = start + len(word)
	length = len(text)
	while pos < length:
		if not (text[pos] in word_chars):
			return pos
		pos += 1
	return -1

def init(win):
	win.findflag = 0
Mixin.setPlugin('editor', 'init', init)

def OnEditDuplicateWord(win, event):
	duplicateMatch(win, 1)
Mixin.setMixin('mainframe', 'OnEditDuplicateWord', OnEditDuplicateWord)

def OnEditDuplicateNextWord(win, event):
	duplicateMatch(win, 2)
Mixin.setMixin('mainframe', 'OnEditDuplicateNextWord', OnEditDuplicateNextWord)

def OnEditDuplicateLine(win, event):
	duplicateMatch(win, 3)
Mixin.setMixin('mainframe', 'OnEditDuplicateLine', OnEditDuplicateLine)

def OnEditDuplicateNextLine(win, event):
	duplicateMatch(win, 4)
Mixin.setMixin('mainframe', 'OnEditDuplicateNextLine', OnEditDuplicateNextLine)

def duplicateMatch(win, kind):
	text = win.document.getRawText()
	length = win.document.GetLength()
	if win.document.findflag == 0:
		win.document.duplicate_pos = win.document.GetCurrentPos()
		win.document.duplicate_word = findLeftWord(text, win.document.duplicate_pos, win.getWordChars())
		win.document.duplicate_length = len(win.document.duplicate_word)
		if win.document.duplicate_length == 0:
			return
		if kind in (1, 3):
			findstart = win.document.duplicate_pos - win.document.duplicate_length - 1
		else:
			findstart = win.document.duplicate_pos + 1	#-1 means skip the char before the word
	else:
		if kind in (1, 3):
			findstart = win.document.duplicate_start - 1
		else:
			findstart = win.document.duplicate_start + win.document.duplicate_match_len
	while (kind in (1, 3) and (findstart >= 0)) or (kind in (2, 4) and (findstart < length)) :
		if kind in (1, 3):
			start = findPreviousWordPos(text, findstart, win.document.duplicate_word, win.getWordChars())
		else:
			start = findNextWordPos(text, findstart, win.document.duplicate_word, win.getWordChars())
		if start > -1:
			end = getMatchWordPos(text, start, win.document.duplicate_word, win.getWordChars())
			if end - start > win.document.duplicate_length:
				if kind in (1, 2) and win.document.findflag:
					if win.document.duplicate_calltip == text[start:end]:
						if kind == 1:
							findstart = start - 1
						else:
							findstart = start + 1
						continue
				win.document.findflag = 1
				win.document.duplicate_start = start
				if kind in (3, 4):
					line = win.document.LineFromPosition(start)
					line_end = win.document.GetLineEndPosition(line)
					win.document.duplicate_calltip = win.document.getLineText(line).expandtabs(win.document.GetTabWidth())
					win.document.duplicate_match_len = line_end - start - win.document.duplicate_length
					win.document.duplicate_match_text = win.document.GetTextRange(start + win.document.duplicate_length , line_end)
				else:
					win.document.duplicate_calltip = text[start:end]
					win.document.duplicate_match_len = end - start - win.document.duplicate_length
					win.document.duplicate_match_text = win.document.GetTextRange(start + win.document.duplicate_length , end)
				win.document.calltip.cancel()
				win.document.calltip_type = CALLTIP_DUPLICATE
				win.document.calltip.show(win.document.duplicate_pos, win.document.duplicate_calltip)
				return
			else:
				if kind in (1, 3):
					findstart = start - 1
				else:
					findstart = start + 1
		else:
			return



#-----------------------  mHelp.py ------------------

from modules import Mixin
import wx
import wx.stc
from modules import Version
import os.path
from modules import common

homepage = 'http://wiki.woodpecker.org.cn/moin/NewEdit'
blog = 'http://www.donews.net/limodou'
email = 'limodou@gmail.com'
author = 'limodou'

class AboutDialog(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, -1, size = (400, 240), style = wx.DEFAULT_DIALOG_STYLE, title = tr('About'))

		box = wx.BoxSizer(wx.VERTICAL)
		t = wx.StaticText(self, -1, label=tr('NewEdit Version %s') % Version.version)
		font = t.GetFont()
		font.SetPointSize(20)
		t.SetFont(font)
		box.Add(t, 0, wx.ALIGN_CENTER|wx.ALL, 10)
		t = wx.StaticText(self, -1, label=tr('Author: %s (%s)') % (author, email))
		font.SetPointSize(12)
		t.SetFont(font)
		box.Add(t, 0, wx.ALIGN_CENTER|wx.BOTTOM, 10)
		line = wx.StaticLine(self, -1, size=(-1, -1))
		box.Add(line, 0, wx.ALIGN_CENTER|wx.BOTTOM, 10)
		t = wx.StaticText(self, -1, label=tr('If you have any question please contact me !\nThe NewEdit project homepage is : \n    %s\nMy Blog is : \n    %s') % (homepage, blog))
		font.SetPointSize(10)
		t.SetFont(font)
		box.Add(t, 0, wx.ALIGN_CENTER|wx.BOTTOM, 10)
		btnOK = wx.Button(self, wx.ID_OK, tr("OK"), size=(60, -1))
		btnOK.SetDefault()
		box.Add(btnOK, 0, wx.ALIGN_CENTER|wx.ALL, 10)

		self.SetSizer(box)
		self.SetAutoLayout(True)

menulist = [ ('IDM_HELP', #parent menu id
	[
		(100, 'IDM_HELP_INDEXT', tr('NewEdit Help Document') + '\tF1', wx.ITEM_NORMAL, 'OnHelpIndex', tr('NewEdit help document')),
		(110, 'IDM_HELP_PROJECT', tr('Visit Project Homepage'), wx.ITEM_NORMAL, 'OnHelpProject', tr('Project Homepage %s') % homepage),
		(120, 'IDM_HELP_MYBLOG', tr('Visit My Blog'), wx.ITEM_NORMAL, 'OnHelpMyBlog', tr('My Blog %s') % blog),
		(130, 'IDM_HELP_EMAIL', tr('Contact Me'), wx.ITEM_NORMAL, 'OnHelpEmail', tr('Send email to me mailto:%s') % email),
		(900, 'IDM_HELP_ABOUT', tr('About...'), wx.ITEM_NORMAL, 'OnHelpAbout', tr('About this program')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

def OnHelpIndex(win, event):
	import webbrowser

	webbrowser.open('file:///'+common.get_app_filename(win, 'doc/index.htm'), 1)
Mixin.setMixin('mainframe', 'OnHelpIndex', OnHelpIndex)

def OnHelpAbout(win, event):
	AboutDialog(win).ShowModal()
Mixin.setMixin('mainframe', 'OnHelpAbout', OnHelpAbout)

def OnHelpProject(win, event):
	import webbrowser

	webbrowser.open(homepage, 1)
Mixin.setMixin('mainframe', 'OnHelpProject', OnHelpProject)

def OnHelpEmail(win, event):
	import webbrowser

	webbrowser.open('mailto:%s' % email)
Mixin.setMixin('mainframe', 'OnHelpEmail', OnHelpEmail)

def OnHelpMyBlog(win, event):
	import webbrowser

	webbrowser.open(blog, 1)
Mixin.setMixin('mainframe', 'OnHelpMyBlog', OnHelpMyBlog)



#-----------------------  mClassBrowser.py ------------------

import wx
from modules import Mixin
from modules.Debug import error
from modules import common

def init(pref):
	pref.python_classbrowser_show = False
Mixin.setPlugin('preference', 'init', init)

preflist = [
	('Python', 100, 'check', 'python_classbrowser_show', tr('Show class browser window as open python source file'), None),
]
Mixin.setMixin('preference', 'preflist', preflist)

menulist = [('IDM_PYTHON', #parent menu id
		[
			(100, 'IDM_PYTHON_CLASSBROWSER', tr('Class Browser'), wx.ITEM_CHECK, 'OnPythonClassBrowser', tr('Show python class browser window')),
			(110, 'IDM_PYTHON_CLASSBROWSER_REFRESH', tr('Class Browser Refresh'), wx.ITEM_NORMAL, 'OnPythonClassBrowserRefresh', tr('Refresh python class browser window')),
		]),
]
Mixin.setMixin('pythonfiletype', 'menulist', menulist)

def init(win):
	win.class_browser = False
	win.init_class_browser = False
Mixin.setPlugin('editor', 'init', init)

def OnPythonClassBrowser(win, event):
	win.document.class_browser = not win.document.class_browser
	win.document.panel.showWindow('LEFT', win.document.class_browser)
	if win.document.panel.LeftIsVisible:
		if win.document.init_class_browser == False:
			win.document.init_class_browser = True
			win.document.classtree.readtext(win.document.GetText())
Mixin.setMixin('mainframe', 'OnPythonClassBrowser', OnPythonClassBrowser)

def OnPythonClassBrowserRefresh(win, event):
	win.document.classtree.readtext(win.document.GetText())
Mixin.setMixin('mainframe', 'OnPythonClassBrowserRefresh', OnPythonClassBrowserRefresh)

def OnPythonUpdateUI(win, event):
	eid = event.GetId()
	if eid == win.IDM_PYTHON_CLASSBROWSER:
		event.Check(win.document.panel.LeftIsVisible)
Mixin.setMixin('mainframe', 'OnPythonUpdateUI', OnPythonUpdateUI)

def on_enter(mainframe, document):
	wx.EVT_UPDATE_UI(mainframe, mainframe.IDM_PYTHON_CLASSBROWSER, mainframe.OnPythonUpdateUI)
	if mainframe.pref.python_classbrowser_show and document.init_class_browser == False:
		document.class_browser = not document.class_browser
		document.panel.showWindow('LEFT', document.class_browser)
		if document.panel.LeftIsVisible:
			if document.init_class_browser == False:
				document.init_class_browser = True
				document.classtree.readtext(document.GetText())
Mixin.setPlugin('pythonfiletype', 'on_enter', on_enter)

def on_leave(mainframe, filename, languagename):
	mainframe.Disconnect(mainframe.IDM_PYTHON_CLASSBROWSER, -1, wx.wxEVT_UPDATE_UI)
Mixin.setPlugin('pythonfiletype', 'on_leave', on_leave)

classbrowser_imagelist = {
	'class_normal':		common.unicode_abspath('images/minus.gif'),
	'class_open':		common.unicode_abspath('images/plus.gif'),
	'method':			common.unicode_abspath('images/item.gif'),
}

def afterinit(win):
	try:
		_imagel = wx.ImageList(16, 16)
		_imagel.Add(wx.Image(classbrowser_imagelist['class_normal']).ConvertToBitmap())
		_imagel.Add(wx.Image(classbrowser_imagelist['class_open']).ConvertToBitmap())
		_imagel.Add(wx.Image(classbrowser_imagelist['method']).ConvertToBitmap())
	except:
		error.traceback()
		_imagel = None
	win.classbrowserimagelist = _imagel
Mixin.setPlugin('mainframe', 'afterinit', afterinit)

def new_window(win, document, panel):
	from ClassTree import ClassTree

	document.classtree = ClassTree(panel.left, document, win.mainframe.classbrowserimagelist)
Mixin.setPlugin('textpanel', 'new_window', new_window)

toollist = [
	(2000, 'classbrowser'),
	(2010, 'classbrowserrefresh'),
	(2050, '|'),
]
Mixin.setMixin('pythonfiletype', 'toollist', toollist)

toolbaritems = {
	'classbrowser':(wx.ITEM_CHECK, 'IDM_PYTHON_CLASSBROWSER', common.unicode_abspath('images/classbrowser.gif'), tr('class browser'), tr('Class browser'), 'OnPythonClassBrowser'),
	'classbrowserrefresh':(wx.ITEM_NORMAL, 'IDM_PYTHON_CLASSBROWSER_REFRESH', common.unicode_abspath('images/classbrowserrefresh.gif'), tr('class browser refresh'), tr('Class browser refresh'), 'OnPythonClassBrowserRefresh'),
}
Mixin.setMixin('pythonfiletype', 'toolbaritems', toolbaritems)



#-----------------------  mRun.py ------------------

from modules import Mixin
import wx
import locale
import types
import os


def init(win):
	wx.EVT_IDLE(win, win.OnIdle)
	wx.EVT_END_PROCESS(win.mainframe, -1, win.mainframe.OnProcessEnded)
	wx.EVT_KEY_DOWN(win, win.OnKeyDown)
	wx.EVT_KEY_UP(win, win.OnKeyUp)
	wx.EVT_UPDATE_UI(win, win.GetId(),  win.RunCheck)

	win.MAX_PROMPT_COMMANDS = 25

	win.process = None
	win.pid = -1

	win.CommandArray = []
	win.CommandArrayPos = -1

	win.editpoint = 0
	win.writeposition = 0
Mixin.setPlugin('messagewindow', 'init', init)

def RunCommand(win, command, guiflag=False, redirect=True):
	"""replace $file = current document filename"""
	if redirect:
		win.createMessageWindow()

		win.panel.showPage(tr('Message'))

		win.messagewindow.SetText('')
		win.messagewindow.editpoint = 0
		win.messagewindow.writeposition = 0
		win.SetStatusText(tr("Running "), 0)
		try:
			win.messagewindow.process = wx.Process(win)
			win.messagewindow.process.Redirect()
			if guiflag:
				win.messagewindow.pid = wx.Execute(command, wx.EXEC_ASYNC|wx.EXEC_NOHIDE, win.messagewindow.process)
			else:
				win.messagewindow.pid = wx.Execute(command, wx.EXEC_ASYNC, win.messagewindow.process)
			win.messagewindow.inputstream = win.messagewindow.process.GetInputStream()
			win.messagewindow.errorstream = win.messagewindow.process.GetErrorStream()
			win.messagewindow.outputstream = win.messagewindow.process.GetOutputStream()
		except:
			win.messagewindow.process = None
			dlg = wx.MessageDialog(win, tr("There are some problems when running the program!\nPlease run it in shell.") ,
				"Stop running", wx.OK | wx.ICON_INFORMATION)
			dlg.ShowModal()
	else:
		wx.Execute(command)
Mixin.setMixin('mainframe', 'RunCommand', RunCommand)

def OnIdle(win, event):
	if win.process is not None:
		if win.inputstream:
			if win.inputstream.CanRead():
				text = win.inputstream.read()
				appendtext(win, text)
				win.writeposition = win.GetLength()
				win.editpoint = win.GetLength()
		if win.errorstream:
			if win.errorstream.CanRead():
				text = win.errorstream.read()
				appendtext(win, text)
				win.writeposition = win.GetLength()
				win.editpoint = win.GetLength()
Mixin.setMixin('messagewindow', 'OnIdle', OnIdle)

def OnKeyDown(win, event):
	keycode = event.GetKeyCode()
	pos = win.GetCurrentPos()
	if win.pid > -1:
		if (pos >= win.editpoint) and (keycode == wx.WXK_RETURN):
			text = win.GetTextRange(win.writeposition, win.GetLength())
			l = len(win.CommandArray)
			if (l < win.MAX_PROMPT_COMMANDS):
				win.CommandArray.insert(0, text)
				win.CommandArrayPos = -1
			else:
				win.CommandArray.pop()
				win.CommandArray.insert(0, text)
				win.CommandArrayPos = -1

			if isinstance(text, types.UnicodeType):
				text = text.encode(locale.getdefaultlocale()[1])
			win.outputstream.write(text + '\n')
			win.GotoPos(win.GetLength())
		if keycode == wx.WXK_UP:
			l = len(win.CommandArray)
			if (len(win.CommandArray) > 0):
				if (win.CommandArrayPos + 1) < l:
					win.GotoPos(win.editpoint)
					win.SetTargetStart(win.editpoint)
					win.SetTargetEnd(win.GetLength())
					win.CommandArrayPos = win.CommandArrayPos + 1
					win.ReplaceTarget(win.CommandArray[win.CommandArrayPos])

		elif keycode == wx.WXK_DOWN:
			if len(win.CommandArray) > 0:
				win.GotoPos(win.editpoint)
				win.SetTargetStart(win.editpoint)
				win.SetTargetEnd(win.GetLength())
				if (win.CommandArrayPos - 1) > -1:
					win.CommandArrayPos = win.CommandArrayPos - 1
					win.ReplaceTarget(win.CommandArray[win.CommandArrayPos])
				else:
					if (win.CommandArrayPos - 1) > -2:
						win.CommandArrayPos = win.CommandArrayPos - 1
					win.ReplaceTarget("")
	if ((pos > win.editpoint) and (not keycode == wx.WXK_UP)) or ((not keycode == wx.WXK_BACK) and (not keycode == wx.WXK_LEFT) and (not keycode == wx.WXK_UP) and (not keycode == wx.WXK_DOWN)):
		if (pos < win.editpoint):
			if (not keycode == wx.WXK_RIGHT):
				event.Skip()
		else:
			event.Skip()
Mixin.setMixin('messagewindow', 'OnKeyDown', OnKeyDown)

def OnKeyUp(win, event):
	keycode = event.GetKeyCode()
	#franz: pos was not used
	if keycode == wx.WXK_HOME:
		if (win.GetCurrentPos() < win.editpoint):
			win.GotoPos(win.editpoint)
		return
	elif keycode == wx.WXK_PRIOR:
		if (win.GetCurrentPos() < win.editpoint):
			win.GotoPos(win.editpoint)
		return
	event.Skip()
Mixin.setMixin('messagewindow', 'OnKeyUp', OnKeyUp)

def OnProcessEnded(win, event):
	if win.messagewindow.inputstream.CanRead():
		text = win.messagewindow.inputstream.read()
		appendtext(win.messagewindow, text)
	if win.messagewindow.errorstream.CanRead():
		text = win.messagewindow.errorstream.read()
		appendtext(win.messagewindow, text)

	if win.messagewindow.process:
		win.messagewindow.process.Destroy()
		win.messagewindow.process = None
		win.messagewindow.pid = -1
		win.SetStatusText(tr("Finished!"), 0)
Mixin.setMixin('mainframe', 'OnProcessEnded', OnProcessEnded)

def appendtext(win, text):
	win.GotoPos(win.GetLength())
	if not isinstance(text, types.UnicodeType):
		text = unicode(text, locale.getdefaultlocale()[1])
	win.AddText(text)
	win.GotoPos(win.GetLength())
	win.EmptyUndoBuffer()

def RunCheck(win, event):
	if (win.GetCurrentPos() < win.editpoint) or (win.pid == -1):
		win.SetReadOnly(1)
	else:
		win.SetReadOnly(0)
Mixin.setMixin('messagewindow', 'RunCheck', RunCheck)



#-----------------------  mScript.py ------------------

from modules import Mixin
import wx
from modules import makemenu
import sys

def init(pref):
	pref.scripts = []
	pref.last_script_dir = ''
Mixin.setPlugin('preference', 'init', init)

menulist = [(None,
	[
		(570, 'IDM_SCRIPT', tr('Script'), wx.ITEM_NORMAL, None, ''),
	]),
	('IDM_SCRIPT', #parent menu id
	[
		(100, 'IDM_SCRIPT_MANAGE', tr('Script Manage...'), wx.ITEM_NORMAL, 'OnScriptManage', tr('Script manage')),
		(110, '', '-', wx.ITEM_SEPARATOR, None, ''),
		(120, 'IDM_SCRIPT_ITEMS', tr('(empty)'), wx.ITEM_NORMAL, 'OnScriptItems', tr('Execute an script')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

def OnScriptManage(win, event):
	from ScriptDialog import ScriptDialog

	dlg = ScriptDialog(win, win.pref)
	answer = dlg.ShowModal()
	if answer == wx.ID_OK:
		makescriptmenu(win, win.pref)
Mixin.setMixin('mainframe', 'OnScriptManage', OnScriptManage)

def beforeinit(win):
	win.scriptmenu_ids=[win.IDM_SCRIPT_ITEMS]
	makescriptmenu(win, win.pref)
Mixin.setPlugin('mainframe', 'beforeinit', beforeinit)

def makescriptmenu(win, pref):
	menu = makemenu.findmenu(win.menuitems, 'IDM_SCRIPT')

	for id in win.scriptmenu_ids:
		menu.Delete(id)

	win.scriptmenu_ids = []
	if len(win.pref.scripts) == 0:
		id = win.IDM_SCRIPT_ITEMS
		menu.Append(id, tr('(empty)'))
		menu.Enable(id, False)
		win.scriptmenu_ids=[id]
	else:
		for description, filename in win.pref.scripts:
			id = wx.NewId()
			win.scriptmenu_ids.append(id)
			menu.Append(id, description)
			wx.EVT_MENU(win, id, win.OnScriptItems)

def OnScriptItems(win, event):
	import wx.lib.dialogs
	import traceback

	eid = event.GetId()
	index = win.scriptmenu_ids.index(eid)
	filename = win.pref.scripts[index][1]

	try:
		scripttext = open(filename, 'r').read()
	except:
		dlg = wx.MessageDialog(win, tr("Can't open the file [%s]!") % filename, tr("Running Script"), wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		return

	try:
		code = compile((scripttext + '\n'), filename, 'exec')
	except:
		d = wx.lib.dialogs.ScrolledMessageDialog(win, (tr("Error compiling script.\n\nTraceback:\n\n") +
			''.join(traceback.format_exception(*sys.exc_info()))), tr("Error"), wx.DefaultPosition, wx.Size(400,300))
		d.ShowModal()
		d.Destroy()
		return

	try:
		namespace = locals()
		exec code in namespace
	except:
		d = wx.lib.dialogs.ScrolledMessageDialog(win, (tr("Error running script.\n\nTraceback:\n\n") +
			''.join(traceback.format_exception(*sys.exc_info()))), tr("Error"), wx.DefaultPosition, wx.Size(400,300))
		d.ShowModal()
		d.Destroy()
		return
Mixin.setMixin('mainframe', 'OnScriptItems', OnScriptItems)



#-----------------------  mLanguage.py ------------------

from modules import Mixin
import wx
import os.path
from modules import makemenu
from modules import IniFile
from modules import common

langinifile = common.unicode_abspath('lang/language.ini')
if os.path.exists(langinifile):
	menulist = [
		('IDM_OPTION',
		[
			(110, 'IDM_OPTION_LANGUAGE', tr('Language'), wx.ITEM_NORMAL, None, tr('Setup lanaguage')),
		]),
		('IDM_OPTION_LANGUAGE',
		[
			(100, 'IDM_OPTION_LANGUAGE_ENGLISH', 'English', wx.ITEM_CHECK, 'OnOptionLanguageChange', 'Change langauage'),
		]),
	]
	Mixin.setMixin('mainframe', 'menulist', menulist)

	def beforeinit(win):
		win.language_ids = [win.IDM_OPTION_LANGUAGE_ENGLISH]
		win.language_country = ['']
		create_language_menu(win, langinifile)
	Mixin.setPlugin('mainframe', 'beforeinit', beforeinit)

def create_language_menu(win, filename):
	menu = makemenu.findmenu(win.menuitems, 'IDM_OPTION_LANGUAGE')

	langs = open(filename).readlines()
	for lang in langs:
		lang = lang.strip()
		if lang == '':
			continue
		if lang[0] == '#':
			continue
		country, language = lang.strip().split(' ', 1)
		id = wx.NewId()
		win.language_ids.append(id)
		win.language_country.append(country)
		menu.Append(id, language, 'Change language', wx.ITEM_CHECK)
		wx.EVT_MENU(win, id, win.OnOptionLanguageChange)

	index = win.language_country.index(win.app.i18n.lang)
	menu.Check(win.language_ids[index], True)

def OnOptionLanguageChange(win, event):
	eid = event.GetId()
	index = win.language_ids.index(eid)
	country = win.language_country[index]
	wx.MessageDialog(win, tr("Because you changed the language, \nit will be enabled at next startup."), tr("Change language"), wx.OK).ShowModal()
	ini = IniFile.IniFile(common.get_app_filename(win, 'config.ini'), encoding='utf-8')
	ini.set('language', 'default', country)
	ini.save()

	# change menu check status
	menu = makemenu.findmenu(win.menuitems, 'IDM_OPTION_LANGUAGE')
	for id in win.language_ids:
		if id == eid:
			menu.Check(id, True)
		else:
			menu.Check(id, False)
Mixin.setMixin('mainframe', 'OnOptionLanguageChange', OnOptionLanguageChange)



#-----------------------  mLexer.py ------------------

__doc__ = 'C syntax highlitght process'

from modules import Mixin
import wx
import wx.stc
import LexerClass
import LexerClass1

lexer = [(LexerClass.CLexer.metaname, tr('C/C++|*.c;*.cc;*.cpp;*.cxx;*.cs;*.h;*.hh;*.hpp;*.hxx'), wx.stc.STC_LEX_CPP, 'c.stx', LexerClass.CLexer)]
Mixin.setMixin('lexerfactory', 'lexers', lexer)
filenewtypes = [('C/C++', LexerClass.CLexer.metaname)]
Mixin.setMixin('mainframe', 'filenewtypes', filenewtypes)

lexer = [(LexerClass.TextLexer.metaname, 'Text|*.txt;*.bak;*.log;*.lst;*.diz;*.nfo', wx.stc.STC_LEX_NULL, 'text.stx', LexerClass.TextLexer)]
Mixin.setMixin('lexerfactory', 'lexers', lexer)
filenewtypes = [('Text', LexerClass.TextLexer.metaname)]
Mixin.setMixin('mainframe', 'filenewtypes', filenewtypes)

lexer = [(LexerClass.HtmlLexer.metaname, tr('Html|*.htm;*.html;*.shtml;*.xml;*.xslt'), wx.stc.STC_LEX_HTML, 'html.stx', LexerClass.HtmlLexer)]
Mixin.setMixin('lexerfactory', 'lexers', lexer)
filenewtypes = [('Html', LexerClass.HtmlLexer.metaname)]
Mixin.setMixin('mainframe', 'filenewtypes', filenewtypes)

lexer = [(LexerClass.PythonLexer.metaname, tr('Python|*.py;*.pyw'), wx.stc.STC_LEX_PYTHON, 'python.stx', LexerClass.PythonLexer)]
Mixin.setMixin('lexerfactory', 'lexers', lexer)
filenewtypes = [('Python', LexerClass.PythonLexer.metaname)]
Mixin.setMixin('mainframe', 'filenewtypes', filenewtypes)

lexer = [(LexerClass1.JavaLexer.metaname, tr('Java|*.java'), wx.stc.STC_LEX_CPP, 'java.stx', LexerClass1.JavaLexer)]
Mixin.setMixin('lexerfactory', 'lexers', lexer)
filenewtypes = [('Java', LexerClass1.JavaLexer.metaname)]
Mixin.setMixin('mainframe', 'filenewtypes', filenewtypes)

lexer = [(LexerClass1.RubyLexer.metaname, tr('Ruby|*.rb'), wx.stc.STC_LEX_RUBY, 'ruby.stx', LexerClass1.RubyLexer)]
Mixin.setMixin('lexerfactory', 'lexers', lexer)
filenewtypes = [('Ruby', LexerClass1.RubyLexer.metaname)]
Mixin.setMixin('mainframe', 'filenewtypes', filenewtypes)

lexer = [(LexerClass1.PerlLexer.metaname, tr('Perl|*.pl'), wx.stc.STC_LEX_PERL, 'perl.stx', LexerClass1.PerlLexer)]
Mixin.setMixin('lexerfactory', 'lexers', lexer)
filenewtypes = [('Perl', LexerClass1.PerlLexer.metaname)]
Mixin.setMixin('mainframe', 'filenewtypes', filenewtypes)

lexer = [(LexerClass1.CSSLexer.metaname, tr('Cascade Style Sheet|*.css'), wx.stc.STC_LEX_CSS, 'css.stx', LexerClass1.CSSLexer)]
Mixin.setMixin('lexerfactory', 'lexers', lexer)
filenewtypes = [('CSS', LexerClass1.CSSLexer.metaname)]
Mixin.setMixin('mainframe', 'filenewtypes', filenewtypes)

lexer = [(LexerClass1.JSLexer.metaname, tr('JavaScript|*.js'), wx.stc.STC_LEX_CPP, 'js.stx', LexerClass1.JSLexer)]
Mixin.setMixin('lexerfactory', 'lexers', lexer)
filenewtypes = [('JavaScript', LexerClass1.JSLexer.metaname)]
Mixin.setMixin('mainframe', 'filenewtypes', filenewtypes)



#-----------------------  mSearchInFiles.py ------------------

from modules import Mixin
import wx
import os.path, sys

menulist = [
	('IDM_SEARCH', #parent menu id
	[
		(145, 'IDM_SEARCH_FIND_IN_FILES', tr('Find In Files...'), wx.ITEM_NORMAL, 'OnSearchFindInFiles', tr('Find text in files')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

def OnSearchFindInFiles(win, event):
	import FindInFiles

	dlg = FindInFiles.FindInFiles(win, win.pref)
	dlg.Show()
Mixin.setMixin('mainframe', 'OnSearchFindInFiles', OnSearchFindInFiles)

def init(pref):
	pref.searchinfile_searchlist = []
	pref.searchinfile_dirlist = []
	pref.searchinfile_extlist = []
	pref.searchinfile_case = False
	pref.searchinfile_subdir = False
	pref.searchinfile_regular = False
	pref.searchinfile_defaultpath = os.path.dirname(sys.argv[0])
Mixin.setPlugin('preference', 'init', init)



#-----------------------  mAutoBak.py ------------------

__doc__ = 'auto make bak file as open a file'

from modules import Mixin
import wx
from modules import common

preflist = [
	(tr('Document'), 200, 'check', 'auto_make_bak', tr('Auto make backup file as open a file'), None)
]
Mixin.setMixin('preference', 'preflist', preflist)

def init(pref):
	pref.auto_make_bak  = False
Mixin.setPlugin('preference', 'init', init)

def openfile(win, filename):
	import shutil

	if filename and win.pref.auto_make_bak:
		bakfile = filename + '.bak'
		try:
			shutil.copyfile(filename, bakfile)
		except Exception, mesg:
			common.showerror(win, mesg)
Mixin.setPlugin('editor', 'openfile', openfile, Mixin.HIGH, 0)



#-----------------------  mAutoCheck.py ------------------

__doc__ = 'Auto check if the file is modified'

from modules import Mixin
import wx
import os, stat

preflist = [
	(tr('Document'), 210, 'check', 'auto_check', tr('Auto check if there are some opened files were modified by others'), None)
]
Mixin.setMixin('preference', 'preflist', preflist)

def init(pref):
	pref.auto_check  = False
Mixin.setPlugin('preference', 'init', init)

def on_idle(win, event):
	if win.pref.auto_check:
		for document in win.editctrl.list:
			if document.filename and document.documenttype == 'edit' and document.opened:
				if os.path.exists(document.filename) and not checkFilename(win, document) and win.editctrl.filetimes.has_key(document.filename):
					if getModifyTime(document.filename) > win.editctrl.filetimes[document.filename]:
						dlg = wx.MessageDialog(win, tr("This file [%s] has been modified by others,\ndo you like reload it?") % document.filename, tr("Check"), wx.YES_NO | wx.ICON_QUESTION)
						answer = dlg.ShowModal()
						if answer == wx.ID_YES:
							document.openfile(document.filename)
							document.editctrl.switch(document)
						win.editctrl.filetimes[document.filename] = getModifyTime(document.filename)
Mixin.setPlugin('mainframe', 'on_idle', on_idle)

def init(win):
	win.filetimes = {}
Mixin.setPlugin('editctrl', 'init', init)

def afteropenfile(win, filename):
	if filename and win.documenttype == 'edit':
		win.editctrl.filetimes[filename] = getModifyTime(filename)
Mixin.setPlugin('editor', 'afteropenfile', afteropenfile)

def aftersavefile(win, filename):
	if win.documenttype == 'edit':
		win.editctrl.filetimes[filename] = getModifyTime(filename)
Mixin.setPlugin('editor', 'aftersavefile', aftersavefile)

def closefile(win, filename):
	if filename and win.document.documenttype == 'edit':
		if win.editctrl.filetimes.has_key(filename):
			del win.editctrl.filetimes[filename]
Mixin.setPlugin('mainframe', 'closefile', closefile)

def getModifyTime(filename):
	try:
		ftime = os.stat(filename)[stat.ST_MTIME]
	except:
		ftime = 0
	return ftime

def checkFilename(win, document):
	if not document.needcheck():
		return True
	if not os.path.exists(document.filename) and win.editctrl.filetimes[document.filename] != 'NO':
		dlg = wx.MessageDialog(win, tr("This file [%s] has been removed by others,\nDo you like save it?") % document.filename, tr("Check"), wx.YES_NO | wx.ICON_QUESTION)
		answer = dlg.ShowModal()
		if answer == wx.ID_YES:
			document.savefile(document.filename, document.locale)
			document.editctrl.switch(document)
			win.editctrl.filetimes[document.filename] = getModifyTime(document.filename)
		else:
			win.editctrl.filetimes[document.filename] = 'NO'
		return True
	else:
		return False



#-----------------------  mTool.py ------------------

from modules import Mixin
import wx

__doc__ = 'Tool menu'

menulist = [(None,
	[
		(550, 'IDM_TOOL', tr('Tool'), wx.ITEM_NORMAL, None, ''),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)



#-----------------------  mPyRun.py ------------------

from modules import Mixin
import wx
import os.path
import sys
from modules import common

def init(pref):
	pref.python_interpreter = [('default', sys.executable)]
	pref.default_interpreter = 'default'
Mixin.setPlugin('preference', 'init', init)

def OnSetInterpreter(win, event):
	from InterpreterDialog import InterpreterDialog
	dlg = InterpreterDialog(win, win.pref)
	dlg.ShowModal()
Mixin.setMixin('prefdialog', 'OnSetInterpreter', OnSetInterpreter)

preflist = [
	('Python', 150, 'button', 'python_interpreter', tr('Setup python interpreter'), 'OnSetInterpreter'),
]
Mixin.setMixin('preference', 'preflist', preflist)

menulist = [('IDM_PYTHON', #parent menu id
		[
			(120, '', '-', wx.ITEM_SEPARATOR, None, ''),
			(130, 'IDM_PYTHON_RUN', tr('Run'), wx.ITEM_NORMAL, 'OnPythonRun', tr('Run python program')),
			(140, 'IDM_PYTHON_SETARGS', tr('Set Arguments...'), wx.ITEM_NORMAL, 'OnPythonSetArgs', tr('Set python program command line arugments')),
			(150, 'IDM_PYTHON_END', tr('Stop Program'), wx.ITEM_NORMAL, 'OnPythonEnd', tr('Stop current python program.')),
		]),
]
Mixin.setMixin('pythonfiletype', 'menulist', menulist)

def init(win):
	win.args = ''
	win.redirect = True
Mixin.setPlugin('editor', 'init', init)

def OnPythonRun(win, event):
	interpreters = dict(win.pref.python_interpreter)
	interpreter = interpreters[win.pref.default_interpreter]

	if win.document.isModified() or win.document.filename == '':
		d = wx.MessageDialog(win, tr("The file has not been saved, and it would not be run.\nWould you like to save the file?"), tr("Run"), wx.YES_NO | wx.ICON_QUESTION)
		answer = d.ShowModal()
		d.Destroy()
		if (answer == wx.ID_YES):
			win.OnFileSave(event)
		else:
			return
	args = win.document.args.replace('$path', os.path.dirname(win.document.filename))
	args = args.replace('$file', win.document.filename)
	ext = os.path.splitext(win.document.filename)[1].lower()
	i_main, i_ext = os.path.splitext(interpreter)
	if ext == '.pyw':
		if not i_main.endswith('w'):
			i_main += 'w'
		command = i_main + i_ext + ' -u "%s" %s' % (win.document.filename, args)
		guiflag = True
	else:
		if i_main.endswith('w'):
			i_main = i_main[:-1]
		command = i_main + i_ext + ' -u "%s" %s' % (win.document.filename, args)
		guiflag = False
	#chanage current path to filename's dirname
	path = os.path.dirname(win.document.filename)
	os.chdir(common.encode_string(path))

	win.RunCommand(command, guiflag, redirect=win.document.redirect)
Mixin.setMixin('mainframe', 'OnPythonRun', OnPythonRun)

def OnPythonSetArgs(win, event):
	from InterpreterDialog import PythonArgsDialog

	dlg = PythonArgsDialog(win, win.pref, tr('Set Python Arguments'),
		tr("Enter the command line arguments:\n$file will be replaced by current document filename\n$path will be replaced by current document filename's directory"),
		win.document.args, win.document.redirect)
	answer = dlg.ShowModal()
	if answer == wx.ID_OK:
		win.document.args = dlg.GetValue()
		win.document.redirect = dlg.GetRedirect()
Mixin.setMixin('mainframe', 'OnPythonSetArgs', OnPythonSetArgs)

def OnPythonEnd(win, event):
	if win.messagewindow.process:
		wx.Process_Kill(win.messagewindow.pid, wx.SIGKILL)
		win.messagewindow.SetReadOnly(1)
		win.messagewindow.pid = -1
		win.messagewindow.process = None
	win.SetStatusText(tr("Stopped!"), 0)
Mixin.setMixin('mainframe', 'OnPythonEnd', OnPythonEnd)

toollist = [
	(2100, 'run'),
	(2110, 'setargs'),
	(2120, 'stop'),
	(2150, '|'),
]
Mixin.setMixin('pythonfiletype', 'toollist', toollist)

toolbaritems = {
	'run':(wx.ITEM_NORMAL, 'IDM_PYTHON_RUN', common.unicode_abspath('images/run.gif'), tr('run'), tr('Run python program'), 'OnPythonRun'),
	'setargs':(wx.ITEM_NORMAL, 'IDM_PYTHON_SETARGS', common.unicode_abspath('images/setargs.gif'), tr('set arguments'), tr('Set python program command line arugments'), 'OnPythonSetArgs'),
	'stop':(wx.ITEM_NORMAL, 'IDM_PYTHON_END', common.unicode_abspath('images/stop.gif'), tr('Stop Program'), tr('Stop current python program.'), 'OnPythonEnd'),
}
Mixin.setMixin('pythonfiletype', 'toolbaritems', toolbaritems)

def OnPythonRunUpdateUI(win, event):
	eid = event.GetId()
	if not win.messagewindow:
		return
	if eid in [ win.IDM_PYTHON_RUN, win.IDM_PYTHON_SETARGS ]:
		event.Enable(not (win.messagewindow.pid > 0))
	elif eid == win.IDM_PYTHON_END:
		event.Enable(win.messagewindow.pid > 0)
Mixin.setMixin('mainframe', 'OnPythonRunUpdateUI', OnPythonRunUpdateUI)

def on_enter(mainframe, document):
	wx.EVT_UPDATE_UI(mainframe, mainframe.IDM_PYTHON_RUN, mainframe.OnPythonRunUpdateUI)
	wx.EVT_UPDATE_UI(mainframe, mainframe.IDM_PYTHON_SETARGS, mainframe.OnPythonRunUpdateUI)
	wx.EVT_UPDATE_UI(mainframe, mainframe.IDM_PYTHON_END, mainframe.OnPythonRunUpdateUI)
Mixin.setPlugin('pythonfiletype', 'on_enter', on_enter)

def on_leave(mainframe, filename, languagename):
	ret = mainframe.Disconnect(mainframe.IDM_PYTHON_RUN, -1, wx.wxEVT_UPDATE_UI)
	ret = mainframe.Disconnect(mainframe.IDM_PYTHON_SETARGS, -1, wx.wxEVT_UPDATE_UI)
Mixin.setPlugin('pythonfiletype', 'on_leave', on_leave)



#-----------------------  mShellRun.py ------------------

__doc__ = 'run shell command'

from modules import Mixin
import wx
from modules import makemenu
import sys
import os.path
import wx.lib.dialogs
import traceback
from modules import Entry

def init(pref):
	pref.shells = []
Mixin.setPlugin('preference', 'init', init)

menulist = [('IDM_TOOL',
	[
		(100, 'IDM_SHELL', tr('Shell Command'), wx.ITEM_NORMAL, None, ''),
	]),
	('IDM_SHELL', #parent menu id
	[
		(100, 'IDM_SHELL_MANAGE', tr('Shell Command Manage...'), wx.ITEM_NORMAL, 'OnShellManage', tr('Shell command manage')),
		(110, '', '-', wx.ITEM_SEPARATOR, None, ''),
		(120, 'IDM_SHELL_ITEMS', tr('(empty)'), wx.ITEM_NORMAL, 'OnShellItems', tr('Execute an shell command')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

def OnShellManage(win, event):
	from ShellDialog import ShellDialog

	dlg = ShellDialog(win, win.pref)
	answer = dlg.ShowModal()
	if answer == wx.ID_OK:
		makeshellmenu(win, win.pref)
Mixin.setMixin('mainframe', 'OnShellManage', OnShellManage)

def beforeinit(win):
	win.shellmenu_ids=[win.IDM_SHELL_ITEMS]
	makeshellmenu(win, win.pref)
Mixin.setPlugin('mainframe', 'beforeinit', beforeinit)

def makeshellmenu(win, pref):
	menu = makemenu.findmenu(win.menuitems, 'IDM_SHELL')

	for id in win.shellmenu_ids:
		menu.Delete(id)

	win.shellmenu_ids = []
	if len(win.pref.shells) == 0:
		id = win.IDM_SHELL_ITEMS
		menu.Append(id, tr('(empty)'))
		menu.Enable(id, False)
		win.shellmenu_ids=[id]
	else:
		for description, filename in win.pref.shells:
			id = wx.NewId()
			win.shellmenu_ids.append(id)
			menu.Append(id, description)
			wx.EVT_MENU(win, id, win.OnShellItems)

def OnShellItems(win, event):
	win.createMessageWindow()

	eid = event.GetId()
	index = win.shellmenu_ids.index(eid)
	command = win.pref.shells[index][1]
	command = command.replace('$path', os.path.dirname(win.document.filename))
	command = command.replace('$file', win.document.filename)
	wx.Execute(command)
Mixin.setMixin('mainframe', 'OnShellItems', OnShellItems)



#-----------------------  mSnippets.py ------------------

from modules import Mixin
import wx
import os.path
from modules import common

menulist = [
	('IDM_TOOL',
	[
		(120, 'IDM_DOCUMENT_SNIPPETS', tr('Snippets'), wx.ITEM_NORMAL, None, ''),
	]),
	('IDM_DOCUMENT_SNIPPETS',
	[
		(100, 'IDM_DOCUMENT_SNIPPETS_CATALOG_MANAGE', tr('Manage Snippets Catalog...'), wx.ITEM_NORMAL, 'OnDocumentSnippetsCatalogManage', tr('Manage snippets catalog')),
		(110, 'IDM_DOCUMENT_SNIPPETS_CODE_MANAGE', tr('Manage Snippets Code...'), wx.ITEM_NORMAL, 'OnDocumentSnippetsCodeManage', tr('Manage snippets code')),
	]),
	('IDM_WINDOW',
	[
		(150, 'IDM_WINDOW_SNIPPETS', tr('Open Snippets Window'), wx.ITEM_NORMAL, 'OnWindowSnippet', tr('Opens snippets window.'))
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

popmenulist = [ (None,
	[
		(140, 'IDPM_SNIPPETWINDOW', tr('Open Snippets Window'), wx.ITEM_NORMAL, 'OnSnippetWindow', tr('Opens snippets window.')),
	]),
]
Mixin.setMixin('notebook', 'popmenulist', popmenulist)

def init(pref):
	pref.snippet_lastitem = 0
Mixin.setPlugin('preference', 'init', init)

snippet_imagelist = {
	'close':common.unicode_abspath('images/minus.gif'),
	'open':common.unicode_abspath('images/plus.gif'),
	'item':common.unicode_abspath('images/item.gif'),
}

def afterinit(win):
	win.snippet_catalogfile = common.unicode_abspath('snippets/catalog.xml')
	win.snippet_imagelist = snippet_imagelist
	#check snippets directory, if not exists then create it
	if not os.path.exists('snippets'):
		os.mkdir('snippets')
Mixin.setPlugin('mainframe', 'afterinit', afterinit)

def createSnippetWindow(win):
	if not win.panel.getPage(tr('Snippets')):
		from SnippetWindow import MySnippet

		page = MySnippet(win.panel.createNotebook('left'), win)
		win.panel.addPage('left', page, tr('Snippets'))
Mixin.setMixin('mainframe', 'createSnippetWindow', createSnippetWindow)

def OnWindowSnippet(win, event):
	win.createSnippetWindow()
	win.panel.showPage(tr('Snippets'))
Mixin.setMixin('mainframe', 'OnWindowSnippet', OnWindowSnippet)

def OnSnippetWindow(win, event):
	win.mainframe.createSnippetWindow()
	win.panel.showPage(tr('Snippets'))
Mixin.setMixin('notebook', 'OnSnippetWindow', OnSnippetWindow)

snippets_resfile = common.unicode_abspath('resources/snippetsdialog.xrc')

def OnDocumentSnippetsCatalogManage(win, event):
	from modules import i18n
	from modules import Resource
	from SnippetWindow import SnippetsCatalogDialog

	filename = i18n.makefilename(snippets_resfile, win.app.i18n.lang)
	dlg = Resource.loadfromresfile(filename, win, SnippetsCatalogDialog, 'SnippetsCatalogDialog', win)
	dlg.Show()
Mixin.setMixin('mainframe', 'OnDocumentSnippetsCatalogManage', OnDocumentSnippetsCatalogManage)

def OnDocumentSnippetsCodeManage(win, event):
	from modules import i18n
	from modules import Resource
	from SnippetWindow import SnippetsCodeDialog

	filename = i18n.makefilename(snippets_resfile, win.app.i18n.lang)
	dlg = Resource.loadfromresfile(filename, win, SnippetsCodeDialog, 'SnippetsCodeDialog', win)
	dlg.Show()
Mixin.setMixin('mainframe', 'OnDocumentSnippetsCodeManage', OnDocumentSnippetsCodeManage)



#-----------------------  mEncoding.py ------------------

from modules import Mixin
import wx
from modules import i18n
from modules import Resource
import EncodingDialog
import os.path
from modules import common

def init(pref):
	pref.select_encoding = False
Mixin.setPlugin('preference', 'init', init)

preflist = [
	(tr('General'), 160, 'check', 'select_encoding', tr('Show encoding selection dialog as openning or saving file.'), None),
]
Mixin.setMixin('preference', 'preflist', preflist)

encoding_resfile = common.unicode_abspath('resources/encodingdialog.xrc')

def getencoding(win, mainframe):
	ret = None
	if win.pref.select_encoding:
		filename = i18n.makefilename(encoding_resfile, mainframe.app.i18n.lang)
		dlg = Resource.loadfromresfile(filename, win, EncodingDialog.EncodingDialog, 'EncodingDialog', mainframe)
		answer = dlg.ShowModal()
		if answer == wx.ID_OK:
			ret = dlg.GetValue()
			dlg.Destroy()
	return ret
Mixin.setPlugin('mainframe', 'getencoding', getencoding)

menulist = [ ('IDM_DOCUMENT',
	[
		(125, 'IDM_DOCUMENT_CHANGE_ENCODING', tr('Change Encoding...'), wx.ITEM_NORMAL, 'OnDocumentChangeEncoding', tr("Chanages current document's saving encoding.")),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

def OnDocumentChangeEncoding(win, event):
	ret = ''
	filename = i18n.makefilename(encoding_resfile, win.app.i18n.lang)
	dlg = Resource.loadfromresfile(filename, win, EncodingDialog.EncodingDialog, 'EncodingDialog', win)
	answer = dlg.ShowModal()
	if answer == wx.ID_OK:
		ret = dlg.GetValue()
		dlg.Destroy()
		win.document.locale = ret
		win.SetStatusText(win.document.locale, 4)
		win.document.modified = True
		win.editctrl.showTitle(win.document)
Mixin.setMixin('mainframe', 'OnDocumentChangeEncoding', OnDocumentChangeEncoding)



#-----------------------  mShowLocale.py ------------------

__doc__ = 'show document locale in statusbar'

from modules import Mixin
import wx

def on_document_enter(win, document):
	if document.documenttype == 'edit':
		win.mainframe.SetStatusText(win.document.locale, 4)
Mixin.setPlugin('editctrl', 'on_document_enter', on_document_enter)

def fileopentext(win, stext):
	win.mainframe.SetStatusText(win.locale, 4)
Mixin.setPlugin('editor', 'openfiletext', fileopentext)

def afteropenfile(win, filename):
	win.mainframe.SetStatusText(win.locale, 4)
Mixin.setPlugin('editor', 'afteropenfile', afteropenfile)



#-----------------------  mDDESupport.py ------------------

__doc__ = 'simulate DDE support'

import sys
from modules import DDE
from modules import Mixin
import wx
from modules import IniFile

def init(app, filenames):
	if app.ddeflag:
		ini = IniFile.IniFile('config.ini')
		port = ini.getint('server', 'port', 0)
		if not DDE.run(app, port):
			DDE.senddata('\n'.join(filenames))
			sys.exit(0)
Mixin.setPlugin('app', 'start', init, Mixin.HIGH, 0)

def afterclosewindow(win):
	if win.app.ddeflag:
		DDE.stop()
Mixin.setPlugin('mainframe', 'afterclosewindow', afterclosewindow)

def openfiles(win, files):
	if files:
		for filename in files:
			win.editctrl.new(filename)
		win.Show()
		win.Raise()
Mixin.setMixin('mainframe', 'openfiles', openfiles)



#-----------------------  mLexerFactory.py ------------------

__doc__ = 'Lexer control'

from modules import Mixin
import wx
import os.path
from LexerFactory import LexerFactory

def afteropenfile(win, filename):
	for lexer in win.mainframe.lexers.lexobjs:
		if lexer.matchfile(filename):
			lexer.colourize(win)
			return
	else:
		if filename:
			win.mainframe.lexers.getNamedLexer('text').colourize(win)
		else:
			win.mainframe.lexers.getDefaultLexer().colourize(win)
Mixin.setPlugin('editor', 'afteropenfile', afteropenfile)

def aftersavefile(win, filename):
	for lexer in win.mainframe.lexers.lexobjs:
		if lexer.matchfile(filename):
			lexer.colourize(win)
			return
Mixin.setPlugin('editor', 'aftersavefile', aftersavefile)

def beforeinit(win):
	win.lexers = LexerFactory(win)
Mixin.setPlugin('mainframe', 'beforeinit', beforeinit)


menulist = [ ('IDM_DOCUMENT',
	[
		(130, '', '-', wx.ITEM_SEPARATOR, None, ''),
		(140, 'IDM_DOCUMENT_SYNTAX_HIGHLIGHT', tr('Syntax Highlight...'), wx.ITEM_NORMAL, 'OnDocumentSyntaxHighlight', tr('Specifies the syntax highlight to current document.')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

def OnDocumentSyntaxHighlight(win, event):
	items = [lexer.name for lexer in win.lexers.lexobjs]
	dlg = wx.SingleChoiceDialog(win, tr('Select a syntax highlight'), tr('Syntax Highlight'), items, wx.CHOICEDLG_STYLE)
	if dlg.ShowModal() == wx.ID_OK:
		lexer = win.lexers.lexobjs[dlg.GetSelection()]
		lexer.colourize(win.document)
		win.editctrl.switch(win.document)
	dlg.Destroy()
Mixin.setMixin('mainframe', 'OnDocumentSyntaxHighlight', OnDocumentSyntaxHighlight)

preflist = [
	(tr('General'), 170, 'choice', 'default_lexer', tr('Default syntax highlight'), LexerFactory.lexnames),
	(tr('General'), 180, 'check', 'caret_line_visible', tr('Show caret line'), None),
]
Mixin.setMixin('preference', 'preflist', preflist)

def init(pref):
	pref.default_lexer = 'text'
	pref.caret_line_visible = True
Mixin.setPlugin('preference', 'init', init)

def savepreference(mainframe, pref):
	mainframe.document.SetCaretLineVisible(pref.caret_line_visible)
Mixin.setPlugin('prefdialog', 'savepreference', savepreference)



#-----------------------  mChangeFileType.py ------------------

__doc__ = 'Process changing file type event'

from modules import Mixin
import wx

def on_document_enter(win, document):
	win.mainframe.changefiletype.enter(win.mainframe, document)
Mixin.setPlugin('editctrl', 'on_document_enter', on_document_enter)

def on_document_leave(win, filename, languagename):
	win.mainframe.changefiletype.leave(win.mainframe, filename, languagename)
Mixin.setPlugin('editctrl', 'on_document_leave', on_document_leave)

def afterinit(win):
	import ChangeFileType

	win.changefiletype = ChangeFileType.ChangeFileType()
Mixin.setPlugin('mainframe', 'afterinit', afterinit)



#-----------------------  mSyntaxPref.py ------------------

__doc__ = 'syntax preference'

from modules import Mixin
import wx
import os.path
from modules import common

menulist = [ ('IDM_DOCUMENT',
	[
		(150, 'IDM_DOCUMENT_SYNTAX_PREFERENCE', tr('Syntax Preference...'), wx.ITEM_NORMAL, 'OnDocumentSyntaxPreference', tr('Syntax highlight preference setup.')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

syntax_resfile = common.unicode_abspath('resources/syntaxdialog.xrc')

def OnDocumentSyntaxPreference(win, event):
	from modules import i18n
	from modules import Resource
	import SyntaxDialog

	filename = i18n.makefilename(syntax_resfile, win.app.i18n.lang)
	if hasattr(win.document, 'languagename'):
		name = win.document.languagename
	else:
		name = ''
	Resource.loadfromresfile(filename, win, SyntaxDialog.SyntaxDialog, 'SyntaxDialog', win, win.lexers, name).ShowModal()
Mixin.setMixin('mainframe', 'OnDocumentSyntaxPreference', OnDocumentSyntaxPreference)



#-----------------------  mPrint.py ------------------

__doc__ = 'print'

from modules import Mixin
import wx
import os
from modules import common

menulist = [('IDM_FILE',
	[
		(200, '', '-', wx.ITEM_SEPARATOR, None, ''),
		(210, 'IDM_FILE_PRINT_MENU', tr('Print'), wx.ITEM_NORMAL, '', None),
	]),
	('IDM_FILE_PRINT_MENU',
	[
		(100, 'IDM_FILE_PAGE_SETUP', tr('Page Setup...'), wx.ITEM_NORMAL, 'OnFilePageSetup', tr('Set page layout and options.')),
		(110, 'IDM_FILE_PRINTER_SETUP', tr('Printer Setup...'), wx.ITEM_NORMAL, 'OnFilePrinterSetup', tr('Selects a printer and printer connection.')),
		(120, 'IDM_FILE_PRINT_PREVIEW', tr('Print Preview...'), wx.ITEM_NORMAL, 'OnFilePrintPreview', tr('Displays the document on the screen as it would appear printed.')),
		(130, 'IDM_FILE_PRINT', tr('Print...'), wx.ITEM_NORMAL, 'OnFilePrint', tr('Prints a document.')),
		(140, 'IDM_FILE_HTML', tr('Html File'), wx.ITEM_NORMAL, '', None),
	]),
	('IDM_FILE_HTML',
	[
		(100, 'IDM_FILE_HTML_PRINT_PREVIEW', tr('Html File Preview...'), wx.ITEM_NORMAL, 'OnFileHtmlPreview', tr('Displays the html document on the screen as it would appear printed.')),
		(110, 'IDM_FILE_HTML_PRINT', tr('Html File Print...'), wx.ITEM_NORMAL, 'OnFileHtmlPrint', tr('Prints a html document.')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

toollist = [
	(125, 'print'),
]
Mixin.setMixin('mainframe', 'toollist', toollist)

toolbaritems = {
	'print':(wx.ITEM_NORMAL, 'IDM_FILE_PRINT', common.unicode_abspath('images/printer.gif'), tr('print'), tr('Prints a document.'), 'OnFilePrint'),
}
Mixin.setMixin('mainframe', 'toolbaritems', toolbaritems)

def init(win):
	from Print import MyPrinter

	win.printer = MyPrinter(win)
Mixin.setPlugin('mainframe', 'init', init)

def OnFilePageSetup(win, event):
	win.printer.PageSetup()
Mixin.setMixin('mainframe', 'OnFilePageSetup', OnFilePageSetup)

def OnFilePrint(win, event):
	win.printer.PrintText(win.printer.convertText(win.document.GetText()), os.path.dirname(win.document.filename))
Mixin.setMixin('mainframe', 'OnFilePrint', OnFilePrint)

def OnFilePrintPreview(win, event):
	win.printer.PreviewText(win.printer.convertText(win.document.GetText()), os.path.dirname(win.document.filename))
Mixin.setMixin('mainframe', 'OnFilePrintPreview', OnFilePrintPreview)

def OnFilePrinterSetup(win, event):
	win.printer.PrinterSetup()
Mixin.setMixin('mainframe', 'OnFilePrinterSetup', OnFilePrinterSetup)

def OnFileHtmlPreview(win, event):
	win.printer.PreviewText(win.document.GetText(), os.path.dirname(win.document.filename))
Mixin.setMixin('mainframe', 'OnFileHtmlPreview', OnFileHtmlPreview)

def OnFileHtmlPrint(win, event):
	win.printer.PrintText(win.document.GetText(), os.path.dirname(win.document.filename))
Mixin.setMixin('mainframe', 'OnFileHtmlPrint', OnFileHtmlPrint)



#-----------------------  mPlugins.py ------------------

__doc__ = 'Plugins manage'

from modules import Mixin
import wx
from modules import common

menulist = [ ('IDM_TOOL',
	[
		(130, 'IDM_TOOL_PLUGINS_MANAGE', tr('Plugins Manage...'), wx.ITEM_NORMAL, 'OnDocumentPluginsManage', 'Manages plugins.'),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

def OnDocumentPluginsManage(win, event):
	from PluginDialog import PluginDialog

	dlg = PluginDialog(win)
	answer = dlg.ShowModal()
	dlg.Destroy()
Mixin.setMixin('mainframe', 'OnDocumentPluginsManage', OnDocumentPluginsManage)

plugin_imagelist = {
	'uncheck':	common.unicode_abspath('images/uncheck.gif'),
	'check':	common.unicode_abspath('images/check.gif'),
}

def afterinit(win):
	win.plugin_imagelist = plugin_imagelist
	win.plugin_initfile = common.get_app_filename(win, 'plugins/__init__.py')
Mixin.setPlugin('mainframe', 'afterinit', afterinit)



#-----------------------  mPythonContextIndent.py ------------------

__doc__ = 'Context indent'

from modules import Mixin
import wx
import wx.stc
import re

def OnKeyDown(win, event):
	if event.GetKeyCode() == wx.WXK_RETURN:
		if win.GetSelectedText():
			return False
		if win.pref.autoindent and win.pref.python_context_indent and win.languagename == 'python':
			pythonContextIndent(win)
			return True
Mixin.setPlugin('editor', 'on_key_down', OnKeyDown, Mixin.HIGH)

preflist = [
	('Python', 110, 'check', 'python_context_indent', tr('Use context sensitive indent'), None)
]
Mixin.setMixin('preference', 'preflist', preflist)

def init(pref):
	pref.python_context_indent = True
Mixin.setPlugin('preference', 'init', init)

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



#-----------------------  mFtp.py ------------------

__doc__ = 'ftp manage'

from modules import Mixin
import wx
from modules.Debug import error
import os.path
from modules import common

menulist = [ ('IDM_WINDOW',
	[
		(160, 'IDM_WINDOW_FTP', tr('Open Ftp Window'), wx.ITEM_NORMAL, 'OnWindowFtp', tr('Opens ftp window.')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

ftp_imagelist = {
	'close':		common.unicode_abspath('images/folderclose.gif'),
	'document':		common.unicode_abspath('images/file.gif'),
	'parentfold':	common.unicode_abspath('images/parentfold.gif'),
}
ftp_resfile = common.unicode_abspath('resources/ftpmanagedialog.xrc')


def afterinit(win):
	win.ftp_imagelist = ftp_imagelist
	win.ftp_resfile = ftp_resfile
	win.ftp = None
Mixin.setPlugin('mainframe', 'afterinit', afterinit)

popmenulist = [ (None,
	[
		(150, 'IDPM_FTPWINDOW', tr('Open Ftp Window'), wx.ITEM_NORMAL, 'OnFtpWindow', tr('Opens ftp window.')),
	]),
]
Mixin.setMixin('notebook', 'popmenulist', popmenulist)

def createFtpWindow(win):
	page = win.panel.getPage('Ftp')
	if not page:
		from FtpClass import Ftp

		page = Ftp(win.panel.createNotebook('bottom'), win)
		win.panel.addPage('bottom', page, 'Ftp')
	win.ftp = page
Mixin.setMixin('mainframe', 'createFtpWindow', createFtpWindow)

def OnWindowFtp(win, event):
	win.createFtpWindow()
	win.panel.showPage('Ftp')
Mixin.setMixin('mainframe', 'OnWindowFtp', OnWindowFtp)

def OnFtpWindow(win, event):
	win.mainframe.createFtpWindow()
	win.panel.showPage('Ftp')
Mixin.setMixin('notebook', 'OnFtpWindow', OnFtpWindow)

def init(pref):
	pref.ftp_sites = []
	pref.sites_info = {}
	pref.last_ftp_site = 0
	pref.remote_paths = []
Mixin.setPlugin('preference', 'init', init)

def afterclosewindow(win):
	if win.ftp and win.ftp.alive:
		try:
			win.ftp.ftp.quit()
		except:
			error.traceback()
Mixin.setPlugin('mainframe', 'afterclosewindow', afterclosewindow)

popmenulist = [ (None, #parent menu id
	[
		(100, 'IDPM_OPEN', tr('Open'), wx.ITEM_NORMAL, 'OnOpen', tr('Open an file or directory.')),
		(110, 'IDPM_NEWFILE', tr('New File'), wx.ITEM_NORMAL, 'OnNewFile', tr('Create an new file.')),
		(120, 'IDPM_NEWDIR', tr('New Directory'), wx.ITEM_NORMAL, 'OnNewDir', tr('Create an new directory.')),
		(130, 'IDPM_DELETE', tr('Delete'), wx.ITEM_NORMAL, 'OnDelete', tr('Delete selected file or directory.')),
		(140, 'IDPM_RENAME', tr('Rename'), wx.ITEM_NORMAL, 'OnRename', tr('Rename selected file or directory.')),
		(150, '-', '', wx.ITEM_SEPARATOR, '', ''),
		(160, 'IDPM_REFRESH', tr('Refresh'), wx.ITEM_NORMAL, 'OnRefresh', tr('Refresh current directory.')),
		(170, '-', '', wx.ITEM_SEPARATOR, '', ''),
		(180, 'IDPM_UPLOAD', tr('Upload'), wx.ITEM_NORMAL, 'OnUpload', tr('Upload files.')),
		(190, 'IDPM_DOWNLOAD', tr('Download'), wx.ITEM_NORMAL, 'OnDownload', tr('Download files.')),
	]),
]
Mixin.setMixin('ftpclass', 'popmenulist', popmenulist)

def OnOpen(win, event):
	win.OnEnter(event)
Mixin.setMixin('ftpclass', 'OnOpen', OnOpen)

def OnNewFile(win, event):
	win.newfile()
Mixin.setMixin('ftpclass', 'OnNewFile', OnNewFile)

def OnNewDir(win, event):
	win.newdir()
Mixin.setMixin('ftpclass', 'OnNewDir', OnNewDir)

def OnDelete(win, event):
	win.delete()
Mixin.setMixin('ftpclass', 'OnDelete', OnDelete)

def OnRename(win, event):
	win.rename()
Mixin.setMixin('ftpclass', 'OnRename', OnRename)

def OnUpload(win, event):
	win.upload()
Mixin.setMixin('ftpclass', 'OnUpload', OnUpload)

def OnDownload(win, event):
	win.download()
Mixin.setMixin('ftpclass', 'OnDownload', OnDownload)

def readfiletext(win, filename, stext):
	import re

	re_ftp = re.compile('^ftp\((\d+)\):')
	b = re_ftp.search(filename)
	if b:
		siteno = int(b.group(1))
		filename = filename.split(':')[1]
		from FtpClass import readfile
		text = readfile(win.mainframe, filename, siteno)
		win.needcheckfile = False
		if text is not None:
			stext.append(text)
		else:
			stext.append(None)
		return True, True
Mixin.setPlugin('editor', 'readfiletext', readfiletext)

def writefiletext(win, filename, text):
	import re

	re_ftp = re.compile('^ftp\((\d+)\):')
	b = re_ftp.search(filename)
	if b:
		siteno = int(b.group(1))
		filename = filename.split(':', 1)[1]
		from FtpClass import writefile
		flag = writefile(win.mainframe, filename, siteno, text)
		return True, True, flag
Mixin.setPlugin('editor', 'writefiletext', writefiletext)

toollist = [
	(127, 'ftp'),
]
Mixin.setMixin('mainframe', 'toollist', toollist)

toolbaritems = {
	'ftp':(wx.ITEM_NORMAL, 'IDM_FILE_FTP', common.unicode_abspath('images/ftp.gif'), tr('open ftp window'), tr('Opens ftp window.'), 'OnWindowFtp'),
}
Mixin.setMixin('mainframe', 'toolbaritems', toolbaritems)

def getShortFilename(win):
	import re
	import os.path

	if win.title:
		return win.title

	re_ftp = re.compile('^ftp\((\d+)\):')
	b = re_ftp.search(win.filename)
	if b:
		return os.path.basename(win.filename.split(':', 1)[1])
	else:
		return os.path.basename(win.getFilename())
Mixin.setMixin('editor', 'getShortFilename', getShortFilename)



#-----------------------  mWindow.py ------------------

from modules import Mixin
import wx
from modules import common

menulist = [(None,
	[
		(700, 'IDM_WINDOW', tr('Window'), wx.ITEM_NORMAL, '', ''),
	]),
	('IDM_WINDOW',
	[
		(100, 'IDM_WINDOW_LEFT', tr('Left Window')+'\tAlt+L', wx.ITEM_CHECK, 'OnWindowLeft', tr('Shows or hides the left Window')),
		(110, 'IDM_WINDOW_BOTTOM', tr('Bottom Window')+'\tAlt+B', wx.ITEM_CHECK, 'OnWindowBottom', tr('Shows or hides the bottom Window')),
		(120, '-', '', wx.ITEM_SEPARATOR, '', ''),
		(130, 'IDM_WINDOW_SHELL', tr('Open Shell Window'), wx.ITEM_NORMAL, 'OnWindowShell', tr('Opens shell window.')),
		(140, 'IDM_WINDOW_MESSAGE', tr('Open Message Window'), wx.ITEM_NORMAL, 'OnWindowMessage', tr('Opens message window.')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)


def OnWindowLeft(win, event):
	flag = not win.panel.LeftIsVisible

	if flag:
		win.createSnippetWindow()

	win.panel.showWindow('left', flag)
Mixin.setMixin('mainframe', 'OnWindowLeft', OnWindowLeft)

def OnWindowBottom(win, event):
	flag = not win.panel.BottomIsVisible
	if flag:
		win.createShellWindow()
		win.createMessageWindow()

	win.panel.showWindow('bottom', flag)
Mixin.setMixin('mainframe', 'OnWindowBottom', OnWindowBottom)

def OnUpdateUI(win, event):
	eid = event.GetId()
	if eid == win.IDM_WINDOW_LEFT:
		event.Check(win.panel.LeftIsVisible)
	elif eid == win.IDM_WINDOW_BOTTOM:
		event.Check(win.panel.BottomIsVisible)
Mixin.setPlugin('mainframe', 'on_update_ui', OnUpdateUI)

def afterinit(win):
	wx.EVT_UPDATE_UI(win, win.IDM_WINDOW_LEFT, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDM_WINDOW_BOTTOM, win.OnUpdateUI)
	win.messagewindow = None
	win.shellwindow = None
Mixin.setPlugin('mainframe', 'afterinit', afterinit)

toollist = [
	(450, 'left'),
	(500, 'bottom'),
]
Mixin.setMixin('mainframe', 'toollist', toollist)

toolbaritems = {
	'left':(wx.ITEM_CHECK, 'IDM_WINDOW_LEFT', common.unicode_abspath('images/left.gif'), tr('Left Window'), tr('Shows or hides the left Window'), 'OnViewToolWindowLeft'),
	'bottom':(wx.ITEM_CHECK, 'IDM_WINDOW_BOTTOM', common.unicode_abspath('images/bottom.gif'), tr('Bottom Window'), tr('Shows or hides the bottom Window'), 'OnViewToolWindowBottom'),
}
Mixin.setMixin('mainframe', 'toolbaritems', toolbaritems)

def createShellWindow(win):
	if not win.panel.getPage(tr('Shell')):
		from ShellWindow import ShellWindow

		page = ShellWindow(win.panel.createNotebook('bottom'), win)
		win.panel.addPage('bottom', page, tr('Shell'))
	win.shellwindow = win.panel.getPage(tr('Shell'))
Mixin.setMixin('mainframe', 'createShellWindow', createShellWindow)

def createMessageWindow(win):
	if not win.panel.getPage(tr('Message')):
		from MessageWindow import MessageWindow

		page = MessageWindow(win.panel.createNotebook('bottom'), win)
		win.panel.addPage('bottom', page, tr('Message'))
	win.messagewindow = win.panel.getPage(tr('Message'))
Mixin.setMixin('mainframe', 'createMessageWindow', createMessageWindow)

def OnWindowShell(win, event):
	win.createShellWindow()
	win.panel.showPage(tr('Shell'))
Mixin.setMixin('mainframe', 'OnWindowShell', OnWindowShell)

def OnWindowMessage(win, event):
	win.createMessageWindow()
	win.panel.showPage(tr('Message'))
Mixin.setMixin('mainframe', 'OnWindowMessage', OnWindowMessage)

popmenulist = [ (None,
	[
		(120, 'IDPM_SHELLWINDOW', tr('Open Shell Window'), wx.ITEM_NORMAL, 'OnShellWindow', tr('Opens shell window.')),
		(130, 'IDPM_MESSAGEWINDOW', tr('Open Message Window'), wx.ITEM_NORMAL, 'OnMessageWindow', tr('Opens message window.')),
	]),
]
Mixin.setMixin('notebook', 'popmenulist', popmenulist)

def OnShellWindow(win, event):
	win.mainframe.createShellWindow()
	win.panel.showPage(tr('Shell'))
Mixin.setMixin('notebook', 'OnShellWindow', OnShellWindow)

def OnMessageWindow(win, event):
	win.mainframe.createMessageWindow()
	win.panel.showPage(tr('Message'))
Mixin.setMixin('notebook', 'OnMessageWindow', OnMessageWindow)



#-----------------------  mRegister.py ------------------

import wx

if wx.Platform == '__WXMSW__':
	from modules import Mixin
	from modules.Debug import error
	import os.path
	import sys

	import _winreg

	menulist = [ ('IDM_OPTION',
	[
		(120, 'IDM_OPTION_REGISTER', tr('Register to Explore'), wx.ITEM_NORMAL, 'OnOptionRegister', tr('Registers to explore context menu.')),
		(130, 'IDM_OPTION_UNREGISTER', tr('Unregister from Explore'), wx.ITEM_NORMAL, 'OnOptionUnRegister', tr('Unregisters from explore context menu.')),
	]),
	]
	Mixin.setMixin('mainframe', 'menulist', menulist)

	def OnOptionRegister(win, event):
		try:
			key = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, '*\\shell', _winreg.KEY_ALL_ACCESS)
			filename = os.path.basename(sys.argv[0])
			f, ext = os.path.splitext(filename)
			if ext == '.exe':
				command = '"%s" %%L' % os.path.normpath(os.path.join(win.app.workpath, filename))
			else:
				path = os.path.normpath(os.path.join(win.app.workpath, '%s.pyw' % f))
				command = '"pythonw.exe" "%s" "%%L"' % path
			_winreg.SetValue(key, 'NewEdit\\command', _winreg.REG_SZ, command)
			wx.MessageDialog(win, tr('Successful!'), tr("Message"), wx.OK | wx.ICON_INFORMATION).ShowModal()
		except:
			error.traceback()
			wx.MessageDialog(win, tr('Register to explore context menu failed!'), tr("Error"), wx.OK | wx.ICON_INFORMATION).ShowModal()
	Mixin.setMixin('mainframe', 'OnOptionRegister', OnOptionRegister)

	def OnOptionUnRegister(win, event):
		try:
			key = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, '*\\shell', _winreg.KEY_ALL_ACCESS)
			_winreg.DeleteKey(key, 'NewEdit\\command')
			_winreg.DeleteKey(key, 'NewEdit')
			wx.MessageDialog(win, tr('Successful!'), tr("Message"), wx.OK | wx.ICON_INFORMATION).ShowModal()
		except:
			error.traceback()
			wx.MessageDialog(win, tr('Unregister from explore context menu failed!'), tr("Error"), wx.OK | wx.ICON_INFORMATION).ShowModal()
	Mixin.setMixin('mainframe', 'OnOptionUnRegister', OnOptionUnRegister)



#-----------------------  mConvert.py ------------------

from modules import Mixin
from modules.Debug import error
import wx
from modules import common

menulist = [ ('IDM_EDIT',
	[
		(270, 'IDM_EDIT_CONVERT', tr('Convert'), wx.ITEM_NORMAL, None, ''),
	]),
	('IDM_EDIT_CONVERT',
	[
		(100, 'IDM_EDIT_CONVERT_OUTPUTHTMLWINDOW', tr('Output In Html Window'), wx.ITEM_RADIO, 'OnConvertOutput', tr('Outputs converted text in html window.')),
		(110, 'IDM_EDIT_CONVERT_OUTPUTMESSAGEWINDOW', tr('Output In Message Window'), wx.ITEM_RADIO, 'OnConvertOutput', tr('Outputs converted text in message window.')),
		(120, 'IDM_EDIT_CONVERT_REPLACEHERE', tr('Replace Selected Text'), wx.ITEM_RADIO, 'OnConvertOutput', tr('Replaces selected text with converted text.')),
		(130, '', '-', wx.ITEM_SEPARATOR, '', ''),
		(140, 'IDM_EDIT_CONVERT_DIRECT', tr('Output Directly In Html Window'), wx.ITEM_NORMAL, 'OnConvertOutputDirectly', tr('Outputs directly the text in html window.')),
		(150, 'IDM_EDIT_CONVERT_REST2HTML', tr('reSt to Html'), wx.ITEM_NORMAL, 'OnConvertRest2Html', tr('Converts reStructuredText source to Html.')),
		(160, 'IDM_EDIT_CONVERT_PY2HTML', tr('Py to Html'), wx.ITEM_NORMAL, 'OnConvertPy2Html', tr('Converts python source to Html.')),
		(170, 'IDM_EDIT_CONVERT_TEXTILE2HTML', tr('Textile to Html'), wx.ITEM_NORMAL, 'OnConvertTextile2Html', tr('Converts textile source to Html.')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

popmenulist = [ (None,
	[
		(240, 'IDPM_EDIT_CONVERT', tr('Convert'), wx.ITEM_NORMAL, None, ''),
	]),
	('IDPM_EDIT_CONVERT',
	[
		(100, 'IDPM_EDIT_CONVERT_OUTPUTHTMLWINDOW', tr('Output In Html Window'), wx.ITEM_RADIO, 'OnConvertOutput', tr('Outputs converted text in html window.')),
		(110, 'IDPM_EDIT_CONVERT_OUTPUTMESSAGEWINDOW', tr('Output In Message Window'), wx.ITEM_RADIO, 'OnConvertOutput', tr('Outputs converted text in message window.')),
		(120, 'IDPM_EDIT_CONVERT_REPLACEHERE', tr('Replace Selected Text'), wx.ITEM_RADIO, 'OnConvertOutput', tr('Replaces selected text with converted text.')),
		(130, '', '-', wx.ITEM_SEPARATOR, '', ''),
		(140, 'IDPM_EDIT_CONVERT_DIRECT', tr('Output Directly In Html Window'), wx.ITEM_NORMAL, 'OnOutputDirectly', tr('Outputs directly the text in html window.')),
		(150, 'IDPM_EDIT_CONVERT_REST2HTML', tr('reSt to Html'), wx.ITEM_NORMAL, 'OnRest2Html', tr('Converts reStructuredText source to Html.')),
		(160, 'IDPM_EDIT_CONVERT_PY2HTML', tr('Py to Html'), wx.ITEM_NORMAL, 'OnPy2Html', tr('Converts python source to Html.')),
		(170, 'IDPM_EDIT_CONVERT_TEXTILE2HTML', tr('Textile to Html'), wx.ITEM_NORMAL, 'OnTextile2Html', tr('Converts textile source to Html.')),
	]),
]
Mixin.setMixin('editor', 'popmenulist', popmenulist)


def OnConvertOutputDirectly(win, event):
	text = win.document.GetSelectedText()
	output_text(win, text, mode=0)
Mixin.setMixin('mainframe', 'OnConvertOutputDirectly', OnConvertOutputDirectly)

def OnOutputDirectly(win, event):
	win.mainframe.OnConvertOutputDirectly(event)
Mixin.setMixin('editor', 'OnOutputDirectly', OnOutputDirectly)

def OnConvertRest2Html(win, event):
	try:
		def html_fragment(input_string, source_path=None, destination_path=None,
					   input_encoding='unicode', doctitle=1, initial_header_level=1):
			from docutils import core

			overrides = {'input_encoding': input_encoding,
						 'doctitle_xform': doctitle,
						 'initial_header_level': initial_header_level}
			parts = core.publish_parts(
				source=input_string, source_path=source_path,
				destination_path=destination_path,
				writer_name='html', settings_overrides=overrides)
			fragment = parts['fragment']
			return fragment

		text = win.document.GetSelectedText()
		otext = html_fragment(text)
		output_text(win, otext)
	except Exception, msg:
		error.traceback()
		common.showerror(win, msg)
Mixin.setMixin('mainframe', 'OnConvertRest2Html', OnConvertRest2Html)

def OnRest2Html(win, event):
	win.mainframe.OnConvertRest2Html(event)
Mixin.setMixin('editor', 'OnRest2Html', OnRest2Html)

def OnConvertTextile2Html(win, event):
	try:
		import textile
	except:
		error.traceback()
		common.showmessage(win, tr("You should install textile module first!"))

	class MyTextiler(textile.Textiler):
		def process(self, head_offset=textile.HEAD_OFFSET):
			self.head_offset = head_offset

			# Process each block.
			self.blocks = self.split_text()

			text = []
			for [function, captures] in self.blocks:
				text.append(function(**captures))

			text = '\n\n'.join(text)

			# Add titles to footnotes.
			text = self.footnotes(text)


			return text
	try:
		text = win.document.GetSelectedText()
		t = MyTextiler(text)
		otext = t.process()

		output_text(win, otext)
	except Exception, msg:
		error.traceback()
		common.showerror(win, msg)
Mixin.setMixin('mainframe', 'OnConvertTextile2Html', OnConvertTextile2Html)

def OnTextile2Html(win, event):
	win.mainframe.OnConvertTextile2Html(event)
Mixin.setMixin('editor', 'OnTextile2Html', OnTextile2Html)

def OnConvertPy2Html(win, event):
	from modules import colourize

	text = win.document.GetSelectedText()
	otext = colourize.Parser(text).format()

	output_text(win, otext)
Mixin.setMixin('mainframe', 'OnConvertPy2Html', OnConvertPy2Html)

def OnPy2Html(win, event):
	win.mainframe.OnConvertPy2Html(event)
Mixin.setMixin('editor', 'OnPy2Html', OnPy2Html)

def OnConvertOutput(win, event):
	eid = event.GetId()
	if eid == win.IDM_EDIT_CONVERT_OUTPUTHTMLWINDOW:
		win.pref.converted_output = 0
	elif eid == win.IDM_EDIT_CONVERT_OUTPUTMESSAGEWINDOW:
		win.pref.converted_output = 1
	elif eid == win.IDM_EDIT_CONVERT_REPLACEHERE:
		win.pref.converted_output = 2
	win.pref.save()
Mixin.setMixin('mainframe', 'OnConvertOutput', OnConvertOutput)

def OnConvertOutput(win, event):
	eid = event.GetId()
	if eid == win.IDPM_EDIT_CONVERT_OUTPUTHTMLWINDOW:
		win.pref.converted_output = 0
	elif eid == win.IDPM_EDIT_CONVERT_OUTPUTMESSAGEWINDOW:
		win.pref.converted_output = 1
	elif eid == win.IDPM_EDIT_CONVERT_REPLACEHERE:
		win.pref.converted_output = 2
	win.pref.save()
Mixin.setMixin('editor', 'OnConvertOutput', OnConvertOutput)

def init(win):
	wx.EVT_UPDATE_UI(win, win.IDM_EDIT_CONVERT_REST2HTML, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDM_EDIT_CONVERT_PY2HTML, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDM_EDIT_CONVERT_TEXTILE2HTML, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDM_EDIT_CONVERT_OUTPUTHTMLWINDOW, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDM_EDIT_CONVERT_DIRECT, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDM_EDIT_CONVERT_OUTPUTMESSAGEWINDOW, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDM_EDIT_CONVERT_REPLACEHERE, win.OnUpdateUI)
Mixin.setPlugin('mainframe', 'init', init)

def OnUpdateUI(win, event):
	eid = event.GetId()
	if hasattr(win, 'document') and win.document:
		if eid in [win.IDM_EDIT_CONVERT_DIRECT, win.IDM_EDIT_CONVERT_REST2HTML,
			win.IDM_EDIT_CONVERT_PY2HTML, win.IDM_EDIT_CONVERT_TEXTILE2HTML]:
			event.Enable(win.document.GetSelectedText and len(win.document.GetSelectedText()) > 0)
		elif eid == win.IDM_EDIT_CONVERT_OUTPUTHTMLWINDOW:
			event.Check(win.pref.converted_output == 0)
		elif eid == win.IDM_EDIT_CONVERT_OUTPUTMESSAGEWINDOW:
			event.Check(win.pref.converted_output == 1)
		elif eid == win.IDM_EDIT_CONVERT_REPLACEHERE:
			event.Check(win.pref.converted_output == 2)
Mixin.setPlugin('mainframe', 'on_update_ui', OnUpdateUI)

def init(win):
	wx.EVT_UPDATE_UI(win, win.IDPM_EDIT_CONVERT_REST2HTML, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDPM_EDIT_CONVERT_PY2HTML, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDPM_EDIT_CONVERT_TEXTILE2HTML, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDPM_EDIT_CONVERT_DIRECT, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDPM_EDIT_CONVERT_OUTPUTHTMLWINDOW, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDPM_EDIT_CONVERT_OUTPUTMESSAGEWINDOW, win.OnUpdateUI)
	wx.EVT_UPDATE_UI(win, win.IDPM_EDIT_CONVERT_REPLACEHERE, win.OnUpdateUI)
Mixin.setPlugin('editor', 'init', init)

def OnUpdateUI(win, event):
	eid = event.GetId()
	if eid in [win.IDPM_EDIT_CONVERT_DIRECT, win.IDPM_EDIT_CONVERT_REST2HTML,
		win.IDPM_EDIT_CONVERT_PY2HTML, win.IDPM_EDIT_CONVERT_TEXTILE2HTML]:
		event.Enable(len(win.GetSelectedText()) > 0)
	elif eid == win.IDPM_EDIT_CONVERT_OUTPUTHTMLWINDOW:
		event.Check(win.pref.converted_output == 0)
	elif eid == win.IDPM_EDIT_CONVERT_OUTPUTMESSAGEWINDOW:
		event.Check(win.pref.converted_output == 1)
	elif eid == win.IDPM_EDIT_CONVERT_REPLACEHERE:
		event.Check(win.pref.converted_output == 2)
Mixin.setPlugin('editor', 'on_update_ui', OnUpdateUI)

def init(pref):
	pref.converted_output = 0
Mixin.setPlugin('preference', 'init', init)

preflist = [
	(tr('Document'), 240, 'choice', 'converted_output', tr('Choose where converted text is be outputed:'), [tr('In html window'), tr('In message window'), tr('Replace selected text')]),
]
Mixin.setMixin('preference', 'preflist', preflist)

def output_text(mainframe, text, mode=-1):
	win = mainframe

	if mode == -1:
		mode = win.pref.converted_output

	if mode == 0:
		from HtmlPage import HtmlDialog

		ot = """<html>
<head>
   <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<body>
%s
</body>
</html>
""" % text.encode('utf-8')

		HtmlDialog(win, tr('Html Convertion'), ot).ShowModal()
	elif mode == 1:
		win.createMessageWindow()
		win.panel.showPage(tr('Message'))
		win.messagewindow.SetText(text)
	elif mode == 2:
		win.document.ReplaceSelection(text)



#-----------------------  mHtmlFileType.py ------------------

__doc__ = 'Html syntax highlitght process'

from modules import Mixin
import wx
import FiletypeBase
import os.path
from modules import common

class HtmlFiletype(FiletypeBase.FiletypeBase):

	__mixinname__ = 'htmlfiletype'
	menulist = [ (None,
		[
			(890, 'IDM_HTML', 'Html', wx.ITEM_NORMAL, None, ''),
		]),
	]
	toollist = []		#your should not use supperclass's var
	toolbaritems= {}

filetype = [('html', HtmlFiletype)]
Mixin.setMixin('changefiletype', 'filetypes', filetype)

menulist = [('IDM_HTML', #parent menu id
		[
			(100, 'IDM_HTML_BROWSER', tr('View Content'), wx.ITEM_CHECK, 'OnHtmlBrowser', tr('Shows python content in Browser.')),
		]),
]
Mixin.setMixin('htmlfiletype', 'menulist', menulist)

def OnHtmlBrowser(win, event):
	if win.document.isModified() or win.document.filename == '':
		d = wx.MessageDialog(win, tr("The file has not been saved, and it would not be run.\nWould you like to save the file?"), tr("Run"), wx.YES_NO | wx.ICON_QUESTION)
		answer = d.ShowModal()
		d.Destroy()
		if (answer == wx.ID_YES):
			win.OnFileSave(event)
		else:
			return
	filename = win.document.filename
	for document in win.editctrl.list:	#if the file has been opened
		if document.isMe(filename, documenttype = 'htmlview'):
			win.editctrl.switch(document)
			document.html.DoRefresh()
			return
	else:
		win.editctrl.newPage(filename, documenttype='htmlview')
Mixin.setMixin('mainframe', 'OnHtmlBrowser', OnHtmlBrowser)

from HtmlPanel import HtmlPanel

panellist = {'htmlview':HtmlPanel}
Mixin.setMixin('editctrl', 'panellist', panellist)

pageimagelist = {
	'htmlview': common.unicode_abspath('images/browser.gif'),
}
Mixin.setMixin('editctrl', 'pageimagelist', pageimagelist)

def closefile(win, filename):
	if win.document.languagename == 'html' and win.document.documenttype == 'edit':
		for d in win.editctrl.list:
			if d.documenttype == 'htmlview' and d.filename == filename:
				index = win.editctrl.getIndex(d)
				win.editctrl.DeletePage(index)
				win.editctrl.list.pop(index)
Mixin.setPlugin('mainframe', 'closefile', closefile)



#-----------------------  mAutoComplete.py ------------------

from modules import Mixin
import wx
import wx.stc
import inspect
from modules.Debug import error
import sets
import re
import sys
from modules import common
import os.path

CALLTIP_AUTOCOMPLETE = 2

def init(pref):
	pref.python_calltip = True
	pref.python_autocomplete = True
Mixin.setPlugin('preference', 'init', init)

preflist = [
	(tr('Python'), 120, 'check', 'python_calltip', tr("Enable calltip"), None),
	(tr('Python'), 130, 'check', 'python_autocomplete', tr("Enable auto completion"), None),
]
Mixin.setMixin('preference', 'preflist', preflist)

def init(win):
	win.AutoCompSetIgnoreCase(True)
	win.AutoCompStops(' .,;:([)]}\'"\\<>%^&+-=*/|`')
	win.AutoCompSetAutoHide(False)
	win.calltip_times = 0
	win.calltip_column = 0
	win.calltip_line = 0
	win.namespace = {}
Mixin.setPlugin('editor', 'init', init)

def on_idle(win, event):
	if not win.app.wxApp.IsActive():
		if win.AutoCompActive():
			win.AutoCompCancel()
Mixin.setPlugin('editor', 'on_idle', on_idle)

def on_key_down(win, event):
	key = event.GetKeyCode()
	control = event.ControlDown()
	#shift=event.ShiftDown()
	alt=event.AltDown()
	if key == wx.WXK_RETURN and not control and not alt:
		if not win.AutoCompActive():
			if win.calltip.active or win.calltip_times > 0:
				win.calltip_times = 0
				win.calltip.cancel()
		else:
			event.Skip()
			return True
	elif key == wx.WXK_ESCAPE:
		win.calltip.cancel()
		win.calltip_times = 0
Mixin.setPlugin('editor', 'on_key_down', on_key_down, Mixin.HIGH, 1)

def on_key_up(win, event):
	curpos = win.GetCurrentPos()
	line = win.GetCurrentLine()
	column = win.GetColumn(curpos)
	if win.calltip.active and win.calltip_type == CALLTIP_AUTOCOMPLETE:
		if column < win.calltip_column or line != win.calltip_line:
			win.calltip_times = 0
			win.calltip.cancel()
Mixin.setPlugin('editor', 'on_key_up', on_key_up)

def on_char(win,event):
	key = event.KeyCode()
	control = event.ControlDown()
	alt=event.AltDown()
	if win.languagename != 'python':
		return False

	# GF We avoid an error while evaluating chr(key), next line.
	if key > 255:
		return False

	# if document has selected text, then skip
	if win.GetSelectedText():
		return False

	# GF No keyboard needs control or alt to make '(', ')' or '.'
	# GF Shift is not included as it is needed in some keyboards.
	if chr(key) in ['(',')','.'] and not control and not alt:
		if win.AutoCompActive():
			win.AutoCompCancel()
		pos=win.GetCurrentPos()
		if key == ord('(') and win.pref.python_calltip:
			# ( start tips
			if win.calltip.active and win.calltip_type == CALLTIP_AUTOCOMPLETE:
				win.calltip_times += 1
				win.AddText('(')
			else:
				obj=getWordObject(win)
				win.AddText('(')
				if not obj:
					return True
				tip=getargspec(obj)
				doc = obj.__doc__
				if doc:
					tip += doc
				if tip:
					if win.AutoCompActive():
						win.AutoCompCancel()
					win.calltip_times = 1
					win.calltip_type = CALLTIP_AUTOCOMPLETE
					tip = tip.rstrip() + tr('\n\n(Press ESC to close)')
					win.calltip.show(pos, tip.replace('\r\n','\n'))

					#save position
					curpos = win.GetCurrentPos()
					win.calltip_column = win.GetColumn(curpos)
					win.calltip_line = win.GetCurrentLine()
				else:
					win.AddText(')')
					win.GotoPos(win.GetCurrentPos() - 1)
		elif key == ord(')'):
			# ) end tips
			win.AddText(')')
			if win.calltip.active:
				win.calltip_times -= 1
				if win.calltip_times == 0:
					win.calltip.cancel()
		elif key == ord('.') and win.pref.python_autocomplete:
			# . Code completion
			if win.calltip.active:
				win.calltip.cancel()
			autoComplete(win, object=1)
		else:
			return False
		return True
	else:
		# GF The fact that I do a win.OnKey here ensures me that I
		# GF will handle the character in a normal way if this does not
		# GF correspond to '(', ')' or '.'
		return False
Mixin.setPlugin('editor', 'on_char', on_char)

def afteropenfile(win, filename):
	win.namespace = {}
Mixin.setMixin('editor', 'afteropenfile', afteropenfile)

def getWordObject(win, word=None, whole=None):
	if not word:
		word = getWord(win, whole=whole)
	try:
		return evaluate(win, word)
	except:
		error.traceback()
		return None
Mixin.setMixin('editor', 'getWordObject', getWordObject)

def getWord(win, whole=None):
	pos=win.GetCurrentPos()
	line = win.GetCurrentLine()
	linePos=win.PositionFromLine(line)
	txt = win.GetLine(line)
	start=win.WordStartPosition(pos,1)
	i = start - 1
	while i >= 0:
		if win.getChar(i) in win.mainframe.getWordChars() + '.':
			start -= 1
			i -= 1
		else:
			break
	if whole:
		end=win.WordEndPosition(pos,1)
	else:
		end=pos
	return txt[start-linePos:end-linePos]


def evaluate(win, word):
	try:
		obj = eval(word, win.namespace)
		return obj
	except:
		import_document(win)
		try:
			obj = eval(word, win.namespace)
			return obj
		except:
			return None

def autoComplete(win, object=0):
	import wx.py.introspect as intro

	word = getWord(win)
	if object:
		win.AddText('.')
		word += '.'

	words = getAutoCompleteList(intro, win, word)
	if words:
		win.AutoCompShow(0, " ".join(words))
	else:
		words = getWords(win, word)
		if words:
			win.AutoCompShow(0, " ".join(words))

def getAutoCompleteList(modules, win, command='', includeMagic=1,
						includeSingle=1, includeDouble=1):
	"""Return list of auto-completion options for command.

	The list of options will be based on the locals namespace."""
	attributes = []
	# Get the proper chunk of code from the command.
	object = None
	if command.endswith('.'):
		root = command[:-1]
	else:
		root = command
	try:
		object = eval(root, win.namespace)
	except:
		error.traceback()
		import_document(win)
		try:
			object = eval(root, win.namespace)
		except:
			error.traceback()
			pass
	if object:
		attributes = modules.getAttributeNames(object, includeMagic,
									   includeSingle, includeDouble)
	return attributes

def import_document(win):
	dir = common.encode_string(os.path.dirname(win.filename))
	if dir not in sys.path:
		sys.path.insert(0, dir)
	r = re.compile(r'^\s*from\s+.*$|^\s*import\s+.*$', re.M)
	result = r.findall(win.GetText())
	result = [s.strip() for s in result]
	for line in result:
		if line.startswith('from'):
			try:
				exec(line) in win.namespace
			except:
				error.traceback()
		elif line.startswith('import'):
			try:
				exec(line) in win.namespace
			except:
				error.traceback()


def getWords(win, word=None, whole=None):
	if not word:
		word = win.getWord(whole=whole)
	if not word:
		return []
	else:
		word = word.replace('.', r'\.')
		words = list(sets.Set([x for x in re.findall(r"\b" + word + r"(\w+)\b", win.GetText())]))
		words.sort(lambda x, y:cmp(x.upper(), y.upper()))
		return words

def getargspec(func):
	"""Get argument specifications"""
	try:
		func=func.im_func
	except:
		error.traceback()
		pass
	try:
		return inspect.formatargspec(*inspect.getargspec(func))+'\n\n'
	except:
		error.traceback()
		pass
	try:
		return inspect.formatargvalues(*inspect.getargvalues(func))+'\n\n'
	except:
		error.traceback()
		return ''



#-----------------------  mHotKey.py ------------------

from modules import Mixin
import wx
from modules import IniFile

def init_accelerator(win, accellist, editoraccellist):
	ini = IniFile.IniFile('config.ini')
	main_options = []
	editor_options = []
	if ini.has_section('main_hotkey'):
		main_options = ini.options('main_hotkey')
	if ini.has_section('editor_hotkey'):
		editor_options = ini.options('editor_hotkey')

	for mid in main_options:
		mid = mid.upper()
		hotkey = ini.get('main_hotkey', mid, '')
		if editoraccellist.has_key(mid):
			keys, func = editoraccellist[mid]
			del editoraccellist[mid]
			accellist[mid] = (hotkey, func)
		elif accellist.has_key(mid):
			keys, func = accellist[mid]
			accellist[mid] = (hotkey, func)

	for mid in editor_options:
		mid = mid.upper()
		hotkey = ini.get('editor_hotkey', mid, '')
		if accellist.has_key(mid):
			keys, func = accellist[mid]
			del accellist[mid]
			editoraccellist[mid] = (hotkey, func)
		elif editoraccellist.has_key(mid):
			keys, func = editoraccellist[mid]
			editoraccellist[mid] = (hotkey, func)
Mixin.setPlugin('mainframe', 'init_accelerator', init_accelerator)



#-----------------------  mPythonFileType.py ------------------

from modules import Mixin
import wx
import FiletypeBase

class PythonFiletype(FiletypeBase.FiletypeBase):

	__mixinname__ = 'pythonfiletype'
	menulist = [ (None,
		[
			(890, 'IDM_PYTHON', 'Python', wx.ITEM_NORMAL, None, ''),
		]),
	]
	toollist = []		#your should not use supperclass's var
	toolbaritems= {}

filetype = [('python', PythonFiletype)]
Mixin.setMixin('changefiletype', 'filetypes', filetype)



#-----------------------  mModuleFile.py ------------------

from modules import Mixin
import wx
import wx.stc
import os.path

menulist = [
    ('IDM_PYTHON', #parent menu id
    [
        (115, '', '-', wx.ITEM_SEPARATOR, None, ''),
        (116, 'IDM_VIEW_OPEN_MODULE', tr('Open Module File') + '\tF6', wx.ITEM_NORMAL, 'OnViewOpenModuleFile', tr('Open current word as Python module file')),
    ]),
]
Mixin.setMixin('pythonfiletype', 'menulist', menulist)

def other_popup_menu(editor, projectname, menus):
    if editor.languagename == 'python' :
        menus.extend([(None, #parent menu id
            [
                (10, 'IDPM_OPEN_MODULE', tr('Open Module File') + '\tF6', wx.ITEM_NORMAL, 'OnOpenModuleFile', tr('Open current word as Python module file')),
                (20, '', '-', wx.ITEM_SEPARATOR, None, ''),
            ]),
        ])
Mixin.setPlugin('editor', 'other_popup_menu', other_popup_menu)

def OnViewOpenModuleFile(win, event):
    openmodulefile(win, getword(win))
Mixin.setMixin('mainframe', 'OnViewOpenModuleFile', OnViewOpenModuleFile)

def OnOpenModuleFile(win, event):
    openmodulefile(win.mainframe, getword(win.mainframe))
Mixin.setMixin('editor', 'OnOpenModuleFile', OnOpenModuleFile)

def openmodulefile(mainframe, module):
    try:
        mod = my_import(module)
        f, ext = os.path.splitext(mod.__file__)
        filename = f + '.py'
        if os.path.exists(filename):
            mainframe.editctrl.new(filename)
    except:
        pass

def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def getword(mainframe):
    doc = mainframe.document
    if doc.GetSelectedText():
        return doc.GetSelectedText()
    pos = doc.GetCurrentPos()
    start = doc.WordStartPosition(pos, True)
    end = doc.WordEndPosition(pos, True)
    if end > start:
        i = start - 1
        while i >= 0:
            if doc.getChar(i) in mainframe.getWordChars() + '.':
                start -= 1
                i -= 1
            else:
                break
        i = end
        length = doc.GetLength()
        while i < length:
            if doc.getChar(i) in mainframe.getWordChars()+ '.':
                end += 1
                i += 1
            else:
                break
    return doc.GetTextRange(start, end)



#-----------------------  mSplashWin.py ------------------


import wx
from modules import common
from modules import Mixin
import time

preflist = [
    (tr('General'), 190, 'check', 'splash_on_startup', tr('Show splash window on startup'), None),
]
Mixin.setMixin('preference', 'preflist', preflist)

splashimg = common.unicode_abspath('images/splash.jpg')

def beforegui(app):
    app.splashwin = None
    if app.pref.splash_on_startup:
        app.splashwin = wx.SplashScreen(wx.Image(splashimg).ConvertToBitmap(),
            wx.SPLASH_CENTRE_ON_SCREEN|wx.SPLASH_NO_TIMEOUT, 0, None, -1)
Mixin.setPlugin('app', 'beforegui', beforegui)

def init(pref):
    pref.splash_on_startup = True
Mixin.setPlugin('preference', 'init', init)

def show(mainframe):
    if mainframe.app.splashwin:
        wx.FutureCall(1000, mainframe.app.splashwin.Destroy)
Mixin.setPlugin('mainframe', 'show', show)



#-----------------------  mModuleInfo.py ------------------

from modules import Mixin
import wx
import os.path
from modules import common

menulist = [ ('IDM_HELP', #parent menu id
	[
		(102, 'IDM_HELP_MODULES', tr('Extended Modules Info'), wx.ITEM_NORMAL, 'OnHelpModules', tr('Extended modules infomation')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

def OnHelpModules(win, event):
    from ModulesInfo import show_modules_info
    show_modules_info(win)
Mixin.setMixin('mainframe', 'OnHelpModules', OnHelpModules)



#-----------------------  mDirBrowser.py ------------------

from modules import Mixin
import wx
import os.path
from modules import common

menulist = [
    ('IDM_FILE',
    [
        (138, 'IDM_WINDOW_DIRBROWSER', tr('Directory Browser')+'\tF2', wx.ITEM_NORMAL, 'OnWindowDirBrowser', tr('Opens directory browser window.'))
    ]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

popmenulist = [ (None,
    [
        (170, 'IDPM_DIRBROWSERWINDOW', tr('Directory Browser'), wx.ITEM_NORMAL, 'OnDirBrowserWindow', tr('Opens directory browser window.')),
    ]),
]
Mixin.setMixin('notebook', 'popmenulist', popmenulist)

dirbrowser_imagelist = {
	'close':common.unicode_abspath('images/folderclose.gif'),
	'open':common.unicode_abspath('images/folderopen.gif'),
	'item':common.unicode_abspath('images/file.gif'),
}

def afterinit(win):
	win.dirbrowser_imagelist = dirbrowser_imagelist
Mixin.setPlugin('mainframe', 'afterinit', afterinit)


def createDirBrowserWindow(win):
    if not win.panel.getPage(tr('Dir Browser')):
        from DirBrowser import DirBrowser

        page = DirBrowser(win.panel.createNotebook('left'), win)
        win.panel.addPage('left', page, tr('Dir Browser'))
Mixin.setMixin('mainframe', 'createDirBrowserWindow', createDirBrowserWindow)

def OnWindowDirBrowser(win, event):
    win.createDirBrowserWindow()
    win.panel.showPage(tr('Dir Browser'))
Mixin.setMixin('mainframe', 'OnWindowDirBrowser', OnWindowDirBrowser)

def OnDirBrowserWindow(win, event):
    win.mainframe.createDirBrowserWindow()
    win.panel.showPage(tr('Dir Browser'))
Mixin.setMixin('notebook', 'OnDirBrowserWindow', OnDirBrowserWindow)

def init(pref):
    pref.recent_dir_paths = []
    pref.recent_dir_paths_num = 10
Mixin.setPlugin('preference', 'init', init)



#-----------------------  mInputAssistant.py ------------------

from modules import Mixin

def mainframe_init(win):
    win.input_assistant = None
Mixin.setPlugin('mainframe', 'init', mainframe_init)

def on_char(win, event):
    if not win.mainframe.input_assistant:
        from InputAssistant import InputAssistant

        win.mainframe.input_assistant = i = InputAssistant()
    else:
        i = win.mainframe.input_assistant
    return i.run(win, event)
Mixin.setPlugin('editor', 'on_char', on_char, nice=10)

def init(pref):
	pref.auto_extend = True
Mixin.setPlugin('preference', 'init', init)

preflist = [
	(tr('Document'), 260, 'check', 'auto_extend', tr('Enable auto extend'), None),
]
Mixin.setMixin('preference', 'preflist', preflist)



#-----------------------  mFileNew.py ------------------

import wx
from modules import Mixin
import os.path
from modules import common

def init(win):
    win.filenewtypes = []
Mixin.setMixin('mainframe', 'init', init)

def OnFileNew(win, event):
    if win.pref.syntax_select:
        dialog = [
            ('single', 'lexer', 'text', tr('Syntax Selection:'), win.filenewtypes),
            ]
        from EasyGui import EasyDialog
        dlg = EasyDialog.EasyDialog(win, tr('Please select a Lexer'), dialog)
        result = dlg.ShowModal()
        lexname = None
        if result == wx.ID_OK:
            lexname = dlg.GetValue()
        dlg.Destroy()
        if result == wx.ID_CANCEL:
            return
        if lexname:
            lexer = win.lexers.getNamedLexer(lexname['lexer'])
            if lexer:
                templatefile = common.getConfigPathFile('template.%s' % lexer.name)
                print templatefile
                if os.path.exists(templatefile):
                    text = file(templatefile).read()
                    text = common.decode_string(text)
                else:
                    text = ''
            print text
            document = win.editctrl.new(defaulttext=text)
            if document:
                lexer.colourize(document)
    else:
        win.editctrl.new()
Mixin.setMixin('mainframe', 'OnFileNew', OnFileNew)

def init(pref):
	pref.syntax_select = True
Mixin.setPlugin('preference', 'init', init)

preflist = [
	(tr('General'), 175, 'check', 'syntax_select', tr('Enable syntax selection as new file'), None),
]
Mixin.setMixin('preference', 'preflist', preflist)



