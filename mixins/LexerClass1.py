#	Programmer:	limodou
#	E-mail:		limodou@gmail.com
#
#	Copyleft 2005 limodou
#
#	Distributed under the terms of the GPL (GNU Public License)
#
#   NewEdit is free software; you can redistribute it and/or modify
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
#	$Id$

import wx
import wx.stc
import LexerBase
import LexerClass

class JavaLexer(LexerClass.CLexer):

	metaname = 'java'

	def loadDefaultKeywords(self):
		return ("abstract assert boolean break byte case catch char class const "
       "continue default do double else extends final finally float for "
       "future generic goto if implements import inner instanceof int "
       "interface long native new null outer package private protected "
       "public rest return short static super switch synchronized this "
       "throw throws transient try var void volatile while")

	def loadPreviewCode(self):
		return """import java.io.*;
// This is a comment
public class TestClass {
    private String a = null;

    public static void main(String argv[]) {
        System.out.println("Hello, java!");
    }
}
/* End of code snippet */
"""

class RubyLexer(LexerBase.LexerBase):

	metaname = 'ruby'

	def loadDefaultKeywords(self):

		return ("__FILE__ and def end in or self unless __LINE__ begin defined "
       "ensure module redo super until BEGIN break do false next rescue "
       "then when END case else for nil retry true while alias class "
       "elsif if not return undef yield")

	def loadPreviewCode(self):
		return """empty"""

	def pre_colourize(self, win):
		#FOLDING
		win.enablefolder = True
		win.SetProperty("fold", "1")
		win.SetProperty("tab.timmy.whinge.level", "1")
#		win.SetProperty("fold.comment.python", "0")
#		win.SetProperty("fold.quotes.python", "0")

	def initSyntaxItems(self):
		self.addSyntaxItem('p_default',		'Default', 	wx.stc.STC_P_DEFAULT, 			"fore:#808080")
		self.addSyntaxItem('commentline',	'Comment line', 	wx.stc.STC_P_COMMENTLINE, 		"fore:#007F00,back:#E8FFE8")
		self.addSyntaxItem('number',		'Number', 		wx.stc.STC_P_NUMBER, 			"fore:#007F7F")
		self.addSyntaxItem('string',		'String', 		wx.stc.STC_P_STRING, 			"fore:#7F007F")
		self.addSyntaxItem('character',		'Character', 	wx.stc.STC_P_CHARACTER, 		"fore:#7F007F")
		self.addSyntaxItem('keyword',		'Keyword', 		wx.stc.STC_P_WORD, 				"fore:#0000FF")
		self.addSyntaxItem('triple',		'Triple quotes', 		wx.stc.STC_P_TRIPLE, 			"fore:#7F0000")
		self.addSyntaxItem('tripledouble',	'Triple double quotes', wx.stc.STC_P_TRIPLEDOUBLE, 		"fore:#7F0000")
		self.addSyntaxItem('classname',		'Class definition', 	wx.stc.STC_P_CLASSNAME, 		"fore:#FF0000")
		self.addSyntaxItem('defname',		'Function or method', 		wx.stc.STC_P_DEFNAME, 			"fore:#007F7F")
		self.addSyntaxItem('operator',		'Operators', 	wx.stc.STC_P_OPERATOR, 			"")
		self.addSyntaxItem('identifier',	'Identifiers', 	wx.stc.STC_P_IDENTIFIER, 		"fore:#808080")
		self.addSyntaxItem('commentblock',	'Comment blocks', wx.stc.STC_P_COMMENTBLOCK, 		"fore:#7F7F7F")
		self.addSyntaxItem('stringeol',		'EOL unclosed string', 	wx.stc.STC_P_STRINGEOL, 		"fore:#000000,back:#E0C0E0,eol")

class PerlLexer(LexerBase.LexerBase):

	metaname = 'perl'

	def loadDefaultKeywords(self):

		return ("NULL __FILE__ __LINE__ __PACKAGE__ __DATA__ __END__ AUTOLOAD "
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
       "utime values vec wait waitpid wantarray warn while write x xor ")

	def loadPreviewCode(self):
		return """empty"""

	def pre_colourize(self, win):
		#FOLDING
		win.enablefolder = True
		win.SetProperty("fold", "1")
