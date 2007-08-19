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

import wx.py
from wx.py.interpreter import Interpreter
from wx.py import dispatcher
import types
import locale
from modules import common
from modules import dict4ini

class ShellWindow(wx.py.shell.Shell):
    def __init__(self, parent, mainframe):

        #add default font settings in config.ini
        inifile = common.getConfigPathFile('config.ini')
        x = dict4ini.DictIni(inifile)
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
        self.parent = parent
        self.mainframe = mainframe
        wx.EVT_KILL_FOCUS(self, self.OnKillFocus)
        
    def OnKillFocus(self, event):
        if self.AutoCompActive():
            self.AutoCompCancel()
        if self.CallTipActive():
            self.CallTipCancel()

    def canClose(self):
        return True

    def write(self, text):
        """Display text in the shell.

        Replace line endings with OS-specific endings."""
        if not isinstance(text, types.UnicodeType):
            text = unicode(text, common.defaultencoding)
        text = self.fixLineEndings(text)
        self.AddText(text)
        self.EnsureCaretVisible()


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
        source = '\n'.join(self.commandBuffer[-1])
        more = self.more = self.runsource(source)
        dispatcher.send(signal='Interpreter.push', sender=self,
                        command=command, more=more, source=source)
        return more
