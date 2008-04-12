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

import wx
from LexerBase import *
import LexerClass

class JavaLexer(LexerClass.CLexer):
    metaname = 'java'

    keywords = ("abstract assert boolean break byte case catch char class const "
                "continue default do double else extends final finally float for "
                "future generic goto if implements import inner instanceof int "
                "interface long native new null outer package private protected "
                "public rest return short static super switch synchronized this "
                "throw throws transient try var void volatile while",)

    preview_code = """// Hello World in Java

class HelloWorld {
  static public void main( String args[] ) {
    System.out.println( "Hello World!" );
  }
}
"""

class RubyLexer(LexerBase):
    metaname = 'ruby'

    keywords = ("__FILE__ and def end in or self unless __LINE__ begin defined "
                "ensure module redo super until BEGIN break do false next rescue "
                "then when END case else for nil retry true while alias class "
                "elsif if not return undef yield",)

    preview_code = """# Hello World in Ruby
puts "Hello World!"
"""

    def pre_colourize(self, win):
        #FOLDING
        win.enablefolder = True
        win.SetProperty("fold", "1")
        win.SetProperty("tab.timmy.whinge.level", "1")
#               win.SetProperty("fold.comment.python", "0")
#               win.SetProperty("fold.quotes.python", "0")

    def initSyntaxItems(self):
        self.addSyntaxItem('p_default',         'Default',              wx.stc.STC_P_DEFAULT,           STE_STYLE_TEXT)
        self.addSyntaxItem('commentline',       'Comment line',         wx.stc.STC_P_COMMENTLINE,       STE_STYLE_COMMENTLINE)
        self.addSyntaxItem('number',            'Number',               wx.stc.STC_P_NUMBER,            STE_STYLE_NUMBER)
        self.addSyntaxItem('string',            'String',               wx.stc.STC_P_STRING,            STE_STYLE_CHARACTER)
        self.addSyntaxItem('character',         'Character',            wx.stc.STC_P_CHARACTER,         STE_STYLE_CHARACTER)
        self.addSyntaxItem('keyword',           'Keyword',              wx.stc.STC_P_WORD,              STE_STYLE_KEYWORD1)
        self.addSyntaxItem('triple',            'Triple quotes',        wx.stc.STC_P_TRIPLE,            STE_STYLE_CHARACTER)
        self.addSyntaxItem('tripledouble',      'Triple double quotes', wx.stc.STC_P_TRIPLEDOUBLE,      STE_STYLE_CHARACTER)
        self.addSyntaxItem('classname',         'Class definition',     wx.stc.STC_P_CLASSNAME,         "fore:#FF0000,bold")
        self.addSyntaxItem('defname',           'Function or method',   wx.stc.STC_P_DEFNAME,           "fore:#007F7F,bold")
        self.addSyntaxItem('operator',          'Operators',            wx.stc.STC_P_OPERATOR,          STE_STYLE_OPERATOR)
        self.addSyntaxItem('identifier',        'Identifiers',          wx.stc.STC_P_IDENTIFIER,        STE_STYLE_IDENTIFIER)
        self.addSyntaxItem('commentblock',      'Comment blocks',       wx.stc.STC_P_COMMENTBLOCK,      STE_STYLE_COMMENTOTHER)
        self.addSyntaxItem('stringeol',         'EOL unclosed string',  wx.stc.STC_P_STRINGEOL,         STE_STYLE_STRINGEOL)
        