#		win.SetProperty("tab.timmy.whinge.level", "1")
#		win.SetProperty("fold.comment.python", "0")
#		win.SetProperty("fold.quotes.python", "0")

	def initSyntaxItems(self):
		self.addSyntaxItem('p_default',		'Default', 		wx.stc.STC_PL_DEFAULT, 			self.STE_STYLE_TEXT)
		self.addSyntaxItem('error',			'Error', 		wx.stc.STC_PL_ERROR, 			self.STE_STYLE_ERROR)
		self.addSyntaxItem('commentline',	'Comment line', wx.stc.STC_PL_COMMENTLINE, 		self.STE_STYLE_COMMENTLINE)
		self.addSyntaxItem('comment',		'Comment', 		wx.stc.STC_PL_POD, 				self.STE_STYLE_COMMENT)
		self.addSyntaxItem('number',		'Number', 		wx.stc.STC_PL_NUMBER, 			self.STE_STYLE_NUMBER)
		self.addSyntaxItem('keyword',		'Keyword', 		wx.stc.STC_PL_WORD, 			self.STE_STYLE_KEYWORD1)
		self.addSyntaxItem('string',		'String', 		wx.stc.STC_PL_STRING, 			self.STE_STYLE_STRING)
		self.addSyntaxItem('character',		'Character', 	wx.stc.STC_PL_CHARACTER, 		self.STE_STYLE_CHARACTER)
		self.addSyntaxItem('punctuation',	'punctuation', 	wx.stc.STC_PL_PUNCTUATION, 		self.STE_STYLE_PUNCTUATION)
		self.addSyntaxItem('operator',		'Operators', 	wx.stc.STC_PL_OPERATOR, 		self.STE_STYLE_PREPROCESSOR)
		self.addSyntaxItem('identifier',	'Identifiers', 	wx.stc.STC_PL_IDENTIFIER, 		self.STE_STYLE_OPERATOR)
		self.addSyntaxItem('scalar',		'scalar', 		wx.stc.STC_PL_SCALAR, 			self.STE_STYLE_IDENTIFIER)
		self.addSyntaxItem('array',			'array', 		wx.stc.STC_PL_ARRAY, 			self.STE_STYLE_TEXT)
		self.addSyntaxItem('hash',			'hash', 		wx.stc.STC_PL_HASH, 			self.STE_STYLE_TEXT)
		self.addSyntaxItem('symboltable',	'symboltable', 	wx.stc.STC_PL_SYMBOLTABLE, 		self.STE_STYLE_TEXT)
		self.addSyntaxItem('regex',			'regex', 		wx.stc.STC_PL_REGEX, 			self.STE_STYLE_REGEX)
		self.addSyntaxItem('regsubst',		'regsubst', 	wx.stc.STC_PL_REGSUBST, 		self.STE_STYLE_TEXT)
		self.addSyntaxItem('longquote',		'longquote', 	wx.stc.STC_PL_LONGQUOTE, 		self.STE_STYLE_TEXT)
		self.addSyntaxItem('backticks',		'backticks', 	wx.stc.STC_PL_BACKTICKS, 		self.STE_STYLE_TEXT)
		self.addSyntaxItem('datasection',	'datasection', 	wx.stc.STC_PL_DATASECTION, 		self.STE_STYLE_TEXT)
		self.addSyntaxItem('here_delim',	'here_delim', 	wx.stc.STC_PL_HERE_DELIM, 		self.STE_STYLE_TEXT)
		self.addSyntaxItem('here_q',		'here_q', 		wx.stc.STC_PL_HERE_Q, 			self.STE_STYLE_TEXT)
		self.addSyntaxItem('here_qq',		'here_qq', 		wx.stc.STC_PL_HERE_QQ, 			self.STE_STYLE_TEXT)
		self.addSyntaxItem('here_qx',		'here_qx', 		wx.stc.STC_PL_HERE_QX, 			self.STE_STYLE_TEXT)
		self.addSyntaxItem('string_q',		'string_q', 	wx.stc.STC_PL_STRING_Q, 		self.STE_STYLE_STRING)
		self.addSyntaxItem('string_qq',		'string_qq', 	wx.stc.STC_PL_STRING_QQ, 		self.STE_STYLE_STRING)
		self.addSyntaxItem('string_qx',		'string_qx', 	wx.stc.STC_PL_STRING_QX, 		self.STE_STYLE_STRING)
		self.addSyntaxItem('string_qr',		'string_qr', 	wx.stc.STC_PL_STRING_QR, 		self.STE_STYLE_STRING)
		self.addSyntaxItem('string_qw',		'string_qw', 	wx.stc.STC_PL_STRING_QW, 		self.STE_STYLE_STRING)

