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
#   $Id: Print.py 1457 2006-08-23 02:12:12Z limodou $
   
import wx.html
import cgi
import re
import os

class MyPrinter(wx.html.HtmlEasyPrinting):

    def __init__(self, mainframe):
        wx.html.HtmlEasyPrinting.__init__(self)
        self.mainframe = mainframe

    def convertText(self, text):
        from modules import common
        text = plaintext2html(text, self.mainframe.pref.tabwidth)
        #htmlify the text:
        text = ("<html><body link=\"#FFFFFF\" vlink=\"#FFFFFF\" alink=\"#FFFFFF\">" 
            + '<font face="%s">' % common.faces['mono']+ text + '</font>'
            + "</body></html>")

        return text

    def Print(self, text, filename):
        self.SetHeader(filename)
        self.PrintText(self.convertText(text), os.path.dirname(filename))

re_string = re.compile(r'(?P<htmlchars>[<&>])|(?P<space>^[ \t]+)|(?P<lineend>\r\n|\r|\n)', re.S|re.M|re.I)
def plaintext2html(text, tabstop=4):
    def do_sub(m):
        c = m.groupdict()
        if c['htmlchars']:
            return cgi.escape(c['htmlchars'])
        if c['lineend']:
            return '<br>'
        elif c['space']:
            t = m.group().replace('\t', '&nbsp;'*tabstop)
            t = t.replace(' ', '&nbsp;')
            return t
        elif c['space'] == '\t':
            return ' '*tabstop;
    return re.sub(re_string, do_sub, text)
