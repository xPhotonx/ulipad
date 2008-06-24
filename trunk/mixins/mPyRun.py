#   Programmer: limodou
#   E-mail:     limodou@gmail.com
#
#   Copyleft 2008 limodou
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
#   $Id: mPyRun.py 1888 2007-02-01 14:47:13Z limodou $

import wx
import os
import sys
from modules import common
from modules import Mixin

def check_python():
    interpreters = []
    if wx.Platform == '__WXMSW__':
        from modules import winreg
        for v in ('2.3', '2.4', '2.5', '2.6', '3.0'):
            try:
                key = winreg.Key(winreg.HKLM, r'SOFTWARE\Python\Pythoncore\%s\InstallPath' % v)
                interpreters.append((v+' console', os.path.join(key.value, 'python.exe')))
                interpreters.append((v+' window', os.path.join(key.value, 'pythonw.exe')))
            except:
                pass
    else:
        version = '.'.join(map(str, sys.version_info[:2]))
        interpreters.append((version, sys.executable))
    return interpreters
        
def pref_init(pref):
    s = check_python()
    pref.python_interpreter = s
    if len(s) == 1:
        pref.default_interpreter = s[0][0]
    else:
        pref.default_interpreter = 'noexist'
    pref.python_show_args = False
    pref.python_save_before_run = False
Mixin.setPlugin('preference', 'init', pref_init)

def OnSetInterpreter(win, event):
    from InterpreterDialog import InterpreterDialog
    dlg = InterpreterDialog(win, win.pref)
    dlg.ShowModal()
Mixin.setMixin('prefdialog', 'OnSetInterpreter', OnSetInterpreter)

def add_pref(preflist):
    preflist.extend([
        ('Python', 150, 'button', 'python_interpreter', tr('Setup Python interpreter...'), 'OnSetInterpreter'),
        ('Python', 155, 'check', 'python_show_args', tr('Show arguments dialog at Python program run'), None),
        ('Python', 156, 'check', 'python_save_before_run', tr('Save modified file at Python program run'), None),
    ])
Mixin.setPlugin('preference', 'add_pref', add_pref)

def add_pyftype_menu(menulist):
    menulist.extend([('IDM_PYTHON', #parent menu id
        [
            (120, '', '-', wx.ITEM_SEPARATOR, None, ''),
            (130, 'IDM_PYTHON_RUN', tr('Run')+u'\tE=F5', wx.ITEM_NORMAL, 'OnPythonRun', tr('Run Python program.')),
            (140, 'IDM_PYTHON_SETARGS', tr('Set Arguments...'), wx.ITEM_NORMAL, 'OnPythonSetArgs', tr('Set Python program command line arugments.')),
            (150, 'IDM_PYTHON_END', tr('Stop Program'), wx.ITEM_NORMAL, 'OnPythonEnd', tr('Stop current Python program.')),
            (155, 'IDM_PYTHON_DOCTEST', tr('Run Doctests'), wx.ITEM_NORMAL, 'OnPythonDoctests', tr('Run doctests in current document.')),
        ]),
    ])
Mixin.setPlugin('pythonfiletype', 'add_menu', add_pyftype_menu)

def editor_init(win):
    win.args = ''
    win.redirect = True
Mixin.setPlugin('editor', 'init', editor_init)

def _get_python_exe(win):
    s = win.pref.python_interpreter
    interpreters = dict(s)
    interpreter = interpreters.get(win.pref.default_interpreter, '')

    #check python execute
    e = check_python()
    for x, v in e:
        flag = False
        for i, t in enumerate(s):
            name, exe = t
            if exe == v:
                flag = True
                if name != x:
                    s[i] = (x, v)
        if not flag:
            s.append((x, v))
    win.pref.save()
    
    if not interpreter:
        value = ''
        if s:
            if len(s) > 1:
                dlg = SelectInterpreter(win, s[0][0], [x for x, v in s])
                if dlg.ShowModal() == wx.ID_OK:
                    value = dlg.GetValue()
                dlg.Destroy()
            else:
                value = s[0][0]
                
        if not value:
            common.showerror(win, tr("You didn't setup python interpreter, \nplease setup it first in Preference dialog"))
        
        interpreter = dict(s).get(value, '')
        win.pref.default_interpreter = value
        win.pref.save()
        
    return interpreter

