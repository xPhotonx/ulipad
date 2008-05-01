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
import re
import wx
from modules import Mixin
from modules import Globals
import Commands


def add_mainframe_menu(menulist):
    menulist.extend([ ('IDM_TOOL', #parent menu id
        [
            (137, 'IDM_TOOL_SEARCHCMDS', tr('Commands Searching'), wx.ITEM_NORMAL, '', ''),
        ]),
        ('IDM_TOOL_SEARCHCMDS',
        [
            (100, 'IDM_TOOL_SEARCHCMDS_SEARCH', tr('Searching...') +'\tCtrl+K', wx.ITEM_NORMAL, 'OnToolSearchCMDS', tr('Searchs commands.')),
            (110, 'IDM_TOOL_SEARCHCMDS_IMPACT_MODE', tr('Switch Impact Mode') +'\tCtrl+Shift+K', wx.ITEM_CHECK, 'OnToolSearchCMDSImpactMode', tr('Switches commands searching impact mode.')),
        ]),
    ])
Mixin.setPlugin('mainframe', 'add_menu', add_mainframe_menu)

def mainframe_init(win):
    win.command_mode = False
Mixin.setPlugin('mainframe', 'init', mainframe_init)

def pref_init(pref):
    pref.vim_mode = False
Mixin.setPlugin('preference', 'init', pref_init)


def editor_init(self):
    self.on_focus = False
    self.cmd_buf = []
    
##    'sH':[self.WordPartRightExtend, 'Move to the next change in capitalisation extending selectionto new caret position.', False], 
##    'sL':[self.WordPartRightExtend, 'Move to the next change in capitalisation extending selectionto new caret position.', False], 
    
    
     
Mixin.setPlugin('editor', 'init', editor_init)

def on_set_focus(win, event):
    win.on_focus = True
Mixin.setPlugin('editor', 'on_set_focus', on_set_focus)

def on_kill_focus(win, event):
    return Globals.mainframe.command_mode is True
Mixin.setPlugin('editor', 'on_kill_focus', on_kill_focus)

def afterinit(win):
    wx.EVT_UPDATE_UI(win, win.IDM_TOOL_SEARCHCMDS_IMPACT_MODE, win.OnUpdateUI)
Mixin.setPlugin('mainframe', 'afterinit', afterinit)

def on_mainframe_updateui(win, event):
    eid = event.GetId()
    if hasattr(win, 'document') and win.document:
        if eid == win.IDM_TOOL_SEARCHCMDS_IMPACT_MODE:
            event.Check(win.pref.commands_impact)
Mixin.setPlugin('mainframe', 'on_update_ui', on_mainframe_updateui)

def showinfo(text):
    win = Globals.mainframe.statusbar
    win.show_panel('Command: '+text, color='#AAFFAA', font=wx.Font(10, wx.TELETYPE, wx.NORMAL, wx.BOLD, True))
    
def OnToolSearchCMDS(win, event):
    if not win.pref.commands_impact:
        from mixins import SearchWin
        s = SearchWin.SearchWin(win, tr("Search Commands"))
        s.Show()
    else:
        win.pref.vim_mode = True
        showinfo('')
Mixin.setMixin('mainframe', 'OnToolSearchCMDS', OnToolSearchCMDS)

def OnToolSearchCMDSImpactMode(win, event):
    win.pref.commands_impact = not win.pref.commands_impact
    win.pref.save()
Mixin.setMixin('mainframe', 'OnToolSearchCMDSImpactMode', OnToolSearchCMDSImpactMode)
    
def pref_init(pref):
    pref.commands_impact = False
    pref.commands_autoclose = True
Mixin.setPlugin('preference', 'init', pref_init)

def add_pref(preflist):
    preflist.extend([
        (tr('Commands'), 100, 'check', 'commands_impact', tr('Enable commands search impact mode'), None),
        (tr('Commands'), 110, 'check', 'commands_autoclose', tr('Auto close commands search window after executing a command'), None),
    ])
Mixin.setPlugin('preference', 'add_pref', add_pref)

def on_first_char(win, event):
    self = win
    self.vim_cmd = {
        # des,repeat 
    'h':[self.CharLeft, 'Move caret left one character', False], 
    'j':[self.LineDown, 'Cursor down', False], 
    'k':[self.LineUp, 'Cursor up', False], 
    'l':[self.CharRight, 'Cursor right', False], 
    ' ':[self.toggle_block, 'open or close folder', False], 
    'b':[self.WordLeft, 'Move caret left one word', False], 
    'B':[self.WordPartLeft, 'Move to the previous change in capitalisation', False], 
    'w':[self.WordRight, 'Move caret right one word.', False], 
    'W':[self.WordPartRight, 'Move to the previous change in capitalisation.', False], 
    'ma':[self.toggle_mark, 'toggle bookmark', False], 
    'mp':[self.GotoBookmarPrevious, 'search  the previous bookmarker in document', False], 
    'mn':[self.GotoBookmarkNext, 'search  the next bookmarker in document', True], 
    'mc':[self.OnPythonEPyDoc, 'using live template to create EPy formate comment', False], 
    'u':[self.Undo, 'Undo', False], 
    '$':[self.LineEnd, 'Move to end of line', False], 
    '^':[self.VCHome, 'Move caret to before first visible character on line. If already there move to first character on line', False], 
    'x':[self.Cut, 'Cut', False], 
    'X':[self.Cut, 'Cut', False], 
    'y':[self.Copy, 'Copy', False], 
    'p':[self.Paste, 'Paste', False], 
    'r':[None, 'Replace the character under the cursor with {char}', False], 
    
    'dd':[self.LineDelete, 'Delete the line containing the caret', False], 
    'dw':[self.DelWordRight, 'Delete the word to the right of the caret', False], 
    'd$':[self.DelLineRight, 'Delete forwards from the current position to the end of the line.', False], 
    'd^':[self.DelLineLeft, 'Delete back from the current position to the start of the line.', False], 
    'db':[self.DelWordLeft, 'Delete the word to the left of the caret.', False], 
    
    's$':[self.LineEndExtend, 'Move caret to last position on line extending selection to new caret position.', False], 
    's^':[self.VCHomeExtend, 'Move caret to before first visible character on line,extending selection to new caret position.', False], 
    'sb':[self.WordLeftExtend, 'Move caret left one word extending selection to new caret position.', False], 
    'sB':[self.WordPartLeftExtend, 'Move to the previous change in capitalisation extending selection to new caret position.', False], 
    'se':[self.SelectionWord, 'Select Word and if Word is selected,the selection will include dot.', False], 
    'sw':[self.WordRightExtend, 'Move caret right one word extending selection to new caret position.', False], 
    'sW':[self.WordPartRightExtend, 'Move to the next change in capitalisation extending selectionto new caret position.', False], 
    'ss':[self.SelectionLine, 'selec one or more line.', False], 
    'sm':[self.SelectionMatch, 'selection to match " or { < ( { etc.', False], 
    }
    if win.pref.vim_mode:
        key = event.GetKeyCode()
        if key < 127:
            win.cmd_buf.append(chr(key))
            cmd = ''.join(win.cmd_buf)
            showinfo(cmd)
            win.vim_routin()
        return True
