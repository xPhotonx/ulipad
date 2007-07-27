#   Programmer: limodou
#   E-mail:     limodou@gmail.com
#
#   Copyleft 2005 limodou
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

import compiler
import pyflakes
from modules import common
import wx
from modules.EasyGui import EasyList
import sys

def check(codeString, filename):
    message = []
    try:
        codeString = codeString.replace('\r\n', '\n')
        tree = compiler.parse(codeString)
    except (SyntaxError, IndentationError):
        value = sys.exc_info()[1]
        (lineno, offset, line) = value[1][1:]
        if line.endswith("\n"):
            line = line[:-1]
        message.append((filename, lineno, tr('could not compile')))
    else:
        w = pyflakes.Checker(tree, filename)
        w.messages.sort(lambda a, b: cmp(a.lineno, b.lineno))
        for warning in w.messages:
            message.append((filename, warning.lineno, warning.message % warning.message_args))

    return message

def Check(mainframe, document):
    message = []
    if document.filename:
        message = check(document.GetText().encode(document.locale),
            common.encode_string(document.filename, common.defaultfilesystemencoding))
    else:
        message = check(document.GetText().encode(document.locale), '<stdin>')
    mainframe.createSyntaxCheckWindow()
    mainframe.syntaxcheckwindow.adddata(message)
    if message:
        mainframe.panel.showPage(tr('Syntax Check'))
    wx.CallAfter(mainframe.document.SetFocus)

class SyntaxCheckWindow(wx.Panel):
    def __init__(self, parent, mainframe):
        wx.Panel.__init__(self, parent, -1)

        self.mainframe = mainframe

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.list = EasyList.AutoWidthListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.list.InsertColumn(0, tr("Filename"))
        self.list.InsertColumn(1, tr("LineNo"))
        self.list.InsertColumn(2, tr("Description"))
        self.list.SetColumnWidth(0, 80)
        self.list.SetColumnWidth(1, 50)
        self.list.SetColumnWidth(1, 200)

        self.sizer.Add(self.list, 1, wx.EXPAND)

        wx.EVT_LIST_ITEM_ACTIVATED(self.list, self.list.GetId(), self.OnEnter)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)

    def adddata(self, data):
        self.list.DeleteAllItems()
        for i in data:
            filename, lineno, desc = i
            lineno = str(lineno)
            desc = desc.strip()
            index = self.list.InsertStringItem(sys.maxint, filename)
            self.list.SetStringItem(index, 1, lineno)
            self.list.SetStringItem(index, 2, desc)

    def OnEnter(self, event):
        index = event.GetIndex()
        filename = self.list.GetItem(index, 0).GetText()
        lineno = self.list.GetItem(index, 1).GetText()
        self.mainframe.editctrl.new(filename)
        wx.CallAfter(self.mainframe.document.goto, int(lineno))

    def canClose(self):
        return True