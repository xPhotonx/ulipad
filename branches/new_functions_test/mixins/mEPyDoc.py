#   Programmer: limodou
#   E-mail:     limodou@gmail.com
#
#   Copyleft 2006 limodou
#
#   Distributed under the terms of the GPL (GNU Public License)
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
#   $Id$

import re
import wx
from modules import Mixin

def other_popup_menu(editor, projectname, menus):
    if editor.languagename == 'python':
        menus.extend([(None, #parent menu id
            [
                (9, 'IDPM_PYTHON_EPYDOC', tr('Create Comment for Function')+u'\tAlt+A', wx.ITEM_NORMAL, 'OnPythonEPyDoc', 'Creates comment for a function.'),
            ]),
        ])
Mixin.setPlugin('editor', 'other_popup_menu', other_popup_menu)


#re_func = re.compile('^(\s*)def\s+[\w\d_]+\((.*?)\):')
re_func = re.compile('^(\s*)(def|class)\s+[\w\d_*]+\s*(\()')
comment_template = """
%(doc)s

@author: %(username)s  

%(parameters)s
@return: %(return)s
@rtype:  %(rtype)s

"""
import SnipMixin
def call_snippet(win, tpl, start, end):
    editor = win
    if editor.snippet:
        snippet = editor.snippet
    else:
        snippet = editor.snippet = SnipMixin.SnipMixin(editor)
    snippet.start(tpl, start, end)
    
def get_definition_line(win):
    """
    
    @author: ygao
    
    @param win: editor
    @type win: instance
    @return:  line number or None
    @rtype:   int
    
    """
    if  win.syntax_info:
        obj = win.syntax_info.guess(win.GetCurrentLine())
        # todo: show list to let user to choose which to comment 2008:03:12 by ygao
        if  len(obj) > 0:
            obj1 = obj[0]
            return obj1.span[0]

def OnPythonEPyDoc(win, event=None, line=None):
    """
    using live template to create EPy formate comment
    
    @author: ygao
    
    @param win: editor
    @type win: instance
    @param event: 
    @type event: 
    @param line: must be at definition
    @type line: int
    @return:  
    @rtype:   
    
    """
    def output(win, indent, parameters, pos, para_sum):
        t = (indent / win.GetTabWidth() + 1) * win.getIndentChar()
        startpos = win.PositionFromLine(win.LineFromPosition(pos)+1)
        win.GotoPos(startpos)
        text = '"""' + comment_template % {'parameters':parameters, 'username':win.pref.personal_username, \
            'doc':"${1:}",'return':" ${" + str(para_sum) + ":}", 'rtype':" ${0}"} + '"""' + win.getEOLChar()
        s = ''.join([t + x for x in text.splitlines(True)])
        win.AddText(s)
        start = startpos
        end = win.GetCurrentPos()
        win.GotoPos(start)
        
        win.EnsureCaretVisible()
        call_snippet(win, win.GetTextRange(start, end), start, end)
            
    if  line is None:    
        line = win.GetCurrentLine()
    else:
        line = line
    text = win.getLineText(line)
    # note: 2008:01:27 by ygao
    # def ygao():
    # 
    #     cursor flash on this 
    if not text.strip():
        for i in range(line-1, -1, -1):
            text = win.getLineText(i)
            # get function definiton line 
            line = line - 1
            if text.strip():
                break
    # note: this case: 2008:01:27 by ygao
    # def __ygao (para,
    #             parameters):
    b = None
    line_d = 0
    if text:
        b = re_func.match(text)
        # current line more priority
        if b is None:
            line_d = get_definition_line(win)
            if line_d:
                text = win.getLineText(line_d - 1)
                b = re_func.match(text)
    if b:
        
        indent = b.groups()[0]
        function_left_char_pos = b.span(3)[0] + win.PositionFromLine(line_d - 1)
        function_right_char_pos = win.BraceMatch(function_left_char_pos)
        if function_right_char_pos == -1:
            return
        parameters = win.GetTextRange(function_left_char_pos + 1, function_right_char_pos)
        pos = function_right_char_pos
        paras = [x.strip() for x in parameters.split(',')]
        s = []
        para_sum = 2
        # note: if no parameters, there is one u'', 2008:01:27 by ygao
        if  paras[0] != '':
            for x in paras:
                if x.startswith('**'):
                    x = x[2:]
                if x.startswith('*'):
                    x = x[1:]
                if '=' in x:
                    x = x.split('=')[0]
                x = x.strip()
                s.append('@param %s:' % x + " ${" + str(para_sum)+":}")
                para_sum = para_sum + 1
                s.append('@type %s:' % x + " ${" + str(para_sum)+":}")
                para_sum = para_sum + 1
        s = win.getEOLChar().join(s)
        output(win, len(indent), s, pos, para_sum)
        return
Mixin.setMixin('editor', 'OnPythonEPyDoc', OnPythonEPyDoc)


def OnPythonEPy(win, event):
    try:
        win.document.OnPythonEPyDoc(event=event)
    except:         
        error.traceback()
Mixin.setMixin('mainframe', 'OnPythonEPy', OnPythonEPy)

def add_pyftype_menu(menulist):
    menulist.extend([('IDM_PYTHON', #parent menu id
        [
            (375, 'IDM_PYTHON_PYTHON_EPYDOC', tr('Create Comment for Function') + u'\tAlt+A', wx.ITEM_NORMAL, 'OnPythonEPy', tr('Creates comment for a function.')),
            
        ]),
    ])
Mixin.setPlugin('pythonfiletype', 'add_menu', add_pyftype_menu)

