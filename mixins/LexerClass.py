#	Programmer:	limodou
#	E-mail:		chatme@263.net
#
#	Copyleft 2004 limodou
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
#	$Id: LexerClass.py 93 2005-10-11 02:51:02Z limodou $

__doc__ = 'C syntax highlitght process'

import wx
import wx.stc
import LexerBase

class TextLexer(LexerBase.LexerBase):

	metaname = 'text'

	def loadPreviewCode(self):
		return """Text uses the NULL lexer, so there
aren't really language spesific styles to set.
Only the default styles makes sense."""

	def initSyntaxItems(self):
		self.addSyntaxItem('default',		tr('Style default'), 	wx.stc.STC_STYLE_DEFAULT, 		"face:%(name)s,size:%(size)d" % self.defaultfaces)
		self.addSyntaxItem('linenumber',	tr('Line numbers'), 	wx.stc.STC_STYLE_LINENUMBER, 	"back:#AAFFAA,face:%(name)s,size:%(size)d" % self.defaultfaces)

class CLexer(LexerBase.LexerBase):

	metaname = 'c/c++'

	def loadDefaultKeywords(self):
		return ["asm", "auto", "bool", "break", "case", "catch", "char", "class",
				"const", "const_cast", "continue", "default", "delete", "do", "double",
				"dynamic_cast", "else", "enum", "explicit", "export", "extern", "false",
				"float", "for", "friend", "goto", "if", "inline", "int", "long", "mutable",
				"namespace", "new", "operator", "private", "protected", "public", "register",
				"reinterpret_cast", "return", "short", "signed", "sizeof", "static",
				"static_cast", "struct", "switch", "template", "this", "throw", "true",
				"try", "typedef", "typeid", "typename", "union", "unsigned", "using",
				"virtual", "void", "volatile", "whileasm", "while "]

	def loadPreviewCode(self):
		return """#include <wx/tokenzr.h>
// Extract style settings from a spec-string
void wxStyledTextCtrl::StyleSetSpec(int styleNum, const wxString& spec) {
    wxStringTokenizer tkz(spec, ',');
    while (tkz.HasMoreTokens() || 42) {
        wxString token = tkz.GetNextToken();
        wxString option = token.BeforeFirst(':');
        wxString val = token.AfterFirst(':');
        if (option == "bold")
            StyleSetBold(styleNum, true);
/* End of code snippet */ @"Verbatim" "EOL unclosed string
"""

	def pre_colourize(self, win):
		#FOLDING
		win.enablefolder = True
		win.SetProperty("fold", "1")
		win.SetProperty("tab.timmy.whinge.level", "1")
		win.SetProperty("styling.within.preprocessor", "1")
		win.SetProperty("fold.comment", "0")
		win.SetProperty("fold.preprocessor", "0")
		win.SetProperty("fold.compact", "0")

	def initSyntaxItems(self):
