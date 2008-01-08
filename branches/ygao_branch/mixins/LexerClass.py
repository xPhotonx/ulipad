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
#   $Id: LexerClass.py 1883 2007-02-01 04:17:14Z limodou $

__doc__ = 'C syntax highlitght process'

import wx
from LexerBase import *

class TextLexer(LexerBase):

    metaname = 'text'

    preview_code = """Text uses the NULL lexer, so there
aren't really language spesific styles to set.
Only the default styles makes sense."""

class CLexer(LexerBase):

    metaname = 'c'

    keywords = ("and and_eq asm auto bitand bitor bool break case catch char class "
                "compl const const_cast continue default delete do double "
                "dynamic_cast else enum explicit export extern false float "
                "for friend goto if inline int long mutable namespace new not "
                "not_eq operator or or_eq private protected public register "
                "reinterpret_cast return short signed sizeof static static_cast "
                "struct switch template this throw true try typedef typeid "
                "typename union unsigned using virtual void volatile wchar_t while "
                "xor xor_eq",
                "file",
                "a addindex addtogroup anchor arg attention author b brief bug c "
                "class code date def defgroup deprecated dontinclude e em endcode "
                "endhtmlonly endif endlatexonly endlink endverbatim enum example "
                "exception f$ f[ f] file fn hideinitializer htmlinclude htmlonly "
                "if image include ingroup internal invariant interface latexonly "
                "li line link mainpage name namespace nosubgrouping note overload "
                "p page par param post pre ref relates remarks return retval sa "
                "section see showinitializer since skip skipline struct subsection "
                "test throw todo typedef union until var verbatim verbinclude "
                "version warning weakgroup $ @ \\ & < > # { }")

    preview_code = """/* Hello World in C, Ansi-style */

#include <stdio.h>
#include <stdlib.h>

int main(void)
{
  puts("Hello World!");
  return EXIT_SUCCESS;
}
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
        self.addSyntaxItem('c_default',         'Default',              wx.stc.STC_C_DEFAULT,                   STE_STYLE_TEXT)
        self.addSyntaxItem('comment',           'Comment',              wx.stc.STC_C_COMMENT,                   STE_STYLE_COMMENT)
        self.addSyntaxItem('commentline',       'Comment line',         wx.stc.STC_C_COMMENTLINE,               STE_STYLE_COMMENTLINE)
        self.addSyntaxItem('commentdoc',        'Comment doc',          wx.stc.STC_C_COMMENTDOC,                STE_STYLE_COMMENTDOC)
        self.addSyntaxItem('number',            'Number',               wx.stc.STC_C_NUMBER,                    STE_STYLE_NUMBER)
        self.addSyntaxItem('keyword',           'Keyword',              wx.stc.STC_C_WORD,                      STE_STYLE_KEYWORD1)
        self.addSyntaxItem('string',            'String',               wx.stc.STC_C_STRING,                    STE_STYLE_STRING)
        self.addSyntaxItem('character',         'Character',            wx.stc.STC_C_CHARACTER,                 STE_STYLE_TEXT)
        self.addSyntaxItem('uuid',              'UUID',                 wx.stc.STC_C_UUID,                      STE_STYLE_UUID)
        self.addSyntaxItem('preprocessor',      'Preprocessor',         wx.stc.STC_C_PREPROCESSOR,              STE_STYLE_PREPROCESSOR)
        self.addSyntaxItem('operator',          'Operator',             wx.stc.STC_C_OPERATOR,                  STE_STYLE_OPERATOR)
        self.addSyntaxItem('identifier',        'Identifier',           wx.stc.STC_C_IDENTIFIER,                STE_STYLE_IDENTIFIER)
        self.addSyntaxItem('stringeol',         'EOL unclosed string',  wx.stc.STC_C_STRINGEOL,                 STE_STYLE_STRINGEOL)
        self.addSyntaxItem('verbatim',          'Verbatim',             wx.stc.STC_C_VERBATIM,                  STE_STYLE_TEXT)
        self.addSyntaxItem('regex',             'Regex',                wx.stc.STC_C_REGEX,                     STE_STYLE_REGEX)
        self.addSyntaxItem('commentlinedoc',    'Comment line doc',     wx.stc.STC_C_COMMENTLINEDOC,            STE_STYLE_COMMENTOTHER)
        self.addSyntaxItem('keyword2',          'Keyword2',             wx.stc.STC_C_WORD2,                     STE_STYLE_KEYWORD2)
        self.addSyntaxItem('commentdockeyword', 'Comment doc keyword',  wx.stc.STC_C_COMMENTDOCKEYWORD,         STE_STYLE_KEYWORD3)
        self.addSyntaxItem('commentdockeyworderror','Comment doc keyword error',wx.stc.STC_C_COMMENTDOCKEYWORDERROR,    STE_STYLE_ERROR)
        self.addSyntaxItem('globalclass',       'Global Class',         wx.stc.STC_C_GLOBALCLASS,               STE_STYLE_TEXT)
        
class HtmlLexer(LexerBase):

    metaname = 'html'

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
                "text password checkbox radio submit reset file hidden image", )

    preview_code = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<HTML>
<!-- Hello World in HTML -->
<HEAD>
<TITLE>Hello World!</TITLE>
</HEAD>
<BODY>
Hello World!
</BODY>
</HTML>
"""

    def pre_colourize(self, win):
        win.enablefolder = False

    def initSyntaxItems(self):
        self.addSyntaxItem('h_default',                 'Default',                              wx.stc.STC_H_DEFAULT,                   STE_STYLE_TEXT)
        self.addSyntaxItem('tag',                       'Tag',                                  wx.stc.STC_H_TAG,                       STE_STYLE_TEXT),
        self.addSyntaxItem('tagunknown',                'Tag unknown',                          wx.stc.STC_H_TAGUNKNOWN,                STE_STYLE_TEXT),
        self.addSyntaxItem('attribute',                 'Attribute',                            wx.stc.STC_H_ATTRIBUTE,                 "fore:#FF0000"),
        self.addSyntaxItem('attributeunknown',          'Attribute unknown',                    wx.stc.STC_H_ATTRIBUTEUNKNOWN,          STE_STYLE_UNDEFINED),
        self.addSyntaxItem('number',                    'Number',                               wx.stc.STC_H_NUMBER,                    STE_STYLE_NUMBER),
        self.addSyntaxItem('doublestring',              'Double string',                        wx.stc.STC_H_DOUBLESTRING,              STE_STYLE_STRING),
        self.addSyntaxItem('singlestring',              'Single string',                        wx.stc.STC_H_SINGLESTRING,              STE_STYLE_STRING),
        self.addSyntaxItem('other',                     'Other',                                wx.stc.STC_H_OTHER,                     STE_STYLE_TEXT),
        self.addSyntaxItem('comment',                   'Comment',                              wx.stc.STC_H_COMMENT,                   STE_STYLE_COMMENT),
        self.addSyntaxItem('entity',                    'Entity',                               wx.stc.STC_H_ENTITY,                    STE_STYLE_LABEL),
        self.addSyntaxItem('tagend',                    'Tag end',                              wx.stc.STC_H_TAGEND,                    STE_STYLE_TEXT),
        self.addSyntaxItem('xmlstart',                  'Xml start',                            wx.stc.STC_H_XMLSTART,                  STE_STYLE_TEXT),
        self.addSyntaxItem('xmlend',                    'Xml end',                              wx.stc.STC_H_XMLEND,                    STE_STYLE_TEXT),
        self.addSyntaxItem('script',                    'Script',                               wx.stc.STC_H_SCRIPT,                    STE_STYLE_SCRIPT),
        self.addSyntaxItem('asp',                       'Asp',                                  wx.stc.STC_H_ASP,                       STE_STYLE_TEXT),
        self.addSyntaxItem('aspat',                     'Aspat',                                wx.stc.STC_H_ASPAT,                     STE_STYLE_TEXT),
        self.addSyntaxItem('cdata',                     'CDATA',                                wx.stc.STC_H_CDATA,                     STE_STYLE_TEXT),
        self.addSyntaxItem('question',                  'Question',                             wx.stc.STC_H_QUESTION,                  STE_STYLE_TEXT),
        self.addSyntaxItem('value',                     'Value',                                wx.stc.STC_H_VALUE,                     STE_STYLE_VALUE),
        self.addSyntaxItem('xcomment',                  'X comment',                            wx.stc.STC_H_XCCOMMENT,                 STE_STYLE_COMMENT),
        self.addSyntaxItem('sgml_default',              'Sgml - default',                       wx.stc.STC_H_SGML_DEFAULT,              STE_STYLE_TEXT)
        self.addSyntaxItem('sgml_command',              'Sgml - command',                       wx.stc.STC_H_SGML_COMMAND,              STE_STYLE_COMMAND),
        self.addSyntaxItem('sgml_param',                'Sgml - param',                         wx.stc.STC_H_SGML_1ST_PARAM,            STE_STYLE_TEXT),
        self.addSyntaxItem('sgml_doublestring',         'Sgml - double string',                 wx.stc.STC_H_SGML_DOUBLESTRING,         STE_STYLE_STRING),
        self.addSyntaxItem('sgml_simplestring',         'Sgml - simple string',                 wx.stc.STC_H_SGML_SIMPLESTRING,         STE_STYLE_STRING),
        self.addSyntaxItem('sgml_error',                'Sgml - error',                         wx.stc.STC_H_SGML_ERROR,                STE_STYLE_ERROR)
        self.addSyntaxItem('sgml_special',              'Sgml - special',                       wx.stc.STC_H_SGML_SPECIAL,              STE_STYLE_TEXT),
        self.addSyntaxItem('sgml_entity',               'Sgml - entity',                        wx.stc.STC_H_SGML_ENTITY,               STE_STYLE_LABEL),
        self.addSyntaxItem('sgml_comment',              'Sgml - comment',                       wx.stc.STC_H_SGML_COMMENT,              STE_STYLE_COMMENT),
        self.addSyntaxItem('sgml_param_comment',        'Sgml - param comment',                 wx.stc.STC_H_SGML_1ST_PARAM_COMMENT,    STE_STYLE_COMMENT),
        self.addSyntaxItem('sgml_block_comment',        'Sgml - block comment',                 wx.stc.STC_H_SGML_BLOCK_DEFAULT,        STE_STYLE_TEXT),

        self.addSyntaxItem('hj_start',                  'Javascript - start',                   wx.stc.STC_HJ_START,                    STE_STYLE_TEXT),
        self.addSyntaxItem('hj_default',                'Javascript - default',                 wx.stc.STC_HJ_DEFAULT,                  STE_STYLE_TEXT),
        self.addSyntaxItem('hj_comment',                'Javascript - comment',                 wx.stc.STC_HJ_COMMENT,                  STE_STYLE_COMMENT),
        self.addSyntaxItem('hj_commentline',            'Javascript - commentline',             wx.stc.STC_HJ_COMMENTLINE,              STE_STYLE_COMMENTLINE),
        self.addSyntaxItem('hj_commentdoc',             'Javascript - commentdoc',              wx.stc.STC_HJ_COMMENTDOC,               STE_STYLE_COMMENTDOC),
        self.addSyntaxItem('hj_number',                 'Javascript - number',                  wx.stc.STC_HJ_NUMBER,                   STE_STYLE_NUMBER),
        self.addSyntaxItem('hj_word',                   'Javascript - word',                    wx.stc.STC_HJ_WORD,                     STE_STYLE_KEYWORD1),
        self.addSyntaxItem('hj_keyword',                'Javascript - keyword',                 wx.stc.STC_HJ_KEYWORD,                  STE_STYLE_KEYWORD2),
        self.addSyntaxItem('hj_doublestring',           'Javascript - doublestring',            wx.stc.STC_HJ_DOUBLESTRING,             STE_STYLE_STRING),                 
        self.addSyntaxItem('hj_singlestring',           'Javascript - singlestring',            wx.stc.STC_HJ_SINGLESTRING,             STE_STYLE_STRING),                 
        self.addSyntaxItem('hj_symbols',                'Javascript - symbols',                 wx.stc.STC_HJ_SYMBOLS,                  STE_STYLE_NUMBER),
        self.addSyntaxItem('hj_stringeol',              'Javascript - stringeol',               wx.stc.STC_HJ_STRINGEOL,                STE_STYLE_STRINGEOL),
        self.addSyntaxItem('hj_regex',                  'Javascript - regex',                   wx.stc.STC_HJ_REGEX,                    STE_STYLE_REGEX),

        self.addSyntaxItem('hja_start',                 'ASP Javascript - start',               wx.stc.STC_HJA_START,                   STE_STYLE_TEXT),
        self.addSyntaxItem('hja_default',               'ASP Javascript - default',             wx.stc.STC_HJA_DEFAULT,                 STE_STYLE_TEXT),
        self.addSyntaxItem('hja_comment',               'ASP Javascript - comment',             wx.stc.STC_HJA_COMMENT,                 STE_STYLE_COMMENT),
        self.addSyntaxItem('hja_commentline',           'ASP Javascript - commentline',         wx.stc.STC_HJA_COMMENTLINE,             STE_STYLE_COMMENTLINE),
        self.addSyntaxItem('hja_commentdoc',            'ASP Javascript - commentdoc',          wx.stc.STC_HJA_COMMENTDOC,              STE_STYLE_COMMENTDOC),
        self.addSyntaxItem('hja_number',                'ASP Javascript - number',              wx.stc.STC_HJA_NUMBER,                  STE_STYLE_NUMBER),
        self.addSyntaxItem('hja_word',                  'ASP Javascript - word',                wx.stc.STC_HJA_WORD,                    STE_STYLE_KEYWORD1),
        self.addSyntaxItem('hja_keyword',               'ASP Javascript - keyword',             wx.stc.STC_HJA_KEYWORD,                 STE_STYLE_KEYWORD2),
        self.addSyntaxItem('hja_doublestring',          'ASP Javascript - doublestring',        wx.stc.STC_HJA_DOUBLESTRING,            STE_STYLE_STRING),                 
        self.addSyntaxItem('hja_singlestring',          'ASP Javascript - singlestring',        wx.stc.STC_HJA_SINGLESTRING,            STE_STYLE_STRING),                 
        self.addSyntaxItem('hja_symbols',               'ASP Javascript - symbols',             wx.stc.STC_HJA_SYMBOLS,                 STE_STYLE_NUMBER),
        self.addSyntaxItem('hja_stringeol',             'ASP Javascript - stringeol',           wx.stc.STC_HJA_STRINGEOL,               STE_STYLE_STRINGEOL),
        self.addSyntaxItem('hja_regex',                 'ASP Javascript - regex',               wx.stc.STC_HJA_REGEX,                   STE_STYLE_REGEX),

        self.addSyntaxItem('hb_start',                  'VBScript - start',                     wx.stc.STC_HB_START,                    STE_STYLE_TEXT),
        self.addSyntaxItem('hb_default',                'VBScript - default',                   wx.stc.STC_HB_DEFAULT,                  STE_STYLE_TEXT),
        self.addSyntaxItem('hb_commentline',            'VBScript - commentline',               wx.stc.STC_HB_COMMENTLINE,              STE_STYLE_COMMENTLINE),
        self.addSyntaxItem('hb_number',                 'VBScript - number',                    wx.stc.STC_HB_NUMBER,                   STE_STYLE_NUMBER),
        self.addSyntaxItem('hb_word',                   'VBScript - word',                      wx.stc.STC_HB_WORD,                     STE_STYLE_KEYWORD1),
        self.addSyntaxItem('hb_string',                 'VBScript - string',                    wx.stc.STC_HB_STRING,                   STE_STYLE_STRING),
        self.addSyntaxItem('hb_identifier',             'VBScript - identifier',                wx.stc.STC_HB_IDENTIFIER,               STE_STYLE_IDENTIFIER),
        self.addSyntaxItem('hb_stringeol',              'VBScript - stringeol',                 wx.stc.STC_HB_STRINGEOL,                STE_STYLE_STRINGEOL),

        self.addSyntaxItem('hba_start',                 'ASP VBScript - start',                 wx.stc.STC_HBA_START,                   STE_STYLE_TEXT),
        self.addSyntaxItem('hba_default',               'ASP VBScript - default',               wx.stc.STC_HBA_DEFAULT,                 STE_STYLE_TEXT),
        self.addSyntaxItem('hba_commentline',           'ASP VBScript - commentline',           wx.stc.STC_HBA_COMMENTLINE,             STE_STYLE_COMMENTLINE),
        self.addSyntaxItem('hba_number',                'ASP VBScript - number',                wx.stc.STC_HBA_NUMBER,                  STE_STYLE_NUMBER),
        self.addSyntaxItem('hba_word',                  'ASP VBScript - word',                  wx.stc.STC_HBA_WORD,                    STE_STYLE_KEYWORD1),
        self.addSyntaxItem('hba_string',                'ASP VBScript - string',                wx.stc.STC_HBA_STRING,                  STE_STYLE_STRING),
        self.addSyntaxItem('hba_identifier',            'ASP VBScript - identifier',            wx.stc.STC_HBA_IDENTIFIER,              STE_STYLE_IDENTIFIER),
        self.addSyntaxItem('hba_stringeol',             'ASP VBScript - stringeol',             wx.stc.STC_HBA_STRINGEOL,               STE_STYLE_STRINGEOL),
                                                                                                                                        
        self.addSyntaxItem('hp_start',                  'Python - start',                       wx.stc.STC_HP_START,                    STE_STYLE_TEXT),
        self.addSyntaxItem('hp_default',                'Python - default',                     wx.stc.STC_HP_DEFAULT,                  STE_STYLE_TEXT),
        self.addSyntaxItem('hp_commentline',            'Python - commentline',                 wx.stc.STC_HP_COMMENTLINE,              STE_STYLE_COMMENTLINE),
        self.addSyntaxItem('hp_number',                 'Python - number',                      wx.stc.STC_HP_NUMBER,                   STE_STYLE_NUMBER),
        self.addSyntaxItem('hp_string',                 'Python - string',                      wx.stc.STC_HP_STRING,                   STE_STYLE_STRING),
        self.addSyntaxItem('hp_character',              'Python - character',                   wx.stc.STC_HP_CHARACTER,                STE_STYLE_NUMBER),
        self.addSyntaxItem('hp_word',                   'Python - word',                        wx.stc.STC_HP_WORD,                     STE_STYLE_KEYWORD1),
        self.addSyntaxItem('hp_triple',                 'Python - triple',                      wx.stc.STC_HP_TRIPLE,                   STE_STYLE_STRING),
        self.addSyntaxItem('hp_tripledouble',           'Python - triple double',               wx.stc.STC_HP_TRIPLEDOUBLE,             STE_STYLE_STRING),
        self.addSyntaxItem('hp_classname',              'Python - classname',                   wx.stc.STC_HP_CLASSNAME,                STE_STYLE_LABEL),
        self.addSyntaxItem('hp_defname',                'Python - defname',                     wx.stc.STC_HP_DEFNAME,                  STE_STYLE_LABEL),
        self.addSyntaxItem('hp_operator',               'Python - operator',                    wx.stc.STC_HP_OPERATOR,                 STE_STYLE_OPERATOR),
        self.addSyntaxItem('hp_identifier',             'Python - identifier',                  wx.stc.STC_HP_IDENTIFIER,               STE_STYLE_IDENTIFIER),
                                                                                                                                        
        self.addSyntaxItem('hpa_start',                 'ASP Python - start',                   wx.stc.STC_HPA_START,                   STE_STYLE_TEXT),
        self.addSyntaxItem('hpa_default',               'ASP Python - default',                 wx.stc.STC_HPA_DEFAULT,                 STE_STYLE_TEXT),
        self.addSyntaxItem('hpa_commentline',           'ASP Python - commentline',             wx.stc.STC_HPA_COMMENTLINE,             STE_STYLE_COMMENTLINE),
        self.addSyntaxItem('hpa_number',                'ASP Python - number',                  wx.stc.STC_HPA_NUMBER,                  STE_STYLE_NUMBER),
        self.addSyntaxItem('hpa_string',                'ASP Python - string',                  wx.stc.STC_HPA_STRING,                  STE_STYLE_STRING),
        self.addSyntaxItem('hpa_character',             'ASP Python - character',               wx.stc.STC_HPA_CHARACTER,               STE_STYLE_NUMBER),
        self.addSyntaxItem('hpa_word',                  'ASP Python - word',                    wx.stc.STC_HPA_WORD,                    STE_STYLE_KEYWORD1),
        self.addSyntaxItem('hpa_triple',                'ASP Python - triple',                  wx.stc.STC_HPA_TRIPLE,                  STE_STYLE_STRING),
        self.addSyntaxItem('hpa_tripledouble',          'ASP Python - triple double',           wx.stc.STC_HPA_TRIPLEDOUBLE,            STE_STYLE_STRING),
        self.addSyntaxItem('hpa_classname',             'ASP Python - classname',               wx.stc.STC_HPA_CLASSNAME,               STE_STYLE_LABEL),
        self.addSyntaxItem('hpa_defname',               'ASP Python - defname',                 wx.stc.STC_HPA_DEFNAME,                 STE_STYLE_LABEL),
        self.addSyntaxItem('hpa_operator',              'ASP Python - operator',                wx.stc.STC_HPA_OPERATOR,                STE_STYLE_OPERATOR),
        self.addSyntaxItem('hpa_identifier',            'ASP Python - identifier',              wx.stc.STC_HPA_IDENTIFIER,              STE_STYLE_IDENTIFIER),
                                                                                                                                        
        self.addSyntaxItem('hphp_default',              'PHP - default',                        wx.stc.STC_HPHP_DEFAULT,                STE_STYLE_TEXT),
        self.addSyntaxItem('hphp_hstring',              'PHP - hstring',                        wx.stc.STC_HPHP_HSTRING,                STE_STYLE_STRING),
        self.addSyntaxItem('hphp_simplestring',         'PHP - simplestring',                   wx.stc.STC_HPHP_SIMPLESTRING,           STE_STYLE_STRING),
        self.addSyntaxItem('hphp_word',                 'PHP - word',                           wx.stc.STC_HPHP_WORD,                   STE_STYLE_KEYWORD1),
        self.addSyntaxItem('hphp_number',               'PHP - number',                         wx.stc.STC_HP_NUMBER,                   STE_STYLE_NUMBER),
        self.addSyntaxItem('hphp_variable',             'PHP - variable',                       wx.stc.STC_HPHP_VARIABLE,               STE_STYLE_VALUE),
        self.addSyntaxItem('hphp_complex_variable',     'PHP - complex variable',               wx.stc.STC_HPHP_COMPLEX_VARIABLE,       STE_STYLE_VALUE),
        self.addSyntaxItem('hphp_comment',              'PHP - comment',                        wx.stc.STC_HPHP_COMMENT,                STE_STYLE_COMMENT),
        self.addSyntaxItem('hphp_commentline',          'PHP - comment line',                   wx.stc.STC_HPHP_COMMENTLINE,            STE_STYLE_COMMENTLINE),
        self.addSyntaxItem('hphp_hstring_variable',     'PHP - hstring variable',               wx.stc.STC_HPHP_HSTRING_VARIABLE,       STE_STYLE_VALUE),
        self.addSyntaxItem('hphp_operator',             'PHP - operator',                       wx.stc.STC_HPHP_OPERATOR,               STE_STYLE_OPERATOR),

