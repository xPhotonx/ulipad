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

from mixins.NewCustomLexer import CustomLexer
import re
from modules.ZestyParser import *
import types
    
class DjangoTmpLexer(CustomLexer):

    metaname = 'djangotmp'
    casesensitive = True
#    fulltext = True

    def loadDefaultKeywords(self):
        keys = ['extends', 'block', 'include', 'comment', 'load', 'firstof', 
            'now', 'for', 'regroup', 'ifequal', 'ifnotequal', 'widthratio', 
            'templatetag', 'ifchanged', 'filter', 'ssi', 'debug', 'if', 
            'spaceless', 'cycle', 'else', 'expr', 'catch', 'call', 'pyif', 'pycall']
        end_keys = ['end' + x for x in keys]
        return keys + end_keys

    def loadPreviewCode(self):
        return """{% load i18n config %}
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html>
<head>
    <title>{% block title %}Woodlog{% endblock %}</title>
    <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
    {% block js %}{% endblock %}
    {% block css %}
    <link href="{% theme_media_path "home" "woodlog.css" %}" rel="stylesheet" type="text/css" />
    {% endblock %}
</head>
"""

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
        self.syl_tag = self.syl_custom + 1
        self.syl_attrname = self.syl_custom + 2
        self.syl_attrvalue = self.syl_custom + 3
        self.syl_variable = self.syl_custom + 4
        self.syl_symbol = self.syl_custom + 5
        self.syl_filter = self.syl_custom + 6
        self.syl_tagtext = self.syl_custom + 7
        self.syl_djangotag = self.syl_custom + 8
        self.syl_script_text = self.syl_custom + 9
        self.syl_style_text = self.syl_custom + 10
        self.addSyntaxItem('r_default',         'Default',              self.syl_default,           self.STE_STYLE_TEXT)
        self.addSyntaxItem('keyword',           'Keyword',              self.syl_keyword,           self.STE_STYLE_KEYWORD1)
        self.addSyntaxItem('tag',               'Tag',                  self.syl_tag,               'bold')
        self.addSyntaxItem('attribute',         'Attribute Name',       self.syl_attrname,          'bold,fore:red')
        self.addSyntaxItem('attrvalue',         'Attribute Value',      self.syl_attrvalue,         'bold,fore:#008080')
        self.addSyntaxItem('comment',           'Comment',              self.syl_comment,           self.STE_STYLE_COMMENT)
        self.addSyntaxItem('variable',          'Variable',             self.syl_variable,          'bold,italic,back:#FFDCFF')
        self.addSyntaxItem('symbol',            'Symbol',               self.syl_symbol,            'fore:#5c8f59,bold')
        self.addSyntaxItem('filter',            'Filter',               self.syl_filter,            'fore:#7f7047,bold')
        self.addSyntaxItem('tagtext',           'Tag Text',             self.syl_tagtext,           'back:#FFEBCD')
        self.addSyntaxItem('djangotag',         'Django Tag',           self.syl_djangotag,         'fore:#228B22,bold')
        self.addSyntaxItem('script_text',       'Script Text',          self.syl_script_text,       self.STE_STYLE_COMMENT)
        self.addSyntaxItem('style_text',        'Style Text',           self.syl_style_text,        self.STE_STYLE_COMMENT)
        
        def p_match(matchobj, style=self.syl_default, group=0):
            span = matchobj.span(group)
            return style, span[0], span[1]
        
        T_DQUOTED_STRING = Token(r'"((?:\\.|[^"])*)?"', callback=self.just_return(5))
        T_SQUOTED_STRING = Token(r"'((?:\\.|[^'])*)?'", callback=self.just_return(5))
        T_SP = Token(r'\s+', callback=self.just_return(self.syl_default))
        T_IDEN = Token(r'[_a-zA-Z][_a-zA-Z0-9:\-]*', callback=self.just_return(self.syl_default))
        
        def p(m):
            m1, m2 = list(m[0]), list(m[1])
            m1[0] = self.syl_attrname
            m2[0] = self.syl_attrvalue
            return [m1, m2]
        
        T_ATTR = (T_IDEN + Omit(Token('\s*=\s*')) + (T_DQUOTED_STRING|T_SQUOTED_STRING)) >> p
        T_COMMENT = Token(r'<!--.*?-->', callback=self.just_return(self.syl_comment))
        T_COMMENT1 = Token(r'\{#.*?#\}', callback=self.just_return(self.syl_comment))
        T_COMMENT2 = Token(r'\{%\s*comment\s*%\}.*\{%\s*endcomment\s*%\}', callback=self.just_return(self.syl_comment))
        T_TEXT = Token('[^<{]+', callback=self.just_return(self.syl_default))
        T_CDATA = Token('<!\[CDATA\[', callback=self.just_return(3)) + Token('.*?(\]\]>)', callback=self.just_return(3, 1))
        
        T_SATTR = (T_IDEN) >> self.just_return(self.syl_attrname)
