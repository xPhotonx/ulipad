#       Programmer:     limodou
#       E-mail:         limodou@gmail.com
#
#       Copyleft 2006 limodou
#
#       Distributed under the terms of the GPL (GNU Public License)
#
#   UliPad is free software; you can redistribute it and/or modify
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
#       $Id: mLexerFactory.py 1457 2006-08-23 02:12:12Z limodou $

__doc__ = 'Lexer control'

import wx
import os
from modules import Mixin
from LexerFactory import LexerFactory

def call_lexer(win, filename, language):
    for lexer in win.mainframe.lexers.lexobjs:
        if language and language == lexer.name or lexer.matchfile(filename):
            lexer.colourize(win)
            return
    else:
        if filename:
            win.mainframe.lexers.getNamedLexer('text').colourize(win)
        else:
            win.mainframe.lexers.getDefaultLexer().colourize(win)
Mixin.setPlugin('editor', 'call_lexer', call_lexer)

def aftersavefile(win, filename):
    for lexer in win.mainframe.lexers.lexobjs:
        if lexer.matchfile(filename):
            lexer.colourize(win)
            return
Mixin.setPlugin('editor', 'aftersavefile', aftersavefile)

def beforeinit(win):
    win.lexers = LexerFactory(win)
Mixin.setPlugin('mainframe', 'beforeinit', beforeinit)

def add_mainframe_menu(menulist):
    menulist.extend([ ('IDM_DOCUMENT',
        [
            (130, '', '-', wx.ITEM_SEPARATOR, None, ''),
            (140, 'IDM_DOCUMENT_SYNTAX_HIGHLIGHT', tr('Syntax Highlight...'), wx.ITEM_NORMAL, 'OnDocumentSyntaxHighlight', tr('Specifies the syntax highlight to current document.')),
        ]),
    ])
Mixin.setPlugin('mainframe', 'add_menu', add_mainframe_menu)

def OnDocumentSyntaxHighlight(win, event):
    items = [lexer.name for lexer in win.lexers.lexobjs]
    dlg = wx.SingleChoiceDialog(win, tr('Select a syntax highlight'), tr('Syntax Highlight'), items, wx.CHOICEDLG_STYLE)
    if dlg.ShowModal() == wx.ID_OK:
        lexer = win.lexers.lexobjs[dlg.GetSelection()]
        lexer.colourize(win.document)
        win.editctrl.switch(win.document)
    dlg.Destroy()
Mixin.setMixin('mainframe', 'OnDocumentSyntaxHighlight', OnDocumentSyntaxHighlight)

def add_pref(preflist):
    preflist.extend([
        (tr('General'), 170, 'choice', 'default_lexer', tr('Default syntax highlight'), LexerFactory.lexnames),
        (tr('General'), 180, 'check', 'caret_line_visible', tr('Show caret line'), None),
    ])
Mixin.setPlugin('preference', 'add_pref', add_pref)

def pref_init(pref):
    pref.default_lexer = 'text'
    pref.caret_line_visible = True
Mixin.setPlugin('preference', 'init', pref_init)

def savepreference(mainframe, pref):
    mainframe.document.SetCaretLineVisible(pref.caret_line_visible)
Mixin.setPlugin('prefdialog', 'savepreference', savepreference)
