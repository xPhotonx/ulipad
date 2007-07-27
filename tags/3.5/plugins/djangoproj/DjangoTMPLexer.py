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

from mixins import CustomLexer
import re
    
class DjangoTmpLexer(CustomLexer.CustomLexer):

    metaname = 'djangotmp'

    def loadDefaultKeywords(self):
        keys = ['extends', 'block', 'include', 'comment', 'load', 'firstof', 
            'now', 'for', 'regroup', 'ifequal', 'ifnotequal', 'widthratio', 
            'templatetag', 'ifchanged', 'filter', 'ssi', 'debug', 'if', 
            'spaceless', 'cycle']
        end_keys = ['end' + x for x in keys]
        return keys + end_keys

    def loadPreviewCode(self):
        return """"""

    def initSyntaxItems(self):
        self.filters = ['truncatewords', 'removetags', 'linebreaksbr', 'yesno', 
            'get_digit', 'timesince', 'random', 'striptags', 'filesizeformat', 
            'escape', 'linebreaks', 'length_is', 'ljust', 'rjust', 'cut', 
            'urlize', 'fix_ampersands', 'title', 'floatformat', 'capfirst', 
            'pprint', 'divisibleby', 'add', 'make_list', 'unordered_list', 
            'urlencode', 'timeuntil', 'urlizetrunc', 'wordcount', 'stringformat', 
            'linenumbers', 'slice', 'date', 'dictsort', 'dictsortreversed', 
            'default_if_none', 'pluralize', 'lower', 'join', 'center', 'default', 
            'upper', 'length', 'phone2numeric', 'wordwrap', 'time', 'addslashes', 
            'slugify', 'first']
        self.addSyntaxItem('r_default',         'Default',              CustomLexer.CustomLexer.syl_default,           self.STE_STYLE_TEXT)
        self.addSyntaxItem('keyword',           'Keyword',              CustomLexer.CustomLexer.syl_keyword,           self.STE_STYLE_KEYWORD1)
        self.addSyntaxItem('variable',          'Variable',             3,           'fore:#ff0000,bold,italic')
        self.addSyntaxItem('symbol',            'Symbol',               4,           'fore:#5C8F59,bold')
        self.addSyntaxItem('filter',            'Filter',               5,           'fore:#7F7047,bold')
        self.addSyntaxItem('comment',           'Comment',              6,           self.STE_STYLE_COMMENT)
        self.formats = [
            (re.compile(r'\{%\s*comment\s*%\}.*?\{%\s*endcomment\s*%\}', re.MULTILINE), 6),
            (re.compile(r'\{\{.*?\}\}'), 3),
            (re.compile(r'\{%.*?%\}'), 2),
        ]
        self.syl_filter = 5
        self.syl_symbol = 4
        self.syl_var = 3

    def styleneeded(self, win, pos):
        oldend = win.PositionFromLine(win.LineFromPosition(win.GetEndStyled()))
        text = win.GetTextRange(oldend, pos).encode('utf-8')
        positions = []
        sbuf = [(oldend, text)]
        for r, style in self.formats:
            nbuf = []
            for begin, txt in sbuf:
                laststart = 0
                while 1:
                    m = r.search(txt, laststart)
                    if not m:
                        break
                    
                    start = m.start()
                    if style == 3:  #variable
                        self.process_variable(win, m.group(), m, begin, positions)
                    elif style == 2:  #tag
                        self.process_tag(win, m.group(), m, begin, positions)
                    else:
                        self.process_default(win, m.group(), m, begin, style, positions)
                    
                    if start > laststart:
                        nbuf.append((begin + laststart, txt[laststart:start]))
                    laststart = m.end()
                nbuf.append((begin + laststart, txt[laststart:]))
                    
            sbuf = nbuf
        
        self.set_default(win, oldend, pos, positions)
        
    r_var = re.compile(r'_\("[^"]+"\)|"[^"]+"|[A-Za-z._]+')
    r_filter = re.compile(r'(?:\|([A-Za-z_]+)(:"[^"]+")?)')
    def process_variable(self, win, txt, m, begin, positions):
        _a = []
        bpos = m.start()
        epos = m.end()
        self.set_style(win, begin + bpos, begin + bpos + 2, self.syl_symbol)
        self.set_style(win, begin + epos - 2, begin + epos, self.syl_symbol)
        _a.append((begin + bpos, begin + bpos + 2))
        _a.append((begin + epos-2, begin + epos))
        positions.append((begin + bpos, begin + epos))
        begin += bpos
        m = self.r_var.search(txt)
        if m:
            start = m.start()
            end = m.end()
            self.set_style(win, begin+start, begin+end, self.syl_var)
            _a.append((begin + start, begin + end))
            while 1:
                m = self.r_filter.search(txt, end)
                if not m: break
                start = m.start()
                end = m.end()
                filter = m.groups()[0]
                if filter in self.filters:
                    self.set_style(win, begin+start+1, begin+start+len(filter)+1, self.syl_filter)
                    _a.append((begin+start+1, begin+start+len(filter)+1))
        self.set_default(win, begin, begin + len(txt), _a)
            
    def process_tag(self, win, txt, m, begin, positions):
        _a = []
        bpos = m.start()
        epos = m.end()
        self.set_style(win, begin + bpos, begin + bpos + 2, self.syl_symbol)
        self.set_style(win, begin + epos - 2, begin + epos, self.syl_symbol)
        _a.append((begin + bpos, begin + bpos + 2))
        _a.append((begin + epos-2, begin + epos))
        positions.append((begin + bpos, begin + epos))
        begin += bpos
        m = self.r_var.search(txt)
        if m:
            start = m.start()
            end = m.end()
            if m.group() in self.keywords:
                self.set_style(win, begin+start, begin+end, self.syl_keyword)
                _a.append((begin + start, begin + end))
        self.set_default(win, begin, begin + len(txt), _a)
        