def OnPythonRun(win, event):
    interpreter = _get_python_exe(win)
    if not interpreter: return

    doc = win.editctrl.getCurDoc()
    if doc.isModified() or doc.filename == '':
        if win.pref.python_save_before_run:
            win.OnFileSave(event)
        else:
            d = wx.MessageDialog(win, tr("The file has not been saved, and it would not be run.\nWould you like to save the file?"), tr("Run"), wx.YES_NO | wx.ICON_QUESTION)
            answer = d.ShowModal()
            d.Destroy()
            if answer == wx.ID_YES:
                win.OnFileSave(event)
            else:
                return
        
    if win.pref.python_show_args:
        if not get_python_args(win):
            return
        
    args = doc.args.replace('$path', os.path.dirname(doc.filename))
    args = args.replace('$file', doc.filename)
    ext = os.path.splitext(doc.filename)[1].lower()
    command = u'"%s" -u "%s" %s' % (interpreter, doc.filename, args)
    #chanage current path to filename's dirname
    path = os.path.dirname(doc.filename)
    os.chdir(common.encode_string(path))

    win.RunCommand(command, redirect=win.document.redirect)
Mixin.setMixin('mainframe', 'OnPythonRun', OnPythonRun)

def get_python_args(win):
    from InterpreterDialog import PythonArgsDialog
    
    dlg = PythonArgsDialog(win, win.pref, tr('Set Python Arguments'),
        tr("Enter the command line arguments:\n$file will be replaced by current document filename\n$path will be replaced by current document filename's directory"),
        win.document.args, win.document.redirect)
    answer = dlg.ShowModal()
    dlg.Destroy()
    if answer == wx.ID_OK:
        win.document.args = dlg.GetValue()
        win.document.redirect = dlg.GetRedirect()
        return True
    else:
        return False
    
def OnPythonSetArgs(win, event=None):
    get_python_args(win)
Mixin.setMixin('mainframe', 'OnPythonSetArgs', OnPythonSetArgs)

def OnPythonEnd(win, event):
    win.StopCommand()
    win.SetStatusText(tr("Stopped!"), 0)
Mixin.setMixin('mainframe', 'OnPythonEnd', OnPythonEnd)

def OnPythonDoctests(win, event):
    from modules import Globals
    from modules.Debug import error
    
    def appendtext(win, text):
        win.SetReadOnly(0)
        win.SetText('')
        win.GotoPos(win.GetLength())
        if not isinstance(text, unicode):
            try:
                text = unicode(text, common.defaultencoding)
            except UnicodeDecodeError:
                def f(x):
                    if ord(x) > 127:
                        return '\\x%x' % ord(x)
                    else:
                        return x
                text = ''.join(map(f, text))
        win.AddText(text)
        win.GotoPos(win.GetLength())
        win.EmptyUndoBuffer()
        win.SetReadOnly(1)
    
    def pipe_command(cmd, callback):
        from modules import Casing
        
        def _run(cmd):
            try:
                o = os.popen(cmd)
                if callback:
                    wx.CallAfter(callback, o.read())
            except:
                error.traceback()
                
        d = Casing.Casing(_run, cmd)
        d.start_thread()
    
    def f(text):
        try:
            win.createMessageWindow()
            win.panel.showPage(tr('Messages'))
            appendtext(win.messagewindow, text)
        except:
            error.traceback()
        
    doc = win.editctrl.getCurDoc()
    if doc.isModified() or doc.filename == '':
        d = wx.MessageDialog(win, tr("The file has not been saved, and it would not be run.\nWould you like to save the file?"), tr("Run"), wx.YES_NO | wx.ICON_QUESTION)
        answer = d.ShowModal()
        d.Destroy()
        if answer == wx.ID_YES:
            win.OnFileSave(event)
        else:
            return
    
    path = os.path.normcase(os.path.join(Globals.workpath, 'packages/cmd_doctest.py'))
    filename = Globals.mainframe.editctrl.getCurDoc().filename
    interpreter = _get_python_exe(win)
    cmd = '%s %s %s' % (interpreter, path, filename)
    pipe_command(cmd, f)
