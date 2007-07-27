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
#	$Id: MyPanel.py 93 2005-10-11 02:51:02Z limodou $
#
#   This file's code is mostly copy from DrPython. Thanks to Daniel Pozmanter

import wx
from modules import Id
from modules import makemenu
from modules import Mixin

class SashPanel(wx.Panel):
	def __init__(self, parent, flag=None):
		wx.Panel.__init__(self, parent, -1)

		self.parent = parent
		self.mainframe = parent

		width, height = self.GetSizeTuple()

		self.pages = {}

		self.ID_TOP = Id.makeid(self, 'ID_TOP')
		self.ID_BOTTOM = Id.makeid(self, 'ID_BOTTOM')
		self.ID_LEFT = Id.makeid(self, 'ID_LEFT')
		self.ID_RIGHT = Id.makeid(self, 'ID_RIGHT')

		wx.EVT_SASH_DRAGGED(self, self.ID_TOP, self.OnSashDrag)
		wx.EVT_SASH_DRAGGED(self, self.ID_BOTTOM, self.OnSashDrag)
		wx.EVT_SASH_DRAGGED(self, self.ID_LEFT, self.OnSashDrag)
		wx.EVT_SASH_DRAGGED(self, self.ID_RIGHT, self.OnSashDrag)

		self.toptuple = (width, height)
		self.lefttuple = (0, 0)
		self.righttuple = (0, 0)
		self.bottomtuple = (0, 0)

		self.bottomsize = 50
		self.leftsize = 30
		self.rightsize = 10

		self.BottomIsVisible = False
		self.LeftIsVisible = False
		self.RightIsVisible = False

		self.top = wx.SashLayoutWindow(self, self.ID_TOP, wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER)

		self.top.SetDefaultSize((width, height))
		self.top.SetOrientation(wx.LAYOUT_HORIZONTAL)
		self.top.SetAlignment(wx.LAYOUT_TOP)

		self.bottom = wx.SashLayoutWindow(self, self.ID_BOTTOM, wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER)

		self.bottom.SetDefaultSize((width, height))
		self.bottom.SetOrientation(wx.LAYOUT_HORIZONTAL)
		self.bottom.SetAlignment(wx.LAYOUT_BOTTOM)
		self.bottom.SetSashVisible(wx.SASH_TOP, True)
		self.bottom.SetSashBorder(wx.SASH_TOP, True)

		self.left = wx.SashLayoutWindow(self, self.ID_LEFT, wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER)

		self.left.SetDefaultSize((100, 1000))
		self.left.SetOrientation(wx.LAYOUT_VERTICAL)
		self.left.SetAlignment(wx.LAYOUT_LEFT)
		self.left.SetSashVisible(wx.SASH_RIGHT, True)
		self.left.SetSashBorder(wx.SASH_RIGHT, True)

		self.right = wx.SashLayoutWindow(self, self.ID_RIGHT, wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER)

		self.right.SetDefaultSize((100, 1000))
		self.right.SetOrientation(wx.LAYOUT_VERTICAL)
		self.right.SetAlignment(wx.LAYOUT_RIGHT)
		self.right.SetSashVisible(wx.SASH_LEFT, True)
		self.right.SetSashBorder(wx.SASH_LEFT, True)

		wx.EVT_SIZE(self, self.OnSize)

		self.leftbook = None
		self.rightbook = None
		self.bottombook = None

	def OnSashDrag(self, event):
		evtheight = event.GetDragRect().height
		evtwidth = event.GetDragRect().width
		width, height = self.GetSizeTuple()
		if (evtwidth < 0):
			evtwidth = 0
		elif (evtwidth > width):
			evtwidth = width
		if event.GetDragStatus() == wx.SASH_STATUS_OUT_OF_RANGE:
			if (not self.BottomIsVisible) or (evtheight < height):
				evtheight = 0
			else:
				evtheight = height
		elif evtheight > height:
			evtheight = height

		oldsize = self.bottomsize
		loldsize = self.leftsize
		roldsize = self.rightsize

		e = event.GetId()
		edge = event.GetEdge()
		if e == self.ID_TOP:
			if edge == wx.SASH_BOTTOM:
				self.top.SetDefaultSize((width, evtheight))
				self.bottom.SetDefaultSize((width, height-evtheight))
				self.bottomsize = ((height*100) - (evtheight*100)) / height
				self.toptuple = (self.toptuple[0], evtheight)
				self.bottomtuple = (self.bottomtuple[0], height-evtheight)
			elif edge == wx.SASH_LEFT:
				if self.RightIsVisible:
					evtwidth = evtwidth + self.righttuple[0]
				self.top.SetDefaultSize((evtwidth, height))
				self.left.SetDefaultSize((width-evtwidth, height))
				self.lefttuple = (width-evtwidth, height)
				self.toptuple = (evtwidth, self.toptuple[1])
				self.leftsize = ((width*100) - (evtwidth*100)) / width
			elif edge == wx.SASH_RIGHT:
				if self.LeftIsVisible:
					evtwidth = evtwidth + self.lefttuple[0]
				self.top.SetDefaultSize((evtwidth, height))
				self.right.SetDefaultSize((width-evtwidth, height))
				self.righttuple = (width-evtwidth, height)
				self.toptuple = (evtwidth, self.toptuple[1])
				self.rightsize = ((width*100) - (evtwidth*100)) / width
		elif e == self.ID_BOTTOM:
			self.top.SetDefaultSize((width, height-evtheight))
			self.bottomsize = ((evtheight*100) / height)
		elif e == self.ID_LEFT:
			if self.LeftIsVisible:
				if self.lefttuple[0] == evtwidth:
					evtwidth = 0
			self.top.SetDefaultSize((width-evtwidth, height))
			self.left.SetDefaultSize((evtwidth, height))
			self.lefttuple = (evtwidth, height)
			self.toptuple = (width-evtwidth, self.toptuple[1])
			self.leftsize = (evtwidth*100) / width
		elif e == self.ID_RIGHT:
			if self.RightIsVisible:
				if self.righttuple[0] == evtwidth:
					evtwidth = 0
			self.top.SetDefaultSize((width-evtwidth, height))
			self.right.SetDefaultSize((evtwidth, height))
			self.righttuple = (evtwidth, height)
			self.toptuple = (width-evtwidth, self.toptuple[1])
			self.rightsize = (evtwidth*100) / width
		if self.bottomsize == 0:
			self.bottomsize = oldsize
			self.BottomIsVisible = False
		elif not self.BottomIsVisible and self.bottomtuple[1] > 0:
			self.BottomIsVisible = True

		if self.leftsize == 0:
			self.leftsize = loldsize
			self.LeftIsVisible = False
		elif not self.LeftIsVisible and self.lefttuple[0] > 0:
			self.LeftIsVisible = True

		if self.rightsize == 0:
			self.rightsize = roldsize
			self.RightIsVisible = False
		elif not self.RightIsVisible and self.righttuple[0] > 0:
			self.RightIsVisible = True

		self.OnSize(event)
		self.Refresh()

	def OnSize(self, event):
		width, height = self.GetSizeTuple()
		if self.BottomIsVisible:
			heightDocument = (height * (100 - self.bottomsize)) / 100
			heightPrompt = (height * self.bottomsize) / 100
		else:
			heightDocument = height
			heightPrompt = 0
		if self.LeftIsVisible and self.RightIsVisible:
			w = (width * (100 - self.leftsize - self.rightsize)) / 100
		elif self.LeftIsVisible:
			w = (width * (100 - self.leftsize)) / 100
		elif self.RightIsVisible:
			w = (width * (100 - self.rightsize)) / 100
		else:
			w = width
		wl = 0
		wr = 0
		if self.LeftIsVisible:
			wl = (width * self.leftsize) / 100
		if self.RightIsVisible:
			wr = (width * self.rightsize) / 100

		self.toptuple = (w, heightDocument)
		self.lefttuple = (wl, height)
		self.righttuple = (wr, height)
		self.bottomtuple = (w, heightPrompt)

		self.top.SetDefaultSize(self.toptuple)
		self.bottom.SetDefaultSize(self.bottomtuple)
		self.left.SetDefaultSize(self.lefttuple)
		self.right.SetDefaultSize(self.righttuple)
		wx.LayoutAlgorithm().LayoutWindow(self, self.top)

	def showWindow(self, panelname, showflag):
		name = panelname.lower()

		if name == 'left':
			self.LeftIsVisible = showflag
		elif name == 'right':
			self.RightIsVisible = showflag
		elif name == 'bottom':
			self.BottomIsVisible = showflag

		self.OnSize(None)
		self.Refresh()

	def showPage(self, name):
		if self.leftbook and self.leftbook.getPageIndex(name) > -1:
			self.showWindow('left', True)
			self.leftbook.showPage(name)
			return

		if self.rightbook and self.rightbook.getPageIndex(name) > -1:
			self.showWindow('right', True)
			self.rightbook.showPage(name)
			return

		if self.bottombook and self.bottombook.getPageIndex(name) > -1:
			self.showWindow('bottom', True)
			self.bottombook.showPage(name)
			return

	def getNotebook(self, name):
		name = name.lower()
		if name == 'left':
			return self.leftbook
		elif name == 'right':
			return self.rightbook
		elif name == 'bottom':
			return self.bottombook

	def delNotebook(self, name):
		name = name.lower()
		if name == 'left':
			self.leftbook.Destroy()
			self.leftbook = None
		elif name == 'right':
			self.rightbook.Destroy()
			self.rightbook = None
		elif name == 'bottom':
			self.bottombook.Destroy()
			self.bottombook = None

	def createNotebook(self, name):
		name = name.lower()
		if name == 'left':
			if not self.leftbook:
				self.leftbook = Notebook(self.left, self, name)
			return self.leftbook
		elif name == 'right':
			notebook = self.rightbook
			if not self.rightbook:
				self.rightbook = Notebook(self.right, self, name)
			return self.rightbook
		elif name == 'bottom':
			notebook = self.bottombook
			if not self.bottombook:
				self.bottombook = Notebook(self.bottom, self, name, style=wx.NB_BOTTOM)
			return self.bottombook

	def addPage(self, panelname, page, name):
		pname = panelname.lower()
		notebook = self.getNotebook(panelname)
		notebook.addPage(page, name)
		self.pages[name] = (pname, notebook, page)

	def delPage(self, side, name):
		notebook = self.getNotebook(side)
		if self.pages.has_key(name):
			del self.pages[name]
		if notebook.GetPageCount() == 0:
			self.delNotebook(side)
			self.showWindow(side, False)

	def closePage(self, name):
		if self.pages.has_key(name):
			notebook = self.pages[name][1]
			return notebook.closePage(name)

	def getPage(self, name):
		if self.pages.has_key(name):
			return self.pages[name][2]
		else:
			return None

