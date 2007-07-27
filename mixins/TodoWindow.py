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

import sys
import StringIO
import re
import wx
from modules.EasyGuider import EasyList
from modules import common
from modules.Debug import error

TODO_C_PATTERN1 = re.compile(r'^\s*/\*\s*todo:?\s+(.*?)$', re.I)
TODO_C_PATTERN2 = re.compile(r'^\s*//\s*todo:?\s+(.*?)$', re.I)
TODO_PY_PATTERN = re.compile(r'^\s*#\s*todo:?\s+(.*?)$', re.I)

todo_patten = {
    'python':TODO_PY_PATTERN,
    'ruby':TODO_PY_PATTERN,
    'perl':TODO_PY_PATTERN,
    'c':(TODO_C_PATTERN1, TODO_C_PATTERN2),
    'java':(TODO_C_PATTERN1, TODO_C_PATTERN2),
}
class TodoWindow(wx.Panel):
    def __init__(self, parent, mainframe):
        wx.Panel.__init__(self, parent, -1)

        self.mainframe = mainframe

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.list = EasyList.AutoWidthListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.list.InsertColumn(0, tr("Filename"))
        self.list.InsertColumn(1, tr("LineNo"))
        self.list.InsertColumn(2, tr("Description"))
        self.list.SetColumnWidth(0, 150)
        self.list.SetColumnWidth(1, 30)
        self.list.SetColumnWidth(1, 200)

        self.sizer.Add(self.list, 1, wx.EXPAND)

        wx.EVT_LIST_ITEM_ACTIVATED(self.list, self.list.GetId(), self.OnEnter)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)

    def adddata(self, data):
        self.list.Freeze()
        self.list.DeleteAllItems()
        for i in data:
            filename, lineno, desc = i
            lineno = str(lineno)
            desc = desc.strip()
            index = self.list.InsertStringItem(sys.maxint, filename)
            self.list.SetStringItem(index, 1, lineno)
            self.list.SetStringItem(index, 2, desc)
        self.list.Thaw()

    def OnEnter(self, event):
        index = event.GetIndex()
        filename = self.list.GetItem(index, 0).GetText()
        lineno = self.list.GetItem(index, 1).GetText()
        self.mainframe.editctrl.new(filename)
        wx.CallAfter(self.mainframe.document.goto, int(lineno))

    def canClose(self):
        return True

    def show(self, editor):
        lang = editor.languagename
        filename = editor.filename
        #set default pattern
        pl = todo_patten.get(lang, [])
        if not isinstance(pl, (list, tuple)):
            pl = [pl]
        #first check the config.ini
        inifile = common.getConfigPathFile('config.ini')
        from modules import dict4ini
        ini = dict4ini.DictIni(inifile)
        if ini.todo_pattern.has_key(lang):
            pattern = ini.todo_pattern[lang]
            if isinstance(pattern, list):
                pl = []
                for i in pattern:
                    try:
                        pl.append(re.compile(i))
                    except:
                        error.traceback()
                        error.info('pattern=' + i)
            else:
                pl = []
                try:
                    pl.append(re.compile(pattern))
                except:
                    error.traceback()
                    error.info('pattern=' + pattern)
        data = []
        if pl:
            buf = StringIO.StringIO(editor.GetText())
            for i, line in enumerate(buf):
                for r in pl:
                    b = r.search(line)
                    if b:
                        result = filter(None, b.groups())
                        data.append((filename, i+1, result[0].rstrip()))
        self.adddata(data)
