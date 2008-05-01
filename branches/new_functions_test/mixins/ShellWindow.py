#coding=utf-8
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
#   $Id: ShellWindow.py 1500 2006-09-01 13:47:51Z limodou $

import os
import sys
import types
import locale
import wx.py
from wx.py.interpreter import Interpreter
from wx.py import introspect
from wx.py import dispatcher
from modules import Mixin
from modules import common
from modules import makemenu

import __main__
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

class ShellWindow(wx.py.shell.Shell, Mixin.Mixin):
    __mixinname__ = 'shellwindow'
    
    popmenulist = [(None, #parent menu id
        [
            (100, 'IDPM_UNDO', tr('Undo') + '\tCtrl+Z', wx.ITEM_NORMAL, 'OnPopupEdit', tr('Reverse previous editing operation')),
            (110, 'IDPM_REDO', tr('Redo') + '\tCtrl+Y', wx.ITEM_NORMAL, 'OnPopupEdit', tr('Reverse previous undo operation')),
            (120, '', '-', wx.ITEM_SEPARATOR, None, ''),
            (130, 'IDPM_CUT', tr('Cut') + '\tCtrl+X', wx.ITEM_NORMAL, 'OnPopupEdit', tr('Deletes text from the shell window and moves it to the clipboard')),
            (140, 'IDPM_COPY', tr('Copy') + '\tCtrl+C', wx.ITEM_NORMAL, 'OnPopupEdit', tr('Copies text from the shell window to the clipboard')),
            (145, 'IDPM_COPY_CLEAR', tr('Copy Without Prompts'), wx.ITEM_NORMAL, 'OnPopupEdit', tr('Copies text without prompts from the shell window to the clipboard')),
            (150, 'IDPM_PASTE', tr('Paste') + '\tCtrl+V', wx.ITEM_NORMAL, 'OnPopupEdit', tr('Pastes text from the clipboard into the shell window')),
            (155, 'IDPM_PASTE_RUN', tr('Paste and Run') + '\tCtrl+Shift+V', wx.ITEM_NORMAL, 'OnPopupEdit', tr('Pastes text from the clipboard into the shell window and also run it')),
            (160, '', '-', wx.ITEM_SEPARATOR, None, ''),
            (170, 'IDPM_SELECTALL', tr('Select All') + '\tCtrl+A', wx.ITEM_NORMAL, 'OnPopupEdit', tr('Selects all text.')),
            (180, 'IDPM_CLEAR', tr('Clear Shell Window') + '\tCtrl+Alt+R', wx.ITEM_NORMAL, 'OnClearShell', tr('Clears content of shell window.')),
        ]),
    ]
    imagelist = {
        'IDPM_UNDO':'images/undo.gif',
        'IDPM_REDO':'images/redo.gif',
        'IDPM_CUT':'images/cut.gif',
        'IDPM_COPY':'images/copy.gif',
        'IDPM_PASTE':'images/paste.gif',
    }
    
    def __init__(self, parent, mainframe, commandtxt=None, shelltxt=None):
        self.initmixin()
        #-----------------------------------------------------------------------
        self.InsertMode = None
        self.EditorMode = None
        self.AppendMode = True
        self.insertcurrpos = None
        #in shell mode when it Enter keep the pos
        self.lastSubmitPos = None
        self.undo_command = []
        
        
        
        #add default font settings in config.ini
        x = common.get_config_file_obj()
        font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        fontname = x.default.get('shell_font', font.GetFaceName())
        fontsize = x.default.get('shell_fontsize', 10)
        #todo fontsize maybe changed for mac
        if wx.Platform == '__WXMAC__':
            fontsize = 13
        #add chinese simsong support, because I like this font
        if not x.default.has_key('shell_font') and locale.getdefaultlocale()[0] == 'zh_CN':
            fontname = u'宋体'

        import wx.py.editwindow as edit
        edit.FACES['mono'] = fontname
        edit.FACES['size'] = fontsize

        wx.py.shell.Shell.__init__(self, parent, -1, InterpClass=NEInterpreter)

        #disable popup
        self.UsePopUp(0)
        
        self.parent = parent
        self.mainframe = mainframe
        wx.EVT_KILL_FOCUS(self, self.OnKillFocus)
        
        for key in ShellWindow.imagelist.keys():
            f = ShellWindow.imagelist[key]
            ShellWindow.imagelist[key] = common.getpngimage(f)
        
        self.popmenu = makemenu.makepopmenu(self, ShellWindow.popmenulist, ShellWindow.imagelist)
        
        wx.EVT_RIGHT_DOWN(self, self.OnPopUp)
        #-----------------------------------------------------------------------