class Notebook(wx.Notebook, Mixin.Mixin):
	__mixinname__ = 'notebook'
	popmenulist = [ (None,
	[
		(100, 'IDPM_CLOSE', tr('Close'), wx.ITEM_NORMAL, 'OnDClick', tr('Closes an opened window.')),
		(110, '', '-', wx.ITEM_SEPARATOR, None, ''),
	]),
]
	imagelist = {}

	def __init__(self, parent, panel, side, style=0):
		self.initmixin()

		wx.Notebook.__init__(self, parent, -1, style=style)
		self.parent = parent
		self.panel = panel
		self.side = side
		self.mainframe = self.panel.mainframe

		self.popmenu = makemenu.makepopmenu(self, self.popmenulist, self.imagelist)
		wx.EVT_LEFT_UP(self, self.OnPageChanged)
		wx.EVT_LEFT_DCLICK(self, self.OnDClick)
		wx.EVT_RIGHT_DOWN(self, self.OnPopUp)

	def OnPageChanged(self, event):
		self.GetPage(self.GetSelection()).SetFocus()
		event.Skip()

	def OnDClick(self, event):
		name = self.GetPageText(self.GetSelection())
		self.closePage(name)

	def OnPopUp(self, event):
		self.PopupMenu(self.popmenu, event.GetPosition())

	def closePage(self, name):
		index = self.getPageIndex(name)
		if index > -1:
			page = self.GetPage(index)
			if hasattr(page, 'canClose'):
				if page.canClose():
					self.DeletePage(index)
					self.panel.delPage(self.side, name)
			else:
				self.DeletePage(index)
				self.panel.delPage(self.side, name)
			return True
		else:
			return False

	def addPage(self, page, name):
		self.AddPage(page, name)

	def showPage(self, name):
		index = self.getPageIndex(name)
		if index > -1:
			self.SetSelection(index)
			self.GetPage(index).SetFocus()
			return True
		else:
			return False

	def getPageIndex(self, name):
		for i in range(self.GetPageCount()):
			if self.GetPageText(i) == name:
				return i
		else:
			return -1

