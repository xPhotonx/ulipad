#       Programmer:     limodou
#       E-mail:         limodou@gmail.com
#
#       Copyleft 2006 limodou
#
#       Distributed under the terms of the GPL (GNU Public License)
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
#       $Id: mLexer.py 1457 2006-08-23 02:12:12Z limodou $

__doc__ = 'C syntax highlitght process'

import wx
from modules import Mixin
import LexerClass
import LexerClass1

def add_lexer(lexer):
    lexer.extend([
        (LexerClass.TextLexer.metaname, 'Text|*.txt;*.bak;*.log;*.lst;*.diz;*.nfo',
            wx.stc.STC_LEX_NULL, 'text.stx', LexerClass.TextLexer),
        (LexerClass.CLexer.metaname, tr('C/C++|*.c;*.cc;*.cpp;*.cxx;*.cs;*.h;*.hh;*.hpp;*.hxx'),
            wx.stc.STC_LEX_CPP, 'c.stx', LexerClass.CLexer),
        (LexerClass.HtmlLexer.metaname, tr('Html|*.htm;*.html;*.shtml'),
            wx.stc.STC_LEX_HTML, 'html.stx', LexerClass.HtmlLexer),
        (LexerClass.XMLLexer.metaname, tr('Xml|*.xml;*.xslt'),
            wx.stc.STC_LEX_HTML, 'xml.stx', LexerClass.XMLLexer),
        (LexerClass.PythonLexer.metaname, tr('Python|*.py;*.pyw'),
            wx.stc.STC_LEX_PYTHON, 'python.stx', LexerClass.PythonLexer),
        (LexerClass1.JavaLexer.metaname, tr('Java|*.java'),
            wx.stc.STC_LEX_CPP, 'java.stx', LexerClass1.JavaLexer),
        (LexerClass1.RubyLexer.metaname, tr('Ruby|*.rb'),
            wx.stc.STC_LEX_RUBY, 'ruby.stx', LexerClass1.RubyLexer),
        (LexerClass1.PerlLexer.metaname, tr('Perl|*.pl'),
            wx.stc.STC_LEX_PERL, 'perl.stx', LexerClass1.PerlLexer),
        (LexerClass1.CSSLexer.metaname, tr('Cascade Style Sheet|*.css'),
            wx.stc.STC_LEX_CSS, 'css.stx', LexerClass1.CSSLexer),
        (LexerClass1.JSLexer.metaname, tr('JavaScript|*.js'),
            wx.stc.STC_LEX_CPP, 'js.stx', LexerClass1.JSLexer),
        (LexerClass1.PHPLexer.metaname, tr('Php|*.php3;*.phtml;*.php'),
            wx.stc.STC_LEX_HTML, 'php.stx', LexerClass1.PHPLexer),
        (LexerClass1.ASPLexer.metaname, tr('Active Server Pages (ASP)|*.asp'),
            wx.stc.STC_LEX_HTML, 'asp.stx', LexerClass1.ASPLexer),
    ])
Mixin.setPlugin('lexerfactory', 'add_lexer', add_lexer)

def add_new_files(new_files):
    new_files.extend([
        ('Text', LexerClass.TextLexer.metaname),
        ('C/C++', LexerClass.CLexer.metaname),
        ('Html', LexerClass.HtmlLexer.metaname),
        ('Xml', LexerClass.XMLLexer.metaname),
        ('Python', LexerClass.PythonLexer.metaname),
        ('Java', LexerClass1.JavaLexer.metaname),
        ('Ruby', LexerClass1.RubyLexer.metaname),
        ('Perl', LexerClass1.PerlLexer.metaname),
        ('Cascade Style Sheet', LexerClass1.CSSLexer.metaname),
        ('JavaScript', LexerClass1.JSLexer.metaname),
        ('PHP', LexerClass1.PHPLexer.metaname),
        ('Active Server Pages (ASP)', LexerClass1.ASPLexer.metaname),
    ])
Mixin.setPlugin('mainframe', 'add_new_files', add_new_files)
