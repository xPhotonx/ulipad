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
#	$Id: mClassBrowser.py 93 2005-10-11 02:51:02Z limodou $

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

#order, IDname, imagefile, short text, long text, func
toolbaritems = {
	'classbrowser':(wx.ITEM_CHECK, 'IDM_PYTHON_CLASSBROWSER', common.unicode_abspath('images/classbrowser.gif'), tr('class browser'), tr('Class browser'), 'OnPythonClassBrowser'),
	'classbrowserrefresh':(wx.ITEM_NORMAL, 'IDM_PYTHON_CLASSBROWSER_REFRESH', common.unicode_abspath('images/classbrowserrefresh.gif'), tr('class browser refresh'), tr('Class browser refresh'), 'OnPythonClassBrowserRefresh'),
}
Mixin.setMixin('pythonfiletype', 'toolbaritems', toolbaritems)


