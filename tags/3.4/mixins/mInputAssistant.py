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

import wx
import sets
import os
import glob
from modules import Mixin
from modules.Debug import error
from modules import Globals
from modules import common
from modules import dict4ini

CALLTIP_AUTOCOMPLETE = 2

def mainframe_init(win):
    win.input_assistant = None
Mixin.setPlugin('mainframe', 'init', mainframe_init)

def editor_init(win):
    win.AutoCompSetIgnoreCase(True)
    win.AutoCompStops(' .,;:()[]{}\'"\\<>%^&+-=*/|`')
    win.AutoCompSetAutoHide(True)
    win.AutoCompSetCancelAtStart(False)
    
    win.inputassistant_obj = None
    win.replace_strings = None
    win.word_len = 0
    win.custom_assistant = []
    
    win.calltip_times = 0
    win.calltip_column = 0
    win.calltip_line = 0
    win.syntax_info = None
    win.auto_routin = None
Mixin.setPlugin('editor', 'init', editor_init)

def on_user_list_selction(win, list_type, text):
    t = list_type
    if t == 1:  #1 is used by input assistant
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
Mixin.setPlugin('editor', 'on_user_list_selction', on_user_list_selction)

def get_inputassistant_obj(win):
    if not win.mainframe.input_assistant:
        from InputAssistant import InputAssistant
    
        win.mainframe.input_assistant = i = InputAssistant()
    else:
        i = win.mainframe.input_assistant
    return i

def after_char(win, event, syncvar):
    i = get_inputassistant_obj(win)
    try:
        return i.run(win, event, True, syncvar)
    except:
        error.traceback()
        return False
Mixin.setPlugin('editor', 'after_char', after_char)

def after_keydown(win, event, syncvar):
    key = event.GetKeyCode()
    if key == wx.WXK_BACK and not event.AltDown() and not event.ControlDown() and not event.ShiftDown():
        i = get_inputassistant_obj(win)
        try:
            return i.run_default(win, syncvar)
        except:
            error.traceback()
            return False
Mixin.setPlugin('editor', 'after_keydown', after_keydown)

def on_key_down(win, event):
    i = get_inputassistant_obj(win)
    try:
        return i.run(win, event, False, True)
    except:
        error.traceback()
        return False
Mixin.setPlugin('editor', 'on_key_down', on_key_down, nice=10)

def pref_init(pref):
    pref.input_assistant = True
    pref.inputass_calltip = True
    pref.inputass_autocomplete = True
    pref.inputass_identifier = True
Mixin.setPlugin('preference', 'init', pref_init)

def add_pref(preflist):
    preflist.extend([
        (tr('Input Assistant'), 100, 'check', 'input_assistant', tr('Enable input assistant'), None),
        (tr('Input Assistant'), 110, 'check', 'inputass_calltip', tr("Enable calltip"), None),
        (tr('Input Assistant'), 120, 'check', 'inputass_autocomplete', tr("Enable auto completion"), None),
        (tr('Input Assistant'), 130, 'check', 'inputass_identifier', tr("Enable auto prompt identifiers"), None),
    ])
Mixin.setPlugin('preference', 'add_pref', add_pref)

def get_acp_files(win):
    i = get_inputassistant_obj(win)
    i.install_acp(win, win.languagename)
    
    files = []
    objs = i.get_acp(win.languagename)
    if objs:
        files = [obj.filename for obj in objs]
       
    b = glob.glob(os.path.join(Globals.workpath, '*.acp')) + glob.glob(os.path.join(Globals.confpath, '*.acp'))
    afiles = sets.Set(b)
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
    
def call_lexer(win, filename, language):
    i = get_inputassistant_obj(win)
    i.install_acp(win, win.languagename)
    
    files = []
    objs = i.get_acp(win.languagename)
    if objs:
        files = [obj.filename for obj in objs]
       
    b = glob.glob(os.path.join(Globals.workpath, '*.acp')) + glob.glob(os.path.join(Globals.confpath, '*.acp'))
    afiles = sets.Set(b)
    afiles.difference_update(files)
    afiles = list(afiles)
    afiles.sort()
    
    prjfile = common.getProjectFile(filename)
    ini = dict4ini.DictIni(prjfile)
    ext = os.path.splitext(filename)[1]

    acps = ini.acp[ext]
    if acps:
        if isinstance(acps, str):
            acps = [acps]
            
        for f in acps:
            for acpf in afiles:
                if os.path.basename(acpf) == f:
                    win.custom_assistant.append(i.get_assistant(acpf))
Mixin.setPlugin('editor', 'call_lexer', call_lexer)

def add_mainframe_menu(menulist):
    menulist.extend([
        ('IDM_DOCUMENT', #parent menu id
        [
            (127, 'IDM_DOCUMENT_APPLYACP', tr('Apply Auto-complete Files'), wx.ITEM_NORMAL, 'OnDocumentApplyAcp', tr('Apply auto-complete files to current document.')),
        ]),
    ])
Mixin.setPlugin('mainframe', 'add_menu', add_mainframe_menu)

def OnDocumentApplyAcp(win, event):
    if hasattr(win, 'document') and win.document.edittype == 'edit':
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

###########################################################################

def on_kill_focus(win, event):
    if win.AutoCompActive():
        win.AutoCompCancel()
    if win.calltip and win.calltip.active:
        win.calltip.cancel()        
Mixin.setPlugin('editor', 'on_kill_focus', on_kill_focus)
    
def on_key_down(win, event):
    key = event.GetKeyCode()
    control = event.ControlDown()
    #shift=event.ShiftDown()
    alt=event.AltDown()
    if key == wx.WXK_RETURN and not control and not alt:
        if not win.AutoCompActive():
            if win.calltip.active or win.calltip_times > 0:
                win.calltip_times = 0
                win.calltip.cancel()
        else:
            event.Skip()
            return True
    elif key == wx.WXK_ESCAPE:
        win.calltip.cancel()
        win.calltip_times = 0
Mixin.setPlugin('editor', 'on_key_down', on_key_down, Mixin.HIGH, 1)

def on_key_up(win, event):
    curpos = win.GetCurrentPos()
    line = win.GetCurrentLine()
    column = win.GetColumn(curpos)
    if win.calltip.active and win.calltip_type == CALLTIP_AUTOCOMPLETE:
        if column < win.calltip_column or line != win.calltip_line:
            win.calltip_times = 0
            win.calltip.cancel()
Mixin.setPlugin('editor', 'on_key_up', on_key_up)
Mixin.setPlugin('editor', 'on_mouse_up', on_key_up)

def leaveopenfile(win, filename):
    if win.pref.input_assistant:
        i = get_inputassistant_obj(win)
        i.install_acp(win, win.languagename)
        if win.pref.inputass_identifier and win.auto_routin and not win.auto_routin.isactive():
            win.auto_routin.start_thread()
Mixin.setPlugin('editor', 'leaveopenfile', leaveopenfile)