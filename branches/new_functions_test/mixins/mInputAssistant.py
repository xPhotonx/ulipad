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
    
#    win.inputassistant_obj = None
    win.replace_strings = None
    win.word_len = 0
    win.custom_assistant = []
    win.function_parameter = []
    win.syntax_info = None
    win.auto_routin = None
    win.snippet = None
    win.modified_line = None
Mixin.setPlugin('editor', 'init', editor_init)

def _replace_text(win, start, end, text):
    if end == -1:
        end = win.GetCurrentPos()
    win.BeginUndoAction()
    win.SetTargetStart(start)
    win.SetTargetEnd(end)
    win.ReplaceTarget('')
    win.GotoPos(start)
    t = text
    for obj in win.mainframe.input_assistant.get_all_acps():
        if obj.ini.autovalues.has_key(text):
            t = obj.ini.autovalues[text]
            break
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

def on_user_list_selction(win, list_type, text):
    t = list_type
    if t == 1:  #1 is used by input assistant
        start, end = win.word_len
        _replace_text(win, start, end, text)
Mixin.setPlugin('editor', 'on_user_list_selction', on_user_list_selction)

def on_auto_completion(win, pos, text):
    start, end = win.word_len
    wx.CallAfter(_replace_text, win, start, end, text)
Mixin.setPlugin('editor', 'on_auto_completion', on_auto_completion)
    
def get_inputassistant_obj(win):
    if not win.mainframe.input_assistant:
        from InputAssistant import InputAssistant
    
        win.mainframe.input_assistant = i = InputAssistant()
    else:
        i = win.mainframe.input_assistant
    return i

def after_char(win, event):
    win.mainframe.auto_routin_ac_action.put({'type':'normal', 'win':win, 
        'event':event, 'on_char_flag':True})
Mixin.setPlugin('editor', 'after_char', after_char)

def on_key_down(win, event):
    key = event.GetKeyCode()
#    if key == ord(']') and event.ControlDown() and not event.AltDown() and not event.ShiftDown():
    if key == wx.WXK_TAB and not event.ControlDown() and not event.AltDown() and not event.ShiftDown():
        if win.snippet and win.snippet.snip_mode:
            if win.AutoCompActive():
                win.AutoCompCancel()
            
            del win.function_parameter[:]
            
            win.snippet.nextField(win.GetCurrentPos())
            return True
    if key == ord('Q') and event.AltDown() and not event.ControlDown() and not event.ShiftDown():
        if win.snippet and win.snippet.snip_mode:
            win.snippet.cancel()
            return True
    if key in (ord('C'), ord('V'), ord('X')) and event.ControlDown() and not event.AltDown() and not event.ShiftDown():
        event.Skip()
        return True
    
    if key == wx.WXK_BACK and not event.AltDown() and not event.ControlDown() and not event.ShiftDown():
        if win.pref.input_assistant and win.pref.inputass_identifier:
            win.mainframe.auto_routin_ac_action.put({'type':'default', 'win':win, 'event':event})
    return False
Mixin.setPlugin('editor', 'on_key_down', on_key_down)

def on_first_keydown(win, event):
    if win.pref.input_assistant:
        win.mainframe.auto_routin_ac_action.put({'type':'normal', 'win':win, 
            'event':event, 'on_char_flag':False})
    return False
Mixin.setPlugin('editor', 'on_first_keydown', on_first_keydown, nice=1)

def pref_init(pref):
    pref.input_assistant = True
    pref.inputass_calltip = True
    pref.inputass_autocomplete = True
    pref.inputass_identifier = True
    pref.inputass_full_identifier = True
    pref.inputass_func_parameter_autocomplete = True
    pref.inputass_calltip_including_source_code = False
    pref.inputass_typing_rate = 500
Mixin.setPlugin('preference', 'init', pref_init)