##        self.SetViewEOL(True)
##        self.SetViewWhiteSpace(1)
##        self.SetIndentationGuides(True)
        
        self.shelltxt = shelltxt
        self.commandtxt = commandtxt
        if self.shelltxt is None:
            self.shelltxt = os.path.join(self.mainframe.workpath, "shell.txt")
        if self.commandtxt is None:
            self.commandtxt = os.path.join(self.mainframe.workpath, "commad.txt")
        self.read_shell(self.shelltxt)
        linesum = self.GetLineCount()
        self.GotoLine(linesum)
        self.setDisplayLineNumbers(True)
        self.AutoCompSetAutoHide(True)
        self.AutoCompSetCancelAtStart(False)
        text , pos = self.GetCurLine()
##        self.eolstring = {'\n':wx.stc.STC_EOL_LF, '\r\n':wx.stc.STC_EOL_CRLF, '\r':wx.stc.STC_EOL_CR}
##        self.ConvertEOLs(self.eolstring.get(os.linesep))

        if text.strip() == '>>>':
            self.LineDelete()
        self.prompt()
        wx.CallAfter(self.ScrollToLine, linesum - 5)
        self.Bind(wx.EVT_KEY_UP,self.on_key_up)
        
        
        
        
        #-----------------------------------------------------------------------
        
        wx.EVT_UPDATE_UI(self, self.IDPM_UNDO, self._OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_REDO, self._OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_CUT, self._OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_COPY, self._OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_COPY_CLEAR, self._OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_PASTE, self._OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_PASTE_RUN, self._OnUpdateUI)
    #---ygao--------------------------------------------------------------------
    def clearCommand(self):
        """Delete the current, unexecuted command."""
        startpos = self.promptPosEnd
        #must handle the insertmode or clear all till end
        thepos = self.GetCurrentPos()        
        if self.InsertMode == True:
            endpos = thepos
        else:
            endpos = self.GetTextLength()
        self.SetSelection(startpos, endpos)
        self.ReplaceSelection('')
        self.more = False
        
    def processLine(self):
        """Process the line of text at which the user hit Enter."""
    
        # The user hit ENTER and we need to decide what to do. They
        # could be sitting on any line in the shell.
        
        thepos = self.GetCurrentPos()
        startpos = self.promptPosEnd
        if self.InsertMode == True:
            endpos = thepos
        elif self.AppendMode == True:
            endpos = self.lastSubmitPos
        else:
              
            endpos = self.GetTextLength()
        ps2 = str(sys.ps2)
        # If they hit RETURN inside the current command, execute the
        # command.
        if self.CanEdit():
            self.SetCurrentPos(endpos)
            self.interp.more = False
            command = self.GetTextRange(startpos, endpos)
            lines = command.split(os.linesep + ps2)
            lines = [line.rstrip() for line in lines]
            command = '\n'.join(lines)
            if self.reader.isreading:
                if not command:
                    # Match the behavior of the standard Python shell
                    # when the user hits return without entering a
                    # value.
                    command = '\n'
                self.reader.input = command
                self.write(os.linesep)
            else:
                self.push(command)
                wx.FutureCall(1, self.EnsureCaretVisible)
        # Or replace the current command with the other command.
        else:
            # If the line contains a command (even an invalid one).
            if self.getCommand(rstrip=False):
                command = self.getMultilineCommand()
                self.clearCommand()
                self.write(command)
            # Otherwise, put the cursor back where we started.
            else:
                self.SetCurrentPos(thepos)
                self.SetAnchor(thepos)
    
    def prompt(self):
        """Display proper prompt for the context: ps1, ps2 or ps3.
    
        If this is a continuation line, autoindent as necessary."""
        isreading = self.reader.isreading
        skip = False
        if isreading:
            prompt = str(sys.ps3)
        elif self.more:
            prompt = str(sys.ps2)
        else:
            prompt = str(sys.ps1)
        pos = self.GetCurLine()[1]
        if pos > 0:
            if isreading:
                skip = True
            else:
                self.write(os.linesep)
        if not self.more:
            self.promptPosStart = self.GetCurrentPos()
        if not skip:
            self.write(prompt)
        if not self.more:
            self.promptPosEnd = self.GetCurrentPos()
            # Keep the undo feature from undoing previous responses.
            self.EmptyUndoBuffer()
        # XXX Add some autoindent magic here if more.
        if self.more:
            #self.write(' '*4)  # Temporary hack indentation.
            pass
        if self.InsertMode == True:
            self.insertcurrpos = self.promptPosEnd
        elif self.AppendMode == True:
                if self.lastSubmitPos == None:
                    self.lastSubmitPos = self.promptPosEnd
        self.EnsureCaretVisible()
        self.ScrollToColumn(0)
        #glo.err_interp = False
        
    def write(self, text):
        """Display text in the shell.
    
        Replace line endings with OS-specific endings."""
        text = self.fixLineEndings(text)
        self.AddText(text)
        #self.Refresh() don't need
        #self.Update()
        self.EnsureCaretVisible()
    
    def run(self, command, prompt=True, verbose=True):
        """Execute command as if it was typed in directly.
        >>> shell.run('print "this"')
        >>> print "this"
        this
        >>>
        """
        # Go to the very bottom of the text.
        endpos = self.GetTextLength()
        self.SetCurrentPos(endpos)
        command = command.rstrip()
        if prompt: self.prompt()
        if verbose: self.write(command)
        if self.AppendMode:
            cupos = self.GetCurrentPos()
            if cupos < self.promptPosEnd:
                self.lastSubmitPos = None
            else:
                #we are waiting at the command prompt.
                #self.lastSubmitPos = cupos #bug  if submitpos is between typing line
                self.lastSubmitPos = self.GetLineEndPosition(self.GetCurrentLine())
                self.undo_command.insert(0,self.promptPosEnd)
                self.undo_command.insert(0,self.promptPosStart)
                self.undo_command.insert(0,self.lastSubmitPos)            
        self.push(command)
    
    def objGetChildren(self, obj):
        """Return dictionary with attributes or contents of object."""
