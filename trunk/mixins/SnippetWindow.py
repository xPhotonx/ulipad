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
#	$Id: SnippetWindow.py 481 2006-01-17 05:54:13Z limodou $

import wx
import SnippetClass
import os.path
import os
from modules import common
from modules import Globals
import re

r = re.compile("<#{(.*?)}#>")

class MySnippetCatalog(wx.TreeCtrl):
	def __init__(self, parent, mainframe, pref):
		wx.TreeCtrl.__init__(self, parent, -1, style = wx.TR_SINGLE|wx.TR_HAS_BUTTONS, size=(0, 0))
		self.parent = parent
		self.pref = pref
		self.mainframe = mainframe

		self.snippetsimagelist = il = wx.ImageList(16, 16)
		self.close_image = il.Add(common.getpngimage(os.path.join(Globals.workpath, 'images/minus.gif')))
		self.open_image = il.Add(common.getpngimage(os.path.join(Globals.workpath, 'images/plus.gif')))
		self.item_image = il.Add(common.getpngimage(os.path.join(Globals.workpath, 'images/item.gif')))

		self.SetImageList(il)

		self.root = self.AddRoot(tr('Snippets'))
		self.SetPyData(self.root, None)
		self.SetItemImage(self.root, self.close_image, wx.TreeItemIcon_Normal)
		self.SetItemImage(self.root, self.open_image, wx.TreeItemIcon_Expanded)

		wx.EVT_TREE_SEL_CHANGED(self, self.GetId(), self.OnChanged)

	def loadData(self):
		self.items = [self.root]
		self.CollapseAndReset(self.root)
		snippet = SnippetClass.SnippetCatalog(self.mainframe.snippet_catalogfile)
		root = self.root
		stack = [self.root]
		lastlevel = 0
		lastnode = self.root
		self.maxid = 0
		for level, name, id in snippet:
			if level < lastlevel:
				stack = stack[:level+1]
			elif level > lastlevel:
				stack.append(lastnode)
			root = stack[level]
			lastlevel = level
			self.maxid = max([self.maxid, id])
			lastnode = self.addnode(root, name, self.item_image, None, id)
			self.Expand(root)
		self.Expand(self.root)
		try:
			self.SelectItem(self.items[self.pref.snippet_lastitem], True)
		except:
			self.SelectItem(self.root)

	def addnode(self, parent, name, imagenormal, imageexpand=None, data=None):
		obj = self.AppendItem(parent, name)
		self.items.append(obj)
		self.SetPyData(obj, data)
		self.SetItemImage(obj, imagenormal, wx.TreeItemIcon_Normal)
		if imageexpand:
			self.SetItemImage(obj, imageexpand, wx.TreeItemIcon_Expanded)
		return obj

	def OnChanged(self, event):
		index = self.items.index(event.GetItem())
		self.pref.snippet_lastitem = index
		self.pref.save()
		id = self.GetPyData(event.GetItem())
		self.parent.items.loadData(getFilename(self.mainframe, id))

class MySnippetCode(wx.ListCtrl):
	def __init__(self, parent, mainframe):
		wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
		self.parent = parent
		self.mainframe = mainframe

		self.InsertColumn(0, tr("Abbreviation"))
		self.InsertColumn(1, tr("Description"))
		self.SetColumnWidth(0, 100)
		self.SetColumnWidth(1, 180)

		wx.EVT_LIST_ITEM_ACTIVATED(self, self.GetId(), self.OnActivated)

	def loadData(self, xmlfile):
		self.DeleteAllItems()
		self.items = {}
		if xmlfile:
			snippetcodes = SnippetClass.SnippetCode(xmlfile)
			items = [v for v in snippetcodes]
			items.sort()
			for i, v in enumerate(items):
				abbr, description, author, version, date, code = v
				self.items[abbr] = code
				self.InsertStringItem(i, abbr)
				self.SetStringItem(i, 1, description)

	def OnActivated(self, event):
		abbr = event.GetText()
		text = self.items[abbr]
		self.elements = []
		text = re.sub(r, self.dosup, text)
		if self.elements:
			from modules.EasyGuider import EasyDialog
			dlg = EasyDialog.EasyDialog(self, title=tr("Code Template"), elements=self.elements)
			values = None
			if dlg.ShowModal() == wx.ID_OK:
				values = dlg.GetValue()
			dlg.Destroy()
			if values:
				from modules.meteor import render
				text = render(text, values, type='string')
			else:
				return
		self.mainframe.document.AddText(text)
		self.mainframe.document.SetFocus()

	def dosup(self, matchobj):
		text = matchobj.groups()[0]
		v = text.split(',')
		result = ''
		values = {}
		for i in v:
			s = i.split('=')
			values[s[0].strip()] = s[1].strip()
		self.elements.append((values.get('type', 'string'), values['name'], values.get('default', ''), values.get('description', values['name']), None))
			
		return '<#' + values['name'] + '#>'