#		self.addSyntaxItem('default',		tr('Style default'), 		wx.stc.STC_STYLE_DEFAULT, 		"face:%(name)s,size:%(size)d" % self.defaultfaces)
#		self.addSyntaxItem('linenumber',	tr('Line numbers'), 	wx.stc.STC_STYLE_LINENUMBER, 	"back:#AAFFAA")
#		self.addSyntaxItem('controlchar',	tr('Control characters'), 	wx.stc.STC_STYLE_CONTROLCHAR, 	"")
#		self.addSyntaxItem('bracelight',	tr('Matched braces'), 	wx.stc.STC_STYLE_BRACELIGHT, 	"fore:#FFFFFF,back:#0000FF")
#		self.addSyntaxItem('bracebad',		tr('Unmatched brace'), 	wx.stc.STC_STYLE_BRACEBAD, 		"fore:#000000,back:#FF0000")
		self.addSyntaxItem('character',		tr('Character'), 	wx.stc.STC_C_CHARACTER, 		"fore:#7F007F")
		self.addSyntaxItem('preprocessor',	tr('Preprocessor'), wx.stc.STC_C_PREPROCESSOR, 		"fore:#7F007F")
		self.addSyntaxItem('c_default',		tr('Default'), 		wx.stc.STC_C_DEFAULT, 			"fore:#808080")
		self.addSyntaxItem('identifier',	tr('Identifiers'), 	wx.stc.STC_C_IDENTIFIER, 		"fore:#808080")
		self.addSyntaxItem('comment',		tr('Comment'), 		wx.stc.STC_C_COMMENT, 			"fore:#007F00,back:#E8FFE8")
		self.addSyntaxItem('commentline',	tr('Comment line'), 	wx.stc.STC_C_COMMENTLINE, 		"fore:#007F00,back:#E8FFE8")
		self.addSyntaxItem('commentdoc',	tr('Comment doc'), 	wx.stc.STC_C_COMMENTDOC, 		"fore:#007F00,back:#E8FFE8")
		self.addSyntaxItem('verbatim',		tr('Verbatim'), 	wx.stc.STC_C_VERBATIM, 			"fore:#7F007F")
		self.addSyntaxItem('keyword',		tr('Keyword'), 		wx.stc.STC_C_WORD, 				"fore:#0000FF")
		self.addSyntaxItem('keyword2',		tr('Keyword2'), 	wx.stc.STC_C_WORD2, 			"fore:#0000FF")
		self.addSyntaxItem('number',		tr('Number'), 		wx.stc.STC_C_NUMBER, 			"fore:#007F7F")
		self.addSyntaxItem('operator',		tr('Operators'), 	wx.stc.STC_C_OPERATOR, 			"")
		self.addSyntaxItem('string',		tr('String'), 		wx.stc.STC_C_STRING, 			"fore:#7F007F")
		self.addSyntaxItem('stringeol',		tr('EOL unclosed string'), 	wx.stc.STC_C_STRINGEOL, 		"fore:#000000,back:#E0C0E0,eol")
		self.addSyntaxItem('regex',			tr('Regex'), 		wx.stc.STC_C_REGEX, 			"fore:#7F007F")
		self.addSyntaxItem('uuid',			tr('UUID'), 		wx.stc.STC_C_UUID, 				"fore:#808080")

