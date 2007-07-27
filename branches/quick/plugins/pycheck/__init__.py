#   Programmer: limodou
#   E-mail:     limodou@gmail.com
#
#   Copyleft 2006 limodou
#
#   Distributed under the terms of the GPL (GNU Public License)
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
#   $Id$

from modules import Mixin
import wx
import os.path
import os
import sys
import images

menulist = [('IDM_PYTHON', #parent menu id
		[
			(170, 'IDM_PYTHON_CHECK', tr('Syntax Check'), wx.ITEM_NORMAL, 'OnPythonCheck', tr('Check python source code syntax.')),
		]),
]
Mixin.setMixin('pythonfiletype', 'menulist', menulist)

toollist = [
	(2140, 'check'),
]
Mixin.setMixin('pythonfiletype', 'toollist', toollist)

#order, IDname, imagefile, short text, long text, func
toolbaritems = {
	'check':(wx.ITEM_NORMAL, 'IDM_PYTHON_CHECK', images.getSpellcheckBitmap(), tr('check'), tr('Check python source code syntax.'), 'OnPythonCheck'),
}
Mixin.setMixin('pythonfiletype', 'toolbaritems', toolbaritems)

def OnPythonCheck(win, event):
    import pycheck
    pycheck.Check(win, win.document)
Mixin.setMixin('mainframe', 'OnPythonCheck', OnPythonCheck)

def init(pref):
	pref.auto_py_check = True
Mixin.setPlugin('preference', 'init', init)

preflist = [
	(tr('Python'), 160, 'check', 'auto_py_check', tr('Auto check syntax as saving'), None),
]
Mixin.setMixin('preference', 'preflist', preflist)

def aftersavefile(win, filename):
	if win.documenttype == 'edit' and win.languagename == 'python':
		import pycheck
		pycheck.Check(win.mainframe, win)
Mixin.setPlugin('editor', 'aftersavefile', aftersavefile)

def createSyntaxCheckWindow(win):
	if not win.panel.getPage(tr('Syntax Check')):
		from pycheck import SyntaxCheckWindow

		page = SyntaxCheckWindow(win.panel.createNotebook('bottom'), win)
		win.panel.addPage('bottom', page, tr('Syntax Check'))
	win.syntaxcheckwindow = win.panel.getPage(tr('Syntax Check'))
Mixin.setMixin('mainframe', 'createSyntaxCheckWindow', createSyntaxCheckWindow)