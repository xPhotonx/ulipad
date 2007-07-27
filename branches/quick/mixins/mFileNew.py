#	Programmer:	limodou
#	E-mail:		limodou@gmail.com
#
#	Copyleft 2006 limodou
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
#	$Id: mEditorCtrl.py 154 2005-11-07 04:48:15Z limodou $

import wx
import os
from modules import Mixin
from modules import common

def mainframe_init(win):
    win.filenewtypes = []
Mixin.setMixin('mainframe', 'init', mainframe_init)

def add_tool_list(toollist, toolbaritems):
    #order, IDname, imagefile, short text, long text, func
    toolbaritems.update({
        'new':(wx.ITEM_NORMAL, 'IDM_FILE_NEWS', 'images/new.gif', tr('new'), tr('Creates a new document'), 'OnFileNews'),
    })
Mixin.setPlugin('mainframe', 'add_tool_list', add_tool_list)

def OnFileNews(win, event):
    if win.pref.syntax_select:
        eid = event.GetId()
        size = win.toolbar.GetToolSize()
        pos = win.toolbar.GetToolPos(eid)
        menu = wx.Menu()
        ids = {}

        def OnFileNew(event, win=win, ids=ids):
            lexname = ids.get(event.GetId(), '')
            if lexname:
                lexer = win.lexers.getNamedLexer(lexname)
                if lexer:
                    templatefile = common.getConfigPathFile('template.%s' % lexer.name)
                    if os.path.exists(templatefile):
                        text = file(templatefile).read()
                        text = common.decode_string(text)
                    else:
                        text = ''
                document = win.editctrl.new(defaulttext=text, language=lexer.name)
#                if document:
#                    lexer.colourize(document)
        for name, lexname in win.filenewtypes:
            _id = wx.NewId()
            menu.Append(_id, "%s" % name)
            ids[_id] = lexname
            wx.EVT_MENU(win, _id, OnFileNew)
        win.PopupMenu(menu, (size[0]*pos, size[1]))
        menu.Destroy()
        
#        dialog = [
#            ('single', 'lexer', 'text', tr('Syntax Selection:'), win.filenewtypes),
#            ]
#        from modules.EasyGuider import EasyDialog
#        dlg = EasyDialog.EasyDialog(win, tr('Please select a Lexer'), dialog)
#        result = dlg.ShowModal()
#        lexname = None
#        if result == wx.ID_OK:
#            lexname = dlg.GetValue()
#        dlg.Destroy()
#        if result == wx.ID_CANCEL:
#            return
#        if lexname:
#            lexer = win.lexers.getNamedLexer(lexname['lexer'])
#            if lexer:
#                templatefile = common.getConfigPathFile('template.%s' % lexer.name)
#                if os.path.exists(templatefile):
#                    text = file(templatefile).read()
#                    text = common.decode_string(text)
#                else:
#                    text = ''
#            document = win.editctrl.new(defaulttext=text)
#            if document:
#                lexer.colourize(document)
    else:
        win.editctrl.new()
Mixin.setMixin('mainframe', 'OnFileNews', OnFileNews)

def pref_init(pref):
	pref.syntax_select = True
Mixin.setPlugin('preference', 'init', pref_init)

def add_pref(preflist):
    preflist.extend([
        (tr('General'), 175, 'check', 'syntax_select', tr('Enable syntax selection as new file'), None),
    ])
Mixin.setPlugin('preference', 'add_pref', add_pref)

def add_mainframe_menulist(menulist):
    menulist.extend([ ('IDM_FILE_NEWMORE',
        [
            (100, 'IDM_FILE_NEWMORE_TEXT', 'Text', wx.ITEM_NORMAL, 'OnFileNewMore', tr('Creates a text file.')),
            (110, 'IDM_FILE_NEWMORE_C', 'C/C++', wx.ITEM_NORMAL, 'OnFileNewMore', tr('Creates a C file.')),
            (120, 'IDM_FILE_NEWMORE_HTML', 'Html', wx.ITEM_NORMAL, 'OnFileNewMore', tr('Creates a HTML file.')),
            (130, 'IDM_FILE_NEWMORE_PYTHON', 'Python', wx.ITEM_NORMAL, 'OnFileNewMore', tr('Creates a Python file.')),
            (140, 'IDM_FILE_NEWMORE_JAVA', 'Java', wx.ITEM_NORMAL, 'OnFileNewMore', tr('Creates a Java file.')),
            (150, 'IDM_FILE_NEWMORE_RUBY', 'Ruby', wx.ITEM_NORMAL, 'OnFileNewMore', tr('Creates a Ruby file.')),
            (160, 'IDM_FILE_NEWMORE_PERL', 'Perl', wx.ITEM_NORMAL, 'OnFileNewMore', tr('Creates a Perl file.')),
            (170, 'IDM_FILE_NEWMORE_CSS', 'Cascade Style Sheet', wx.ITEM_NORMAL, 'OnFileNewMore', tr('Creates a CSS file.')),
            (180, 'IDM_FILE_NEWMORE_JS', 'JavaScript', wx.ITEM_NORMAL, 'OnFileNewMore', tr('Creates a JavaScript file.')),
        ]),
    ])
Mixin.setPlugin('mainframe', 'add_menulist', add_mainframe_menulist)

def OnFileNewMore(win, event):
    ids = {
        win.IDM_FILE_NEWMORE_TEXT:'text',
        win.IDM_FILE_NEWMORE_C:'c',
        win.IDM_FILE_NEWMORE_HTML:'html',
        win.IDM_FILE_NEWMORE_PYTHON:'python',
        win.IDM_FILE_NEWMORE_JAVA:'java',
        win.IDM_FILE_NEWMORE_RUBY:'ruby',
        win.IDM_FILE_NEWMORE_PERL:'perl',
        win.IDM_FILE_NEWMORE_CSS:'css',
        win.IDM_FILE_NEWMORE_JS:'js',
    }
    lexname = ids.get(event.GetId(), '')
    if lexname:
        lexer = win.lexers.getNamedLexer(lexname)
        if lexer:
            templatefile = common.getConfigPathFile('template.%s' % lexer.name)
            if os.path.exists(templatefile):
                text = file(templatefile).read()
                text = common.decode_string(text)
            else:
                text = ''
        document = win.editctrl.new(defaulttext=text)
        if document:
            lexer.colourize(document)
Mixin.setMixin('mainframe', 'OnFileNewMore', OnFileNewMore)

