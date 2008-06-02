#   Programmer: limodou
#   E-mail:     limodou@gmail.com
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
#   $Id: mEncoding.py 1897 2007-02-03 10:33:43Z limodou $

import wx
from modules import Mixin
from modules import common

def pref_init(pref):
    pref.select_encoding = False
#    pref.default_encoding = common.defaultencoding
#    pref.custom_encoding = ''
Mixin.setPlugin('preference', 'init', pref_init)

#encodings = [common.defaultencoding]
#if 'utf-8' not in encodings:
#    encodings.append('utf-8')
#
def add_pref(preflist):
    preflist.extend([
        (tr('General'), 120, 'check', 'select_encoding', tr('Show encoding selection dialog when opening or saving file'), None),
#        (tr('General'), 161, 'choice', 'default_encoding', tr('Default document encoding:'), encodings),
#        (tr('General'), 162, 'text', 'custom_encoding', tr("Custom default encoding(if set, it'll be the default):"), None),
    ])
Mixin.setPlugin('preference', 'add_pref', add_pref)

def _getencoding():
    ret = None
    from EncodingDialog import EncodingDialog
    dlg = EncodingDialog()
    answer = dlg.ShowModal()
    if answer == wx.ID_OK:
        ret = dlg.GetValue()
    dlg.Destroy()
    return ret

def getencoding(win, mainframe):
    ret = None
    if win.pref.select_encoding:
        ret = _getencoding()
    return ret
Mixin.setPlugin('mainframe', 'getencoding', getencoding)

def add_mainframe_menu(menulist):
    menulist.extend([ ('IDM_DOCUMENT',
        [
            (125, 'IDM_DOCUMENT_CHANGE_ENCODING', tr('Change Encoding...'), wx.ITEM_NORMAL, 'OnDocumentChangeEncoding', tr("Chanages current document's saving encoding.")),
        ]),
    ])
Mixin.setPlugin('mainframe', 'add_menu', add_mainframe_menu)

def add_editor_menu(popmenulist):
    popmenulist.extend([ (None, #parent menu id
        [
            (250, '', '-', wx.ITEM_SEPARATOR, None, ''),
            (260, 'IDPM_CHANGE_ENCODING', tr('Change Encoding...'), wx.ITEM_NORMAL, 'OnEditorDocumentChangeEncoding', tr("Chanages current document's saving encoding.")),
        ]),
    ])
Mixin.setPlugin('editor', 'add_menu', add_editor_menu)

def OnDocumentChangeEncoding(win, event):
    ret = _getencoding()
    if ret:
        win.document.locale = ret
        win.SetStatusText(win.document.locale, 4)
        win.document.modified = True
        wx.CallAfter(win.editctrl.showTitle, win.document)
        wx.CallAfter(win.editctrl.showPageTitle, win.document)
Mixin.setMixin('mainframe', 'OnDocumentChangeEncoding', OnDocumentChangeEncoding)

def OnEditorDocumentChangeEncoding(win, event):
    win.mainframe.OnDocumentChangeEncoding(None)
Mixin.setMixin('editor', 'OnEditorDocumentChangeEncoding', OnEditorDocumentChangeEncoding)