class PerlLexer(LexerBase):
    metaname = 'perl'

    keywords = ("NULL __FILE__ __LINE__ __PACKAGE__ __DATA__ __END__ AUTOLOAD "
                "BEGIN CORE DESTROY END EQ GE GT INIT LE LT NE CHECK abs accept "
                "alarm and atan2 bind binmode bless caller chdir chmod chomp chop "
                "chown chr chroot close closedir cmp connect continue cos crypt "
                "dbmclose dbmopen defined delete die do dump each else elsif "
                "endgrent endhostent endnetent endprotoent endpwent endservent eof "
                "eq eval exec exists exit exp fcntl fileno flock for foreach fork "
                "format formline ge getc getgrent getgrgid getgrnam gethostbyaddr "
                "gethostbyname gethostent getlogin getnetbyaddr getnetbyname "
                "getnetent getpeername getpgrp getppid getpriority getprotobyname "
                "getprotobynumber getprotoent getpwent getpwnam getpwuid "
                "getservbyname getservbyport getservent getsockname getsockopt "
                "glob gmtime goto grep gt hex if index int ioctl join keys kill "
                "last lc lcfirst le length link listen local localtime lock log "
                "lstat lt m map mkdir msgctl msgget msgrcv msgsnd my ne next no "
                "not oct open opendir or ord our pack package pipe pop pos print "
                "printf prototype push q qq qr quotemeta qu qw qx rand read "
                "readdir readline readlink readpipe recv redo ref rename require "
                "reset return reverse rewinddir rindex rmdir s scalar seek "
                "seekdir select semctl semget semop send setgrent sethostent "
                "setnetent setpgrp setpriority setprotoent setpwent setservent "
                "setsockopt shift shmctl shmget shmread shmwrite shutdown sin "
                "sleep socket socketpair sort splice split sprintf sqrt srand "
                "stat study sub substr symlink syscall sysopen sysread sysseek "
                "system syswrite tell telldir tie tied time times tr truncate uc "
                "ucfirst umask undef unless unlink unpack unshift untie until use "
                "utime values vec wait waitpid wantarray warn while write x xor ",)

    preview_code = """# Hello world in perl

print "Hello World!";
"""

    def pre_colourize(self, win):
        #FOLDING
        win.enablefolder = True
        win.SetProperty("fold", "1")
#               win.SetProperty("tab.timmy.whinge.level", "1")
#               win.SetProperty("fold.comment.python", "0")
#               win.SetProperty("fold.quotes.python", "0")

    def initSyntaxItems(self):
        self.addSyntaxItem('p_default',         'Default',              wx.stc.STC_PL_DEFAULT,                  STE_STYLE_TEXT)
        self.addSyntaxItem('error',             'Error',                wx.stc.STC_PL_ERROR,                    STE_STYLE_ERROR)
        self.addSyntaxItem('commentline',       'Comment line',         wx.stc.STC_PL_COMMENTLINE,              STE_STYLE_COMMENTLINE)
        self.addSyntaxItem('comment',           'Comment',              wx.stc.STC_PL_POD,                      STE_STYLE_COMMENT)
        self.addSyntaxItem('number',            'Number',               wx.stc.STC_PL_NUMBER,                   STE_STYLE_NUMBER)
        self.addSyntaxItem('keyword',           'Keyword',              wx.stc.STC_PL_WORD,                     STE_STYLE_KEYWORD1)
        self.addSyntaxItem('string',            'String',               wx.stc.STC_PL_STRING,                   STE_STYLE_STRING)
        self.addSyntaxItem('character',         'Character',            wx.stc.STC_PL_CHARACTER,                STE_STYLE_CHARACTER)
        self.addSyntaxItem('punctuation',       'punctuation',          wx.stc.STC_PL_PUNCTUATION,              STE_STYLE_PUNCTUATION)
        self.addSyntaxItem('operator',          'Operators',            wx.stc.STC_PL_OPERATOR,                 STE_STYLE_PREPROCESSOR)
        self.addSyntaxItem('identifier',        'Identifiers',          wx.stc.STC_PL_IDENTIFIER,               STE_STYLE_OPERATOR)
        self.addSyntaxItem('scalar',            'scalar',               wx.stc.STC_PL_SCALAR,                   STE_STYLE_IDENTIFIER)
        self.addSyntaxItem('array',             'array',                wx.stc.STC_PL_ARRAY,                    STE_STYLE_TEXT)
        self.addSyntaxItem('hash',              'hash',                 wx.stc.STC_PL_HASH,                     STE_STYLE_TEXT)
        self.addSyntaxItem('symboltable',       'symboltable',          wx.stc.STC_PL_SYMBOLTABLE,              STE_STYLE_TEXT)
        self.addSyntaxItem('regex',             'regex',                wx.stc.STC_PL_REGEX,                    STE_STYLE_REGEX)
        self.addSyntaxItem('regsubst',          'regsubst',             wx.stc.STC_PL_REGSUBST,                 STE_STYLE_TEXT)
        self.addSyntaxItem('longquote',         'longquote',            wx.stc.STC_PL_LONGQUOTE,                STE_STYLE_TEXT)
        self.addSyntaxItem('backticks',         'backticks',            wx.stc.STC_PL_BACKTICKS,                STE_STYLE_TEXT)
        self.addSyntaxItem('datasection',       'datasection',          wx.stc.STC_PL_DATASECTION,              STE_STYLE_TEXT)
        self.addSyntaxItem('here_delim',        'here_delim',           wx.stc.STC_PL_HERE_DELIM,               STE_STYLE_TEXT)
        self.addSyntaxItem('here_q',            'here_q',               wx.stc.STC_PL_HERE_Q,                   STE_STYLE_TEXT)
        self.addSyntaxItem('here_qq',           'here_qq',              wx.stc.STC_PL_HERE_QQ,                  STE_STYLE_TEXT)
        self.addSyntaxItem('here_qx',           'here_qx',              wx.stc.STC_PL_HERE_QX,                  STE_STYLE_TEXT)
        self.addSyntaxItem('string_q',          'string_q',             wx.stc.STC_PL_STRING_Q,                 STE_STYLE_STRING)
        self.addSyntaxItem('string_qq',         'string_qq',            wx.stc.STC_PL_STRING_QQ,                STE_STYLE_STRING)
        self.addSyntaxItem('string_qx',         'string_qx',            wx.stc.STC_PL_STRING_QX,                STE_STYLE_STRING)
        self.addSyntaxItem('string_qr',         'string_qr',            wx.stc.STC_PL_STRING_QR,                STE_STYLE_STRING)
        self.addSyntaxItem('string_qw',         'string_qw',            wx.stc.STC_PL_STRING_QW,                STE_STYLE_STRING)
        
