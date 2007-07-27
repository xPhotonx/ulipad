#	Programmer:	limodou
#	E-mail:		chatme@263.net
#
#	Copyleft 2004 limodou
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
#	$Id: ClassTree.py 176 2005-11-22 02:46:37Z limodou $

import wx
from modules import PyParse
import os.path

class ClassTree(wx.TreeCtrl):
	def __init__(self, parent, document, imagelist):
		wx.TreeCtrl.__init__(self, parent, -1, style=wx.TR_HAS_BUTTONS|wx.TR_SINGLE|wx.TR_HIDE_ROOT)
		self.document = document
		self.class_normal_image = 0
		self.class_open_image = 1
		self.method_image     = 2
		if imagelist:
			self.SetImageList(imagelist)
		self.root = self.AddRoot(os.path.basename(document.filename))
		wx.EVT_LEFT_DOWN(self, self.OnLeftUp)
		wx.EVT_TREE_SEL_CHANGED(self, self.GetId(), self.OnSelected)

	def OnLeftUp(self, event):
		pt = event.GetPosition();
		item, flags = self.HitTest(pt)
		if item.IsOk():
			if item == self.GetSelection():
				self.SelectItem(self.GetSelection(), False)
				wx.CallAfter(self.SelectItem, item, True)
				return
		event.Skip()
		
	def OnSelected(self, event):
		item = event.GetItem()
		lineno = self.GetPyData(item)
		if self.document:
			wx.CallAfter(self.document.goto, lineno)
		
#	def OnCompareItems(self, item1, item2):
#		t1 = self.GetItemText(item1)
#		t2 = self.GetItemText(item2)
#		if t1 < t2: return -1
#		if t1 == t2: return 0
#		return 1

	def readtext(self, text):
		self.DeleteAllItems()
		nodes = PyParse.parseString(text)
		imports = nodes['import']
		for info, lineno in imports:
			self.addnode(self.root, info, self.method_image, None, lineno)
		functions = nodes['function'].values()
		functions.sort()
		for info, lineno in functions:
			self.addnode(self.root, info, self.method_image, None,  lineno)
		classes = nodes['class'].values()
		classes.sort()
		for c in classes:
			node = self.addnode(self.root, c.info, self.class_normal_image, self.class_open_image, c.lineno)
			functions = c.methods.values()
			functions.sort()
			for info, lineno in functions:
				self.addnode(node, info, self.method_image, None,  lineno)
			self.Expand(node)

	def addnode(self, parent, name, imagenormal, imageexpand=None, data=None):
		obj = self.AppendItem(parent, name)
		self.SetPyData(obj, data)
		self.SetItemImage(obj, imagenormal, wx.TreeItemIcon_Normal)
		if imageexpand:
			self.SetItemImage(obj, imageexpand, wx.TreeItemIcon_Expanded)
		return obj