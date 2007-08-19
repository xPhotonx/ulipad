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

from mixins import NewCustomLexer
from modules.ZestyParser import *
import re
    
class FortranLexer(NewCustomLexer.CustomLexer):

    metaname = 'fortran'
    casesensitive = False

    def loadDefaultKeywords(self):
        return ('''admit allocatable allocate assign assignment at
backspace block
call case character close common complex contains continue cycle
data deallocate default dimension do double
else elseif elsewhere end enddo endfile endif endwhile entry equivalence execute exit external
forall format function
go goto guess
if implicit in inout inquire integer intent interface intrinsic
kind
logical loop
map module
namelist none nullify
only open operator optional otherwise out
parameter pointer private procedure program public
quit
read real record recursive remote result return rewind
save select sequence stop structure subroutine
target then to type
union until use
where while write''').split()

    def loadPreviewCode(self):
        return """
! Free Format
program main
write(*,*) "Hello" !This is also comment
write(*,*) &
"Hello"
wri&
&te(*,*) "Hello"
end
"""

    def initSyntaxItems(self):
        self.addSyntaxItem('r_default',         'Default',              self.syl_default,           self.STE_STYLE_TEXT)
        self.addSyntaxItem('keyword',           'Keyword',              self.syl_keyword,           self.STE_STYLE_KEYWORD1)
        self.addSyntaxItem('comment',           'Comment',              self.syl_comment,           self.STE_STYLE_COMMENT)
        self.addSyntaxItem('integer',           'Integer',              self.syl_integer,           self.STE_STYLE_NUMBER)
        self.addSyntaxItem('string',            'String',               self.syl_string,            self.STE_STYLE_CHARACTER)

        T_COMMENT = Token(re.compile(r'![^\n\r]*'), callback=self.just_return(self.syl_comment))
        T_IDEN = Token(r'[_a-zA-Z][_a-zA-Z0-9]*', callback=self.is_keyword())
        T_OTHER = Token(r'[^ _a-zA-Z0-9]', callback=self.just_return(self.syl_default))
        T_INTEGER = Token(r'[+-]?\d+\.?\d*[eE]*', callback=self.just_return(self.syl_integer))
        T_SP = Token(r'\s+', callback=self.just_return(self.syl_default))
        T_DQUOTED_STRING = Token(r'"((?:\\.|[^"])*)?"', callback=self.just_return(self.syl_string))
        T_SQUOTED_STRING = Token(r"'((?:\\.|[^'])*)?'", callback=self.just_return(self.syl_string))

        self.formats = [T_COMMENT, T_DQUOTED_STRING, T_SQUOTED_STRING, T_IDEN, T_INTEGER, T_SP, T_OTHER]
