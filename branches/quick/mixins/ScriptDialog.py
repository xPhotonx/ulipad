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
#	$Id: ScriptDialog.py 475 2006-01-16 09:50:28Z limodou $

import wx
from modules import makemenu
import sys
import os.path
import wx.lib.dialogs
import traceback

class ScriptDialog(wx.Dialog):
	def __init__(self, parent, pref):
		wx.Dialog.__init__(self, parent, -1, tr('Script Manage'), size=(500, 300))
		self.parent = parent
		self.pref = pref

		box = wx.BoxSizer(wx.VERTICAL)
		self.list = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.LC_EDIT_LABELS | wx.SUNKEN_BORDER)
		self.list.InsertColumn(0, tr("Description"))
		self.list.InsertColumn(1, tr("Filename"))
		self.list.SetColumnWidth(0, 150)
		self.list.SetColumnWidth(1, 330)
		for i, item in enumerate(pref.scripts):
			description, filename = item
			self.list.InsertStringItem(i, description)
			self.list.SetStringItem(i, 1, filename)

		box.Add(self.list, 1, wx.EXPAND|wx.ALL, 5)
		box2 = wx.BoxSizer(wx.HORIZONTAL)
		self.ID_UP = wx.NewId()
		self.ID_DOWN = wx.NewId()
		self.ID_ADD = wx.NewId()
		self.ID_REMOVE = wx.NewId()
		self.btnUp = wx.Button(self, self.ID_UP, tr("Up"), size=(60, -1))
		box2.Add(self.btnUp, 0, 0, 5)
		self.btnDown = wx.Button(self, self.ID_DOWN, tr("Down"), size=(60, -1))
		box2.Add(self.btnDown, 0, 0, 5)
		self.btnAdd = wx.Button(self, self.ID_ADD, tr("Add"), size=(60, -1))
		box2.Add(self.btnAdd, 0, 0, 5)
		self.btnRemove = wx.Button(self, self.ID_REMOVE, tr("Remove"), size=(60, -1))
		box2.Add(self.btnRemove, 0, 0, 5)
		self.btnOK = wx.Button(self, wx.ID_OK, tr("OK"), size=(60, -1))
		self.btnOK.SetDefault()
		box2.Add(self.btnOK, 0, 0, 5)
		self.btnCancel = wx.Button(self, wx.ID_CANCEL, tr("Cancel"), size=(60, -1))
		box2.Add(self.btnCancel, 0, 0, 5)
		box.Add(box2, 0, wx.ALIGN_CENTER|wx.ALL, 5)

		wx.EVT_BUTTON(self.btnUp, self.ID_UP, self.OnUp)
		wx.EVT_BUTTON(self.btnDown, self.ID_DOWN, self.OnDown)
		wx.EVT_BUTTON(self.btnAdd, self.ID_ADD, self.OnAdd)
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
		description, filename = self.getItemText(item)
		self.list.DeleteItem(item)
		self.list.InsertStringItem(ins, description)
		self.list.SetStringItem(ins, 1, filename)

	def getItemText(self, item):
		return self.list.GetItemText(item), self.list.GetItem(item, 1).GetText()

	def OnUp(self, event):
		if self.list.GetSelectedItemCount() > 1:
			dlg = wx.MessageDialog(self, tr("You can select only one item"), tr("Up Script"), wx.OK | wx.ICON_INFORMATION)
			dlg.ShowModal()
			return
		item = self.list.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
		self.exchangeItem(item, item - 1)

	def OnDown(self, event):
		if self.list.GetSelectedItemCount() > 1:
			dlg = wx.MessageDialog(self, tr("You can select only one item"), tr("Down Script"), wx.OK | wx.ICON_INFORMATION)
			dlg.ShowModal()
			return
		item = self.list.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
		self.exchangeItem(item, item + 1)

	def OnRemove(self, event):
		lastitem = -1
		item = self.list.GetNextItem(lastitem, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
		while item > -1:
			dlg = wx.MessageDialog(self, tr("Do you realy want to delete current item [%s]?") % self.getItemText(item)[0], tr("Deleting Script"), wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
			answer = dlg.ShowModal()
			if answer == wx.ID_YES:
				self.list.DeleteItem(item)
			elif answer == wx.ID_NO:
				lastitem = item
			else:
				return
			item = self.list.GetNextItem(lastitem, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)

	def OnAdd(self, event):
		dlg = wx.FileDialog(self, tr("Open Script"), self.pref.last_script_dir, "", tr("Python file (*.py)|*.py"), wx.OPEN|wx.HIDE_READONLY)
		if dlg.ShowModal() == wx.ID_OK:
			filename = dlg.GetPath()
			i = self.list.GetItemCount()
			self.list.InsertStringItem(i, 'Change the description')
			self.list.SetStringItem(i, 1, filename)
			self.pref.last_script_dir = os.path.dirname(filename)
			self.pref.save()
			self.list.EditLabel(i)

	def OnOK(self, event):
		scripts = []
		for i in range(self.list.GetItemCount()):
			description, filename = self.getItemText(i)
			scripts.append((description, filename))
			if (description == '') or (description == 'Change the description'):
				dlg = wx.MessageDialog(self, tr("The description must not be empty or ") + '"Change the description"' +
					 tr('.\nPlease change them first!'), tr("Saving Script"), wx.OK | wx.ICON_INFORMATION)
				dlg.ShowModal()
				return
		else:
			self.pref.scripts = scripts[:]
			self.pref.save()
			event.Skip()

	def OnItemSelected(self, event):
		self.btnUp.Enable(True)
		self.btnDown.Enable(True)
		self.btnRemove.Enable(True)

	def OnItemDeselected(self, event):
		self.btnUp.Enable(False)
		self.btnDown.Enable(False)
		self.btnRemove.Enable(False)