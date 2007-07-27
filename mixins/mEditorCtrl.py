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
#	$Id: mEditorCtrl.py 176 2005-11-22 02:46:37Z limodou $

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