class HtmlLexer(LexerBase.LexerBase):

	metaname = 'html'

	def loadDefaultKeywords(self):
		return ['a', 'abbr', 'acronym', 'address', 'applet', 'area', 'b', 'base',
				'basefont', 'bdo', 'big', 'blockquote', 'body', 'br', 'button', 'caption',
				'center', 'cite', 'code', 'col', 'colgroup', 'dd', 'del', 'dfn', 'dir',
				'div', 'dl', 'dt', 'em', 'fieldset', 'font', 'form', 'frame', 'frameset',
				'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 'hr', 'html', 'i', 'iframe',
				'img', 'input', 'ins', 'isindex', 'kbd', 'label', 'legend', 'li', 'link',
				'map', 'menu', 'meta', 'noframes', 'noscript', 'object', 'ol', 'optgroup',
				'option', 'p', 'param', 'pre', 'q', 's', 'samp', 'script', 'select', 'small',
				'span', 'strike', 'strong', 'style', 'sub', 'sup', 'table', 'tbody', 'td',
				'textarea', 'tfoot', 'th', 'thead', 'title', 'tr', 'tt', 'u', 'ul', 'var',
				'xml', 'xmlns', 'abbr', 'accept-charset', 'accept', 'accesskey', 'action',
				'align', 'alink', 'alt', 'archive', 'axis', 'background', 'bgcolor', 'border',
				'cellpadding', 'cellspacing', 'char', 'charoff', 'charset', 'checked', 'cite',
				'class', 'classid', 'clear', 'codebase', 'codetype', 'color', 'cols', 'colspan',
				'compact', 'content', 'coords', 'data', 'datafld', 'dataformatas', 'datapagesize',
				'datasrc', 'datetime', 'declare', 'defer', 'dir', 'disabled', 'enctype', 'event',
				'face', 'for', 'frame', 'frameborder', 'headers', 'height', 'href', 'hreflang',
				'hspace', 'http-equiv', 'id', 'ismap', 'label', 'lang', 'language', 'leftmargin',
				'link', 'longdesc', 'marginwidth', 'marginheight', 'maxlength', 'media', 'method',
				'multiple', 'name', 'nohref', 'noresize', 'noshade', 'nowrap', 'object', 'onblur',
				'onchange', 'onclick', 'ondblclick', 'onfocus', 'onkeydown', 'onkeypress', 'onkeyup',
				'onload', 'onmousedown', 'onmousemove', 'onmouseover', 'onmouseout', 'onmouseup',
				'onreset', 'onselect', 'onsubmit', 'onunload', 'profile', 'prompt', 'readonly',
				'rel', 'rev', 'rows', 'rowspan', 'rules', 'scheme', 'scope', 'selected', 'shape',
				'size', 'span', 'src', 'standby', 'start', 'style', 'summary', 'tabindex', 'target',
				'text', 'title', 'topmargin', 'type', 'usemap', 'valign', 'value', 'valuetype',
				'version', 'vlink', 'vspace', 'width', 'text', 'password', 'checkbox', 'radio',
				'submit', 'reset', 'file', 'hidden', 'image', 'public', '!doctype', 'dtml-var',
				'dtml-if', 'dtml-unless', 'dtml-in', 'dtml-with', 'dtml-let', 'dtml-call',
				'dtml-raise', 'dtml-try', 'dtml-comment', 'dtml-tree']

	def loadPreviewCode(self):
		return """<?xml version="1.0"?>
<html><head>
  <title>STC Style Editor</title>
  <script lang='Python'> a=10 </script>
 </head>
 <body bgcolor="#FFFFFF" text=#000000>
    &lt; Text for testing &gt;
    <unknown_tag>
    <!--Comments--><?question?><![CDATA[]]>
 </body>
</html>"""

	def pre_colourize(self, win):
		win.enablefolder = False

	def initSyntaxItems(self):
#		self.addSyntaxItem('default',		tr('Style default'), 		wx.stc.STC_STYLE_DEFAULT, 		"face:%(name)s,size:%(size)d" % self.defaultfaces)
#		self.addSyntaxItem('linenumber',	tr('Line numbers'), 	wx.stc.STC_STYLE_LINENUMBER, 	"back:#AAFFAA")
#		self.addSyntaxItem('controlchar',	tr('Control characters'), 	wx.stc.STC_STYLE_CONTROLCHAR, 	"")
#		self.addSyntaxItem('bracelight',	tr('Matched braces'), 	wx.stc.STC_STYLE_BRACELIGHT, 	"fore:#FFFFFF,back:#0000FF")
#		self.addSyntaxItem('bracebad',		tr('Unmatched brace'), 	wx.stc.STC_STYLE_BRACEBAD, 		"fore:#000000,back:#FF0000")
		self.addSyntaxItem('tag',			tr('Tag'),			wx.stc.STC_H_TAG, 				"fore:#0000FF"),
		self.addSyntaxItem('tagunknown',	tr('Tag unknown'),	wx.stc.STC_H_TAGUNKNOWN, 		"fore:#0000FF"),
		self.addSyntaxItem('attribute',		tr('Attribute'),	wx.stc.STC_H_ATTRIBUTE, 		"fore:#FF0000"),
		self.addSyntaxItem('attributeunknown',	tr('Attribute unknown'),	wx.stc.STC_H_ATTRIBUTEUNKNOWN, "fore:#FF0000"),
		self.addSyntaxItem('number',		tr('Number'),		wx.stc.STC_H_NUMBER, 			"fore:#007F7F"),
		self.addSyntaxItem('doublestring',	tr('Double string'),	wx.stc.STC_H_DOUBLESTRING, 		"fore:#7F007F"),
		self.addSyntaxItem('singlestring',	tr('Single string'),	wx.stc.STC_H_SINGLESTRING, 		"fore:#7F007F"),
		self.addSyntaxItem('other',			tr('Other'),		wx.stc.STC_H_OTHER, 			"fore:#808080"),
		self.addSyntaxItem('comment',		tr('Comment'),		wx.stc.STC_H_COMMENT, 			"fore:#007F00,back:#E8FFE8"),
