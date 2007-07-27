#	Programmer:	limodou
#	E-mail:		limodou@gmail.com
#
#	Copyleft 2005 limodou
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
from modules import Mixin
import os.path
from modules import common

def init(win):
    win.filenewtypes = []
Mixin.setMixin('mainframe', 'init', init)

def OnFileNew(win, event):
    if win.pref.syntax_select:
        dialog = [
            ('single', 'lexer', 'text', tr('Syntax Selection:'), win.filenewtypes),
            ]
        from EasyGui import EasyDialog
        dlg = EasyDialog.EasyDialog(win, tr('Please select a Lexer'), dialog)
        result = dlg.ShowModal()
        lexname = None
        if result == wx.ID_OK:
            lexname = dlg.GetValue()
        dlg.Destroy()
        if result == wx.ID_CANCEL:
            return
        if lexname:
            lexer = win.lexers.getNamedLexer(lexname['lexer'])
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
    else:
        win.editctrl.new()
Mixin.setMixin('mainframe', 'OnFileNew', OnFileNew)

def init(pref):
	pref.syntax_select = True
Mixin.setPlugin('preference', 'init', init)

preflist = [
	(tr('General'), 175, 'check', 'syntax_select', tr('Enable syntax selection as new file'), None),
]
Mixin.setMixin('preference', 'preflist', preflist)
