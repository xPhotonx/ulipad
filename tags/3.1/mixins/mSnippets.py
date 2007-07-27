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
#	$Id: mSnippets.py 176 2005-11-22 02:46:37Z limodou $

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