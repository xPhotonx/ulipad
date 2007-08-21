#   Programmer:     limodou
#   E-mail:         limodou@gmail.com
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

import LexerBase
from modules.ZestyParser import *
import re
import types
from modules.common import pout

class CustomLexer(LexerBase.LexerBase):
    metaname = 'newcustom'
    syl_default = 1
    syl_keyword = 2
    syl_comment = 3
    syl_integer = 4
    syl_string = 5
    syl_custom = 20
    casesensitive = True
    fulltext = False
    
    def loadDefaultKeywords(self):
        return []
    
    def loadPreviewCode(self):
        pass
    
    def pre_colourize(self, win):
        pass
    
    def load(self):
        super(CustomLexer, self).load()
        if not self.casesensitive:
            self.keywords = [x.lower() for x in self.keywords]
        self.backstyles = self.initbackstyle()
    
    def initSyntaxItems(self):
        self.addSyntaxItem('r_default',         'Default',              self.syl_default,           self.STE_STYLE_TEXT)
        self.addSyntaxItem('keyword',           'Keyword',              self.syl_keyword,           self.STE_STYLE_KEYWORD1)
        self.addSyntaxItem('comment',           'Comment',              self.syl_comment,           self.STE_STYLE_COMMENT)
        self.addSyntaxItem('integer',           'Integer',              self.syl_integer,           self.STE_STYLE_NUMBER)
        self.addSyntaxItem('string',            'String',               self.syl_string,            self.STE_STYLE_STRING)
        
        T_COMMENT = Token(re.compile(r'#[^\n\r]*'), callback=self.just_return(self.syl_comment))
        T_IDEN = Token(r'[_a-zA-Z][_a-zA-Z0-9]*', callback=self.is_keyword())
        T_OTHER = Token(r'[^ _a-zA-Z0-9]', callback=self.just_return(self.syl_default))
        T_INTEGER = Token(r'[+-]?\d+\.?\d*[eE]*', callback=self.just_return(self.syl_integer))
        T_SP = Token(r'\s+', callback=self.just_return(self.syl_default))
        T_DQUOTED_STRING = Token(r'"((?:\\.|[^"])*)?"', callback=self.just_return(self.syl_string))
        T_SQUOTED_STRING = Token(r"'((?:\\.|[^'])*)?'", callback=self.just_return(self.syl_string))
        
        self.formats = [T_COMMENT, T_DQUOTED_STRING, T_SQUOTED_STRING, T_IDEN, T_INTEGER, T_SP, T_OTHER]
    
    def is_keyword(self, group=0):
        def r(matchobj):
            key = matchobj.group(group)
            span = matchobj.span(group)
            if not self.casesensitive:
                key = key.lower()
            if key in self.keywords:
                return self.syl_keyword, span[0], span[1]
            else:
                return self.syl_default, span[0], span[1]
        return r
        
    def just_return(self, style=None, group=0):
        if not style:
            style = self.syl_default
        def r(matchobj):
            span = matchobj.span(group)
            return style, span[0], span[1]
        return r
    
    def initbackstyle(self):
        '''
        The element should be (currentstyle, leadingstyle)
        '''
        return []
    
    def styletext(self, win):
        begin = win.GetEndStyled()
        
        for i in xrange(begin, -1, -1):
            style = win.GetStyleAt(i)
            if style:
                begin = i
                break
            
        flag = False
        cs, ls, match = None, None, None
        for v in self.backstyles:
            if len(v) == 2:
                (cs, ls), match = v, None
            else:
                cs, ls, match = v
            if cs == style:
                flag = True
                break
        if flag:
            for i in xrange(begin-1, -1, -1):
                es = win.GetStyleAt(i)
                if es == ls:
                    if match:
                        text = win.GetTextRange(i, begin).encode('utf-8')
                        if isinstance(match, str):
                            if text.startswith(match):
                                begin = i
                                break
                        elif match.match(text):
                            begin = i
                            break
                else:
                    if not match:
                        break
            else:
                begin = 0
            return begin
        else:
            return None
    
    def styleneeded(self, win, pos):
        begin = self.styletext(win)
        if begin is not None:
            text = win.GetTextRange(begin, pos).encode('utf-8')
        else:
            if self.fulltext:
                text = win.getRawText()
                begin = 0
            else:
                begin = win.PositionFromLine(win.LineFromPosition(win.GetEndStyled()))
                text = win.GetTextRange(begin, pos).encode('utf-8')
#        print '--------------------------------' , begin, win.filename
#        print text
#        print '--------------------------------'
        if not text:
            return
        parser = ZestyParser(text)
        try:
            for i in parser.iter(self.formats):
                if isinstance(i, (list, types.GeneratorType)):
                    for x in i:
                        style, start, end = x
                        self.set_style(win, begin + start, begin + end, style)
                else:
                    style, start, end = i
                    self.set_style(win, begin + start, begin + end, style)
        except:
            import traceback
            traceback.print_exc()
            
            
    def set_style(self, win, start, end, style):
        pout('set_style >>>>>', start, end, style, win.GetTextRange(start, end))
        win.StartStyling(start, 0xff)
        win.SetStyling(end - start, style)
        
    def merge_list(self, s, a):
        for i in a:
            style_i, begin_i, end_i = i
            for n, j in enumerate(s):
                style, b, e = j
                if begin_i >= b and end_i <= e: #include
                    if style_i != style:
                        left, right = None, None
                        if begin_i > b:
                            left = (style, b, begin_i)
                        if end_i < e:
                            right = (style, end_i, e)
                        if left:
                            s.insert(n, i)
                            del s[n+1]
                        else:
                            left = i
                            del s[n]
                        if right:
                            if n < len(s)-1 and s[n+1][0] == right[0]:
                                r = s[n+1]
                                s[n+1] = (right[0], right[1], r[2])
                            else:
                                if n < len(s) -1:
                                    s.insert(n+1, right)
                                else:
                                    s.append(right)
                        if left:
                            if n > 1 and s[n-1][0] == left[0]:
                                l = s[n-1]
                                s[n-1] = (left[0], l[1], left[2])
                            else:
                                s.insert(n, left)
                        break
    
        return s
    