from NCustomLexer import *

class XMLLexer(CustomLexer):
    metaname = 'xml'

    preview_code = """<<?xml version="1.0" encoding="ISO-8859-1"?>
<?xml-stylesheet type="text/xsl" href="HelloWorld.xsl" ?>
<!-- Hello World in XML -->
<text><string>Hello, World</string></text>
"""
    
    syl_tag = STYLE_CUSTOM + 1
    syl_attrname = STYLE_CUSTOM + 2
    syl_attrvalue = STYLE_CUSTOM + 3
    syl_cdatavalue = STYLE_CUSTOM + 4
    syl_cdatatag = STYLE_CUSTOM + 5

    def initSyntaxItems(self):
        self.addSyntaxItem('r_default',         'Default',              STYLE_DEFAULT,          STE_STYLE_TEXT)
        self.addSyntaxItem('keyword',           'Keyword',              STYLE_KEYWORD,          STE_STYLE_KEYWORD1)
        self.addSyntaxItem('tag',               'Tag',                  self.syl_tag,           'back:#E6E6FA')
        self.addSyntaxItem('attribute',         'Attribute Name',       self.syl_attrname,      'bold,fore:red')
        self.addSyntaxItem('attrvalue',         'Attribute Value',      self.syl_attrvalue,     'bold,fore:#008080')
        self.addSyntaxItem('comment',           'Comment',              STYLE_COMMENT,          STE_STYLE_COMMENT)
