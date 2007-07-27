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
#	$Id: QuoteDialog.py 176 2005-11-22 02:46:37Z limodou $

import wx

quote_string = [
	('\'', '\''),
	('"', '"'),
	("'''", "'''"),
	('"""', '"""'),
	('(', ')'),
	('[', ']'),
	('{', '}'),
	('<', '>'),
	('/*', '*/')
	]
class MyQuoteDialog(wx.Dialog):
	def __init__(self, *args, **kwargs):
		wx.Dialog.__init__(self, *args, **kwargs)

	def init(self, win):
		self.win = win
		self.obj_ID_OK.SetId(wx.ID_OK)
		self.obj_ID_CANCEL.SetId(wx.ID_CANCEL)
		wx.EVT_BUTTON(self, wx.ID_OK, self.OnOK)
		wx.EVT_CHECKBOX(self, self.ID_USER, self.OnCheckUser)

		self.setValue()

	def setValue(self):
		self.obj_ID_USER.SetValue(self.win.quote_user)
		self.obj_ID_START.SetValue(self.win.quote_start)
		self.obj_ID_END.SetValue(self.win.quote_end)
		self.obj_ID_KIND.SetSelection(self.win.quote_index)
		self.obj_ID_KIND.Enable(not self.win.quote_user)

	def getValue(self):
		self.win.quote_user = self.obj_ID_USER.GetValue()
		self.win.quote_start = self.obj_ID_START.GetValue()
		self.win.quote_end = self.obj_ID_END.GetValue()
		self.win.quote_index = self.obj_ID_KIND.GetSelection()

	def OnOK(self, event):
		self.getValue()
		event.Skip()

	def OnCheckUser(self, event):
		self.obj_ID_KIND.Enable(not self.obj_ID_USER.GetValue())