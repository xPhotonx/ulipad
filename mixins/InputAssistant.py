#	Programmer:	limodou
#	E-mail:		limodou@gmail.com
#
#	Copyleft 2005 limodou
#
#	Distributed under the terms of the GPL (GNU Public License)
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
#	$Id$

import dict4ini
import os.path
import os
import re
import wx
import wx.stc
from modules.Debug import error
from modules import common
from modules import Mixin

class DUMY_CLASS:pass

assistant = {}
KEYS = {'<space>':' ', '<tab>':'\t', '<equal>':'=', '<div>':'/'}

class InputAssistant(Mixin.Mixin):
    __mixinname__ = 'inputassistant'

    def __init__(self):
        self.initmixin()

    def run(self, editor, event):
        if not editor.pref.auto_extend:
            return False

        self.editor = editor
        self.event = event
        self.key = event.KeyCode()
        self.ctrl = event.ControlDown()
        self.alt = event.AltDown()
        self.shift = event.ShiftDown()
        self.language = editor.languagename

        filename = common.getConfigPathFile('%s.acp' % self.language)
        if not os.path.exists(filename):
            if assistant.has_key(self.language):
                del assistant[self.language]
            return False
        self.install_assistant(filename)

        if self.key < 255:
            self.key = chr(self.key)
        else:
            return False
        try:
            return self._run()
        except:
            error.traceback()
            return False

    def _run(self):
        win = self.editor
        if self.ctrl or self.alt:
            return False
        objs = assistant.get(self.language, None)
        if not objs:
            return False
        else:
            for obj in objs:
                if obj.projectname and obj.projectname != common.getProjectName(win.filename):
                    continue
                #autostring
                if obj.autostring.has_key(self.key):
                    s = obj.autostring[self.key]
                    for k, text in s:
                        word, start, end = self.getWord(k)
                        word = word + self.key
                        if k == word:
                            if not isinstance(text, list):
                                win.BeginUndoAction()
                                win.SetTargetStart(start)
                                win.SetTargetEnd(end)
                                win.ReplaceTarget('')
                                win.GotoPos(start)
                                self.settext(text)
                                win.EndUndoAction()
                            else:
                                win.BeginUndoAction()
                                win.AddText(self.key)
                                win.AutoCompShow(0, " ".join(text))
                                win.EndUndoAction()
                            return True
                #autore
                if obj.autore.has_key(self.key):
                    line = win.GetCurrentLine()
                    txt = win.GetTextRange(win.PositionFromLine(line), win.GetCurrentPos()) + self.key
                    s = obj.autore[self.key]
                    length = len(txt)
                    flag = False
                    for k, text in s:
                        pos = 0
                        b = k.search(txt, pos)
                        while b:
                            if b.end() == length: #find
                                flag = True
                                break
                            else:
                                pos += 1
                                b = k.search(txt, pos)
                        if flag:
                            if not isinstance(text, list):
                                r = []
                                r.append(b.group())
                                r.extend(b.groups())
                                m = []
                                for p in text:
                                    for i in range(len(r)):
                                        p = p.replace('\\' + str(i), r[i])
                                    m.append(p)
                                win.BeginUndoAction()
                                pos = win.PositionFromLine(line)
                                win.SetTargetStart(pos + b.start())
                                win.SetTargetEnd(pos + b.end() - 1)
                                win.ReplaceTarget('')
                                win.GotoPos(pos + b.start())
                                self.settext(m)
                                win.EndUndoAction()
                            else:
                                win.BeginUndoAction()
                                win.AddText(self.key)
                                win.AutoCompShow(0, " ".join(text))
                                win.EndUndoAction()
                            return True

            return False

    def install_assistant(self, filename):
        if not assistant.has_key(self.language):
            assistant[self.language] = [self.get_assistant(filename)]
            obj = assistant[self.language][0]
            #install include files
            for f in obj.ini.include.values():
                fname = common.getConfigPathFile(f)
                if fname:
                    assistant[self.language].append(self.get_assistant(fname))
        else:
            objs = assistant[self.language]
            for i, obj in enumerate(objs):
                if os.path.getmtime(obj.filename) > obj.ftime:
                    del assistant[self.language]
                    self.install_assistant(filename)
                    break

    def get_assistant(self, filename):
        obj = DUMY_CLASS()
        obj.ini = dict4ini.DictIni(filename)
        obj.filename = filename
        obj.ftime = os.path.getmtime(filename)
        obj.autostring = self.install_keylist(obj.ini.autostring, False)
        obj.autore = self.install_keylist(obj.ini.autore, True)
        obj.projectname = obj.ini.default.get('projectname', '')
        return obj

    def install_keylist(self, keys, re_flag=False):
        d = {}
        for key, value in keys.items():
            for k, v in KEYS.items():
                key = key.replace(k, v)
            last_key = key[-1]
            if re_flag:
                r = re.compile(key)
            else:
                r = key
            if d.has_key(last_key):
                d[last_key].append((r, self.gettext(value)))
            else:
                d[last_key] =[(r, self.gettext(value))]
        for key in d.keys():
            d[key].reverse()
        return d

    def getWord(self, key):
        win = self.editor
        end = win.GetCurrentPos()
        line = win.LineFromPosition(end)
        linestart = win.PositionFromLine(line)
        ch = key[0]
        if ch.isalpha():
            txt = []
            start = end - 1
            while start >= linestart:
                if win.getChar(start) in win.mainframe.getWordChars() + '.':
                    txt.insert(0, win.getChar(start))
                    start -= 1
                else:
                    break
            start += 1
            text = ''.join(txt)
        else:
            start = max(end - len(key[:-1]), 0)
            text = win.GetTextRange(start, end)
        return text, start, end

    def gettext(self, text):
        if isinstance(text, (str, unicode)):
            s = self._split(text, r'\n')
            r = []
            for i in s:
                t = self._split(i, r'\t')
                for k in t:
                    r.append(k)
            return tuple(r)
        else:
#            s = []
#            for i in text:
#                s.append(self.gettext(i))
#            return s
            text.sort()
            return text

    def _split(self, text, delimeter):
        s = []
        pos = 0
        index = text.find(delimeter, pos)
        length = len(delimeter)
        while index > -1:
            s.append(text[pos:index])
            s.append(delimeter)
            pos = index + length
            index = text.find(delimeter, pos)
        if pos < len(text):
            s.append(text[pos:])
        return s

    def settext(self, text):
        win = self.editor
        cur_pos = -1
        for t in text:
            pos = t.find('!^')
            if pos > -1:
                t = t.replace('!^', '')
                cur_pos = win.GetCurrentPos() + pos
            if t == r'\n':
                if win.pref.autoindent:
                    line = win.GetCurrentLine()
                    txt = win.GetTextRange(win.PositionFromLine(line), win.GetCurrentPos())
                    if txt.strip() == '':
                        win.AddText(win.getEOLChar() + txt)
                    else:
                        n = win.GetLineIndentation(line) / win.GetTabWidth()
                        win.AddText(win.getEOLChar() + win.getIndentChar() * n)
                else:
                    win.AddText(win.getEOLChar())
            elif t == r'\t':
                win.CmdKeyExecute(wx.stc.STC_CMD_TAB)
            else:
                win.AddText(t)
            if cur_pos > -1:
                win.GotoPos(cur_pos)