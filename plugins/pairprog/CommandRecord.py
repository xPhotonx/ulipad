#   Programmer: limodou
#   E-mail:     limodou@gmail.com
#
#   Copyleft 2006 limodou
#
#   Distributed under the terms of the GPL (GNU Public License)
#
#   NewEdit is free software; you can redistribute it and/or modify
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
import time
from modules import common
from modules import Globals

class CommandRecord(object):
    def __init__(self, commands=None, filename=None):
        self.commands = []
        self.setcommands(commands, filename)
        self.curstep = -1
        self.playing = False
            
    def append(self, command):
        """
        command should be a tuple, the first is command name, the second is parameter
        commands format is:
            ('openfile', (filename, text)),
            ('setlex', lexname)
            ('settext', text),
            ('gotopos', pos),
            ('gotoline', line),
            ('addtext', text),
            ('deltext', textlength)
        """
        self.commands.append(command)
        
    def play(self, auto=False, timestep=0.1):
        self.curstep = -1
        self.playing = True
        if auto:
            while self.next():
                if timestep:
                    time.sleep(timestep)
        
    def next(self):
        wx.SafeYield()
        if not self.playing:
            common.showerror(Globals.mainframe, tr("You shuld execute play method first"))
            return
        self.curstep += 1
        if self.curstep < len(self.commands):
            self.do_command()
            return True
        else:
            self.playing = False
            return
    
    def stop(self):
        self.playing = False
        
    def do_command(self):
        mainframe = Globals.mainframe
        editctrl = mainframe.editctrl
        cmd, v = self.commands[self.curstep]
        print cmd, v
        if cmd == 'openfile':
            filename, text = v
            document = editctrl.new()
            if isinstance(text, str):
                text = unicode(text, 'utf-8')
            document.SetText(text)
            document.setTitle(filename)
            self.curdoc = document
        elif cmd == 'setlex':
            self.check_document()
            for lexer in mainframe.lexers.lexobjs:
                if lexer.name == v:
                    lexer.colourize(self.curdoc)
        elif cmd == 'settext':
            self.check_document()
            self.curdoc.SetText(v)
        elif cmd == 'gotopos':
            self.check_document()
            self.curdoc.GotoPos(v)
        elif cmd == 'gotoline':
            self.check_document()
            self.curdoc.GotoLine(v)
        elif cmd == 'addtext':
            self.check_document()
            self.curdoc.AddText(v)
        elif cmd == 'deltext':
            self.check_document()
            pos = self.curdoc.GetCurrentPos()
            self.curdoc.SetTargetStart(pos)
            self.curdoc.SetTargetEnd(pos + v)
            self.curdoc.ReplaceTarget('')
        self.curdoc.EnsureCaretVisible()
        
    def check_document(self):
        mainframe = Globals.mainframe
        editctrl = mainframe.editctrl
        if editctrl.getCurDoc() is not self.curdoc:
            editctrl.swith(self.curdoc)

    def save(self, filename):
        from modules.EasyGuider import obj2ini
        try:
            obj2ini.dump(self.commands, filename)
        except:
            common.warn("Saving commands to %(file)s failed" % {'file':filename})
            
    def clear(self):
        self.commands = []
        
    def setcommands(self, commands=None, filename=None):
        if filename:
            from modules.EasyGuider import obj2ini
            try:
                self.commands = obj2ini.load(filename)
            except:
                self.commands = None
                common.warn(tr("Can't open the file %(file)s" % {'file':filename}))
        elif commands:
            self.commands = commands