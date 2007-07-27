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
#   $Id: LexerFactory.py 1457 2006-08-23 02:12:12Z limodou $

__doc__ = 'Lexer control'

from modules import Mixin

class LexerFactory(Mixin.Mixin):
    __mixinname__ = 'lexerfactory'

    lexers = [] #(name, filewildchar, stxfile, lexerclass)
    lexnames = []

    def __init__(self, mainframe):
        self.initmixin()

        self.mainframe = mainframe
        self.pref = mainframe.pref
        self.lexobjs = []

        #@add_lexer name, filewildchar, stxfile, lexerclass
        self.callplugin_once('add_lexer', LexerFactory.lexers)

        self.lexers.sort()
        for name, filewildchar, syntaxtype, stxfile, lexerclass in self.lexers:
            lexobj = lexerclass(name, filewildchar, syntaxtype, stxfile)
            self.lexobjs.append(lexobj)
            LexerFactory.lexnames.append(name)
            self.mainframe.filewildchar.append(lexobj.getFilewildchar())

    def items(self):
        return self.lexobjs

    def getDefaultLexer(self):
        try:
            obj = self.lexobjs[self.lexnames.index(self.pref.default_lexer)]
        except:
            obj = self.lexobjs[self.lexnames.index('text')]
            self.pref.default_lexer = 'text'
            self.pref.save()
        return obj

    def getNamedLexer(self, name):
        try:
            obj = self.lexobjs[self.lexnames.index(name)]
        except:
            obj = None
        return obj
