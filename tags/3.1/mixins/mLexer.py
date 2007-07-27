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
#	$Id: mLexer.py 176 2005-11-22 02:46:37Z limodou $

__doc__ = 'C syntax highlitght process'

from modules import Mixin
import wx
import wx.stc
import LexerClass
import LexerClass1

lexer = [(LexerClass.CLexer.metaname, tr('C/C++|*.c;*.cc;*.cpp;*.cxx;*.cs;*.h;*.hh;*.hpp;*.hxx'), wx.stc.STC_LEX_CPP, 'c.stx', LexerClass.CLexer)]
Mixin.setMixin('lexerfactory', 'lexers', lexer)
filenewtypes = [('C/C++', LexerClass.CLexer.metaname)]
Mixin.setMixin('mainframe', 'filenewtypes', filenewtypes)

lexer = [(LexerClass.TextLexer.metaname, 'Text|*.txt;*.bak;*.log;*.lst;*.diz;*.nfo', wx.stc.STC_LEX_NULL, 'text.stx', LexerClass.TextLexer)]
Mixin.setMixin('lexerfactory', 'lexers', lexer)
filenewtypes = [('Text', LexerClass.TextLexer.metaname)]
Mixin.setMixin('mainframe', 'filenewtypes', filenewtypes)

lexer = [(LexerClass.HtmlLexer.metaname, tr('Html|*.htm;*.html;*.shtml;*.xml;*.xslt'), wx.stc.STC_LEX_HTML, 'html.stx', LexerClass.HtmlLexer)]
Mixin.setMixin('lexerfactory', 'lexers', lexer)
filenewtypes = [('Html', LexerClass.HtmlLexer.metaname)]
Mixin.setMixin('mainframe', 'filenewtypes', filenewtypes)

lexer = [(LexerClass.PythonLexer.metaname, tr('Python|*.py;*.pyw'), wx.stc.STC_LEX_PYTHON, 'python.stx', LexerClass.PythonLexer)]
Mixin.setMixin('lexerfactory', 'lexers', lexer)
filenewtypes = [('Python', LexerClass.PythonLexer.metaname)]
Mixin.setMixin('mainframe', 'filenewtypes', filenewtypes)

lexer = [(LexerClass1.JavaLexer.metaname, tr('Java|*.java'), wx.stc.STC_LEX_CPP, 'java.stx', LexerClass1.JavaLexer)]
Mixin.setMixin('lexerfactory', 'lexers', lexer)
filenewtypes = [('Java', LexerClass1.JavaLexer.metaname)]
Mixin.setMixin('mainframe', 'filenewtypes', filenewtypes)

lexer = [(LexerClass1.RubyLexer.metaname, tr('Ruby|*.rb'), wx.stc.STC_LEX_RUBY, 'ruby.stx', LexerClass1.RubyLexer)]
Mixin.setMixin('lexerfactory', 'lexers', lexer)
filenewtypes = [('Ruby', LexerClass1.RubyLexer.metaname)]
Mixin.setMixin('mainframe', 'filenewtypes', filenewtypes)

lexer = [(LexerClass1.PerlLexer.metaname, tr('Perl|*.pl'), wx.stc.STC_LEX_PERL, 'perl.stx', LexerClass1.PerlLexer)]
Mixin.setMixin('lexerfactory', 'lexers', lexer)
filenewtypes = [('Perl', LexerClass1.PerlLexer.metaname)]
Mixin.setMixin('mainframe', 'filenewtypes', filenewtypes)

lexer = [(LexerClass1.CSSLexer.metaname, tr('Cascade Style Sheet|*.css'), wx.stc.STC_LEX_CSS, 'css.stx', LexerClass1.CSSLexer)]
Mixin.setMixin('lexerfactory', 'lexers', lexer)
filenewtypes = [('CSS', LexerClass1.CSSLexer.metaname)]
Mixin.setMixin('mainframe', 'filenewtypes', filenewtypes)

lexer = [(LexerClass1.JSLexer.metaname, tr('JavaScript|*.js'), wx.stc.STC_LEX_CPP, 'js.stx', LexerClass1.JSLexer)]
Mixin.setMixin('lexerfactory', 'lexers', lexer)
filenewtypes = [('JavaScript', LexerClass1.JSLexer.metaname)]
Mixin.setMixin('mainframe', 'filenewtypes', filenewtypes)
