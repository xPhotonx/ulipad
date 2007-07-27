#coding=utf-8
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
#   $Id: LexerBase.py 1576 2006-10-10 04:24:26Z limodou $

__doc__ = 'Lexer base class'

import wx
import os
from modules import common
from modules import Mixin
from modules import dict4ini

if wx.Platform == '__WXMSW__':
    faces = { 'times': 'Times New Roman',
              'mono' : 'Courier New',
              'helv' : 'Arial',
              'other': 'Comic Sans MS',
              'size' : 11,
              'lnsize' : 10,
             }
else:
    faces = { 'times': 'Times',
              'mono' : 'Courier 10 Pitch',
              'helv' : 'Helvetica',
              'other': 'new century schoolbook',
              'size' : 12,
              'lnsize' : 10,
             }

class LexerBase(Mixin.Mixin):
    __mixinname__ = 'lexerbase'

    STE_STYLE_TEXT = "fore:#000000"
    STE_STYLE_KEYWORD1 = "fore:#0000FF,bold"
    STE_STYLE_KEYWORD2 = "fore:#AA0000"
    STE_STYLE_KEYWORD3 = "fore:#6F4242"
    STE_STYLE_KEYWORD4 = "fore:#AAAA00"
    STE_STYLE_KEYWORD5 = "fore:#2F2F2F"
    STE_STYLE_KEYWORD6 = "fore:#808080"
    STE_STYLE_COMMENT = "fore:#238E23,back:#E8FFE8"
    STE_STYLE_COMMENTDOC = "fore:#238E23,back:#E8FFE8"
    STE_STYLE_COMMENTLINE = "fore:#238E23,back:#E8FFE8"
    STE_STYLE_COMMENTOTHER = "fore:#238E23,back:#E8FFE8"
    STE_STYLE_CHARACTER = "fore:#9F9F9F"
    STE_STYLE_CHARACTEREOL = "fore:#9F9F9F"
    STE_STYLE_STRING = "fore:#2A2AA5"
    STE_STYLE_STRINGEOL = "fore:#000000,back:#E0C0E0,eol" #"fore:#2A2AA5,eol"
    STE_STYLE_DELIMITER = "fore:#3232CC"
    STE_STYLE_PUNCTUATION = "fore:#3232CC"
    STE_STYLE_OPERATOR = "fore:#000000"
    STE_STYLE_BRACE = "fore:#4F2F4F"
    STE_STYLE_COMMAND = "fore:#FF0000"
    STE_STYLE_IDENTIFIER = "fore:#000000"
    STE_STYLE_LABEL = "fore:#4F2F4F"
    STE_STYLE_NUMBER = "fore:#6B238E"
    STE_STYLE_PARAMETER = "fore:#4F2F4F"
    STE_STYLE_REGEX = "fore:#DB70DB"
    STE_STYLE_UUID = "fore:#DB70DB"
    STE_STYLE_VALUE = "fore:#DB70DB"
    STE_STYLE_PREPROCESSOR = "fore:#808080"
    STE_STYLE_SCRIPT = "fore:#2F2F2F"
    STE_STYLE_ERROR = "fore:#0000FF"
    STE_STYLE_UNDEFINED = "fore:#3232CC"
    STE_STYLE_UNUSED = "fore:#000000"
    STC_STYLE_DEFAULT = "face:%(mono)s,size:%(size)d"
    STC_STYLE_LINENUMBER = "back:#AAFFAA,size:%(lnsize)d" #back:#C0C0C0
    STC_STYLE_BRACELIGHT = "fore:#FF0000,bold" #fore:#0000FF,back:#AAFFAA,bold
    STC_STYLE_BRACEBAD = "fore:#0000FF,bold"   #fore:#FF0000,back:#FFFF00,bold
    STC_STYLE_CONTROLCHAR = "fore:#000000"
    STC_STYLE_INDENTGUIDE = "fore:#808080"
    STE_STYLE_SELECTION_COLOUR = "fore:#FFFFFF,back:#C0C0C0"
    STE_STYLE_WHITESPACE_COLOUR = "fore:#000000"
    STE_STYLE_EDGE_COLOUR = "fore:#C0C0C0"
    STE_STYLE_CARET_COLOUR = "fore:#000000,back:#F9F9F9"
    STE_STYLE_FOLD_COLOUR = "fore:#E0E0E0"

    no_expand_styles = ()   #used to indicate which styles will forbid InputAssistant

    def __init__(self, name, filewildchar, syntaxtype, stxfile=''):
        self.initmixin()

        self.name = name
        if filewildchar:
            self.wildcharprompt, self.wildchar = filewildchar.split('|')
        else:
            self.wildchar = self.wildchar = ''
        self.stxfile = common.getConfigPathFile(stxfile)
        if not self.stxfile:
            from modules import Globals
            self.stxfile = os.path.join(Globals.confpath, stxfile)
        self.syntaxtype = syntaxtype
        self.keywords = ()
        self.syntaxitems = {}
        self.syntaxnames = []
        self.preview_code = ''

        #add default font settings in config.ini
        inifile = common.getConfigPathFile('config.ini')
        x = dict4ini.DictIni(inifile, encoding='utf-8')
