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
#	$Id: PluginDialog.py 481 2006-01-17 05:54:13Z limodou $

import wx
import glob
import os.path
import re
from modules import dict4ini
from modules import CheckList

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

		box = wx.BoxSizer(wx.VERTICAL)
		self.list = CheckList.CheckList(self, columns=[
			(tr("Name"), 80, 'left'),
			(tr("Description"), 150, 'left'),
			(tr("Author"), 80, 'right'),
			(tr("Version"), 40, 'right'),
			(tr("Date"), 80, 'right'),
			], style=wx.LC_REPORT | wx.SUNKEN_BORDER)
		self.list.load(self.getdata)

		box.Add(self.list, 1, wx.EXPAND|wx.ALL, 5)
		box2 = wx.BoxSizer(wx.HORIZONTAL)
		self.btnOK = wx.Button(self, wx.ID_OK, tr("OK"), size=(80, -1))
		self.btnOK.SetDefault()
		box2.Add(self.btnOK, 0, 0, 5)
		self.btnCancel = wx.Button(self, wx.ID_CANCEL, tr("Cancel"), size=(80, -1))
		box2.Add(self.btnCancel, 0, 0, 5)
		box.Add(box2, 0, wx.ALIGN_CENTER|wx.ALL, 5)

		wx.EVT_LIST_ITEM_ACTIVATED(self.list, self.list.GetId(), self.OnEnter)
		wx.EVT_BUTTON(self.btnOK, wx.ID_OK, self.OnOK)

		self.SetSizer(box)
		self.SetAutoLayout(True)

	def getdata(self):
		s = self.plugins.keys()
		s.sort()
		for i, name in enumerate(s):
			ini = dict4ini.DictIni(self.plugins[name])
			description = ini.info.description or ''
			author = ini.info.author or ''
			version = ini.info.version or ''
			date = ini.info.date or ''
			yield (self.state[name], (unicode(name, 'utf-8'), unicode(description, 'utf-8'),
				unicode(author, 'utf-8'), unicode(version, 'utf-8'), unicode(date, 'utf-8')))

	def OnEnter(self, event):
		index =  event.GetSelection()
		self.list.notFlag(index)

	def OnOK(self, event):
		for flag, v in self.list.GetValue():
			self.state[v[0]] = flag
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