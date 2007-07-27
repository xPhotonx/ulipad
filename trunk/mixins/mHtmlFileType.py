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
#       $Id: mHtmlFileType.py 1457 2006-08-23 02:12:12Z limodou $

__doc__ = 'Html syntax highlitght process'

import wx
from modules import Mixin
import FiletypeBase

class HtmlFiletype(FiletypeBase.FiletypeBase):

    __mixinname__ = 'htmlfiletype'
    menulist = [ (None,
        [
            (890, 'IDM_HTML', 'Html', wx.ITEM_NORMAL, None, ''),
        ]),
    ]
    toollist = []               #your should not use supperclass's var
    toolbaritems= {}

def add_filetypes(filetypes):
    filetypes.extend([('html', HtmlFiletype)])
Mixin.setPlugin('changefiletype', 'add_filetypes', add_filetypes)

def add_html_menu(menulist):
    menulist.extend([('IDM_HTML', #parent menu id
            [
                (100, 'IDM_HTML_BROWSER', tr('View Content'), wx.ITEM_CHECK, 'OnHtmlBrowser', tr('Shows python content in Browser.')),
            ]),
    ])
Mixin.setPlugin('htmlfiletype', 'add_menu', add_html_menu)

def OnHtmlBrowser(win, event):
    if win.document.isModified() or win.document.filename == '':
        d = wx.MessageDialog(win, tr("The file has not been saved, and it would not be run.\nWould you like to save the file?"), tr("Run"), wx.YES_NO | wx.ICON_QUESTION)
        answer = d.ShowModal()
        d.Destroy()
        if (answer == wx.ID_YES):
            win.OnFileSave(event)
        else:
            return
    filename = win.document.filename
    for document in win.editctrl.list:  #if the file has been opened
        if document.isMe(filename, documenttype = 'htmlview'):
            win.editctrl.switch(document)
            document.html.DoRefresh()
            return
    else:
        win.editctrl.newPage(filename, documenttype='htmlview')
Mixin.setMixin('mainframe', 'OnHtmlBrowser', OnHtmlBrowser)

def add_panel_list(panellist):
    from HtmlPanel import HtmlPanel

    panellist['htmlview'] = HtmlPanel
Mixin.setPlugin('editctrl', 'add_panel_list', add_panel_list)

pageimagelist = {
        'htmlview': 'images/browser.gif',
}
Mixin.setMixin('editctrl', 'pageimagelist', pageimagelist)

def closefile(win, filename):
    if win.document.languagename == 'html' and win.document.documenttype == 'edit':
        for d in win.editctrl.list:
            if d.documenttype == 'htmlview' and d.filename == filename:
                index = win.editctrl.getIndex(d)
                win.editctrl.DeletePage(index)
                win.editctrl.list.pop(index)
Mixin.setPlugin('mainframe', 'closefile', closefile)
