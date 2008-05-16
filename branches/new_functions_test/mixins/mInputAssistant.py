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
import time
import glob
import __builtin__
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
    win.calltip_stack = {} # collecting nested calltip's text and pos.
    win.syntax_info = None
    win.auto_routin = None
    win.snippet = None
    win.modified_line = None
    win.documented_word = ''
    win.exiting = False
    win.complete_list = []
    win.complete_obj = None
    win.document_show_obj = None

    # for autocomplete box
    win.RegisterImage(0, common.getpngimage('images/save.gif'))
    win.RegisterImage(1, common.getpngimage('images/open.gif'))
    win.RegisterImage(2, common.getpngimage('images/class1.png'))
    win.RegisterImage(3, common.getpngimage('images/method2.gif'))
    win.RegisterImage(4, common.getpngimage('images/file_py.gif'))
    win.RegisterImage(5, common.getpngimage('images/vars.gif'))
    win.RegisterImage(6, common.getpngimage('images/strtype.png'))
    win.RegisterImage(7, common.getpngimage('images/inttype.png'))
    win.RegisterImage(8, common.getpngimage('images/listtype.png'))
    win.RegisterImage(9, common.getpngimage('images/tupletype.png'))
    win.RegisterImage(10, common.getpngimage('images/dicttype.png'))
    win.RegisterImage(11, common.getpngimage('images/bfmethod1.png'))
    win.RegisterImage(12, common.getpngimage('images/rmmethod1.png'))
    win.RegisterImage(13, common.getpngimage('images/filetype.png'))
    win.RegisterImage(14, common.getpngimage('images/insttype.gif'))
    win.RegisterImage(15, common.getpngimage('images/etype.gif'))
    win.RegisterImage(16, common.getpngimage('images/booltype.gif'))
    win.RegisterImage(17, common.getpngimage('images/unitype.gif'))
    win.RegisterImage(18, common.getpngimage('images/nonetype.gif'))
    win.RegisterImage(19, common.getpngimage('images/instmethod.gif'))
    win.RegisterImage(20, common.getpngimage('images/kwtype.png'))
    win.RegisterImage(21, common.getpngimage('images/typetype.png'))
    win.RegisterImage(22, common.getpngimage('images/pyobject.png'))
    win.RegisterImage(23, common.getpngimage('images/Otypetype.png'))
    win.RegisterImage(24, common.getpngimage('images/longtype.png'))
    win.RegisterImage(25, common.getpngimage('images/floattype.png'))
    win.RegisterImage(26, common.getpngimage('images/argstype.png'))
    win.RegisterImage(27, common.getpngimage('images/pkgtype.png'))
    win.RegisterImage(28, common.getpngimage('images/builtinmodule.png'))
    win.autocomp_popwin = None
    win.autocomp_listview = None

    self = win
    self.warning = ''
    synErrIndc = 0
    self.IndicatorSetStyle(synErrIndc, wx.stc.STC_INDIC_SQUIGGLE)
    self.IndicatorSetForeground(synErrIndc, wx.RED)
##    self.IndicatorSetStyle(0, wx.stc.STC_INDIC_ROUNDBOX)
##    self.IndicatorSetForeground(0, wx.BLUE)


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
    pref.inputass_typing_rate = 400
Mixin.setPlugin('preference', 'init', pref_init)

def _get(name):
    def _f(name=name):
        return getattr(Globals.pref, name)
    return _f

from modules import meide as ui

mInputAssistant_ia = ui.Check(_get('input_assistant'), tr('Enable input assistant'))
mInputAssistant_s1 = ui.Check(_get('inputass_calltip'), tr("Enable calltip"))
mInputAssistant_s2 = ui.Check(_get('inputass_autocomplete'), tr("Enable auto completion"))
mInputAssistant_s3 = ui.Check(_get('inputass_identifier'), tr("Enable auto prompt identifiers"))
mInputAssistant_s4 = ui.Check(_get('inputass_full_identifier'), tr("Enable full identifiers search"))
mInputAssistant_s5 = ui.Check(_get('inputass_func_parameter_autocomplete'), tr("Enable function parameter autocomplete"))

def _toggle(event=None):
    ss = [mInputAssistant_s1, mInputAssistant_s2, mInputAssistant_s3, mInputAssistant_s4, mInputAssistant_s5]
    if mInputAssistant_ia.GetValue():
        for s in ss:
            s.get_widget().Enable()
    else:
        for s in ss:
            s.get_widget().Disable()