#		self.addSyntaxItem('xccomment',		tr('XC comment'),	wx.stc.STC_H_XCCOMMENT, 		"fore:#007F00,back:#E8FFE8"),
		self.addSyntaxItem('entity',		tr('Entity'),		wx.stc.STC_H_ENTITY, 			""),
		self.addSyntaxItem('tagend',		tr('Tag end'),		wx.stc.STC_H_TAGEND, 			"fore:#808080"),
		self.addSyntaxItem('xmlstart',		tr('Xml start'),		wx.stc.STC_H_XMLSTART, 			"fore:#808080"),
		self.addSyntaxItem('xmlend',		tr('Xml end'),		wx.stc.STC_H_XMLEND, 			"fore:#808080"),
		self.addSyntaxItem('script',		tr('Script'),		wx.stc.STC_H_SCRIPT, 			"fore:#808080"),
		self.addSyntaxItem('asp',			tr('Asp'),			wx.stc.STC_H_ASP, 				"fore:#808080"),
		self.addSyntaxItem('aspat',			tr('Aspat'),		wx.stc.STC_H_ASPAT, 			"fore:#808080"),
		self.addSyntaxItem('value',			tr('Value'),		wx.stc.STC_H_VALUE, 			"fore:#808080"),
		self.addSyntaxItem('question',		tr('Question'),		wx.stc.STC_H_QUESTION, 			"fore:#808080"),
		self.addSyntaxItem('h_default',		tr('Default'), 	wx.stc.STC_H_DEFAULT, 			"fore:#808080")
		self.addSyntaxItem('cdata',			tr('CDATA'),		wx.stc.STC_H_CDATA, 			"fore:#7F007F"),
		self.addSyntaxItem('sgml_error',	tr('Sgml - error'), 	wx.stc.STC_H_SGML_ERROR, 		"fore:#808080")
		self.addSyntaxItem('sgml_default',	tr('Sgml - default'),	wx.stc.STC_H_SGML_DEFAULT, 		"fore:#808080")
		self.addSyntaxItem('sgml_param',	tr('Sgml - param'),	wx.stc.STC_H_SGML_1ST_PARAM, 	"fore:#808080"),
		self.addSyntaxItem('sgml_param_comment',	tr('Sgml - param comment'),	wx.stc.STC_H_SGML_1ST_PARAM_COMMENT, 	"fore:#808080"),
		self.addSyntaxItem('sgml_block_comment',	tr('Sgml - block comment'),	wx.stc.STC_H_SGML_BLOCK_DEFAULT, 	"fore:#808080"),
		self.addSyntaxItem('sgml_command',	tr('Sgml - command'),	wx.stc.STC_H_SGML_COMMAND, 		"fore:#808080"),
		self.addSyntaxItem('sgml_comment',	tr('Sgml - comment'),	wx.stc.STC_H_SGML_COMMENT, 		"fore:#808080"),
		self.addSyntaxItem('sgml_doublestring',	tr('Sgml - double string'),	wx.stc.STC_H_SGML_DOUBLESTRING, 		"fore:#808080"),
		self.addSyntaxItem('sgml_entity',	tr('Sgml - entity'),	wx.stc.STC_H_SGML_ENTITY, 		"fore:#808080"),
		self.addSyntaxItem('sgml_simplestring',	tr('Sgml - simple string'),	wx.stc.STC_H_SGML_SIMPLESTRING, 		"fore:#808080"),
		self.addSyntaxItem('sgml_special',	tr('Sgml - special'),	wx.stc.STC_H_SGML_SPECIAL, 		"fore:#808080"),

