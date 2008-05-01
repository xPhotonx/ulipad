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
#   $Id$

import wx
import re
from modules import Mixin

def add_editor_menu(popmenulist):
    popmenulist.extend([ (None, #parent menu id
        [
            (5, 'IDPM_COPY_RUN', tr('&Run in Shell') + '\tCtrl+F5', wx.ITEM_NORMAL, 'OnEditorCopyRun', ''),
        ]),
    ])
Mixin.setPlugin('editor', 'add_menu', add_editor_menu)

def editor_init(win):
    wx.EVT_UPDATE_UI(win, win.IDPM_COPY_RUN, win.OnUpdateUI)
Mixin.setPlugin('editor', 'init', editor_init)

def editor_updateui(win, event):
    eid = event.GetId()
    if eid == win.IDPM_COPY_RUN:
        event.Enable(bool(win.hasSelection()))
Mixin.setPlugin('editor', 'on_update_ui', editor_updateui)

def OnEditorCopyRun(win, event):
    _copy_and_run(win)
Mixin.setMixin('editor', 'OnEditorCopyRun', OnEditorCopyRun)


re_space = re.compile(r'^\s+')
def lstrip_multitext(text):
    lines = text.splitlines()
    m = 999999
    for line in lines:
        b = re_space.search(line)
        if b:
            m = min(len(b.group()), m)
        else:
            m = 0
            break
    return '\n'.join([x[m:] for x in lines])

def _copy_and_run(doc):
    from modules import Globals

    win = Globals.mainframe
    text = doc.GetSelectedText()
    if text:
        win.createShellWindow()
        win.panel.showPage(tr('Shell'))
        shellwin = win.panel.getPage(tr('Shell'))
        shellwin.Execute(lstrip_multitext(text))

def OnEditCopyRun(win, event):
    _copy_and_run(win.editctrl.getCurDoc())
Mixin.setMixin('mainframe', 'OnEditCopyRun', OnEditCopyRun)

def add_mainframe_menu(menulist):
    menulist.extend([
        ('IDM_EDIT',
        [
            (285, 'IDM_EDIT_COPY_RUN', tr('&Run in Shell') + '\tCtrl+F5', wx.ITEM_NORMAL, 'OnEditCopyRun', tr('Copy code to shell window and run it.')),
        ]),
    ])
Mixin.setPlugin('mainframe', 'add_menu', add_mainframe_menu)

def on_mainframe_updateui(win, event):
    eid = event.GetId()
    if eid == win.IDM_EDIT_COPY_RUN:
        doc = win.editctrl.getCurDoc()
        event.Enable(bool(doc.hasSelection()))
Mixin.setPlugin('mainframe', 'on_update_ui', on_mainframe_updateui)

def afterinit(win):
    wx.EVT_UPDATE_UI(win, win.IDM_EDIT_COPY_RUN, win.OnUpdateUI)
Mixin.setPlugin('mainframe', 'afterinit', afterinit)

def OnClose(win, event):
    shellwin = win.panel.getPage(tr('Shell'))
    if shellwin:
        shellwin.OnClose(event)
Mixin.setPlugin('mainframe', 'on_close', OnClose)

def is_compound_part(textline):
    if textline=="":
        return False
    finded = textline.find(":")
    if finded!=-1:
        textline = textline[0:finded]
    else:
        return False
    if textline.find("else")==0:
        return True
    elif textline.find("except")==0:
        return True
    elif textline.find("elif")==0:
        return True
    elif textline.find("finally")==0:
        return True
    else:
        return False

def get_left_whitespace(textline):
    """get  whitespace from  one line and fixs it with os.linesep"""
    if not ("\r\n" in textline or "\n" in textline or "\r" in textline):
        textline +=os.linesep
    left_whitespace_count=len(textline)-len(textline.lstrip())    
    if  left_whitespace_count==0:
        #not contain any whitespace like "123\n" and 
        return ""
    elif textline.lstrip()=="":
        #line "   \n"  "\n"
        if ("\n" in textline or "\r" in textline) and len(textline)==1:
            return ""
        elif "\r\n" in textline and len(textline)==2:
            return ""
        elif "\r\n" in textline:
            return textline[0:-2]
        elif "\n" in textline or "\r" in textline:            
            return textline[0:-1]
    elif left_whitespace_count!=0:
        #if contain  whitespace return it.
        return textline[0:left_whitespace_count]


space_re = re.compile('^\s*$')#match any empty line
def session_run_one(win,command):
    shell = win.mainframe.shellwindow
    if shell.more==True:
        left_whitespace = get_left_whitespace(command)
        match = space_re.match(command)
        if match != None:
            win.emptyLineCount = win.emptyLineCount + 1
        if  win.emptyLineCount >= 1:
            shell.write('\n')#Insert line break.
            shell.more = True
            shell.prompt()
            win.emptyLineCount = 0
            return
        if is_compound_part(command):
            shell.run(command, prompt=False, verbose=True)
            return
        else:
            if left_whitespace=="":
##                shell.run(win.eol_mode, prompt=False, verbose=True)
                shell.run('\n', prompt=False, verbose=True)
    shell.run(command, prompt=False, verbose=True)
Mixin.setMixin('editor', 'session_run_one', session_run_one)



def on_key_down(win, event):
    key = event.GetKeyCode()
    if key == ord('6') and event.ControlDown() and not event.AltDown() and not event.ShiftDown():
        cmd =  win.GetCurLine()[0]
        shell = win.mainframe.shellwindow
        win.session_run_one(cmd)
        win.GotoLine(win.GetCurrentLine()+1)
        shell.EnsureCaretVisible()
        shell.ScrollToColumn(0)
        win.EnsureCaretVisible()
        win.ScrollToColumn(0)
        return True
Mixin.setPlugin('editor', 'on_key_down', on_key_down, nice=100)

def editor_init(win):
    win.emptyLineCount = 0
Mixin.setPlugin('editor', 'init', editor_init)

