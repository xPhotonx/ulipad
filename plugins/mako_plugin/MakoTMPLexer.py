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

from mixins.NCustomLexer import *
import re
    
class MakoTmpLexer(CustomLexer):

    metaname = 'makotmp'
    casesensitive = True

    def loadDefaultKeywords(self):
        keys = ['include', 'def', 'namespace', 'inherit', 'call', 'doc',
            'text', 'page']
        return keys

    def loadPreviewCode(self):
        return """Hello there ${username}, how are ya.  Lets see what your account says:

${account()}

<%def name="account()">
    Account for ${username}:<br/>

    % for row in accountdata:
        Value: ${row}<br/>
    % endfor
</%def>
"""

    def initSyntaxItems(self):
        self.syl_tag = STYLE_CUSTOM + 1
        self.syl_attrname = STYLE_CUSTOM + 2
        self.syl_attrvalue = STYLE_CUSTOM + 3
        self.syl_variable = STYLE_CUSTOM + 4
        self.syl_symbol = STYLE_CUSTOM + 5
#        self.syl_filter = self.syl_custom + 6
        self.syl_tagtext = STYLE_CUSTOM + 7
        self.syl_makotag = STYLE_CUSTOM + 8
        self.syl_script_text = STYLE_CUSTOM + 9
        self.syl_style_text = STYLE_CUSTOM + 10
        self.syl_cdatatag = STYLE_CUSTOM + 11
        
        self.addSyntaxItem('r_default',         'Default',              STYLE_DEFAULT,              self.STE_STYLE_TEXT)
        self.addSyntaxItem('keyword',           'Keyword',              STYLE_KEYWORD,              self.STE_STYLE_KEYWORD1)
        self.addSyntaxItem('tag',               'Tag',                  self.syl_tag,               'bold')
        self.addSyntaxItem('attribute',         'Attribute Name',       self.syl_attrname,          'bold,fore:red')
        self.addSyntaxItem('attrvalue',         'Attribute Value',      self.syl_attrvalue,         'bold,fore:#008080')
        self.addSyntaxItem('comment',           'Comment',              STYLE_COMMENT,              self.STE_STYLE_COMMENT)
        self.addSyntaxItem('variable',          'Variable',             self.syl_variable,          'bold,italic,back:#FFDCFF')
        self.addSyntaxItem('symbol',            'Symbol',               self.syl_symbol,            'fore:#5c8f59,bold')
        self.addSyntaxItem('tagtext',           'Tag Text',             self.syl_tagtext,           'back:#FFEBCD')
        self.addSyntaxItem('makotag',           'Mako Tag',             self.syl_makotag,           'fore:#228B22,bold')
        self.addSyntaxItem('script_text',       'Script Text',          self.syl_script_text,       self.STE_STYLE_COMMENT)
        self.addSyntaxItem('style_text',        'Style Text',           self.syl_style_text,        self.STE_STYLE_COMMENT)
        self.addSyntaxItem('cdatatag',          'CDATA Tag',            self.syl_cdatatag,          'fore:#FF833F')
        
        token_tag = TokenList([
            (r'([\w\-:_.]+)\s*=\s*(%s|%s|\S+)' % (PATTERN_DOUBLE_STRING, PATTERN_SINGLE_STRING),
                    [(1, self.syl_attrname), (2, self.syl_attrvalue)]),
            (r'([\w\-:_.]+)\b(?!=)', self.syl_attrname),
        ])
            
        self.tokens = TokenList([
            (r'<!--.*?-->', STYLE_COMMENT),
            (re.compile(r'^(##.*?)$', re.M), [(1, STYLE_COMMENT)]),
            (r'(<!\[CDATA\[)(.*?)(\]\]>)', 
                [(1, self.syl_cdatatag), (3, self.syl_cdatatag)]),
            (r'(<)(script)(.*?)(>)(.*?)(</)(script)(>)', 
                [(1, self.syl_tag), (2, STYLE_KEYWORD), (3, token_tag),
                (4, self.syl_tag), (5, self.syl_script_text), (6, self.syl_tag), 
                (7, STYLE_KEYWORD), (8, self.syl_tag),
                ]),
            (r'(<)(style)(.*?)(>)(.*?)(</)(style)(>)', 
                [(1, self.syl_tag), (2, STYLE_KEYWORD), (3, token_tag),
                (4, self.syl_tag), (5, self.syl_style_text), (6, self.syl_tag), 
                (7, STYLE_KEYWORD), (8, self.syl_tag),
                ]),
            (r'(</?%!?)\s*(\w+)\s*(.*?)\s*(/?>)', 
                [(1, self.syl_symbol), (2, self.syl_makotag),
                (3, token_tag), (4, self.syl_symbol),
                ]),
            (r'(\$\{)\s*(.*?)\s*(\})',
                [(1, self.syl_symbol), (2, self.syl_variable),
                (3, self.syl_symbol),
                ]),
            (r'(<!|<\?|</?)\s*([\w\-:_.]+)\s*(.*?)\s*(\?>|/?>)', 
                [(1, self.syl_tag), (2, STYLE_KEYWORD), 
                (3, token_tag), (4, self.syl_tag)
                ]),
        ])
        
    def initbackstyle(self):
        return [(STYLE_COMMENT, '<!--'),
                (self.syl_cdatatag, '<![CDATA['),
                (self.syl_tag, '<script'),
                (self.syl_tag, '<style'),
                (self.syl_tag, '<'),
                ]
        