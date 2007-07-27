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
#       $Id$

import os
import glob
from sets import Set
import wx.stc
from modules import Mixin
from modules.Debug import error
from modules import Globals

def mainframe_init(win):
    win.input_assistant = None
Mixin.setPlugin('mainframe', 'init', mainframe_init)

def editor_init(win):
    wx.stc.EVT_STC_USERLISTSELECTION(win, win.GetId(), win.OnUserListSelection)
    win.type_list = 1
    win.inputassistant_obj = None
    win.replace_strings = None
    win.word_len = 0
    win.custom_assistant = []
Mixin.setPlugin('editor', 'init', editor_init)

def OnUserListSelection(win, event):
    t = event.GetListType()
    text = event.GetText()
    if t == win.type_list:
        start, end = win.word_len
        if end == -1:
            end = win.GetCurrentPos()
        win.BeginUndoAction()
        win.SetTargetStart(start)
        win.SetTargetEnd(end)
        win.ReplaceTarget('')
        win.GotoPos(start)
        obj = win.inputassistant_obj
        if obj.ini.autovalues.has_key(text):
            t = obj.ini.autovalues[text]
        else:
            t = text
        txt = win.mainframe.input_assistant.gettext(t)
        if win.replace_strings:
            r = win.replace_strings
            m = []
            for p in txt:
                for i in range(len(r)):
                    p = p.replace('\\' + str(i), r[i])
                m.append(p)
            txt = m
        win.mainframe.input_assistant.settext(txt)
        win.EndUndoAction()
Mixin.setMixin('editor', 'OnUserListSelection', OnUserListSelection)

def get_inputassistant_obj(win):
    if not win.mainframe.input_assistant:
        from InputAssistant import InputAssistant
    
        win.mainframe.input_assistant = i = InputAssistant()
    else:
      i = win.mainframe.input_assistant
    return i

def on_char(win, event):
    i = get_inputassistant_obj(win)
    try:
        return i.run(win, event, on_char=True)
    except:
        error.traceback()
        return False
Mixin.setPlugin('editor', 'on_char', on_char, nice=10)

def on_key_down(win, event):
    i = get_inputassistant_obj(win)
    try:
        return i.run(win, event, on_char=False)
    except:
        error.traceback()
        return False
Mixin.setPlugin('editor', 'on_key_down', on_key_down, nice=10)

def pref_init(pref):
    pref.auto_extend = True
Mixin.setPlugin('preference', 'init', pref_init)

def add_pref(preflist):
    preflist.extend([
        (tr('Document'), 260, 'check', 'auto_extend', tr('Enable auto extend'), None),
    ])
Mixin.setPlugin('preference', 'add_pref', add_pref)

def get_acp_files(win):
    i = get_inputassistant_obj(win)
    i.install_acp(win.languagename)
    
    files = []
    objs = i.get_acp(win.languagename)
    if objs:
        files = [obj.filename for obj in objs]
       
    b = glob.glob(os.path.join(Globals.workpath, '*.acp')) + glob.glob(os.path.join(Globals.confpath, '*.acp'))
    afiles = Set(b)
    afiles.difference_update(files)
    afiles = list(afiles)
    afiles.sort()
    
    sfiles = [obj.filename for obj in win.custom_assistant]
    
    elements = [
    ('static', 'applied', '\n'.join(files), tr('Deault acp files:'), None),
    ('multi', 'custom', sfiles, tr('Available acp files:'), afiles),
    ]
    from modules.EasyGuider import EasyDialog
    easy = EasyDialog.EasyDialog(win, title=tr('Acp Selector'), elements=elements)
    values = None
    if easy.ShowModal() == wx.ID_OK:
        values = easy.GetValue()
        win.custom_assistant = []
        for f in values['custom']:
            win.custom_assistant.append(i.get_assistant(f))
            
    easy.Destroy()

def add_mainframe_menu(menulist):
    menulist.extend([
        ('IDM_DOCUMENT', #parent menu id
        [
            (127, 'IDM_DOCUMENT_APPLYACP', tr('Apply Auto-complete Files'), wx.ITEM_NORMAL, 'OnDocumentApplyAcp', tr('Apply auto-complete files to current document.')),
        ]),
    ])
Mixin.setPlugin('mainframe', 'add_menu', add_mainframe_menu)

def OnDocumentApplyAcp(win, event):
    if hasattr(win, 'document') and win.document.documenttype == 'edit':
       get_acp_files(win.document)
Mixin.setMixin('mainframe', 'OnDocumentApplyAcp', OnDocumentApplyAcp)
    
def add_editor_menu(popmenulist):
    popmenulist.extend([
        (None,
        [
            (270, 'IDPM_APPLYACP', tr('Apply Auto-complete Files'), wx.ITEM_NORMAL, 'OnApplyAcp', tr('Apply auto-complete files to current document.')),
        ]),
    ])
Mixin.setPlugin('editor', 'add_menu', add_editor_menu)

def OnApplyAcp(win, event):
    win.mainframe.OnDocumentApplyAcp(event)
Mixin.setMixin('editor', 'OnApplyAcp', OnApplyAcp)
