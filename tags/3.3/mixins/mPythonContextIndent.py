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
#   This function is referenced with DrPython.
#
#       $Id: mPythonContextIndent.py 1457 2006-08-23 02:12:12Z limodou $

__doc__ = 'Context indent'

from modules import Mixin
import wx
import re

def OnKeyDown(win, event):
    if event.GetKeyCode() == wx.WXK_RETURN:
        if win.GetSelectedText():
            return False
        if win.pref.autoindent and win.pref.python_context_indent and win.languagename == 'python':
            pythonContextIndent(win)
            return True
Mixin.setPlugin('editor', 'on_key_down', OnKeyDown, Mixin.HIGH)

def add_pref(preflist):
    preflist.extend([
        ('Python', 110, 'check', 'python_context_indent', tr('Use context sensitive indent'), None)
    ])
Mixin.setPlugin('preference', 'add_pref', add_pref)

def pref_init(pref):
    pref.python_context_indent = True
Mixin.setPlugin('preference', 'init', pref_init)

def pythonContextIndent(win):
    pos = win.GetCurrentPos()
    if win.languagename == 'python':
        linenumber = win.GetCurrentLine()
        numtabs = win.GetLineIndentation(linenumber) / win.GetTabWidth()
        text = win.GetTextRange(win.PositionFromLine(linenumber), win.GetCurrentPos())
        if text.strip() == '':
            win.AddText(win.getEOLChar()+text)
            win.EnsureCaretVisible()
            return
        if win.pref.python_context_indent:
            linetext = win.GetLine(linenumber).rstrip()
            if linetext:
                if linetext[-1] == ':':
                    numtabs = numtabs + 1
                else:
                    #Remove Comment:
                    comment = linetext.find('#')
                    if comment > -1:
                        linetext = linetext[:comment]
                    #Keyword Search.
                    keyword = re.compile(r"(\sreturn\b)|(\sbreak\b)|(\spass\b)|(\scontinue\b)|(\sraise\b)", re.MULTILINE)
                    slash = re.compile(r"\\\Z")

                    if slash.search(linetext.rstrip()) is None:
                        if keyword.search(linetext) is not None:
                            numtabs = numtabs - 1
        #Go to current line to add tabs
        win.AddText(win.getEOLChar() + win.getIndentChar()*numtabs)
        win.EnsureCaretVisible()
#add indent copy support

def pref_init(pref):
    pref.paste_auto_indent = True
Mixin.setPlugin('preference', 'init', pref_init)

def add_pref(preflist):
    preflist.extend([
        (tr('General'), 250, 'check', 'paste_auto_indent', tr('Auto indent pasting text block.'), None)
    ])
Mixin.setPlugin('preference', 'add_pref', add_pref)

re_spaces = re.compile(r'^(\s*)')
re_eol = re.compile(r'\r\n|\r|\n')
re_eol_end = re.compile(r'\r\n$|\r$|\n$', re.MULTILINE)

def on_paste(win, content):
    if win.pref.paste_auto_indent and not win.selection_column_mode:
        b = re_eol_end.search(content)
        if not b:
            return False
        win.BeginUndoAction()
        try:
            if win.GetSelectedText():
                win.ReplaceSelection('')
            col = win.GetColumn(win.GetCurrentPos())
            line = win.getLineText(win.GetCurrentLine())
            if line[:col].strip() == '':
                b = re_spaces.search(line)
                if b:
                    indent = len(b.group().expandtabs(win.GetTabWidth()))
                else:
                    indent = 0

                col = 0
                win.GotoPos(win.PositionFromLine(win.GetCurrentLine()))

            tabs, spaces = divmod(indent, win.GetTabWidth())
            if win.usetab:
                indentchars = '\t'*tabs + ' '*spaces
            else:
                indentchars = ' ' * indent

            minspaces = []
            contentlines = re_eol.sub(win.getEOLChar(), content).splitlines(True)
            for line in contentlines:
                b = re_spaces.search(line)
                if b:
                    minspaces.append(b.span()[1])
            minspace = min(minspaces)
            if col == 0:
                lines = [indentchars + x[minspace:] for x in contentlines[:1]]
            else:
                lines = [x[minspace:] for x in contentlines[:1]]
            lines.extend([indentchars + x[minspace:] for x in contentlines[1:]])
            if col and lines[-1]:
                if lines[-1].endswith(win.getEOLChar()):
                    lines[-1] = lines[-1][:-1*len(win.getEOLChar())]
            if win.GetSelectedText():
                win.ReplaceSelection('')
            win.AddText(''.join(lines))
            win.EnsureCaretVisible()
        finally:
            win.EndUndoAction()
        return True
    elif win.selection_column_mode:
        col = win.GetColumn(win.GetCurrentPos())
        line = win.GetCurrentLine()
        lines = content.splitlines()
        win.BeginUndoAction()
        endline = min(len(lines) + line, win.GetLineCount()-1)
        i = 0
        while line+i < endline:
            pos = min(win.PositionFromLine(line+i) + col, win.GetLineEndPosition(line+i))
            win.GotoPos(pos)
            win.AddText(lines[i])
            i += 1
        win.EnsureCaretVisible()
        win.EndUndoAction()
        return True
    else:
        return False
Mixin.setPlugin('editor', 'on_paste', on_paste)
