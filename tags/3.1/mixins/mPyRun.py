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
#	$Id: mPyRun.py 176 2005-11-22 02:46:37Z limodou $

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

#order, IDname, imagefile, short text, long text, func
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