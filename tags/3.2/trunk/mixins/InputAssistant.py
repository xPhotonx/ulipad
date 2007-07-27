#	Programmer:	limodou
#	E-mail:		limodou@gmail.com
#
#	Copyleft 2006 limodou
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

import os
import re
import wx
from modules import dict4ini
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
            if not self.key.isalnum() and self.key != '_' and editor.AutoCompActive():
                editor.AutoCompCancel()
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
                if obj.projectname and obj.projectname not in common.getProjectName(win.filename):
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
                                return True
                            else:
                                win.BeginUndoAction()
                                win.AddText(self.key)
                                win.inputassistant_obj = obj
                                win.word_len = start, end + 1
                                win.replace_strings = None
                                win.UserListShow(win.type_list, " ".join(text))
                                win.EndUndoAction()
                                return True
                #autostring_append
                if obj.autostring_append.has_key(self.key):
                    s = obj.autostring_append[self.key]
                    for k, text in s:
                        word, start, end = self.getWord(k)
                        word = word + self.key
                        if k == word:
                            if not isinstance(text, list):
                                win.BeginUndoAction()
                                win.AddText(self.key)
                                self.settext(text)
                                win.EndUndoAction()
                                return True
                            else:
                                win.BeginUndoAction()
                                win.AddText(self.key)
                                win.inputassistant_obj = obj
                                win.replace_strings = None
                                win.word_len = win.GetCurrentPos(), -1
                                win.UserListShow(win.type_list, " ".join(text))
                                win.EndUndoAction()
                                return True
                #autore
                if obj.autore.has_key(self.key):
                    line = win.GetCurrentLine()
                    txt = win.GetTextRange(win.PositionFromLine(line), win.GetCurrentPos())
                    txt = txt.encode('utf-8')
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
                            r = []
                            r.append(unicode(b.group(), 'utf-8'))
                            r.extend(unicode(x, 'utf-8') for x in b.groups())
                            if not isinstance(text, list):
                                m = []
                                for p in text:
                                    for i in range(len(r)):
                                        p = p.replace('\\' + str(i), r[i])
                                    m.append(p)
                                win.BeginUndoAction()
                                pos = win.PositionFromLine(line)
                                win.SetTargetStart(pos + b.start())
                                win.SetTargetEnd(pos + b.end())
                                win.ReplaceTarget('')
                                win.GotoPos(pos + b.start())
                                self.settext(m)
                                win.EndUndoAction()
                                return True
                            else:
                                win.BeginUndoAction()
                                win.AddText(self.key)
                                win.inputassistant_obj = obj
                                pos = win.PositionFromLine(line)
                                win.replace_strings = r
                                win.word_len = pos + b.start(), pos + b.end()
                                win.UserListShow(win.type_list, " ".join(text))
                                win.EndUndoAction()
                                return True
                #autore_append
                if obj.autore_append.has_key(self.key):
                    line = win.GetCurrentLine()
                    txt = win.GetTextRange(win.PositionFromLine(line), win.GetCurrentPos())
                    txt = txt.encode('utf-8')
                    s = obj.autore_append[self.key]
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
                            r = []
                            r.append(unicode(b.group(), 'utf-8'))
                            r.extend(unicode(x, 'utf-8') for x in b.groups())
                            if not isinstance(text, list):
                                m = []
                                for p in text:
                                    for i in range(len(r)):
                                        p = p.replace('\\' + str(i), r[i])
                                    m.append(p)
                                win.BeginUndoAction()
                                win.AddText(self.key)
                                self.settext(m)
                                win.EndUndoAction()
                                return True
                            else:
                                win.BeginUndoAction()
                                win.AddText(self.key)
                                win.inputassistant_obj = obj
                                pos = win.PositionFromLine(line)
                                win.replace_strings = r
                                win.word_len = win.GetCurrentPos(), -1
                                win.UserListShow(win.type_list, " ".join(text))
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
                    assistant[self.language].insert(-1, self.get_assistant(fname))
        else:
            objs = assistant[self.language]
            for i, obj in enumerate(objs):
                if os.path.getmtime(obj.filename) > obj.ftime:
                    del assistant[self.language]
                    self.install_assistant(filename)
                    break

    def get_assistant(self, filename):
        obj = DUMY_CLASS()
        obj.ini = dict4ini.DictIni(filename, encoding='utf-8', onelevel=True)
        obj.filename = filename
        obj.ftime = os.path.getmtime(filename)
        #autostring is used to replace
        obj.autostring = self.install_keylist(obj.ini.ordereditems(obj.ini.autostring, ['autostring']), False)
        #autostring_append is used to append
        obj.autostring_append = self.install_keylist(obj.ini.ordereditems(obj.ini.autostring_append, ['autostring_append']), False)
        #autore is used to replace
        obj.autore = self.install_keylist(obj.ini.ordereditems(obj.ini.autore, ['autore']), True)
        #autore_replace is used to append
        obj.autore_append = self.install_keylist(obj.ini.ordereditems(obj.ini.autore_append, ['autore_append']), True)
        obj.projectname = obj.ini.default.get('projectname', '')
        return obj

    def install_keylist(self, items, re_flag=False):
        d = {}
        for key, value in items:
            for k, v in KEYS.items():
                key = key.replace(k, v)
            last_key = key[-1]
            if re_flag:
                try:
                    r = re.compile(key[:-1])
                except:
                    error.info("key=%s, value=%s" % (key,value))
                    error.traceback()
                    continue
            else:
                r = key
            if d.has_key(last_key):
                d[last_key].append((r, self.gettext(value)))
            else:
                d[last_key] =[(r, self.gettext(value))]
#        for key in d.keys():
#            d[key].reverse()
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
            pos = t.encode('utf-8').find('!^')
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