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
#	$Id: EncodingDialog.py 475 2006-01-16 09:50:28Z limodou $

__doc__ = 'Encoding selection dialog'

import wx

class EncodingDialog(wx.Dialog):
	EncodingList = [
		(tr('Default'),''),
		('UTF-8','utf-8'),
		('Base64','base64'),
		('Ascii','ascii'),
		('ISO_8859_1','latin_1'),
		('JIS','jis_7'),
		('KOI','kio8_r'),
		('GBK','cp936'),
	]

	def __init__(self, *args, **kwargs):
		wx.Dialog.__init__(self, *args, **kwargs)

	def init(self, mainframe):
		self.mainframe = mainframe
		self.pref = mainframe.pref

		self.obj_ID_OK.SetId(wx.ID_OK)
		self.obj_ID_CANCEL.SetId(wx.ID_CANCEL)

		self.setValue()

		wx.EVT_RADIOBUTTON(self.obj_ID_R_ENCODING, self.ID_R_ENCODING, self.OnRadio)
		wx.EVT_RADIOBUTTON(self.obj_ID_R_CUSTOM, self.ID_R_CUSTOM, self.OnRadio)
		wx.EVT_BUTTON(self.obj_ID_OK, wx.ID_OK, self.OnOk)
		wx.EVT_BUTTON(self.obj_ID_CANCEL, wx.ID_CANCEL, self.OnCancel)
		wx.EVT_CLOSE(self, self.OnClose)

	def setValue(self):
		self.encodings = {}
		for key, encoding in self.EncodingList:
			self.obj_ID_ENCODING.Append(key)
			self.encodings[key] = encoding

		self.obj_ID_ENCODING.SetSelection(0)

		self.obj_ID_ENCODING.Enable(True)
		self.obj_ID_CUSTOM.Enable(False)

	def OnRadio(self, event):
		eid = event.GetId()
		if eid == self.ID_R_ENCODING:
			self.obj_ID_ENCODING.Enable(True)
			self.obj_ID_CUSTOM.Enable(False)
		elif eid == self.ID_R_CUSTOM:
			self.obj_ID_ENCODING.Enable(False)
			self.obj_ID_CUSTOM.Enable(True)

	def GetValue(self):
		if self.obj_ID_R_ENCODING.GetValue():
			return self.encodings[self.obj_ID_ENCODING.GetValue()]
		else:
			return self.obj_ID_CUSTOM.GetValue()

	def OnClose(self, event):
		self.Destroy()

	def OnOk(self, event):
		event.Skip()
		self.Destroy()

	def OnCancel(self, event):
		event.Skip()
		self.Destroy()