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
#   $Id: mLineending.py 1805 2007-01-04 02:07:31Z limodou $

import wx
from modules import Mixin
import re

eolmess = [tr(r"Unix Mode ('\n')"), tr(r"DOS/Windows Mode ('\r\n')"), tr(r"Mac Mode ('\r')")]

def beforeinit(win):
    win.lineendingsaremixed = False
    win.eolmode = win.pref.default_eol_mode
    win.eols = {0:wx.stc.STC_EOL_LF, 1:wx.stc.STC_EOL_CRLF, 2:wx.stc.STC_EOL_CR}
    win.eolstr = {0:'Unix', 1:'Win', 2:'Mac'}
    win.eolstring = {0:'\n', 1:'\r\n', 2:'\r'}
    win.eolmess = eolmess
    win.SetEOLMode(win.eols[win.eolmode])
Mixin.setPlugin('editor', 'init', beforeinit)

def add_pref(preflist):
    preflist.extend([
        (tr('Document'), 190, 'choice', 'default_eol_mode', tr('Default line ending used in document:'), eolmess)
    ])
Mixin.setPlugin('preference', 'add_pref', add_pref)

def pref_init(pref):
    if wx.Platform == '__WXMSW__':
        pref.default_eol_mode = 1
    else:
        pref.default_eol_mode = 0
Mixin.setPlugin('preference', 'init', pref_init)

def add_mainframe_menu(menulist):
    menulist.extend([ ('IDM_DOCUMENT',
        [
            (120, 'IDM_DOCUMENT_EOL_CONVERT', tr('Convert Line Ending'), wx.ITEM_NORMAL, None, ''),
        ]),
        ('IDM_DOCUMENT_EOL_CONVERT',
        [
            (100, 'IDM_DOCUMENT_EOL_CONVERT_PC', tr('Convert to Windows Format'), wx.ITEM_NORMAL, 'OnDocumentEolConvertWin', tr('Convert line ending to windows format')),
            (200, 'IDM_DOCUMENT_EOL_CONVERT_UNIX', tr('Convert to Unix Format'), wx.ITEM_NORMAL, 'OnDocumentEolConvertUnix', tr('Convert line ending to unix format')),
            (300, 'IDM_DOCUMENT_EOL_CONVERT_MAX', tr('Convert to Mac Format'), wx.ITEM_NORMAL, 'OnDocumentEolConvertMac', tr('Convert line ending to mac format')),
        ]),
    ])
Mixin.setPlugin('mainframe', 'add_menu', add_mainframe_menu)

def setEOLMode(win, mode):
    win.lineendingsaremixed = False
    win.eolmode = mode
    state = win.save_state()
    win.BeginUndoAction()
    text = win.GetText()
    text = re.sub(r'\r\n|\r|\n', win.eolstring[mode], text)
    win.SetText(text)
#    win.ConvertEOLs(win.eols[mode])
    win.EndUndoAction()
    win.restore_state(state)
    win.SetEOLMode(win.eols[mode])
    win.mainframe.SetStatusText(win.eolstr[mode], 3)

def OnDocumentEolConvertWin(win, event):
    setEOLMode(win.document, 1)
Mixin.setMixin('mainframe', 'OnDocumentEolConvertWin', OnDocumentEolConvertWin)

def OnDocumentEolConvertUnix(win, event):
    setEOLMode(win.document, 0)
Mixin.setMixin('mainframe', 'OnDocumentEolConvertUnix', OnDocumentEolConvertUnix)

def OnDocumentEolConvertMac(win, event):
    setEOLMode(win.document, 2)
Mixin.setMixin('mainframe', 'OnDocumentEolConvertMac', OnDocumentEolConvertMac)

def fileopentext(win, stext):
    text = stext[0]

    win.lineendingsaremixed = False

    eollist = "".join(map(getEndOfLineCharacter, text))

    len_win = eollist.count('\r\n')
    len_unix = eollist.count('\n')
    len_mac = eollist.count('\r')
    if len_mac > 0 and len_unix == 0:
        win.eolmode = 2
    elif len_win == len_unix:
        win.eolmode = 1
    elif len_unix > 0 and len_win == 0 and len_mac == 0:
        win.eolmode = 0
    else:
        win.lineendingsaremixed = True
Mixin.setPlugin('editor', 'openfiletext', fileopentext)

def afteropenfile(win, filename):
    if win.lineendingsaremixed:
        eolmodestr = "MIX"
        d = wx.MessageDialog(win,
            tr('%s is currently Mixed.\nWould you like to change it to the default?\nThe Default is: %s')
            % (win.filename, win.eolmess[win.pref.default_eol_mode]),
            tr("Mixed Line Ending"), wx.YES_NO | wx.ICON_QUESTION)
        if d.ShowModal() == wx.ID_YES:
            setEOLMode(win, win.pref.default_eol_mode)
#            win.savefile(win.filename, win.locale)
    if win.lineendingsaremixed == False:
        eolmodestr = win.eolstr[win.eolmode]
    win.mainframe.SetStatusText(eolmodestr, 3)
    win.SetEOLMode(win.eolmode)
Mixin.setPlugin('editor', 'afteropenfile', afteropenfile)

#def savefile(win, filename):
#    if not win.lineendingsaremixed:
#        setEOLMode(win, win.eolmode)
#Mixin.setPlugin('editor', 'savefile', savefile)

def on_document_enter(win, document):
    if document.edittype == 'edit':
        if document.lineendingsaremixed:
            eolmodestr = "MIX"
        else:
            eolmodestr = document.eolstr[document.eolmode]
        win.mainframe.SetStatusText(eolmodestr, 3)
Mixin.setPlugin('editctrl', 'on_document_enter', on_document_enter)

def getEndOfLineCharacter(character):
    if character == '\r' or character == '\n':
        return character
    return ""
