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

class CustomLexer(LexerBase.LexerBase):
    metaname = 'custom'
    syl_default = 1
    syl_keyword = 2
    case = True
    
    def loadDefaultKeywords(self):
        raise Exception, "Undefined"
    
    def loadPreviewCode(self):
        pass
    
    def pre_colourize(self, win):
        pass
    
    def initSyntaxItems(self):
        pass

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
                    if style == self.syl_keyword:  #keywords
                        self.process_keyword(win, m.group(), m, begin, positions)
                    else:
                        self.process_default(win, m.group(), m, begin, style, positions)
                    
                    if start > laststart:
                        nbuf.append((begin + laststart, txt[laststart:start]))
                    laststart = m.end()
                nbuf.append((begin + laststart, txt[laststart:]))
                                    
            sbuf = nbuf
        
        self.set_default(win, oldend, pos, positions)
        
    def process_default(self, win, txt, m, begin, style, positions):
        _a = []
        if len(m.groups()) > 0:
            ms = filter(None, m.groups())[0]
            index = m.group().index(ms)
            start = m.start() + index
            end = start + len(ms)
            _a.append((begin + start, begin + end))
        else:
            start = m.start()
            end = m.end()
        self.set_style(win, begin + start, begin + end, style)
        positions.append((begin + start, begin + end))
        self.set_default(win, begin + m.start(), begin + m.end(), _a)
        
    def process_keyword(self, win, txt, m, begin, positions):
        _a = []
        flag = False
        if len(m.groups()) > 0:
            s = filter(None, m.groups())
            if len(s) > 0:
                ms = filter(None, m.groups())[0]
                key = ms
                index = m.group().index(ms)
                start = m.start() + index
                end = start + len(ms)
                flag = True
        if not flag:
            start = m.start()
            end = m.end()
            key = txt
        if not self.case:
            key = key.lower()
        if key in self.keywords:
            _a.append((begin + start, begin + end))
            self.set_style(win, begin + start, begin + end, self.syl_keyword)
            positions.append((begin + start, begin + end))
        self.set_default(win, begin + m.start(), begin + m.end(), _a)
    
    def set_style(self, win, start, end, style):
        win.StartStyling(start, 0xff)
        win.SetStyling(end - start, style)
        
    def set_default(self, win, begin, end, positions):
        positions.sort(lambda (aStart, aEnd), (bStart, bEnd): cmp(aStart, bStart))
        start = begin
        styledEnd = begin
        for (styledStart, styledEnd) in positions:
            if styledStart > start:
                self.set_style(win, start, styledStart, self.syl_default)         
            start = styledEnd+1
        
        # style the rest of the doc
        if styledEnd < end:   
            self.set_style(win, styledEnd, end, self.syl_default)         
    
