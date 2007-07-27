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
#	$Id: MessageWindow.py 93 2005-10-11 02:51:02Z limodou $

__doc__ = 'message window'

from modules import Mixin
import wx
import wx.stc

class MessageWindow(wx.stc.StyledTextCtrl, Mixin.Mixin):
	__mixinname__ = 'messagewindow'

	def __init__(self, parent, mainframe):
		self.initmixin()

		wx.stc.StyledTextCtrl.__init__(self, parent, -1)
		self.parent = parent
		self.mainframe = mainframe
		self.SetMarginWidth(0, 0)
		self.SetMarginWidth(1, 0)
		self.SetMarginWidth(2, 0)
		font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
		self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, "face:%s,size:10" % font.GetFaceName())

		self.SetScrollWidth(1)
		self.maxline = 'WWWW'
		wx.stc.EVT_STC_MODIFIED(self, self.GetId(), self.OnModified)

		self.callplugin('init', self)

	def SetText(self, text):
		ro = self.GetReadOnly()
		self.SetReadOnly(0)
		wx.stc.StyledTextCtrl.SetText(self, text)
		self.SetReadOnly(ro)

	def SetSelectedText(self, text):
		ro = self.GetReadOnly()
		self.SetReadOnly(0)
		self.SetTargetStart(self.GetSelectionStart())
		self.SetTargetEnd(self.GetSelectionEnd())
		self.ReplaceTarget(text)
		self.SetReadOnly(ro)

	def setWidth(self, text=''):
		if not text:
			text = self.maxline
		if self.GetWrapMode() == wx.stc.STC_WRAP_NONE:
			ll = self.TextWidth(wx.stc.STC_STYLE_DEFAULT, "W")*4
			line = text.expandtabs(self.GetTabWidth())
			current_width = self.GetScrollWidth()
			width = self.TextWidth(wx.stc.STC_STYLE_DEFAULT, line)
			if width>current_width:
				self.maxline = line
				self.SetScrollWidth(width + ll)

	def OnModified(self, event):
		self.setWidth(self.GetCurLine()[0])

	def canClose(self):
		return True

