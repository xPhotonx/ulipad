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
#   $Id: mSnippets.py 481 2006-01-17 05:54:13Z limodou $

import wx
import os
from modules import Mixin
from modules import common

def add_mainframe_menu(menulist):
    menulist.extend([
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
    ])
Mixin.setPlugin('mainframe', 'add_menu', add_mainframe_menu)

def add_editor_menu(popmenulist):
    popmenulist.extend([ (None,
        [
            (140, 'IDPM_SNIPPETWINDOW', tr('Open Snippets Window'), wx.ITEM_NORMAL, 'OnSnippetWindow', tr('Opens snippets window.')),
        ]),
    ])
Mixin.setPlugin('notebook', 'add_menu', add_editor_menu)

def pref_init(pref):
    pref.snippet_lastitem = 0
Mixin.setPlugin('preference', 'init', pref_init)

def afterinit(win):
    win.snippet_catalogfile = common.uni_work_file('snippets/catalog.xml')
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

def OnDocumentSnippetsCatalogManage(win, event):
    from modules import i18n
    from modules import Resource
    from SnippetWindow import SnippetsCatalogDialog

    snippets_resfile = common.uni_work_file('resources/snippetsdialog.xrc')
    filename = i18n.makefilename(snippets_resfile, win.app.i18n.lang)
    dlg = Resource.loadfromresfile(filename, win, SnippetsCatalogDialog, 'SnippetsCatalogDialog', win)
    dlg.Show()
Mixin.setMixin('mainframe', 'OnDocumentSnippetsCatalogManage', OnDocumentSnippetsCatalogManage)

def OnDocumentSnippetsCodeManage(win, event):
    from modules import i18n
    from modules import Resource
    from SnippetWindow import SnippetsCodeDialog

    snippets_resfile = common.uni_work_file('resources/snippetsdialog.xrc')
    filename = i18n.makefilename(snippets_resfile, win.app.i18n.lang)
    dlg = Resource.loadfromresfile(filename, win, SnippetsCodeDialog, 'SnippetsCodeDialog', win)
    dlg.Show()
Mixin.setMixin('mainframe', 'OnDocumentSnippetsCodeManage', OnDocumentSnippetsCodeManage)