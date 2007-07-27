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
#	$Id: FindInFiles.py 481 2006-01-17 05:54:13Z limodou $

import wx
import os, fnmatch
import re

class FindInFiles(wx.Dialog):
	def __init__(self, parent, pref):
		wx.Dialog.__init__(self, parent, -1, tr("Find in files..."), size=(600,400),
						  style=wx.RESIZE_BORDER|wx.DEFAULT_DIALOG_STYLE)

		self.parent = parent
		self.mainframe = parent
		self.pref = pref

		self.running = 0
		self.stopping = 0
		self.starting = 0

		box = wx.BoxSizer(wx.VERTICAL)

		txt = wx.StaticText(self, -1, tr("Multiple directories or extensions should be separated by semicolons ';'"))
		box.Add(txt, 0, wx.ALL, 4)

		box1 = wx.BoxSizer(wx.HORIZONTAL)

		txt = wx.StaticText(self, -1, tr("Search for:"), size=(100, -1))
		box1.Add(txt, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 2)

		self.search = wx.ComboBox(self, -1, choices=self.pref.searchinfile_searchlist, style=wx.CB_DROPDOWN)
		text = self.mainframe.document.GetSelectedText()
		if text and len(text.splitlines()) == 1:
			self.search.SetValue(text)
		else:
			self.search.SetSelection(0)
		box1.Add(self.search, 1, wx.RIGHT, 2)

		box.Add(box1, 0, wx.ALL|wx.EXPAND, 4)

		box1 = wx.BoxSizer(wx.HORIZONTAL)

		txt = wx.StaticText(self, -1, tr("Directories:"), size=(100, -1))
		box1.Add(txt, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 2)

		self.sdirs = wx.ComboBox(self, -1, choices=self.pref.searchinfile_dirlist, style=wx.CB_DROPDOWN)
		self.sdirs.SetSelection(0)
		box1.Add(self.sdirs, 1, wx.RIGHT, 2)

		self.ID_BROW = wx.NewId()
		self.btnBrow = wx.Button(self, self.ID_BROW, tr("Add Path"), size=(80, -1))
		box1.Add(self.btnBrow)

		box.Add(box1, 0, wx.ALL|wx.EXPAND, 4)

		box1 = wx.BoxSizer(wx.HORIZONTAL)

		txt = wx.StaticText(self, -1, tr("Extensions:"), size=(100, -1))
		box1.Add(txt, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 2)

		self.extns = wx.ComboBox(self, -1, choices=self.pref.searchinfile_extlist, style=wx.CB_DROPDOWN)
		if self.pref.searchinfile_extlist:
			self.extns.SetValue('*.*')
		box1.Add(self.extns, 1, wx.RIGHT, 2)

		box.Add(box1, 0, wx.ALL|wx.EXPAND, 4)

		box1 = wx.BoxSizer(wx.HORIZONTAL)

		self.cs = wx.CheckBox(self, -1, tr("Case sensitive"))
		self.cs.SetValue(self.pref.searchinfile_case)
		box1.Add(self.cs, 1)

		self.ss = wx.CheckBox(self, -1, tr("Search Subdirectories"))
		self.ss.SetValue(self.pref.searchinfile_subdir)
		box1.Add(self.ss, 1)

		self.re = wx.CheckBox(self, -1, tr("Regular Expression"))
		self.re.SetValue(self.pref.searchinfile_regular)
		box1.Add(self.re, 1)

		box.Add(box1, 0, wx.ALL|wx.EXPAND, 4)

		self.ID_LIST = wx.NewId()
		self.results = wx.ListBox(self, self.ID_LIST, style=wx.LB_SINGLE|wx.LB_NEEDED_SB)
		box.Add(self.results, 1, wx.EXPAND, 4)

		box1 = wx.BoxSizer(wx.HORIZONTAL)

		txt = wx.StaticText(self, -1, tr('Status:'), size=(100, -1))
		box1.Add(txt, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 2)
		self.status = wx.TextCtrl(self, -1, tr("Ready."))
		box1.Add(self.status, 1, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 2)
		self.status.Enable(False)

		self.ID_RUN = wx.NewId()
		self.btnRun = wx.Button(self, self.ID_RUN, tr("Start Search"))
		box1.Add(self.btnRun, 0, wx.ALIGN_CENTER_VERTICAL)

		box.Add(box1, 0, wx.ALL|wx.EXPAND, 4)

		self.SetSizer(box)
		self.SetAutoLayout(True)

		wx.EVT_BUTTON(self, self.ID_BROW, self.OnDirButtonClick)
		wx.EVT_LISTBOX_DCLICK(self.results, self.ID_LIST, self.OpenFound)
		wx.EVT_BUTTON(self.btnRun, self.ID_RUN, self.OnFindButtonClick)
		tid = wx.NewId()
		self.timer = wx.Timer(self, tid)
		wx.EVT_TIMER(self, tid, self.OnFindButtonClick)

	def OpenFound(self, e):
		selected = self.results.GetSelection()
		if selected < 0:
			return
		cur = selected
		while (cur > 0) and (self.results.GetString(cur)[0] == ' '):
			cur -= 1
		fn = self.results.GetString(cur)
		line = 1
		a = self.results.GetString(selected)
		if a[0] == ' ':
			line = int(a.split(':', 1)[0])

		self.mainframe.editctrl.new(fn)
		self.mainframe.document.goto(line)

	def OnDirButtonClick(self, e):
		dlg = wx.DirDialog(self, tr("Choose a directory"), defaultPath = self.pref.searchinfile_defaultpath, style=wx.DD_DEFAULT_STYLE)
		a = dlg.ShowModal()
		if a == wx.ID_OK:
			a = self.sdirs.GetValue()
			if a:
				self.sdirs.SetValue(a+';'+dlg.GetPath())
			else:
				self.sdirs.SetValue(dlg.GetPath())
			self.pref.searchinfile_defaultpath = dlg.GetPath()
			self.pref.save()
		dlg.Destroy()

	def OnFindButtonClick(self, e):
		if self.stopping:
			#already stopping
			return

		elif self.running:
			#running, we want to try to stop
			self.stopping = 1
			self.status.SetValue(tr("Stopping...please wait."))
			self.btnRun.SetLabel("Start Search")
			return

		if e.GetId() == self.ID_RUN:
			if self.starting:
				#previously was waiting to start due to an
				#external yield, abort waiting and cancel
				#search
				self.starting = 0
				self.status.SetValue(tr("Search cancelled."))
				self.btnRun.SetLabel(tr("Start Search"))
				return
		elif not self.starting:
			#I was a waiting timer event, but I don't
			#need to start anymore
			return

		#try to start
		self.starting = 1
		self.btnRun.SetLabel(tr("Stop Search"))

		try:
			wx.Yield()
		except:
			#would have tried to start while in another function's
			#wx.Yield() call.  Will wait 100ms and try again
			self.status.SetValue(tr("Waiting for another process to stop, please wait."))
			self.timer.Start(100, wx.TIMER_ONE_SHOT)
			return

		#am currently the topmost call, so will continue.
		self.starting = 0
		self.running = 1
		wx.Yield()

		def getlist(c):
			cc = c.GetCount()
			e = [c.GetString(i) for i in xrange(cc)]
			a = c.GetValue()
			if a in e:
				e.remove(a)
			e = [a] + e
			e = e[:10]
			if len(e) > cc:
				c.Append(e[-1])
			for i in xrange(len(e)):
				c.SetString(i, e[i])
			c.SetSelection(0)
			return e

		self.pref.searchinfile_searchlist = getlist(self.search)
		self.pref.searchinfile_dirlist = getlist(self.sdirs)
		self.pref.searchinfile_extlist = getlist(self.extns)
		self.pref.searchinfile_case = self.cs.IsChecked()
		self.pref.searchinfile_subdir = self.ss.IsChecked()
		self.pref.searchinfile_regular = self.re.IsChecked()
		self.pref.save()

		search = self.search.GetValue()
		paths = self.sdirs.GetValue().split(';')
		extns = self.extns.GetValue().split(';') or ['*.*']
		case = self.cs.IsChecked()
		subd = self.ss.IsChecked()

		sfunct = self.searchST
		if self.re.IsChecked():
			sfunct = self.searchRE
			if case:
				search = re.compile(search)
			else:
				search = re.compile(search, re.IGNORECASE)

		results = self.results
		results.Clear()

		def file_iterator(path, subdirs, extns):
			try:    lst = os.listdir(path)
			except: return
			d = []
			for file in lst:
				a = os.path.join(path, file)
				if os.path.isfile(a):
					for extn in extns:
						if fnmatch.fnmatch(file, extn):
							yield a
							break
				elif subdirs and os.path.isdir(a):
					d.append(a)
			if not subdirs:
				return
			for p in d:
				for f in file_iterator(p, subdirs, extns):
					yield f

		filecount = 0
		filefcount = 0
		foundcount = 0
		ss = tr("Found %i instances in %i files out of %i files checked.")
		for path in paths:
			wx.Yield()
			if not self.running:
				break
			for filename in file_iterator(path, subd, extns):
				wx.Yield()
				filecount += 1
				if not self.stopping:
					r = sfunct(filename, search, case)
					if r:
						try:
							for a in r:
								results.Append(a)
						except:
							#for platforms with limited sized
							#wx.ListBox controls
							pass
						filefcount += 1
						foundcount += len(r)-1
					self.status.SetValue((ss % (foundcount, filefcount, filecount)) + tr('...searching...'))
				else:
					break
		if self.stopping:
			self.stopping = 0
			ex = tr('...cancelled.')
			#was stopped by a button press
		else:
			self.running = 0
			ex = tr('...done.')
		self.btnRun.SetLabel(tr("Start Search"))
		self.status.SetValue((ss%(foundcount, filefcount, filecount)) + ex)
		self.stopping = 0
		self.running = 0
		self.starting = 0

	def searchST(self, filename, pattern, casesensitive):
		try:
			lines = open(filename, 'r').readlines()
		except:
			lines = []
		found = []
		if not casesensitive:
			pattern = pattern.lower()
		spt = self.pref.tabwidth*' '
		for i in range(len(lines)):
			try:
				if not casesensitive:
					line = lines[i].lower()
				else:
					line = lines[i]
				if line.find(pattern) > -1:
					if not found:
						found.append(filename)
					found.append('  '+`i+1` + ': '+lines[i].rstrip().replace('\t', spt))
			except: pass
			wx.Yield()
		return found

	def searchRE(self, filename, pattern, toss):
		try:
			lines = open(filename, 'r').readlines()
		except:
			lines = []
		found = []
		spt = self.pref.tabwidth*' '
		for i in range(len(lines)):
			try:
				line = lines[i]
				if pattern.search(line) is not None:
					if not found:
						found.append(filename)
					found.append('  '+`i+1` + ': '+line.rstrip().replace('\t', spt))
			except: pass
			wx.Yield()
		return found