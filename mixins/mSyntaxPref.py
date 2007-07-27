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
#	$Id: mSyntaxPref.py 93 2005-10-11 02:51:02Z limodou $

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