def add_pref(preflist):
    preflist.extend([
        (tr('Input Assistant'), 100, 'check', 'input_assistant', tr('Enable input assistant'), None),
        (tr('Input Assistant'), 110, 'check', 'inputass_calltip', tr("Enable calltip"), None),
        (tr('Input Assistant'), 120, 'check', 'inputass_autocomplete', tr("Enable auto completion"), None),
        (tr('Input Assistant'), 130, 'check', 'inputass_identifier', tr("Enable auto prompt identifiers"), None),
        (tr('Input Assistant'), 140, 'check', 'inputass_full_identifier', tr("Enable full identifiers search"), None),
        (tr('Input Assistant'), 150, 'check', 'inputass_func_parameter_autocomplete', tr("Enable function parameter autocomplete"), None),
        (tr('Input Assistant'), 160, 'check', 'inputass_calltip_including_source_code', tr("Enable calltip content including source code"), None),
        (tr('Input Assistant'), 170, 'int',   'inputass_typing_rate', tr("skip input assistant when typing rate faster than this "), None),
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
        i.install_acp(win, win.languagename, True)
            
    easy.Destroy()
    
def call_lexer(win, oldfilename, filename, language):
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

Mixin.setPlugin('editor', 'on_kill_focus', on_kill_focus)
    
def on_key_down(win, event):
    key = event.GetKeyCode()
    control = event.ControlDown()
    #shift=event.ShiftDown()
    alt=event.AltDown()
    if key == wx.WXK_RETURN and not control and not alt:
        if  win.AutoCompActive():
            event.Skip()
            return True
        
Mixin.setPlugin('editor', 'on_key_down', on_key_down, Mixin.HIGH, 1)



def on_key_up(win, event):
    type = None
    key = ()
    if  isinstance(event, wx.KeyEvent):
        type = "key"
        
        keycode = event.GetKeyCode()
        ctrl = event.ControlDown()
        alt = event.AltDown()
        shift = event.ShiftDown()
        
        f = 0
        if ctrl:
            f |= wx.stc.STC_SCMOD_CTRL
        elif alt:
            f |= wx.stc.STC_SCMOD_ALT
        elif shift:
            f |= wx.stc.STC_SCMOD_SHIFT
        
        
        key = (f, keycode)    
    elif  isinstance(event, wx.MouseEvent):
        type = "mouse"
   
    win.mainframe.auto_routin_document_show.put({'win':win, 'key':key, 'type':type}) 
    #win.mainframe.auto_routin_document_show.put({'win':win, 'event':event}) 
Mixin.setPlugin('editor', 'on_key_up', on_key_up)
Mixin.setPlugin('editor', 'on_mouse_up', on_key_up)

def leaveopenfile(win, filename):
    if win.pref.input_assistant:
        i = get_inputassistant_obj(win)
        i.install_acp(win, win.languagename)
        win.mainframe.auto_routin_analysis.put(win)
Mixin.setPlugin('editor', 'leaveopenfile', leaveopenfile)

def on_modified(win, event):
#    if not win.dont_analysis:
    type = event.GetModificationType()
    for flag in (wx.stc.STC_MOD_INSERTTEXT, wx.stc.STC_MOD_DELETETEXT):
        if flag & type:
            modified_line = win.LineFromPosition(event.GetPosition())
            if  win.modified_line is None:
                win.modified_line = modified_line
                win.mainframe.auto_routin_analysis.put(win)
            else:
                if  win.modified_line != modified_line or event.GetLinesAdded() != 0:
                    import sys
                    print>>sys.__stdout__,modified_line
                    win.modified_line = modified_line
                    win.mainframe.auto_routin_analysis.put(win)
Mixin.setPlugin('editor', 'on_modified', on_modified)

from modules import AsyncAction

class DocumentShow(AsyncAction.AsyncAction):
    
    def do_timeout(self):
        return float(Globals.pref.inputass_typing_rate)/1000
    
    def do_action(self, obj):
        if not self.empty:
            return
        pref = Globals.pref
        win = obj['win']
        try:
            if not win: return
            i = get_inputassistant_obj(win)
            #event = obj['event']
            key = obj['key']
            type = obj['type']
            win.lock.acquire()
            i.run2(win, type, key, self)
            win.lock.release()
            return True
        except:
            win.input_assistant = None
            error.traceback()
    
  
    


KEYS = [' ','=','/','[']
class InputAssistantAction(AsyncAction.AsyncAction):
    
    
    def run1(self):
        pref = Globals.pref
        try:
            while not self.stop:
                self.last = None
                self.prev = 1000
                obj = None
                while 1:
                    try:
                        obj = self.q.get(True, self.do_timeout())
                        self.last = obj
                        if obj['on_char_flag']:
                            tt = obj['event'].time_stamp - self.prev < pref.inputass_typing_rate - pref.inputass_typing_rate/5
                            self.prev = obj['event'].time_stamp
                            key = obj['event'].GetKeyCode()
                            if chr(key) in KEYS and tt:
                                self.last = obj
                                break
                            elif chr(key) in KEYS and (not tt):
                                try:
                                    obj1 = self.q.get(True, float(pref.inputass_typing_rate*2)/1000)
                                    self.last = obj1
                                    break
                                except:
                                    #no key typing,trigger tmplater expand
                                    self.last = obj
                                    if self.last:
                                        break
                    except:
                        if self.last:
                            break

                if self.last:
                    try:
                        self.do_action(self.last)
                        self.last = None
                    except:
                        pass

        except:
            pass

 
    
    def do_action(self, obj):
        if not self.empty:
            return
        
        pref = Globals.pref
        
        action = obj['type']
        win = obj['win']
        try:
            if not win: return
            i = get_inputassistant_obj(win)
            win.lock.acquire()
            if action == 'default':
                i.run_default(win, self)
            else:
                event, on_char_flag = obj['event'], obj['on_char_flag']
                i.run(win, event, on_char_flag, self)
            win.lock.release()
            return True
        except:
            Globals.mainframe.input_assistant = None
            error.traceback()
            
    def do_timeout(self):
        return float(Globals.pref.inputass_typing_rate)/1000
        
class Analysis(AsyncAction.AsyncAction):

    def do_timeout(self):
        return 0.2

    def do_action(self, obj):
        win = Globals.mainframe
        if not self.empty:
            return
        try:
            if not obj: return
            i = get_inputassistant_obj(obj)
            i.call_analysis(self)
            return True
        except:
            win.input_assistant = None
            error.traceback()
        
def main_init(win):
    win.auto_routin_analysis = Analysis()
    win.auto_routin_analysis.start()
    win.auto_routin_ac_action = InputAssistantAction()
    win.auto_routin_ac_action.start()
    win.auto_routin_document_show = DocumentShow()
    win.auto_routin_document_show.start()
    
Mixin.setPlugin('mainframe', 'init', main_init)