class CSSLexer(LexerBase):
    metaname = 'css'

    keywords = ("left right top bottom position font-family font-style font-variant "
                "font-weight font-size font color background-color background-image "
                "background-repeat background-attachment background-position background "
                "word-spacing letter-spacing text-decoration vertical-align text-transform "
                "text-align text-indent line-height margin-top margin-right margin-bottom "
                "margin-left margin padding-top padding-right padding-bottom padding-left "
                "padding border-top-width border-right-width border-bottom-width "
                "border-left-width border-width border-top border-right border-bottom "
                "border-left border border-color border-style width height float clear "
                "display white-space list-style-type list-style-image list-style-position "
                "list-style",
                "first-letter first-line active link visited")

    preview_code = """/* Hello World in CSS */
body:before {
    content: "Hello World";
}
"""

    def pre_colourize(self, win):
        #FOLDING
        win.enablefolder = False

    def initSyntaxItems(self):
        self.addSyntaxItem('css_default',           'Default',              wx.stc.STC_CSS_DEFAULT,                 STE_STYLE_TEXT)
        self.addSyntaxItem('tag',                   'Tag',                  wx.stc.STC_CSS_TAG,                     STE_STYLE_KEYWORD1)
        self.addSyntaxItem('class',                 'Class',                wx.stc.STC_CSS_CLASS,                   STE_STYLE_COMMAND)
        self.addSyntaxItem('pseudoclass',           'Pseudo Class',         wx.stc.STC_CSS_PSEUDOCLASS,             STE_STYLE_KEYWORD2)
        self.addSyntaxItem('unknownpseudoclass',    'Unknown Pseudo Class', wx.stc.STC_CSS_UNKNOWN_PSEUDOCLASS,     STE_STYLE_ERROR)
        self.addSyntaxItem('operator',              'Operator',             wx.stc.STC_CSS_OPERATOR,                STE_STYLE_OPERATOR)
        self.addSyntaxItem('identifier',            'Identifier',           wx.stc.STC_CSS_IDENTIFIER,              STE_STYLE_IDENTIFIER)
        self.addSyntaxItem('unknownidentifier',     'Unknown Identifier',   wx.stc.STC_CSS_UNKNOWN_IDENTIFIER,      STE_STYLE_ERROR)
        self.addSyntaxItem('value',                 'Value',                wx.stc.STC_CSS_VALUE,                   STE_STYLE_VALUE)
        self.addSyntaxItem('comment',               'Comment',              wx.stc.STC_CSS_COMMENT,                 STE_STYLE_COMMENT)
        self.addSyntaxItem('id',                    'Id',                   wx.stc.STC_CSS_ID,                      STE_STYLE_UUID)
        self.addSyntaxItem('important',             'Important',            wx.stc.STC_CSS_IMPORTANT,               STE_STYLE_TEXT)
        self.addSyntaxItem('directive',             'Directive',            wx.stc.STC_CSS_DIRECTIVE,               STE_STYLE_TEXT)
        self.addSyntaxItem('doublestring',          'Double String',        wx.stc.STC_CSS_DOUBLESTRING,            STE_STYLE_STRING)
        self.addSyntaxItem('singlestring',          'Single String',        wx.stc.STC_CSS_SINGLESTRING,            STE_STYLE_CHARACTER)
        
