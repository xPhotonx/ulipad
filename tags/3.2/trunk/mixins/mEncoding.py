#   Programmer: limodou
#   E-mail:     limodou@gmail.com
#
#   Copyleft 2006 limodou
#
#   Distributed under the terms of the GPL (GNU Public License)
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
#   $Id: mEncoding.py 481 2006-01-17 05:54:13Z limodou $

import wx
from modules import Mixin
from modules import i18n
from modules import Resource
import EncodingDialog
from modules import common

def pref_init(pref):
    pref.select_encoding = False
    pref.default_encoding = common.defaultencoding
    pref.custom_encoding = ''
Mixin.setPlugin('preference', 'init', pref_init)

encodings = [common.defaultencoding]
if 'utf-8' not in encodings:
    encodings.append('utf-8')

def add_pref(preflist):
    preflist.extend([
        (tr('General'), 160, 'check', 'select_encoding', tr('Show encoding selection dialog as openning or saving file.'), None),
        (tr('General'), 161, 'choice', 'default_encoding', tr('Default document encoding:'), encodings),
        (tr('General'), 162, 'text', 'custom_encoding', tr("Custom default encoding(if set, it'll be the default):"), None),
    ])
Mixin.setPlugin('preference', 'add_pref', add_pref)


def getencoding(win, mainframe):
    ret = None
    if win.pref.select_encoding:
        encoding_resfile = common.uni_work_file('resources/encodingdialog.xrc')
        filename = i18n.makefilename(encoding_resfile, mainframe.app.i18n.lang)
        dlg = Resource.loadfromresfile(filename, win, EncodingDialog.EncodingDialog, 'EncodingDialog', mainframe)
        answer = dlg.ShowModal()
        if answer == wx.ID_OK:
            ret = dlg.GetValue()
            dlg.Destroy()
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
    ret = ''
    encoding_resfile = common.uni_work_file('resources/encodingdialog.xrc')
    filename = i18n.makefilename(encoding_resfile, win.app.i18n.lang)
    dlg = Resource.loadfromresfile(filename, win, EncodingDialog.EncodingDialog, 'EncodingDialog', win)
    answer = dlg.ShowModal()
    if answer == wx.ID_OK:
        ret = dlg.GetValue()
        dlg.Destroy()
        win.document.locale = ret
        win.SetStatusText(win.document.locale, 4)
        win.document.modified = True
        win.editctrl.showTitle(win.document)
Mixin.setMixin('mainframe', 'OnDocumentChangeEncoding', OnDocumentChangeEncoding)

def OnEditorDocumentChangeEncoding(win, event):
    win.mainframe.OnDocumentChangeEncoding(None)
Mixin.setMixin('editor', 'OnEditorDocumentChangeEncoding', OnEditorDocumentChangeEncoding)
    