Mixin.setMixin('mainframe', 'OnPythonDoctests', OnPythonDoctests)

def add_tool_list(toollist, toolbaritems):
    toollist.extend([
        (2100, 'run'),
        (2110, 'setargs'),
        (2120, 'stop'),
        (2150, '|'),
    ])

    #order, IDname, imagefile, short text, long text, func
    toolbaritems.update({
        'run':(wx.ITEM_NORMAL, 'IDM_PYTHON_RUN', 'images/run.gif', tr('Run'), tr('Run python program'), 'OnPythonRun'),
        'setargs':(wx.ITEM_NORMAL, 'IDM_PYTHON_SETARGS', 'images/setargs.gif', tr('Set Arguments'), tr('Set python program command line arugments'), 'OnPythonSetArgs'),
        'stop':(wx.ITEM_NORMAL, 'IDM_PYTHON_END', 'images/stop.gif', tr('Stop Program'), tr('Stop current python program.'), 'OnPythonEnd'),
    })
Mixin.setPlugin('pythonfiletype', 'add_tool_list', add_tool_list)

def OnPythonRunUpdateUI(win, event):
    eid = event.GetId()
    if eid in [ win.IDM_PYTHON_RUN, win.IDM_PYTHON_SETARGS ]:
        if not hasattr(win, 'messagewindow') or not win.messagewindow or not (win.messagewindow.pid > 0):
            event.Enable(True)
        else:
            event.Enable(False)
    elif eid == win.IDM_PYTHON_END:
        if hasattr(win, 'messagewindow') and win.messagewindow and (win.messagewindow.pid > 0):
            event.Enable(True)
        else:
            event.Enable(False)
Mixin.setMixin('mainframe', 'OnPythonRunUpdateUI', OnPythonRunUpdateUI)

def on_enter(mainframe, document):
    wx.EVT_UPDATE_UI(mainframe, mainframe.IDM_PYTHON_RUN, mainframe.OnPythonRunUpdateUI)
    wx.EVT_UPDATE_UI(mainframe, mainframe.IDM_PYTHON_SETARGS, mainframe.OnPythonRunUpdateUI)
    wx.EVT_UPDATE_UI(mainframe, mainframe.IDM_PYTHON_END, mainframe.OnPythonRunUpdateUI)
Mixin.setPlugin('pythonfiletype', 'on_enter', on_enter)

def on_leave(mainframe, filename, languagename):
    ret = mainframe.Disconnect(mainframe.IDM_PYTHON_RUN, -1, wx.wxEVT_UPDATE_UI)
    ret = mainframe.Disconnect(mainframe.IDM_PYTHON_SETARGS, -1, wx.wxEVT_UPDATE_UI)
Mixin.setPlugin('pythonfiletype', 'on_leave', on_leave)


################################# Dialogs
from modules import meide as ui

class SelectInterpreter(ui.SimpleDialog):
    def __init__(self, parent, value, interpreters):
        box = ui.VBox(namebinding='element')
        box.add(ui.Label(tr('Which python interpreter do you want to use?')))
        box.add(ui.ComboBox(value, choices=interpreters, style=wx.CB_READONLY), name='interpreter')
        super(SelectInterpreter, self).__init__(parent, box, title=tr('Select Python Interpreter'), fit=2)
        
        self.layout.SetFocus()

    def GetValue(self):
        return self.interpreter.GetValue()