##        busy = wx.BusyCursor()
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
    
    def on_key_up(self,event):
        if self.AutoCompActive():
            if self.AutoCompGetCurrent() == -1:
                self.AutoCompCancel()
            else:
                root = introspect.getRoot(self.command, terminator='.')
                try:
                    object = eval(root, __main__.__dict__)
                except:
                    object = eval(root)
                name = self.list[self.AutoCompGetCurrent()]
                obj = self.objGetChildren(object).get(name, None)
                if obj is None:
                    return
                otype = type(obj)
                obj_name = self.command + name + "\n"
                text = obj_name + ''
                text += '\n\nType: ' + str(otype)
                try:
                    value = str(obj)
                except:
                    value = ''
                if otype is types.StringType or otype is types.UnicodeType:
                    value = repr(obj)
                text += '\n\nValue: ' + value
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
                self.mainframe.document_show_window.show(text)
                self.SetFocus()
                
        key = event.GetKeyCode()
        controlDown = event.ControlDown()
        altDown = event.AltDown()
        shiftDown = event.ShiftDown()
        cpos = self.GetCurrentPos()
        if key == wx.WXK_BACK:
            if not self.AutoCompActive():
                self.OnCallTipAutoCompleteManually(False)
        
    def autoCompleteShow(self, command, offset = 0):
        """Display auto-completion popup list."""
        self.command = command
        self.AutoCompSetAutoHide(self.autoCompleteAutoHide)
        self.AutoCompSetIgnoreCase(self.autoCompleteCaseInsensitive)
        self.list = self.interp.getAutoCompleteList(command,
                    includeMagic=self.autoCompleteIncludeMagic,
                    includeSingle=self.autoCompleteIncludeSingle,
                    includeDouble=self.autoCompleteIncludeDouble)
        if self.list:
            options = ' '.join(self.list)
            #offset = 0
            self.AutoCompShow(offset, options)

              
    
    def save_command(self,filepath):
        """save the history to history.ini"""        
      
        x = DictIni(filepath)
        x.common.list = self.history[:]
        x.save()
     
    
    def read_command(self,filepath):        
        """read history from history.ini"""      
        x = DictIni(filepath)
        x.read()        
        if not x.common.list:
            self.history = []
        else:
            self.history = x.common.list
            
    def read_shell(self,filepath):
        shelltxt_fp = open(filepath,'a+')
        try:
            shelltxt=shelltxt_fp.read().decode('utf8')
        finally:
            shelltxt_fp.close()
        self.SetText(shelltxt)
        
    def read_shell_temp(self,filepath):
        shelltxt_fp = open(filepath,'w+')
        try:
            shelltxt=shelltxt_fp.read()
        finally:
            shelltxt_fp.close()
        self.SetText(shelltxt)
    
    def save_shell(self,filepath):
        shelltxt_fp = open(filepath,'w')
        try:
            shelltxt_fp.write(self.GetText().encode('utf8'))
        finally:
            shelltxt_fp.close()
            
    def OnClose(self, event):
        """Event handler for closing."""
        self.save_shell(self.shelltxt)
        #self.save_command(self.commandtxt)
        #self.Destroy()
    
    
    
    
    
    
    
    
    
    #---ygao--------------------------------------------------------------------
    
    
    def OnPopUp(self, event):
        other_menus = []
        if self.popmenu:
            self.popmenu.Destroy()
            self.popmenu = None
        self.callplugin('other_popup_menu', self, other_menus)
        import copy
        if other_menus:
            pop_menus = copy.deepcopy(ShellWindow.popmenulist + other_menus)
        else:
            pop_menus = copy.deepcopy(ShellWindow.popmenulist)
        self.popmenu = pop_menus = makemenu.makepopmenu(self, pop_menus, ShellWindow.imagelist)
    
        self.PopupMenu(self.popmenu, event.GetPosition())
    
    def OnPopupEdit(self, event):
        eid = event.GetId()
        if eid == self.IDPM_CUT:
            self.Cut()
        elif eid == self.IDPM_COPY:
            self.Copy()
        elif eid == self.IDPM_COPY_CLEAR:
            super(ShellWindow, self).Copy()
        elif eid == self.IDPM_PASTE:
            self.Paste()
        elif eid == self.IDPM_PASTE_RUN:
            self.PasteAndRun()
        elif eid == self.IDPM_SELECTALL:
            self.SelectAll()
        elif eid == self.IDPM_UNDO:
            self.Undo()
        elif eid == self.IDPM_REDO:
            self.Redo()
    
    def _OnUpdateUI(self, event):
        eid = event.GetId()
        if eid == self.IDPM_CUT:
            event.Enable(not self.GetReadOnly() and bool(self.GetSelectedText()))
        elif eid in (self.IDPM_COPY, self.IDPM_COPY_CLEAR):
            event.Enable(bool(self.GetSelectedText()))
        elif eid in (self.IDPM_PASTE, self.IDPM_PASTE_RUN):
            event.Enable(not self.GetReadOnly() and bool(self.CanPaste()))
        elif eid == self.IDPM_UNDO:
            event.Enable(bool(self.CanUndo()))
        elif eid == self.IDPM_REDO:
            event.Enable(bool(self.CanRedo()))
    
    def OnClearShell(self, event):
        self.clear()
        self.prompt()
    
    def OnKillFocus(self, event):
        if  not self.mainframe.document_show_window.showing:
            if self.AutoCompActive():
                self.AutoCompCancel()
            if self.CallTipActive():
                self.CallTipCancel()
        event.Skip()
        event.Skip()

    def canClose(self):
        return False