#        font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
#        font = wx.Font(10, wx.TELETYPE, wx.NORMAL, wx.NORMAL, True)
#        fontname = x.default.get('editor_font', font.GetFaceName())
        fontname = x.default.get('editor_font', faces['mono'])
        fontsize = x.default.get('editor_fontsize', faces['size'])
        linesize = x.default.get('editor_linesize', faces['lnsize'])

        if isinstance(fontname, str):
            fontname = unicode(fontname, 'utf-8')
        faces.update({
            'mono':fontname,
            'size':fontsize,
            'lnsize':linesize,
        })

        self.addSyntaxItem('default',       tr('Style default'),            wx.stc.STC_STYLE_DEFAULT,       self.STC_STYLE_DEFAULT % faces)
        self.addSyntaxItem('-caretfore',    tr('Caret fore colour'),        0,  "fore:#FF0000")
        self.addSyntaxItem('-caretback',    tr('CaretLine back colour'),    0,  "back:#EEEEEE")
        self.addSyntaxItem('-selback',      tr('Selection back colour'),    0,  "back:#000080")
        self.addSyntaxItem('linenumber',    tr('Line numbers'),             wx.stc.STC_STYLE_LINENUMBER,    self.STC_STYLE_LINENUMBER % faces)
        self.addSyntaxItem('controlchar',   tr('Control characters'),       wx.stc.STC_STYLE_CONTROLCHAR,   self.STC_STYLE_CONTROLCHAR)
        self.addSyntaxItem('bracelight',    tr('Matched braces'),           wx.stc.STC_STYLE_BRACELIGHT,    self.STC_STYLE_BRACELIGHT)
        self.addSyntaxItem('bracebad',      tr('Unmatched brace'),          wx.stc.STC_STYLE_BRACEBAD,      self.STC_STYLE_BRACEBAD)
        self.initSyntaxItems()
        self.load()

    def matchfile(self, filename):
        ext = os.path.splitext(filename)[1]
        return ext.lower() in [ext[1:].lower() for ext in self.wildchar.split(';')]

    def colourize(self, win, force=False):
        if force or win.languagename != self.name:
            defaultset = (
                wx.stc.STC_STYLE_DEFAULT,
            )
            win.languagename = self.name