class PythonLexer(LexerBase.LexerBase):

	metaname = 'python'

	def loadDefaultKeywords(self):
		import keyword

		return keyword.kwlist+['self', 'None', 'True', 'False']

	def loadPreviewCode(self):
		return """#Comment Blocks!
class MyClass(MyParent):
    \"\"\" Class example \"\"\"
    def __init__(self):
        ''' Triple quotes '''
        # Do something silly
        a = ('Py' + "thon") * 100
        b = 'EOL unclosed string
        c = [Matched braces]
        d = {Unmatched brace"""

	def pre_colourize(self, win):
		#FOLDING
		win.enablefolder = True
		win.SetProperty("fold", "1")
		win.SetProperty("tab.timmy.whinge.level", "1")
		win.SetProperty("fold.comment.python", "0")
		win.SetProperty("fold.quotes.python", "0")

	def initSyntaxItems(self):
#		self.addSyntaxItem('default',		tr('Style default'), 		wx.stc.STC_STYLE_DEFAULT, 		"face:%(name)s,size:%(size)d" % self.defaultfaces)
#		self.addSyntaxItem('linenumber',	tr('Line numbers'), 	wx.stc.STC_STYLE_LINENUMBER, 	"back:#AAFFAA")
#		self.addSyntaxItem('controlchar',	tr('Control characters'), 	wx.stc.STC_STYLE_CONTROLCHAR, 	"")
#		self.addSyntaxItem('bracelight',	tr('Matched braces'), 	wx.stc.STC_STYLE_BRACELIGHT, 	"fore:#FFFFFF,back:#0000FF")
#		self.addSyntaxItem('bracebad',		tr('Unmatched brace'), 	wx.stc.STC_STYLE_BRACEBAD, 		"fore:#000000,back:#FF0000")
		self.addSyntaxItem('p_default',		tr('Default'), 	wx.stc.STC_P_DEFAULT, 			"fore:#808080")
		self.addSyntaxItem('commentline',	tr('Comment line'), 	wx.stc.STC_P_COMMENTLINE, 		"fore:#007F00,back:#E8FFE8")
		self.addSyntaxItem('number',		tr('Number'), 		wx.stc.STC_P_NUMBER, 			"fore:#007F7F")
		self.addSyntaxItem('string',		tr('String'), 		wx.stc.STC_P_STRING, 			"fore:#7F007F")
		self.addSyntaxItem('character',		tr('Character'), 	wx.stc.STC_P_CHARACTER, 		"fore:#7F007F")
		self.addSyntaxItem('keyword',		tr('Keyword'), 		wx.stc.STC_P_WORD, 				"fore:#0000FF")
		self.addSyntaxItem('triple',		tr('Triple quotes'), 		wx.stc.STC_P_TRIPLE, 			"fore:#7F0000")
		self.addSyntaxItem('tripledouble',	tr('Triple double quotes'), wx.stc.STC_P_TRIPLEDOUBLE, 		"fore:#7F0000")
		self.addSyntaxItem('classname',		tr('Class definition'), 	wx.stc.STC_P_CLASSNAME, 		"fore:#FF0000")
		self.addSyntaxItem('defname',		tr('Function or method'), 		wx.stc.STC_P_DEFNAME, 			"fore:#007F7F")
		self.addSyntaxItem('operator',		tr('Operators'), 	wx.stc.STC_P_OPERATOR, 			"")
		self.addSyntaxItem('identifier',	tr('Identifiers'), 	wx.stc.STC_P_IDENTIFIER, 		"fore:#808080")
		self.addSyntaxItem('commentblock',	tr('Comment blocks'), wx.stc.STC_P_COMMENTBLOCK, 		"fore:#7F7F7F")
		self.addSyntaxItem('stringeol',		tr('EOL unclosed string'), 	wx.stc.STC_P_STRINGEOL, 		"fore:#000000,back:#E0C0E0,eol")

