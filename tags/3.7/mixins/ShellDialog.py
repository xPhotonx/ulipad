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
#   $Id: ShellDialog.py 1731 2006-11-22 03:35:50Z limodou $

__doc__ = 'run shell command'

import wx
from modules import Entry

class ShellDialog(wx.Dialog):
    def __init__(self, parent, pref):
        wx.Dialog.__init__(self, parent, -1, tr('Shell Manage'), size=(500, 300))
        self.parent = parent
        self.pref = pref

        box = wx.BoxSizer(wx.VERTICAL)
        self.list = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_EDIT_LABELS)
        self.list.InsertColumn(0, tr("Description"))
        self.list.InsertColumn(1, tr("Shell Command Line"))
        self.list.SetColumnWidth(0, 150)
        self.list.SetColumnWidth(1, 330)
        for i, item in enumerate(pref.shells):
            description, command = item
            self.list.InsertStringItem(i, description)
            self.list.SetStringItem(i, 1, command)

        box.Add(self.list, 1, wx.EXPAND|wx.ALL, 5)
        box2 = wx.BoxSizer(wx.HORIZONTAL)
        self.ID_UP = wx.NewId()
        self.ID_DOWN = wx.NewId()
        self.ID_ADD = wx.NewId()
        self.ID_REMOVE = wx.NewId()
        self.ID_MODIFY = wx.NewId()
        self.btnUp = wx.Button(self, self.ID_UP, tr("Up"))
        box2.Add(self.btnUp, 0, 0, 5)
        self.btnDown = wx.Button(self, self.ID_DOWN, tr("Down"))
        box2.Add(self.btnDown, 0, 0, 5)
        self.btnAdd = wx.Button(self, self.ID_ADD, tr("Add"))
        box2.Add(self.btnAdd, 0, 0, 5)
        self.btnModify = wx.Button(self, self.ID_MODIFY, tr("Modify"))
        box2.Add(self.btnModify, 0, 0, 5)
        self.btnRemove = wx.Button(self, self.ID_REMOVE, tr("Remove"))
        box2.Add(self.btnRemove, 0, 0, 5)
        self.btnOK = wx.Button(self, wx.ID_OK, tr("OK"))
        self.btnOK.SetDefault()
        box2.Add(self.btnOK, 0, 0, 5)
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, tr("Cancel"))
        box2.Add(self.btnCancel, 0, 0, 5)
        box.Add(box2, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        wx.EVT_BUTTON(self.btnUp, self.ID_UP, self.OnUp)
        wx.EVT_BUTTON(self.btnDown, self.ID_DOWN, self.OnDown)
        wx.EVT_BUTTON(self.btnAdd, self.ID_ADD, self.OnAdd)
        wx.EVT_BUTTON(self.btnModify, self.ID_MODIFY, self.OnModify)
        wx.EVT_BUTTON(self.btnRemove, self.ID_REMOVE, self.OnRemove)
        wx.EVT_BUTTON(self.btnOK, wx.ID_OK, self.OnOK)
        wx.EVT_LIST_ITEM_SELECTED(self.list, self.list.GetId(), self.OnItemSelected)
        wx.EVT_LIST_ITEM_DESELECTED(self.list, self.list.GetId(), self.OnItemDeselected)

        self.OnItemDeselected(None)

        self.SetSizer(box)
        self.SetAutoLayout(True)

    def exchangeItem(self, a, b):
        if b<0 or b>self.list.GetItemCount()-1:
            return
        item = max([a, b])
        ins = min([a, b])
        description, command = self.getItemText(item)
        self.list.DeleteItem(item)
        self.list.InsertStringItem(ins, description)
        self.list.SetStringItem(ins, 1, command)

    def getItemText(self, item):
        return self.list.GetItemText(item), self.list.GetItem(item, 1).GetText()

    def OnUp(self, event):
        if self.list.GetSelectedItemCount() > 1:
            dlg = wx.MessageDialog(self, tr("You can select only one item"), tr("Up Shell Command"), wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            return
        item = self.list.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
        self.exchangeItem(item, item - 1)

    def OnDown(self, event):
        if self.list.GetSelectedItemCount() > 1:
            dlg = wx.MessageDialog(self, tr("You can select only one item"), tr("Down Shell Command"), wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            return
        item = self.list.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
        self.exchangeItem(item, item + 1)

    def OnRemove(self, event):
        lastitem = -1
        item = self.list.GetNextItem(lastitem, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
        while item > -1:
            dlg = wx.MessageDialog(self, tr("Do you realy want to delete current item [%s]?") % self.getItemText(item)[0], tr("Deleting Shell Command"), wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
            answer = dlg.ShowModal()
            if answer == wx.ID_YES:
                self.list.DeleteItem(item)
            elif answer == wx.ID_NO:
                lastitem = item
            else:
                return
            item = self.list.GetNextItem(lastitem, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)

    def OnAdd(self, event):
        dlg = Entry.MyFileEntry(self, tr("Shell Command Line"), tr("Enter the shell command line:\n$file will be replaced by current document filename\n$path will be replaced by current document filename's directory"), '')
        answer = dlg.ShowModal()
        if answer == wx.ID_OK:
            command = dlg.GetValue()
            if len(command) > 0:
                i = self.list.GetItemCount()
                self.list.InsertStringItem(i, 'Change the description')
                self.list.SetStringItem(i, 1, command)
                self.list.EditLabel(i)

    def OnModify(self, event):
        if self.list.GetSelectedItemCount() > 1:
            dlg = wx.MessageDialog(self, tr("You can select only one item"), tr("Modify Shell Command"), wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            return
        item = self.list.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
        dlg = Entry.MyFileEntry(self, tr("Shell Command Line"), tr("Enter the shell command line:\n$file will be replaced by current document filename\n$path will be replaced by current document filename's directory"), self.getItemText(item)[1])
        answer = dlg.ShowModal()
        if answer == wx.ID_OK:
            command = dlg.GetValue()
            if len(command) > 0:
                self.list.SetStringItem(item, 1, command)

    def OnOK(self, event):
        shells = []
        for i in range(self.list.GetItemCount()):
            description, command = self.getItemText(i)
            shells.append((description, command))
            if (description == '') or (description == 'Change the description'):
                dlg = wx.MessageDialog(self, tr("The description must not be empty or ") + '"Change the description"' +
                         tr('.\nPlease change them first!'), tr("Saving Shell Command"), wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                return
        else:
            self.pref.shells = shells[:]
            self.pref.save()
            event.Skip()

    def OnItemSelected(self, event):
        self.btnUp.Enable(True)
        self.btnDown.Enable(True)
        self.btnRemove.Enable(True)
        self.btnModify.Enable(True)

    def OnItemDeselected(self, event):
        self.btnUp.Enable(False)
        self.btnDown.Enable(False)
        self.btnRemove.Enable(False)
        self.btnModify.Enable(False)
