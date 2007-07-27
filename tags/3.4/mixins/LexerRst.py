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

import CustomLexer
import re
    
class RstLexer(CustomLexer.CustomLexer):

    metaname = 'rst'

    def loadDefaultKeywords(self):
        return ['Author', 'Version', 'Copyright', 'contents', 'sectnum', 'note',
            'image']

    def loadPreviewCode(self):
        return """==========================================
 Docutils_ Project Documentation Overview
==========================================

:Author: David Goodger
:Contact: goodger@python.org
:Date: $Date: 2005-12-14 18:37:07 +0100 (Wed, 14 Dec 2005) $
:Revision: $Revision: 4215 $
:Copyright: This document has been placed in the public domain.

The latest working documents may be accessed individually below, or
from the ``docs`` directory of the `Docutils distribution`_.

.. _Docutils: http://docutils.sourceforge.net/
.. _Docutils distribution: http://docutils.sourceforge.net/#download

.. contents::
"""

    def pre_colourize(self, win):
        #FOLDING
#        win.enablefolder = True
        win.SetProperty("fold", "1")
        win.SetProperty("tab.timmy.whinge.level", "1")

    def initSyntaxItems(self):
        self.addSyntaxItem('r_default',         'Default',              CustomLexer.CustomLexer.syl_default,           self.STE_STYLE_TEXT)
        self.addSyntaxItem('keyword',           'Keyword',              CustomLexer.CustomLexer.syl_keyword,           self.STE_STYLE_KEYWORD1)
        self.addSyntaxItem('inlineliteral',     'Inline Literal',       3,           self.STE_STYLE_CHARACTER)
        self.addSyntaxItem('directurl',         'DirectUrl',            4,           'fore:#0000FF,underline')
        self.addSyntaxItem('interpretedtext',   'Interpreted Text',     5,           'fore:#339933')
        self.addSyntaxItem('bold',              'Bold',                 6,           'bold')
        self.addSyntaxItem('emphasis',          'Emphasis',             7,           'italic')
        self.formats = [
            (re.compile(r'(``.*?``)'), 3),
            (re.compile(r'(`.*?`)'), 5),
            (re.compile(r'(\*\*.*?\*\*)'), 6),
            (re.compile(r'(\*.*?\*)'), 7),
            (re.compile("((?:file|https?|ftp|mailto)://[^\s<]*)"), 4),
            (re.compile(r':(\w+):'), 2),
        ]

