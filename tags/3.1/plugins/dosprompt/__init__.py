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
#	$Id: DosPrompt.py,v 1.1 2005/07/31 09:08:14 limodou Exp $

__doc__ = 'Dos Prompt'

from modules import Mixin
import wx
from modules.Debug import error
import os.path
from modules import common
from mixins import MessageWindow
import DosPrompt
import images

menulist = [ ('IDM_WINDOW',
	[
		(180, 'IDM_WINDOW_DOS', tr('Open Dos Prompt Window'), wx.ITEM_NORMAL, 'OnWindowDos', tr('Opens dos prompt window.')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

popmenulist = [ (None,
	[
		(150, 'IDPM_DOSWINDOW', tr('Open Dos Prompt Window'), wx.ITEM_NORMAL, 'OnDosWindow', tr('Opens dos prompt window.')),
	]),
]
Mixin.setMixin('notebook', 'popmenulist', popmenulist)

class DosPromptWindow(MessageWindow.MessageWindow):
    __mixinname__ = 'dospromptwindow'

    def __init__(self, parent, mainframe):
        MessageWindow.MessageWindow.__init__(self, parent, mainframe)

def createDosWindow(win):
	page = win.panel.getPage('Dos')
	if not page:
		page = DosPromptWindow(win.panel.createNotebook('bottom'), win)
		win.panel.addPage('bottom', page, 'Dos')
	win.dosprompt = page
Mixin.setMixin('mainframe', 'createDosWindow', createDosWindow)

def OnWindowDos(win, event):
	path = os.getcwd()
	path = common.decode_string(path)
	dlg = wx.DirDialog(win, tr('Choose a directory'), path)
	answer = dlg.ShowModal()
	if answer == wx.ID_OK:
		path = dlg.GetPath()
		win.createDosWindow()
		win.panel.showPage('Dos')
		win.RunDosCommand('cmd.exe /k "cd %s"' % path)
Mixin.setMixin('mainframe', 'OnWindowDos', OnWindowDos)

def OnDosWindow(win, event):
	win.mainframe.createDosWindow()
	win.panel.showPage('Dos')
	win.RunDosCommand("cmd.exe")
Mixin.setMixin('notebook', 'OnDosWindow', OnDosWindow)

toollist = [
	(1000, 'dos'),
]
Mixin.setMixin('mainframe', 'toollist', toollist)

#order, IDname, imagefile, short text, long text, func
toolbaritems = {
	'dos':(wx.ITEM_NORMAL, 'IDM_WINDOW_DOS', images.getDosBitmap(), tr('open dos prompt window'), tr('Open dos prompt window.'), 'OnWindowDos'),
}
Mixin.setMixin('mainframe', 'toolbaritems', toolbaritems)