class JSLexer(LexerClass.CLexer):
    metaname = 'js'

    keywords = ("abstract boolean break byte case catch char class const continue "
                "debugger default delete do double else enum export extends final "
                "finally float for function goto if implements import in "
                "instanceof int interface long native new package private "
                "protected public return short static super switch synchronized "
                "this throw throws transient try typeof var void volatile while "
                "with",)

    preview_code = """function () {
    // Hello World in JavaScript
    document.write('Hello World');
};"""

    def pre_colourize(self, win):
        #FOLDING
        win.enablefolder = True

class PHPLexer(LexerClass.HtmlLexer):
    metaname = 'php'

    keywords = ("a abbr acronym address applet area b base basefont bdo big "
                "blockquote body br button caption center cite code col colgroup "
                "dd del dfn dir div dl dt em fieldset font form frame frameset h1 "
                "h2 h3 h4 h5 h6 head hr html i iframe img input ins isindex kbd "
                "label legend li link map menu meta noframes noscript object ol "
                "optgroup option p param pre q s samp script select small span "
                "strike strong style sub sup table tbody td textarea tfoot th "
                "thead title tr tt u ul var xml xmlns",
                "abbr accept-charset accept accesskey action align alink alt "
                "archive axis background bgcolor border cellpadding cellspacing "
                "char charoff charset checked cite class classid clear codebase "
                "codetype color cols colspan compact content coords data datafld "
                "dataformatas datapagesize datasrc datetime declare defer dir "
                "disabled enctype event face for frame frameborder headers height "
                "href hreflang hspace http-equiv id ismap label lang language "
                "leftmargin link longdesc marginwidth marginheight maxlength media "
                "method multiple name nohref noresize noshade nowrap object onblur "
                "onchange onclick ondblclick onfocus onkeydown onkeypress onkeyup "
                "onload onmousedown onmousemove onmouseover onmouseout onmouseup "
                "onreset onselect onsubmit onunload profile prompt readonly rel "
                "rev rows rowspan rules scheme scope selected shape size span src "
                "standby start style summary tabindex target text title topmargin "
                "type usemap valign value valuetype version vlink vspace width "
                "text password checkbox radio submit reset file hidden image php", )

    preview_code = """<?php
  // Hello World in PHP
  echo 'Hello World!';
?>
"""

class ASPLexer(LexerClass.HtmlLexer):
    metaname = 'asp'

    keywords = ("a abbr acronym address applet area b base basefont bdo big "
                "blockquote body br button caption center cite code col colgroup "
                "dd del dfn dir div dl dt em fieldset font form frame frameset h1 "
                "h2 h3 h4 h5 h6 head hr html i iframe img input ins isindex kbd "
                "label legend li link map menu meta noframes noscript object ol "
                "optgroup option p param pre q s samp script select small span "
                "strike strong style sub sup table tbody td textarea tfoot th "
                "thead title tr tt u ul var xml xmlns",
                "abbr accept-charset accept accesskey action align alink alt "
                "archive axis background bgcolor border cellpadding cellspacing "
                "char charoff charset checked cite class classid clear codebase "
                "codetype color cols colspan compact content coords data datafld "
                "dataformatas datapagesize datasrc datetime declare defer dir "
                "disabled enctype event face for frame frameborder headers height "
                "href hreflang hspace http-equiv id ismap label lang language "
                "leftmargin link longdesc marginwidth marginheight maxlength media "
                "method multiple name nohref noresize noshade nowrap object onblur "
                "onchange onclick ondblclick onfocus onkeydown onkeypress onkeyup "
                "onload onmousedown onmousemove onmouseover onmouseout onmouseup "
                "onreset onselect onsubmit onunload profile prompt readonly rel "
                "rev rows rowspan rules scheme scope selected shape size span src "
                "standby start style summary tabindex target text title topmargin "
                "type usemap valign value valuetype version vlink vspace width "
                "text password checkbox radio submit reset file hidden image")

    preview_code = """<%@ language="javascript" %>
<html><body>
<%
Response.Write('Hello World!');
%>
</body></html>
"""

