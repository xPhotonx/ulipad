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
#	$Id: PluginDialog.py 93 2005-10-11 02:51:02Z limodou $

import wx
import glob
import os.path
import re
from modules import dict4ini

class PluginDialog(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, -1, tr('Plugin Manage'), size=(500, 300))
		self.parent = parent
		self.mainframe = parent
		self.state = {}

		self.plugins = self.loadPlugins()
		for key in self.plugins.keys():
			self.state[key] = False
		text = file(self.mainframe.plugin_initfile).read()
		re_i = re.compile("^\timport\s+(\w+)$", re.M)
		result = re_i.findall(text)
		for key in result:
			self.state[key] = True

		self.imagel = wx.ImageList(16, 16)
		imagelist = self.mainframe.plugin_imagelist
		self.uncheck_state = self.imagel.Add(wx.Image(imagelist['uncheck']).ConvertToBitmap())
		self.check_state = self.imagel.Add(wx.Image(imagelist['check']).ConvertToBitmap())

		box = wx.BoxSizer(wx.VERTICAL)
		self.list = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
		self.list.SetImageList(self.imagel, wx.IMAGE_LIST_SMALL)
		self.list.InsertColumn(0, "")
		self.list.InsertColumn(1, tr("Name"))
		self.list.InsertColumn(2, tr("Description"))
		self.list.InsertColumn(3, tr("Author"))
		self.list.InsertColumn(4, tr("Version"))
		self.list.InsertColumn(5, tr("Date"))
		self.list.SetColumnWidth(0, 22)
		self.list.SetColumnWidth(1, 150)
		self.list.SetColumnWidth(2, 330)
		s = self.plugins.keys()
		s.sort()
		for i, name in enumerate(s):
			ini = dict4ini.DictIni(self.plugins[name])
			description = ini.info.description or ''
			author = ini.info.author or ''
			version = ini.info.version or ''
			date = ini.info.date or ''
			if self.state[name]:
				self.list.InsertImageItem(i, 1)
			else:
				self.list.InsertImageItem(i, 0)
			self.list.SetStringItem(i, 1, unicode(name, 'utf-8'))
			self.list.SetStringItem(i, 2, unicode(description, 'utf-8'))
			self.list.SetStringItem(i, 3, unicode(author, 'utf-8'))
			self.list.SetStringItem(i, 4, unicode(version, 'utf-8'))
			self.list.SetStringItem(i, 5, unicode(date, 'utf-8'))

		box.Add(self.list, 1, wx.EXPAND|wx.ALL, 5)
		box2 = wx.BoxSizer(wx.HORIZONTAL)
		self.ID_TOGGLE = wx.NewId()
		self.btnToggle = wx.Button(self, self.ID_TOGGLE, tr("Select Toggle"), size=(100, 20))
		box2.Add(self.btnToggle, 0, 0, 5)
		self.btnOK = wx.Button(self, wx.ID_OK, tr("OK"), size=(80, 20))
		self.btnOK.SetDefault()
		box2.Add(self.btnOK, 0, 0, 5)
		self.btnCancel = wx.Button(self, wx.ID_CANCEL, tr("Cancel"), size=(80, 20))
		box2.Add(self.btnCancel, 0, 0, 5)
		box.Add(box2, 0, wx.ALIGN_CENTER|wx.ALL, 5)

		wx.EVT_LIST_ITEM_SELECTED(self.list, self.list.GetId(), self.OnItemSelected)
		wx.EVT_LIST_ITEM_DESELECTED(self.list, self.list.GetId(), self.OnItemDeselected)
		wx.EVT_LIST_ITEM_ACTIVATED(self.list, self.list.GetId(), self.OnEnter)
		self.btnToggle.Enable(False)
		wx.EVT_BUTTON(self.btnOK, wx.ID_OK, self.OnOK)
		wx.EVT_BUTTON(self.btnToggle, self.ID_TOGGLE, self.OnToggle)

		self.SetSizer(box)
		self.SetAutoLayout(True)

	def OnItemSelected(self, event):
		self.btnToggle.Enable(True)

	def OnItemDeselected(self, event):
		self.btnToggle.Enable(False)

	def OnToggle(self, event):
		index = self.list.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
		s = self.plugins.keys()
		s.sort()
		flag = self.state[s[index]]
		self.state[s[index]] = not flag
		if not flag:
			self.list.SetItemImage(index, self.check_state, self.check_state)
		else:
			self.list.SetItemImage(index, self.uncheck_state, self.uncheck_state)

	def OnEnter(self, event):
		self.OnToggle(event)

	def OnOK(self, event):
		text = file(self.mainframe.plugin_initfile).read()
		pos1 = text.find('from')
		pos2 = text.find('import')
		pos = min([pos1, pos2])
		if pos:
			text = text[:pos]
		file(self.mainframe.plugin_initfile, 'w').write(text + "from modules.Debug import error\nflag=False\n" + '\n'.join(["""
try:
	import %s
except:
	error.traceback()
	flag = True
""" % s for s in self.plugins if self.state[s]]) + """
if flag:
	raise Exception
""")
		self.copy_mo()
		event.Skip()

	def loadPlugins(self):
		files = glob.glob(os.path.join(self.mainframe.workpath, 'plugins/*/*.pin'))
		plugins = {}
		for f in files:
			plugins[os.path.basename(os.path.dirname(f))] = f
		return plugins

	def copy_mo(self):
		files = glob.glob(os.path.join(self.mainframe.workpath, 'plugins/*/*.mo'))
		import shutil
		for f in files:
			fname = os.path.splitext(os.path.basename(f))[0]
			lang = fname.split('_', 1)[1]
			dst = os.path.join(self.mainframe.workpath, 'lang', lang, os.path.basename(f))
			shutil.copyfile(f, dst)
		