def aftercreate(dlg):
    _toggle()
Mixin.setPlugin('prefdialog', 'aftercreate', aftercreate)
    
def add_pref(preflist):
    
    mInputAssistant_ia.bind('check', _toggle)
    
    preflist.extend([
        (tr('Input Assistant'), 100, mInputAssistant_ia, 'input_assistant', '', None),
        (tr('Input Assistant'), 110, mInputAssistant_s1, 'inputass_calltip', '', None),
        (tr('Input Assistant'), 120, mInputAssistant_s2, 'inputass_autocomplete', '', None),
        (tr('Input Assistant'), 130, mInputAssistant_s3, 'inputass_identifier', '', None),
        (tr('Input Assistant'), 140, mInputAssistant_s4, 'inputass_full_identifier', '', None),
        (tr('Input Assistant'), 150, mInputAssistant_s5, 'inputass_func_parameter_autocomplete', '', None),
        (tr('Input Assistant'), 160, 'check', 'inputass_calltip_including_source_code', tr("Enable calltip content including source code"), None),
        (tr('Input Assistant'), 170, 'int', 'inputass_typing_rate', tr("Skip Input Assistant when typing rate faster than this milisecond"), None),
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
        if not win.mainframe.document_show_window.showing:
            win.AutoCompCancel()
    event.Skip()
##Mixin.setPlugin('editor', 'on_kill_focus', on_kill_focus)

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
        win.mainframe.auto_routin_check_error.put({'win':win, 'key':key})
    elif  isinstance(event, wx.MouseEvent):
        type = "mouse"

    win.mainframe.auto_routin_document_show.put({'win':win, 'key':key, 'type':type})
Mixin.setPlugin('editor', 'on_key_up', on_key_up)
Mixin.setPlugin('editor', 'on_mouse_up', on_key_up)


def on_key_up1(win, event):
    if win.pref.vim_mode:
        win.MarkerDeleteAll(win.vim_number)
        win.MarkerAdd(win.GetCurrentLine(), win.vim_number)
        
        
Mixin.setPlugin('editor', 'on_key_up', on_key_up1)
Mixin.setPlugin('editor', 'on_mouse_up', on_key_up1)
    










def leaveopenfile(win, filename):
    if win.pref.input_assistant:
        i = get_inputassistant_obj(win)
        i.install_acp(win, win.languagename)
        win.mainframe.auto_routin_analysis.put(win)
Mixin.setPlugin('editor', 'leaveopenfile', leaveopenfile)

def auto_add_bookmarker(win, modified_line):
    line_privious_marker = win.get_marker_previous(modified_line + 1, win.bookmarker_mask, False)
    line_next_marker = win.get_marker_next(modified_line,win.bookmarker_mask,  False)
    if line_privious_marker:
##        print line_privious_marker, line_next_marker, modified_line
        if line_privious_marker + 20 > modified_line  > line_privious_marker + 10:
            if line_next_marker and modified_line > line_next_marker - 20:
                return
            win.toggle_mark(modified_line, win.bookmark_number)
            win.toggle_mark(line_privious_marker - 1, win.bookmark_number)
        elif (modified_line >= line_privious_marker + 20) :
            if line_next_marker  and modified_line > line_next_marker - 20:
                return
            win.toggle_mark(modified_line, win.bookmark_number)
    else:
        if line_next_marker:
            if line_next_marker < modified_line +  20:
                return
        win.toggle_mark(modified_line, win.bookmark_number)

def on_modified(win):
    win.mainframe.auto_routin_analysis.put(win)
Mixin.setPlugin('editor', 'on_modified', on_modified)

def on_modified_text(win, event):
    type = event.GetModificationType()
    for flag in (wx.stc.STC_MOD_INSERTTEXT, wx.stc.STC_MOD_DELETETEXT):
        if flag & type:
            modified_line = win.LineFromPosition(event.GetPosition())
            if  win.modified_line is None:
                win.modified_line = modified_line
            else:
                if  win.modified_line != modified_line:# or event.GetLinesAdded() != 0:

                    auto_add_bookmarker(win, modified_line)
                    win.modified_line = modified_line
Mixin.setPlugin('editor', 'on_modified_text', on_modified_text)

from modules import AsyncAction
def on_close(win, event):
    "when app close, keep thread from running do_action"
    AsyncAction.AsyncAction.STOP = True
    win.auto_routin_analysis.join()
    win.auto_routin_ac_action.join()
Mixin.setPlugin('mainframe','on_close', on_close ,Mixin.HIGH, 1)


import types
from wx.py import introspect
import inspect

COMMONTYPES = [getattr(types, t) for t in dir(types) \
               if not t.startswith('_') \
               and t not in ('ClassType', 'InstanceType', 'ModuleType')]

DOCTYPES = ('BuiltinFunctionType', 'BuiltinMethodType', 'ClassType',
            'FunctionType', 'GeneratorType', 'InstanceType',
            'LambdaType', 'MethodType', 'ModuleType',
            'UnboundMethodType', 'method-wrapper')

SIMPLETYPES = [getattr(types, t) for t in dir(types) \
               if not t.startswith('_') and t not in DOCTYPES]

def objGetChildren(obj):
    """Return dictionary with attributes or contents of object."""
    if hasattr(obj, 'mro'):
        otype = obj
    else:
        otype = type(obj)

##        if otype is types.DictType \
##        or str(otype)[17:23] == 'BTrees' and hasattr(obj, 'keys'):
##            return obj
    if  str(otype)[17:23] == 'BTrees' and hasattr(obj, 'keys'):
        return obj
    d = {}
    if otype is types.ListType or otype is types.TupleType:
        for n in range(len(obj)):
            key = '[' + str(n) + ']'
            d[key] = obj[n]
    if otype not in COMMONTYPES:
        for key in introspect.getAttributeNames(obj):
            # Believe it or not, some attributes can disappear,
            # such as the exc_traceback attribute of the sys
            # module. So this is nested in a try block.
            try:
                d[key] = getattr(obj, key)
            except:
                pass
    else:
        for key in introspect.getAttributeNames(obj):
            # Believe it or not, some attributes can disappear,
            # such as the exc_traceback attribute of the sys
            # module. So this is nested in a try block.
            try:
                d[key] = getattr(obj, key)
            except:
                pass

    return d





def show_listitem_info(editor, name):
    obj = objGetChildren(editor.complete_obj).get(name, None)
    if obj is None:
        return
    if hasattr(obj, 'mro'):
        otype = obj
    else:
        otype = type(obj)
    obj_name = name + "\n"
    text = obj_name + ''
    text += '\n\nType: ' + str(otype)
    try:
        value = str(obj)
    except:
        value = ''
    if otype is types.StringType or otype is types.UnicodeType:
        value = repr(obj)
    text += '\n\nValue: ' + value
    if  editor.complete_obj is __builtin__:
        try:
            text += '\n\nDocstring:\n\n"""' + \
                    inspect.getdoc(obj).strip() + '"""'
        except:
            pass
    else:
        if otype not in SIMPLETYPES:
            try:
                text += '\n\nDocstring:\n\n"""' + \
                        inspect.getdoc(obj).strip() + '"""'
            except:
                pass
    if otype is types.InstanceType:
        try:
            text += '\n\nClass Definition:\n\n' + \
                    inspect.getsource(obj.__class__)
        except:
            pass
    else:
        try:
            text += '\n\nSource Code:\n\n' + \
                    inspect.getsource(obj)
        except:
            pass
    while editor.mainframe.document_show_window.showing:
        # maybe another thread was started, used document_show_window. sometime python crashed.
        time.sleep(0.5)
    editor.mainframe.document_show_window.show(text)
    editor.SetFocus()
    return True

def OnAutoCompItemSelected(win, event):
    currentItem = event.m_itemIndex
    text = win.autocomp_listview.GetItem(currentItem, 1).GetText()
    show_listitem_info(win, text)
Mixin.setMixin('editor', 'OnAutoCompItemSelected', OnAutoCompItemSelected)

def OnAutoCompDeSelected(win, event):
    item = event.GetItem()
Mixin.setMixin('editor', 'OnAutoCompDeSelected', OnAutoCompDeSelected)


class DocumentShow(AsyncAction.AsyncAction):


    def do_action(self, obj):
        if not self.empty:
            return
        pref = Globals.pref
        win = obj['win']
        if win.AutoCompActive():
            return
        try:
            if not win: return
            page = win.mainframe.panel.rightbook.GetSelection()
            if page != 0:
                return
            i = get_inputassistant_obj(win)
            #event = obj['event']
            #Mixin.reload_obj(i)
            key = obj['key']
            type = obj['type']
            win.lock.acquire()
            i.run2(win, type, key, self)
            win.lock.release()
            return True
        except:
            #win.input_assistant = None
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

    def get_timestep(self):
        return float(Globals.pref.inputass_typing_rate)/1000

class Analysis(AsyncAction.AsyncAction):
    def do_action(self, obj):
        win = Globals.mainframe
        if not self.empty:
            return
        try:
            if not obj: return
            i = get_inputassistant_obj(obj)
            i.call_analysis(self, Globals.mainframe.document)
            return True
        except:
            win.input_assistant = None
            error.traceback()


def markError(self,lineno,offset):
    if offset is None:
        offset = len(self.GetLine(lineno - 1))
    self.StartStyling(self.PositionFromLine(lineno-1), wx.stc.STC_INDICS_MASK)
    self.SetStyling(offset, wx.stc.STC_INDIC2_MASK)
    self.Colourise(0, -1)
Mixin.setMixin('editor', 'markError', markError)

def clearError(self,length):
    self.StartStyling(0, wx.stc.STC_INDICS_MASK)
    self.SetStyling(length, 0)
    self.Colourise(0, -1)
Mixin.setMixin('editor', 'clearError',clearError )


def check_source(self):
    source = self.GetText()
    length = len(source)
    source = source.replace('\r\n', '\n').replace('\r', '\n') + '\n'
    try:
        # at 2008:02:24 author ygao note:
        # PEP: 0263 http://www.python.org/dev/peps/pep-0263/
        # If a Unicode string with a coding declaration is passed to compile(),
        # a SyntaxError will be raised
        # todo: how to fix this
        tree = compile(str(source), 'c:/t', 'exec')
        warning = ''
        e = None
    except Exception, e:
        if hasattr(e,'text'):
            if type(e.text) in types.StringTypes:
                text= e.text.strip()
            else:
                text= ''
            warning = '%s: %s at line %s, col %s.'%(os.path.basename(self.filename),e.msg,e.lineno,e.offset)
        else:
            warning = repr(e)
    if  warning  != self.warning:
        if warning:
            wx.CallAfter(self.mainframe.statusbar.setHint,warning,msgType='Warning')
            if e and hasattr(e,'lineno') and not (e.lineno is None):
                def f():
                    self.clearError(length)
                    self.MarkerDeleteAll(self.error_number)
                    self.markError(e.lineno,e.offset)
                    self.MarkerAdd(e.lineno - 1 ,self.error_number)
                    if e.msg == 'unexpected indent' or e.msg == 'unindent does not match any outer indentation level' \
                        or e.msg =='expected an indented block':
                        self.SetIndentationGuides(True)
##                        self.GotoPos(self.PositionFromLine(e.lineno - 1) + self.GetLineIndentation(e.lineno -1 ))
                wx.CallAfter(f)
        else:
            wx.CallAfter(self.mainframe.statusbar.setHint,self.mainframe.statusbar.text,msgType='Info')
            if self.e and hasattr(self.e,'lineno'):
                def f():
                    self.clearError(length)
                    self.MarkerDeleteAll(self.error_number)
                    self.SetIndentationGuides(False)
                wx.CallAfter(f)
        self.warning = warning
        self.e = e
Mixin.setMixin('editor', 'check_source',check_source )


class CheckError(AsyncAction.AsyncAction):

    def get_timestep(self):
        return float(Globals.pref.inputass_typing_rate*2)/1000

    def do_action(self, obj):
        if not self.empty:
            return
        pref = Globals.pref
        win = obj['win']
        key = obj['key']
        if win.languagename != 'python':
            return
        if win.AutoCompActive() and (not win.warning):
            return
        try:
            if not win: return
            win.lock.acquire()
            win.check_source()
            win.lock.release()
            return True
        except:
            error.traceback()



def main_init(win):
    win.auto_routin_analysis = Analysis(.2)
    win.auto_routin_analysis.start()
    win.auto_routin_ac_action = InputAssistantAction(float(win.pref.inputass_typing_rate)/1000)
    win.auto_routin_ac_action.start()
    win.auto_routin_document_show = DocumentShow(.5)
    win.auto_routin_document_show.start()
    win.auto_routin_check_error = CheckError(.6)
    win.auto_routin_check_error.start()

Mixin.setPlugin('mainframe', 'init', main_init)