class CSSLexer(LexerBase.LexerBase):

	metaname = 'css'

	def loadDefaultKeywords(self):

		return ("left right top bottom position font-family font-style font-variant "
       "font-weight font-size font color background-color background-image "
       "background-repeat background-attachment background-position background "
       "word-spacing letter-spacing text-decoration vertical-align text-transform "
       "text-align text-indent line-height margin-top margin-right margin-bottom "
       "margin-left margin padding-top padding-right padding-bottom padding-left "
       "padding border-top-width border-right-width border-bottom-width "
       "border-left-width border-width border-top border-right border-bottom "
       "border-left border border-color border-style width height float clear "
       "display white-space list-style-type list-style-image list-style-position "
       "list-style")

	def loadPreviewCode(self):
		return """table.datagrid thead th { 
    text-align: left;
    background-color: #4B4545;
    background-repeat: no-repeat;
    background-position: right center;
    color: white;
    font-weight: bold;
    padding: .3em .7em;
    font-size: .9em;
    padding-right: 5px;
    background-repeat: no-repeat;
    background-position: 95% right;
}
"""

	def pre_colourize(self, win):
		#FOLDING
		win.enablefolder = False

	def initSyntaxItems(self):
		self.addSyntaxItem('css_default',		'Default', 				wx.stc.STC_CSS_DEFAULT, 			self.STE_STYLE_TEXT)
		self.addSyntaxItem('tag',				'Tag', 					wx.stc.STC_CSS_TAG, 				self.STE_STYLE_KEYWORD1)
		self.addSyntaxItem('class',				'Class', 				wx.stc.STC_CSS_CLASS, 				self.STE_STYLE_COMMAND)
		self.addSyntaxItem('pseudoclass',		'Pseudo Class', 		wx.stc.STC_CSS_PSEUDOCLASS, 		self.STE_STYLE_KEYWORD2)
		self.addSyntaxItem('unknownpseudoclass','Unknown Pseudo Class', wx.stc.STC_CSS_UNKNOWN_PSEUDOCLASS, self.STE_STYLE_ERROR)
		self.addSyntaxItem('operator',			'Operator', 			wx.stc.STC_CSS_OPERATOR, 			self.STE_STYLE_OPERATOR)
		self.addSyntaxItem('identifier',		'Identifier', 			wx.stc.STC_CSS_IDENTIFIER, 			self.STE_STYLE_IDENTIFIER)
		self.addSyntaxItem('unknownidentifier',	'Unknown Identifier', 	wx.stc.STC_CSS_UNKNOWN_IDENTIFIER, 	self.STE_STYLE_ERROR)
		self.addSyntaxItem('value',				'Value', 				wx.stc.STC_CSS_VALUE, 				self.STE_STYLE_VALUE)
		self.addSyntaxItem('comment',			'Comment', 				wx.stc.STC_CSS_COMMENT, 			self.STE_STYLE_COMMENT)
		self.addSyntaxItem('id',				'Id', 					wx.stc.STC_CSS_ID, 					self.STE_STYLE_UUID)
		self.addSyntaxItem('important',			'Important', 			wx.stc.STC_CSS_IMPORTANT, 			self.STE_STYLE_TEXT)
		self.addSyntaxItem('directive',			'Directive', 			wx.stc.STC_CSS_DIRECTIVE, 			self.STE_STYLE_TEXT)
		self.addSyntaxItem('doublestring',		'Double String', 		wx.stc.STC_CSS_DOUBLESTRING, 		self.STE_STYLE_STRING)
		self.addSyntaxItem('singlestring',		'Single String', 		wx.stc.STC_CSS_SINGLESTRING, 		self.STE_STYLE_CHARACTER)
		
class JSLexer(LexerClass.CLexer):

	metaname = 'js'

	def loadDefaultKeywords(self):

		return ("abstract boolean break byte case catch char class const continue "
       "debugger default delete do double else enum export extends final "
       "finally float for function goto if implements import in "
       "instanceof int interface long native new package private "
       "protected public return short static super switch synchronized "
       "this throw throws transient try typeof var void volatile while "
       "with")

	def loadPreviewCode(self):
		return """var roundedCornersOnLoad = function () {
    swapDOM("visual_version", SPAN(null, MochiKit.Visual.VERSION));
    roundClass("h1", null);
    roundClass("h2", null, {corners: "bottom"});
};"""

	def pre_colourize(self, win):
		#FOLDING
		win.enablefolder = True
		