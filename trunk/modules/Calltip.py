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
#	$Id: Calltip.py 481 2006-01-17 05:54:13Z limodou $

import wx

class MyCallTip(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, -1, size=(200, 50), style=wx.SIMPLE_BORDER |wx.NO_3D)
		self.Enable(False)
		self.parent = parent
		self.text = wx.StaticText(self, -1, label='', pos=(3, 3))
#		self.bgcolor = 'yellow'
		self.bgcolor = '#FFFFE1'

		self.active = False
		self.Hide()

	def show(self, pos, text):
		self.text.SetLabel(text.strip())
		w, h = self.text.GetBestSize()
		self.SetSize((w+8, h+8))
		x, y = self.parent.PointFromPosition(pos)
		dh = self.parent.TextHeight(self.parent.LineFromPosition(pos))
		cw, ch = self.parent.GetClientSize()
		if y + dh + h > ch:
			y -= h + 8
		else:
			y += dh
		self.Move((x, y))
		self.active = True
		self.SetBackgroundColour(self.bgcolor)
		self.text.SetBackgroundColour(self.bgcolor)
		self.Show()
		self.parent.SetFocus()

	def cancel(self):
		if self.active:
			self.Hide()
			self.active = False

	def setHightLight(self, start, end):
		pass