class MySnippet(wx.SplitterWindow):
	def __init__(self, parent, mainframe, imagelist = None):
		wx.SplitterWindow.__init__(self, parent, -1, style = wx.SP_LIVE_UPDATE )
		self.parent = parent
		self.mainframe = mainframe
		self.pref = mainframe.pref

		self.catalog = MySnippetCatalog(self, self.mainframe, self.pref)

		self.items = MySnippetCode(self, mainframe)

		self.SetMinimumPaneSize(50)
		self.SplitHorizontally(self.catalog, self.items,150)

		self.catalog.loadData()

	def canClose(self):
		return True

class SnippetsCatalogDialog(wx.Dialog):
	def __init__(self, *args, **kwargs):
		wx.Dialog.__init__(self, *args, **kwargs)

	def init(self, mainframe):
		self.mainframe = mainframe
		self.pref = mainframe.pref
		self.snippetswindow = mainframe.panel.getPage(tr('Snippets'))

		self.loadcatalog()

		self.new = []
		self.delete = []

		self.obj_ID_OK.SetId(wx.ID_OK)
		self.obj_ID_CANCEL.SetId(wx.ID_CANCEL)

		wx.EVT_CLOSE(self, self.OnClose)
		wx.EVT_LISTBOX(self.obj_ID_CATALOG, self.obj_ID_CATALOG.GetId(), self.OnCatalogSelected)
		wx.EVT_BUTTON(self.obj_ID_ADDITEM, self.ID_ADDITEM, self.OnAddItem)
		wx.EVT_BUTTON(self.obj_ID_ADDSUBITEM, self.ID_ADDSUBITEM, self.OnAddSubItem)
		wx.EVT_BUTTON(self.obj_ID_UPDATE, self.ID_UPDATE, self.OnUpdate)
		wx.EVT_BUTTON(self.obj_ID_DELETE, self.ID_DELETE, self.OnDelete)
		wx.EVT_BUTTON(self.obj_ID_UP, self.ID_UP, self.OnUp)
		wx.EVT_BUTTON(self.obj_ID_DOWN, self.ID_DOWN, self.OnDown)
		wx.EVT_BUTTON(self.obj_ID_LEFT, self.ID_LEFT, self.OnLeft)
		wx.EVT_BUTTON(self.obj_ID_RIGHT, self.ID_RIGHT, self.OnRight)
		wx.EVT_BUTTON(self.obj_ID_OK, wx.ID_OK, self.OnOk)
		wx.EVT_BUTTON(self.obj_ID_CANCEL, wx.ID_CANCEL, self.OnCancel)
		wx.EVT_BUTTON(self.obj_ID_APPLY, self.ID_APPLY, self.OnApply)

		wx.EVT_UPDATE_UI(self.obj_ID_ADDSUBITEM, self.ID_ADDSUBITEM, self.OnUpdateUI)
		wx.EVT_UPDATE_UI(self.obj_ID_UP, self.ID_UP, self.OnUpdateUI)
		wx.EVT_UPDATE_UI(self.obj_ID_DOWN, self.ID_DOWN, self.OnUpdateUI)
		wx.EVT_UPDATE_UI(self.obj_ID_LEFT, self.ID_LEFT, self.OnUpdateUI)
		wx.EVT_UPDATE_UI(self.obj_ID_RIGHT, self.ID_RIGHT, self.OnUpdateUI)
		wx.EVT_UPDATE_UI(self.obj_ID_DELETE, self.ID_DELETE, self.OnUpdateUI)
		wx.EVT_UPDATE_UI(self.obj_ID_UPDATE, self.ID_UPDATE, self.OnUpdateUI)

	def loadcatalog(self):
		self.catalogitems = []
		snippet = SnippetClass.SnippetCatalog(self.mainframe.snippet_catalogfile)
		self.tab = '    '
		self.maxid = snippet.getmaxid()
		for i, v in enumerate(snippet):
			level, name, id = v
			s = self.tab * level + name
			self.obj_ID_CATALOG.InsertItems([s], i)
			self.catalogitems.append((s, id))

	def OnUpdateUI(self, event):
		catalog_selected = len(self.obj_ID_CATALOG.GetSelections()) > 0
		event.Enable(catalog_selected)

	def OnClose(self, event):
		self.Destroy()

	def OnCatalogSelected(self, event):
		index = event.GetSelection()
		self.obj_ID_CATALOG_TEXT.SetValue(self.getCatalogRealText(index))

	def getCatalogRealText(self, index):
		text = self.catalogitems[index][0]
		return text.replace(' ', '')

	def getCatalogText(self, index):
		return self.catalogitems[index][0]

	def OnAddItem(self, event):
		index = self.getIndex()
		if index != wx.NOT_FOUND:
			self.obj_ID_CATALOG.InsertItems([self.obj_ID_CATALOG_TEXT.GetValue()], index+1)
			self.maxid += 1
			self.catalogitems.insert(index+1, (self.obj_ID_CATALOG_TEXT.GetValue(), self.maxid))
			index += 1
		else:
			self.obj_ID_CATALOG.InsertItems([self.obj_ID_CATALOG_TEXT.GetValue()], self.obj_ID_CATALOG.GetCount())
			self.maxid += 1
			self.catalogitems.append((self.obj_ID_CATALOG_TEXT.GetValue(), self.maxid))
			index = self.obj_ID_CATALOG.GetCount() - 1
		self.new.append(self.maxid)
		self.obj_ID_CATALOG.SetSelection(index)

	def OnAddSubItem(self, event):
		index = self.getIndex()
		text = self.tab + self.getCatalogText(index)
		text = text.replace(self.getCatalogRealText(index), self.obj_ID_CATALOG_TEXT.GetValue())
		self.obj_ID_CATALOG.InsertItems([text], index+1)
		self.maxid += 1
		self.catalogitems.insert(index+1, (text, self.maxid))
		self.new.append(self.maxid)
		self.obj_ID_CATALOG.SetSelection(index + 1)

	def OnUpdate(self, event):
		index = self.getIndex()
		text = self.getCatalogText(index)
		text = text.replace(self.getCatalogRealText(index), self.obj_ID_CATALOG_TEXT.GetValue())
		self.obj_ID_CATALOG.SetString(index, text)
		self.catalogitems[index] = (text, self.catalogitems[index][1])

	def OnDelete(self, event):
		index = self.getIndex()
		if index < self.obj_ID_CATALOG.GetCount()-1:
			level = self.getLevel(index)
			if level < self.getLevel(index + 1):	#has child node, then popup a dialog
				wx.MessageDialog(self, tr("The node has child nodes, cann't be deleted!\nPlease delete child nodes first!"), tr("Delete Catalog"), wx.OK | wx.ICON_INFORMATION).ShowModal()
				return
		self.delete.append(self.catalogitems[index][1])
		del self.catalogitems[index]
		self.obj_ID_CATALOG.Delete(index)

	def OnUp(self, event):
		index = self.getIndex()
		up = self.getUpSibling(index)
		if up > -1:
			self.move(self.getNodeAndChilds(index), up)

	def OnDown(self, event):
		index = self.getIndex()
		down = self.getDownSibling(index)
		if down > -1:
			indexes = self.getNodeAndChilds(down)
			pos = indexes[-1]+1
			self.move(self.getNodeAndChilds(index), pos)

	def OnLeft(self, event):
		index = self.getIndex()
		level = self.getLevel(index)
		if level > 0:
			r = self.getNodeAndChilds(index)
			for i in r:
				text = self.getCatalogText(i)
				text = text[len(self.tab):]
				self.obj_ID_CATALOG.SetString(i, text)
				self.catalogitems[i] = (text, self.catalogitems[i][1])

	def OnRight(self, event):
		index = self.getIndex()
		level = self.getLevel(index)
		i = index - 1
		maxlevel = -1
		while i >= 0:
			maxlevel = max([self.getLevel(i), maxlevel])
			i -= 1
		if level < maxlevel + 1:
			r = self.getNodeAndChilds(index)
			for i in r:
				text = self.getCatalogText(i)
				text = self.tab + text
				self.obj_ID_CATALOG.SetString(i, text)
				self.catalogitems[i] = (text, self.catalogitems[i][1])

	def OnOk(self, event):
		self.save()
		self.Destroy()

	def OnCancel(self, event):
		self.Destroy()

	def OnApply(self, event):
		self.save()

	def save(self):
		SnippetClass.WriteSnippetCatalog(self.mainframe.snippet_catalogfile, self.maxid, self.listitems())
		for id in self.new:
			filename = getFilename(self.mainframe, id)
			SnippetClass.WriteSnippetCode(filename)

		for id in self.delete:
			filename = getFilename(self.mainframe, id)
			os.rename(filename, filename+'.bak')

		self.delete = []
		page = self.mainframe.panel.getPage(tr('Snippets'))
		if page:
			self.snippetswindow.catalog.loadData()

	def getLevel(self, index):
		text = self.getCatalogText(index)
		i = 0
		while text.startswith(self.tab):
			i += 1
			text = text[len(self.tab):]
		return i

	def getIndex(self):
		return self.obj_ID_CATALOG.GetSelection()

	def getNodeAndChilds(self, index):
		r = [index]
		level = self.getLevel(index)
		i = index + 1
		while i < self.obj_ID_CATALOG.GetCount():
			if level < self.getLevel(i):
				r.append(i)
				i += 1
			else:
				break
		return r

	def getUpSibling(self, index):
		i = index - 1
		level = self.getLevel(index)
		while i >= 0:
			if level == self.getLevel(i):
				return i
			i -= 1
		return -1

	def getDownSibling(self, index):
		i = index + 1
		level = self.getLevel(index)
		while i < self.obj_ID_CATALOG.GetCount():
			if level == self.getLevel(i):
				return i
			i += 1
		return -1

	def move(self, indexes, pos):
		items = []
		s = indexes[:]
		s.reverse()
		for index in s:
			self.obj_ID_CATALOG.Delete(index)
			items.append(self.catalogitems.pop(index))
		items.reverse()
		if pos > indexes[-1]:	#will insert after
			pos -= len(indexes)
		self.obj_ID_CATALOG.InsertItems([v[0] for v in items], pos)
		i = pos
		for item in items:
			self.catalogitems.insert(i, item)
			i += 1
		self.obj_ID_CATALOG.SetSelection(pos)

	def listitems(self):
		for i, v in enumerate(self.catalogitems):
			s, id = v
			yield self.getLevel(i), self.getCatalogRealText(i), str(id)