#            if wx.Platform == '__WXMSW__':
#                win.StyleClearAll()
#            win.ClearDocumentStyle()
#            win.StyleResetDefault()
            win.SetLexer(self.syntaxtype)
            win.lexer = self
            win.SetStyleBits(7)
            win.enablefolder = False

            self.pre_colourize(win)
            if self.syntaxtype != wx.stc.STC_LEX_CONTAINER:
                for i in range(len(self.keywords)):
                    win.SetKeyWords(i, self.keywords[i])
            for name, style in self.syntaxitems.items():
                if style.wx_const in defaultset:
                    win.StyleSetSpec(style.wx_const, style.getStyleString())
            #if wx.Platform != '__WXMSW__':
            win.StyleClearAll()
            for style in self.syntaxitems.values():
                if style.wx_const not in defaultset and style.name[0] != '-':
                    win.StyleSetSpec(style.wx_const, style.getStyleString())
            win.Colourise(0, win.GetTextLength())

            #add caret line
            win.SetCaretForeground(self.syntaxitems['-caretfore'].style.fore)
            win.SetCaretLineBack(self.syntaxitems['-caretback'].style.back)
            if hasattr(win, 'pref') and win.pref:
                win.SetCaretLineVisible(win.pref.caret_line_visible)
            win.SetSelBackground(1, self.syntaxitems['-selback'].style.back)

        #
        self.callplugin('colourize', win)
        

    def load(self):
        if self.stxfile and os.path.exists(self.stxfile):
            from modules import dict4ini
            ini = dict4ini.DictIni(self.stxfile)

            #load keywords
            self.keywords =  ini.keywords.get('keywords', self.keywords)

            #load file extensions
            self.wildchar = ini.common.get('extension', self.wildchar)

            #load preview code
            self.preview_code = ini.common.get('previewcode', '')
            if self.preview_code:
                self.preview_code = self.preview_code.replace(r'\n', '\n')

            for name, item in self.syntaxitems.items():
                stylestring = ini.styleitems.get(name, '')
                item.style.setStyleString(stylestring)

        if not self.keywords:
            self.keywords = self.loadDefaultKeywords()

        if not self.preview_code:
            self.preview_code = self.loadPreviewCode()

    def save(self):
        if self.stxfile:
            from  modules import dict4ini
            ini = dict4ini.DictIni(self.stxfile)

            ini.common.extension = self.wildchar
            ini.keywords.keywords = self.keywords
            ini.common.previewcode = self.preview_code.replace('\n', r'\n')
            for name, item in self.syntaxitems.items():
                ini.styleitems[name] = item.style.getStyleString()
            ini.save()

    def initSyntaxItems(self):
        """install syntax items"""
        pass

    def addSyntaxItem(self, name, dispname, wx_const, defaultstylestring):
        if not self.syntaxitems.has_key(name):
            self.syntaxitems[name] = SyntaxItem(name, dispname, wx_const, defaultstylestring)
            self.syntaxnames.append(name)

    def getSyntaxItems(self):
        return self.syntaxitems

    def getSyntaxNames(self):
        return self.syntaxnames

    def getFilewildchar(self):
        return "%s (%s)|%s" % (self.wildcharprompt, self.wildchar, self.wildchar)

    def loadDefaultKeywords(self):
        return ''

    def loadPreviewCode(self):
        return ''

    def pre_colourize(self, win):
        pass

    def clone(self):
        return self.__class__(self.name, self.wildcharprompt+'|'+self.wildchar, self.syntaxtype, self.stxfile)

    def copyto(self, target):
        target.wildchar = self.wildchar
        for key, item in self.syntaxitems.items():
            target.syntaxitems[key].setStyleString(self.syntaxitems[key].getStyleString())

    def cannot_expand(self, document):
        pos = document.GetCurrentPos()
        style = document.GetStyleAt(pos)
        while style == 0:
            linepos = document.PositionFromLine(document.GetCurrentLine())
            if pos > linepos:
                pos -= 1
                style = document.GetStyleAt(pos)
            else:
                break
        return style in self.no_expand_styles
    
    def styleneeded(self):
        pass

class SyntaxItem:
    def __init__(self, name, dispname, wx_const, defaultstylestring):
        self.name = name
        self.dispname = dispname
        self.wx_const = wx_const
        self.defaultstyle = Style()
        self.defaultstyle.setStyleString(defaultstylestring)
        self.style = self.defaultstyle.clone()

    def getStyleString(self):
        if not self.style.getStyleString():
            return self.defaultstyle.getStyleString()
        else:
            return self.style.getStyleString()
        
    def __str__(self):
        return self.getStyleString()


    def setStyleString(self, stylestring):
        self.style.setStyleString(stylestring)

class Style:
    def __init__(self, bold='', italic='', underline='', fore='', back='', face='', size='', eol=''):
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.fore = fore
        self.back = back
        self.face = face
        self.size = size
        self.eol = eol

    def setStyleString(self, stylestring):
        self.bold = ''
        self.italic = ''
        self.underline = ''
        self.fore = ''
        self.back = ''
        self.face = ''
        self.size = ''
        self.eol = ''
        s = stylestring.split(',')
        for item in s:
            if item.find(':') > -1:
                name, value = item.split(':')
            else:
                name = item
            if name == 'bold':
                self.bold = 'bold'
            elif name == 'italic':
                self.italic = 'italic'
            elif name == 'underline':
                self.underline = 'underline'
            elif name == 'fore':
                self.fore = value
            elif name == 'back':
                self.back = value
            elif name == 'face':
                self.face = value
                if isinstance(self.face, str):
                    self.face = unicode(self.face, 'utf-8')
            elif name == 'size':
                self.size = value
            elif name == 'eol':
                self.eol = 'eol'
                
    def __str__(self):
        return self.getStyleString()
    
    def getStyleString(self):
        s = []
        if self.bold:
            s.append(self.bold)
        if self.italic:
            s.append(self.italic)
        if self.underline:
            s.append(self.underline)
        if self.fore:
            s.append('fore:'+self.fore)
        if self.back:
            s.append('back:'+self.back)
        if self.face:
            s.append('face:'+self.face)
        if self.size:
            s.append('size:'+self.size)
        if self.eol:
            s.append('eol')
        return ','.join(map(unicode, s))

    def clone(self):
        a = Style()
        a.setStyleString(self.getStyleString())
        return a

if __name__ == '__main__':
    s = Style()
    s.setStyleString('fore:#0000FF,bold,size:9')
    print s.getStyleString()