#    def write(self, text):
#        """Display text in the shell.
#
#        Replace line endings with OS-specific endings."""
#        if not isinstance(text, unicode):
#            try:
#                text = unicode(text, common.defaultencoding)
#            except UnicodeDecodeError:
#                def f(x):
#                    if ord(x) > 127:
#                        return '\\x%x' % ord(x)
#                    else:
#                        return x
#                text = ''.join(map(f, text))
#        text = self.fixLineEndings(text)
#        self.AddText(text)
#        self.EnsureCaretVisible()
#        
    def Copy(self):
        self.CopyWithPrompts()
        
    def OnKeyDown(self, event):
        key = event.GetKeyCode()
        # If the auto-complete window is up let it do its thing.
        if self.AutoCompActive():
            event.Skip()
            return
        
        # Prevent modification of previously submitted
        # commands/responses.
        controlDown = event.ControlDown()
        altDown = event.AltDown()
        shiftDown = event.ShiftDown()
        currpos = self.GetCurrentPos()
        endpos = self.GetTextLength()
        selecting = self.GetSelectionStart() != self.GetSelectionEnd()
        
        if not controlDown and altDown and not shiftDown and key in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER]:
            if self.CallTipActive():
                self.CallTipCancel()
            if currpos == endpos:
                self.processLine()
            else:
                self.insertLineBreak()
        if not controlDown and not altDown and not shiftDown and key in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER]:
            if self.AppendMode == True:
                #if cuspos sits on exist command last line meaning you just typed command.
                cupos = self.GetCurrentPos()
                if cupos < self.promptPosEnd:
                    self.lastSubmitPos = None
                else:
                    #we are waiting at the command prompt.
                    #self.lastSubmitPos = cupos #bug  if submitpos is between typing line
                    self.lastSubmitPos = self.GetLineEndPosition(self.GetCurrentLine())
                    self.undo_command.insert(0,self.promptPosEnd)
                    self.undo_command.insert(0,self.promptPosStart)
                    self.undo_command.insert(0,self.lastSubmitPos)
        
        if controlDown and key == wx.WXK_BACK and not altDown and not shiftDown and self.AppendMode == True:
            cupos = self.GetCurrentPos()
            if self.undo_command != []:
                if cupos>self.undo_command[2]:
                    self.lastSubmitPos = self.undo_command.pop(0)
                    self.promptPosStart = self.undo_command.pop(0) #last .saveed PromptPosStart
                    self.promptPosEnd = self.undo_command.pop(0)#last saveed PromptPosEnd
                    self.SetSelection(self.lastSubmitPos,cupos)#lasted SubmitPos
                    self.ReplaceSelection('')
                    return
        if altDown and key == wx.WXK_BACK and not controlDown and not shiftDown and self.AppendMode == True:
            if self.undo_command != []:
                self.SetSelection(self.undo_command[-1],self.GetTextLength())
                self.ReplaceSelection('')
                self.promptPosStart = self.undo_command[-2]#restore to the correct pos in prompt
                self.promptPosEnd = self.undo_command[-1]
                del self.undo_command[:]#delete  all object in list to empty list
        if shiftDown and key == wx.WXK_BACK and not controlDown and not altDown and self.AppendMode == True:
            cupos = self.GetCurrentPos()
            if self.undo_command != []:
                self.lastSubmitPos = self.undo_command.pop(0)
                self.promptPosStart = self.undo_command.pop(0) #last saved PromptPosStart
                self.promptPosEnd = self.undo_command.pop(0)#last saved PromptPosEnd
                self.SetSelection(self.promptPosEnd,cupos)#lasted SubmitPos
                self.ReplaceSelection('')
        if self.InsertMode == True:
            if key in NAVKEYS:
                return
            else:                
                self.insertcurrpos = self.GetCurrentPos()
        super(ShellWindow, self).OnKeyDown(event)

class NEInterpreter(Interpreter):
    def push(self, command):
        """Send command to the interpreter to be executed.

        Because this may be called recursively, we append a new list
        onto the commandBuffer list and then append commands into
        that.  If the passed in command is part of a multi-line
        command we keep appending the pieces to the last list in
        commandBuffer until we have a complete command. If not, we
        delete that last list."""

        if isinstance(command, types.UnicodeType):
            command = command.encode(common.defaultencoding)
        if not self.more:
            try: del self.commandBuffer[-1]
            except IndexError: pass
        if not self.more: self.commandBuffer.append([])
        self.commandBuffer[-1].append(command)
        source = "#coding:%s" % common.defaultencoding + '\n' + '\n'.join(self.commandBuffer[-1])
        more = self.more = self.runsource(source)
        dispatcher.send(signal='Interpreter.push', sender=self,
                        command=command, more=more, source=source)
        return more