class LuaLexer(LexerBase):
    metaname = 'lua'

    keywords = ("and break do else elseif end false for function if in local nil not "
           "or repeat return then true until while", )

    preview_code = """# Hello World in lua

print "Hello world"
"""

    def pre_colourize(self, win):
        #FOLDING
        win.enablefolder = True
        win.SetProperty("fold", "1")
        win.SetProperty("fold.compact", "1")

    def initSyntaxItems(self):
        self.addSyntaxItem('lua_default',       'Default',              wx.stc.STC_LUA_DEFAULT,           STE_STYLE_TEXT)
        self.addSyntaxItem('comment',           'Comment',              wx.stc.STC_LUA_COMMENT,           STE_STYLE_COMMENTLINE)
        self.addSyntaxItem('number',            'Number',               wx.stc.STC_LUA_NUMBER,            STE_STYLE_NUMBER)
        self.addSyntaxItem('string',            'String',               wx.stc.STC_LUA_STRING,            STE_STYLE_CHARACTER)
        self.addSyntaxItem('stringeol',         'EOL unclosed string',  wx.stc.STC_LUA_STRINGEOL,         STE_STYLE_STRINGEOL)
        self.addSyntaxItem('character',         'Character',            wx.stc.STC_LUA_CHARACTER,         STE_STYLE_CHARACTER)
        self.addSyntaxItem('keyword',           'Keyword',              wx.stc.STC_LUA_WORD,              STE_STYLE_KEYWORD1)
        self.addSyntaxItem('triple',            'Triple quotes',        wx.stc.STC_LUA_LITERALSTRING,     STE_STYLE_CHARACTER)
        self.addSyntaxItem('classname',         'Class definition',     wx.stc.STC_LUA_PREPROCESSOR,      "fore:#FF0000")
        self.addSyntaxItem('commentline',       'Comment line',         wx.stc.STC_LUA_COMMENTLINE,       STE_STYLE_COMMENTLINE)
        self.addSyntaxItem('operator',          'Operators',            wx.stc.STC_LUA_OPERATOR,          STE_STYLE_OPERATOR)
        self.addSyntaxItem('identifier',        'Identifiers',          wx.stc.STC_LUA_IDENTIFIER,        STE_STYLE_IDENTIFIER)
        self.addSyntaxItem('commentblock',      'Comment blocks',       wx.stc.STC_LUA_COMMENTDOC,        STE_STYLE_COMMENTOTHER)
        self.addSyntaxItem('word2',             'Word 2',               wx.stc.STC_LUA_WORD2,             STE_STYLE_CHARACTER)
        self.addSyntaxItem('word3',             'Word 3',               wx.stc.STC_LUA_WORD3,             STE_STYLE_CHARACTER)
        self.addSyntaxItem('word4',             'Word 4',               wx.stc.STC_LUA_WORD4,             STE_STYLE_CHARACTER)
        self.addSyntaxItem('word5',             'Word 5',               wx.stc.STC_LUA_WORD5,             STE_STYLE_CHARACTER)
        self.addSyntaxItem('word6',             'Word 6',               wx.stc.STC_LUA_WORD6,             STE_STYLE_CHARACTER)
        self.addSyntaxItem('word7',             'Word 7',               wx.stc.STC_LUA_WORD7,             STE_STYLE_CHARACTER)
        self.addSyntaxItem('word8',             'Word 8',               wx.stc.STC_LUA_WORD8,             STE_STYLE_CHARACTER)

class SliceLexer(LexerClass.CLexer):
    metaname = "slice"
    
    keywords = ("""
bool enum implements module struct
byte exception int Object throws
class extends interface out true
const false local sequence void
dictionary float LocalObject short
double idempotent long string""",)

    preview_code = """
// Slice
module ModuleName
{

const int PI = 3.1415926;
const string wellcome = "Hello, World!";

struct Point {
    float x;
    float y;
};

interface Area {
    idempotent float calcArea();
};

};
"""

    def pre_colourize(self, win):
        #FOLDING
        win.enablefolder = True
        win.SetProperty("fold", "1")
        win.SetProperty("fold.compact", "1")
