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
from modules import Mixin
import FiletypeBase
from modules import Globals

class RestFiletype(FiletypeBase.FiletypeBase):

    __mixinname__ = 'restfiletype'
    menulist = [ (None,
        [
            (890, 'IDM_REST', 'ReST', wx.ITEM_NORMAL, None, ''),
        ]),
    ]
    toollist = []               #your should not use supperclass's var
    toolbaritems= {}

def add_filetypes(filetypes):
    filetypes.extend([('rst', RestFiletype)])
Mixin.setPlugin('changefiletype', 'add_filetypes', add_filetypes)

def add_rest_menu(menulist):
    menulist.extend([('IDM_REST', #parent menu id
            [
                (100, 'IDM_REST_VIEW_IN_LEFT', tr('View Html in Left Side'), wx.ITEM_NORMAL, 'OnRestViewHtmlInLeft', tr('Views html in left side.')),
                (110, 'IDM_REST_VIEW_IN_BOTTOM', tr('View Html in Bottom Side'), wx.ITEM_NORMAL, 'OnRestViewHtmlInBottom', tr('Views html in bottom side.')),
            ]),
    ])
Mixin.setPlugin('restfiletype', 'add_menu', add_rest_menu)

def OnRestViewHtmlInLeft(win, event):
    dispname = win.createRestHtmlViewWindow('left', Globals.mainframe.document)
    if dispname:
        win.panel.showPage(dispname)
Mixin.setMixin('mainframe', 'OnRestViewHtmlInLeft', OnRestViewHtmlInLeft)

def OnRestViewHtmlInBottom(win, event):
    dispname = win.createRestHtmlViewWindow('bottom', Globals.mainframe.document)
    if dispname:
        win.panel.showPage(dispname)
Mixin.setMixin('mainframe', 'OnRestViewHtmlInBottom', OnRestViewHtmlInBottom)

def closefile(win, document, filename):
    for pname, v in Globals.mainframe.panel.getPages().items():
        page = v[2]
        if hasattr(page, 'resthtmlview') and page.document is document:
            Globals.mainframe.panel.closePage(pname)
Mixin.setPlugin('mainframe', 'closefile', closefile)

def setfilename(document, filename):
    for pname, v in Globals.mainframe.panel.getPages().items():
        page = v[2]
        if hasattr(page, 'resthtmlview') and page.document is document:
            title = document.getShortFilename()
            Globals.mainframe.panel.setName(page, title)
Mixin.setPlugin('editor', 'setfilename', setfilename)

def createRestHtmlViewWindow(win, side, document):
    dispname = document.getShortFilename()
    if not win.panel.getPage(dispname):
        if hasattr(win.document, 'GetDocPointer'):
            from mixins import HtmlPage
            
            text = html_fragment(document.GetText().encode('utf-8'))
            page = HtmlPage.HtmlImpactView(win.panel.createNotebook(side), text)
            page.document = win.document    #save document object
            page.resthtmlview = True
            win.panel.addPage(side, page, dispname)
            return dispname
    else:
        return dispname
Mixin.setMixin('mainframe', 'createRestHtmlViewWindow', createRestHtmlViewWindow)


def html_fragment(content):
    from docutils.core import publish_string

    return publish_string(content, writer_name = 'html' )