#        self.addSyntaxItem('cdatavalue',        'CDATA Value',          self.syl_cdatavalue,    self.STE_STYLE_TEXT)
        self.addSyntaxItem('cdatatag',          'CDATA Tag',            self.syl_cdatatag,      'fore:#FF833F')
        
        
    def loadToken(self):
        def is_tag(win, begin, end, text, matchobj):
            if text.startswith('"') and text.endswith('"'):
                return self.syl_attrvalue
            else:
                return STYLE_DEFAULT
        
        token_tag = TokenList([
            (r'([\w\-:_.]+)\s*=\s*(%s|%s|\S+)' % (PATTERN_DOUBLE_STRING, PATTERN_SINGLE_STRING),
                [(1, self.syl_attrname), (2, is_tag)]),
            (r'([\w\-:_.]+)\b(?!=)', self.syl_attrname),
        ])
            
        return TokenList([
            (r'<!--.*?-->', STYLE_COMMENT),
            (r'(<!\[CDATA\[)(.*?)(\]\]>)', 
                [(1, self.syl_cdatatag), (3, self.syl_cdatatag)]),
            (r'(<!|<\?|</?)\s*([\w\-:_.]+)\s*(.*?)\s*(\?>|/?>)', 
                [(1, self.syl_tag), (2, STYLE_KEYWORD), 
                (3, token_tag), (4, self.syl_tag)]),
        ])
        
    backstyles = [(syl_cdatatag, '<![CDATA['),
        (STYLE_COMMENT, '<!--'),
        (syl_tag, '<'),
    ]

class PythonLexer(LexerBase):

    metaname = 'python'
    no_expand_styles = (wx.stc.STC_P_COMMENTLINE,
                        wx.stc.STC_P_STRING,
#                        wx.stc.STC_P_TRIPLE,
#                        wx.stc.STC_P_TRIPLEDOUBLE,
                        wx.stc.STC_P_CHARACTER,
                        wx.stc.STC_P_COMMENTBLOCK)

    def loadDefaultKeywords(self):
        import keyword

        return (' '.join(keyword.kwlist + ['self', 'None', 'True', 'False', 'as']),)

    preview_code = """#Comment Blocks!
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