Mixin.setPlugin('editor', 'on_first_char', on_first_char)

def vim_routin(win):
    if win.pref.vim_mode:
        cmd = ''.join(win.cmd_buf)
        re_single_key_cmd = re.compile(r'(?P<count>\d*)\s*(?P<command>[a-zA-Z\$^]{0,1})$')
        m_single_cmd = re_single_key_cmd.match(cmd)
        re_two_key_cmd = re.compile(r'(?P<count>\d*)\s*(?P<command>[a-zA-Z\$^]{2})$')
        m_two_cmd = re_two_key_cmd.match(cmd)
        
        cpos = win.GetCurrentPos()
        cline = win.GetCurrentLine()
        if m_single_cmd:
            try:
                repeat =  int(m_single_cmd.group('count'))
            except :
                repeat = 1
            single_key = m_single_cmd.group('command')
            single_key_info = win.vim_cmd.get(single_key, None)
            if single_key_info:
                command = single_key_info[0] # get function.
                arg = ()
                for times  in range(repeat):
                    command(*arg)
                showinfo(' '.join([str(repeat)] + [single_key] + ['('+single_key_info[1]+')']))
                win.cmd_buf = []
            else:
                showinfo(' '.join([str(repeat)] + [single_key] + ['(unkonw command)']))
                return True
        if m_two_cmd:
            try:
                repeat =  int(m_two_cmd.group('count'))
            except :
                repeat = 1
            two_key = m_two_cmd.group('command')
            two_key_info = win.vim_cmd.get(two_key, None)
            if two_key_info:
                command = two_key_info[0] # get function.
                arg = ()
                if two_key == 'ma':
                    arg = (cline, win.bookmark_number)
                elif two_key == 'mp':
                    arg = (cline, )
                elif two_key == 'mn':
                    arg = (cline, )
             
                for times  in range(repeat):
                    command(*arg)
                showinfo(' '.join([str(repeat)] + [two_key] + ['('+two_key_info[1]+')']))
                if two_key == 'mc':
                    win.toggle_vim_mode(False)
                win.cmd_buf = []
            else:
                showinfo(' '.join([str(repeat)] + [cmd] + ['(unkonw command)']))
                win.cmd_buf = []
                return
        else:
            win.cmd_buf = []
            return True
Mixin.setMixin('editor', 'vim_routin', vim_routin)    


def on_first_keydown(win, event):
        key = event.GetKeyCode()
        if key in (wx.WXK_ESCAPE, ):
            if  win.on_focus:
                if win.AutoCompActive():
                    win.AutoCompCancel()
                    return
                if  not win.pref.vim_mode:
                    win.toggle_vim_mode(True)
                    return True
                else:
                    win.toggle_vim_mode(False)
                    return True
        elif key == ord(';') and event.ShiftDown() and not event.AltDown() and \
            not event.ControlDown() and win.pref.vim_mode:
            win.mainframe.statusbar.hide_panel()
            vim = win.mainframe.statusbar.vim_pad
            vim.Show()
            vim.SetFocus()
            win.pref.vim_mode = False
            return True
        else:
            return False
Mixin.setPlugin('editor', 'on_first_keydown', on_first_keydown)

def toggle_block(self):
    lineCount = self.GetLineCount()
    for lineNum in range(lineCount):
        if self.GetFoldLevel(lineNum) & wx.stc.STC_FOLDLEVELHEADERFLAG:
            expanding = not self.GetFoldExpanded(lineNum)
            break;
Mixin.setMixin('editor', 'toggle_block',toggle_block )   
    
def toggle_vim_mode(self, flag):
    self.pref.vim_mode = flag
    if flag == False:
        self.mainframe.statusbar.hide_panel()
        self.MarkerDeleteAll(self.vim_number)
        self.cmd_buf = []
    elif flag == True:
        self.mainframe.statusbar.vim_pad.Hide()
        showinfo("vim mode begin")
        self.MarkerDeleteAll(self.vim_number)
        self.MarkerAdd(self.GetCurrentLine(), self.vim_number)
Mixin.setMixin('editor', 'toggle_vim_mode',toggle_vim_mode)   