class SnippetsCodeDialog(wx.Dialog):
	def __init__(self, *args, **kwargs):
		wx.Dialog.__init__(self, *args, **kwargs)

	def init(self, mainframe):
		self.mainframe = mainframe
		self.pref = mainframe.pref
		self.xmlfile = ''

		self.obj_ID_OK.SetId(wx.ID_OK)
		self.obj_ID_CANCEL.SetId(wx.ID_CANCEL)

		self.loadcatalog()

		wx.EVT_CLOSE(self, self.OnClose)
		wx.EVT_LISTBOX(self.obj_ID_CATALOG, self.obj_ID_CATALOG.GetId(), self.OnCatalogSelected)
		wx.EVT_LISTBOX(self.obj_ID_CODES, self.obj_ID_CODES.GetId(), self.OnCodesSelected)
		wx.EVT_BUTTON(self.obj_ID_ADD, self.ID_ADD, self.OnAdd)
		wx.EVT_BUTTON(self.obj_ID_UPDATE, self.ID_UPDATE, self.OnUpdate)
		wx.EVT_BUTTON(self.obj_ID_DELETE, self.ID_DELETE, self.OnDelete)
		wx.EVT_BUTTON(self.obj_ID_OK, wx.ID_OK, self.OnOk)
		wx.EVT_BUTTON(self.obj_ID_CANCEL, wx.ID_CANCEL, self.OnCancel)
		wx.EVT_BUTTON(self.obj_ID_APPLY, self.ID_APPLY, self.OnApply)
		wx.EVT_BUTTON(self.obj_ID_DISCARD, self.ID_DISCARD, self.OnDiscard)
		wx.EVT_BUTTON(self.obj_ID_IMPORT, self.ID_IMPORT, self.OnImport)
		wx.EVT_BUTTON(self.obj_ID_EXPORT, self.ID_EXPORT, self.OnExport)
		wx.EVT_UPDATE_UI(self, self.ID_ADD, self.OnUpdateUI)
		wx.EVT_UPDATE_UI(self, self.ID_UPDATE, self.OnUpdateUI)
		wx.EVT_UPDATE_UI(self, self.ID_DELETE, self.OnUpdateUI)

		self.obj_ID_IMPORT.Enable(False)
		self.obj_ID_EXPORT.Enable(False)

	def loadcatalog(self):
		self.catalogitems = []
		snippet = SnippetClass.SnippetCatalog(self.mainframe.snippet_catalogfile)
		self.tab = '    '
		for i, v in enumerate(snippet):
			level, name, id = v
			s = self.tab * level + name
			self.obj_ID_CATALOG.InsertItems([s], i)
			self.catalogitems.append((s, id))

	def loadcodes(self, xmlfile):
		self.obj_ID_ABBR.SetValue('')
		self.obj_ID_DESCRIPTION.SetValue('')
		self.obj_ID_AUTHOR.SetValue('')
		self.obj_ID_VERSION.SetValue('')
		self.obj_ID_DATE.SetValue('')
		self.obj_ID_CODE.SetValue('')

		self.obj_ID_CODES.Clear()
		self.codes = {}
		snippet = SnippetClass.SnippetCode(xmlfile)
		for i, v in enumerate(snippet):
			abbr = v[0]
			self.codes[abbr] = v

		keys = self.codes.keys()
		keys.sort()
		for i, v in enumerate(keys):
			self.obj_ID_CODES.InsertItems([v], i)

	def OnUpdateUI(self, event):
		code_selected = self.obj_ID_CODES.GetSelection() > -1
		eid = event.GetId()
		if eid == self.ID_ADD:
			event.Enable(len(self.obj_ID_ABBR.GetValue()) > 0 and self.obj_ID_CATALOG.GetSelection() > -1)
		elif eid == self.ID_UPDATE:
			event.Enable(code_selected)
		elif eid == self.ID_DELETE:
			event.Enable(code_selected)

	def OnClose(self, event):
		self.Destroy()

	def OnOk(self, event):
		self.save()
		self.Destroy()

	def OnCancel(self, event):
		self.Destroy()

	def OnApply(self, event):
		self.save()
		self.obj_ID_CATALOG.Enable(True)

	def OnDiscard(self, event):
		self.obj_ID_CATALOG.Enable(True)
		self.loadcodes(self.xmlfile)

	def OnCatalogSelected(self, event):
		index = event.GetSelection()
		self.xmlfile = getFilename(self.mainframe, self.catalogitems[index][1])
		self.loadcodes(self.xmlfile)
		self.obj_ID_IMPORT.Enable(True)
		self.obj_ID_EXPORT.Enable(True)

	def OnCodesSelected(self, event):
		index = event.GetSelection()
		key = self.obj_ID_CODES.GetString(index)
		abbr, description, author, version, date, code = self.codes[key]
		self.obj_ID_ABBR.SetValue(abbr)
		self.obj_ID_DESCRIPTION.SetValue(description)
		self.obj_ID_AUTHOR.SetValue(author)
		self.obj_ID_VERSION.SetValue(version)
		self.obj_ID_DATE.SetValue(date)
		self.obj_ID_CODE.SetValue(code)

	def OnAdd(self, event):
		abbr = self.obj_ID_ABBR.GetValue()
		if self.codes.has_key(abbr):
			wx.MessageDialog(self, tr("The abbreviation has been added,\nPlease try another!"), tr("Add Code"), wx.OK | wx.ICON_INFORMATION).ShowModal()
			return
		self.codes[abbr] = (abbr, self.obj_ID_DESCRIPTION.GetValue(),
			self.obj_ID_AUTHOR.GetValue(), self.obj_ID_VERSION.GetValue(),
			self.obj_ID_DATE.GetValue(), self.obj_ID_CODE.GetValue())

		keys = self.codes.keys()
		keys.sort()
		index = keys.index(abbr)
		self.obj_ID_CODES.InsertItems([abbr], index)
		self.obj_ID_CODES.SetSelection(index)
		self.obj_ID_CATALOG.Enable(False)

	def OnUpdate(self, event):
		self.OnDelete(event)
		self.OnAdd(event)
		self.obj_ID_CATALOG.Enable(False)

	def OnDelete(self, event):
		index = self.getIndex()
		abbr = self.obj_ID_CODES.GetString(index)
		del self.codes[abbr]
		self.obj_ID_CODES.Delete(index)
		self.obj_ID_CATALOG.Enable(False)

	def getIndex(self):
		return self.obj_ID_CODES.GetSelection()

	def save(self):
		if self.obj_ID_CATALOG.GetSelection() > -1:
			SnippetClass.WriteSnippetCode(self.xmlfile, self.listitems())
			page = self.mainframe.panel.getPage(tr('Snippets'))
			if page:
				page.catalog.loadData()

	def listitems(self):
		for v in self.codes.values():
			yield v

	def OnImport(self, event):
		dlg = wx.FileDialog(self, tr("Select A File"), "", "", tr("Snippets code file (xml file)|*.*"), wx.OPEN|wx.HIDE_READONLY)
		if dlg.ShowModal() == wx.ID_OK:
			xmlfile = dlg.GetPath()
			dlg.Destroy()
			snippet = SnippetClass.SnippetCode(xmlfile)
			for i, v in enumerate(snippet):
				abbr = v[0]
				self.codes[abbr] = v

			self.obj_ID_CODES.Clear()
			keys = self.codes.keys()
			keys.sort()
			for i, v in enumerate(keys):
				self.obj_ID_CODES.InsertItems([v], i)
			self.obj_ID_CATALOG.Enable(False)

	def OnExport(self, event):
		dlg = wx.FileDialog(self, tr("Select A File"), "", "", tr("Snippets code file (xml file)|*.*"), wx.OPEN|wx.HIDE_READONLY)
		if dlg.ShowModal() == wx.ID_OK:
			xmlfile = dlg.GetPath()
			dlg.Destroy()
			SnippetClass.WriteSnippetCode(xmlfile, self.listitems())

def getFilename(mainframe, id):
	if id:
		return os.path.join(Globals.workpath, 'snippets/snippet%d.xml' % id)
	else:
		return ''