#        T_SCRIPT = Token(re.compile(r'.*?(?=</script>)', re.DOTALL), callback=self.just_return(self.syl_comment))

        @CallbackFor(Token(r'((?:</|<!|<\?|<))\s*([_a-zA-Z0-9\-]+)\s*(.*?)((?:\?>|>))'))
        def T_TAGLINE(parser, m, cursor):
            yield p_match(m, self.syl_tag, 1)
            yield p_match(m, self.syl_keyword, 2)
            if m.group(3):
                begin, end = m.span(3)
                p = ZestyParser(m.group(3))
                for i in p.iter([T_ATTR, T_SATTR, T_SP]):
                    if isinstance(i, (list, types.GeneratorType)):
                        for x in i:
                            t = list(x)
                            t[1] += begin
                            t[2] += begin
                            yield t
                    else:
                        t = list(i)
                        t[1] += begin
                        t[2] += begin
                        yield t
            yield p_match(m, self.syl_tag, 4)
            if m.group(2).lower() == 'script' and m.group(1) == '<':
                text = parser.data[parser.cursor:]
                b = re.search(re.compile('</script>', re.IGNORECASE), text)
                if b:
                    pos = b.start()
                else:
                    pos = len(text)
                yield self.syl_script_text, parser.cursor, parser.cursor + pos
                
                parser.cursor += pos
            
            elif m.group(2).lower() == 'style' and m.group(1) == '<':
                text = parser.data[parser.cursor:]
                b = re.search(re.compile('</style>', re.IGNORECASE), text)
                if b:
                    pos = b.start()
                else:
                    pos = len(text)
                yield self.syl_script_text, parser.cursor, parser.cursor + pos
                
                parser.cursor += pos
            
        
        @CallbackFor(Token(r'(\{%)\s*(\w+)\s*(.*?)\s*(%\})'))
        def T_D_TAG(parser, m ,cursor):
            yield p_match(m, self.syl_symbol, 1)
            yield p_match(m, self.syl_djangotag, 2)
            yield p_match(m, self.syl_tagtext, 3)
            yield p_match(m, self.syl_symbol, 4)
            
        @CallbackFor(Token(r'(\{\{)\s*(.*?)\s*(\}\})'))
        def T_D_VAR(parser, m, cursor):
            yield p_match(m, self.syl_symbol, 1)
            yield p_match(m, self.syl_variable, 2)
            yield p_match(m, self.syl_symbol, 3)
        self.formats = [T_COMMENT, T_COMMENT1, T_COMMENT2, T_D_TAG, T_D_VAR, T_CDATA, T_TAGLINE, T_TEXT, T_SP]
        
    def initbackstyle(self):
        return [(self.syl_comment, self.syl_comment),
                (self.syl_script_text, self.syl_tag, re.compile(r'<script', re.I)),
                (self.syl_style_text, self.syl_tag, re.compile(r'<style', re.I)),
                ]
    