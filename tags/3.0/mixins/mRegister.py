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
#	$Id: mRegister.py 93 2005-10-11 02:51:02Z limodou $

import wx

if wx.Platform == '__WXMSW__':
	from modules import Mixin
	from modules.Debug import error
	import os.path
	import sys

	import _winreg

	menulist = [ ('IDM_OPTION',
	[
		(120, 'IDM_OPTION_REGISTER', tr('Register to Explore'), wx.ITEM_NORMAL, 'OnOptionRegister', tr('Registers to explore context menu.')),
		(130, 'IDM_OPTION_UNREGISTER', tr('Unregister from Explore'), wx.ITEM_NORMAL, 'OnOptionUnRegister', tr('Unregisters from explore context menu.')),
	]),
	]
	Mixin.setMixin('mainframe', 'menulist', menulist)

	def OnOptionRegister(win, event):
		try:
			key = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, '*\\shell', _winreg.KEY_ALL_ACCESS)
			filename = os.path.basename(sys.argv[0])
			f, ext = os.path.splitext(filename)
			if ext == '.exe':
				command = '"%s" %%L' % os.path.normpath(os.path.join(win.app.workpath, filename))
			else:
				path = os.path.normpath(os.path.join(win.app.workpath, '%s.pyw' % f))
				command = '"pythonw.exe" "%s" "%%L"' % path
			_winreg.SetValue(key, 'NewEdit\\command', _winreg.REG_SZ, command)
			wx.MessageDialog(win, tr('Successful!'), tr("Message"), wx.OK | wx.ICON_INFORMATION).ShowModal()
		except:
			error.traceback()
			wx.MessageDialog(win, tr('Register to explore context menu failed!'), tr("Error"), wx.OK | wx.ICON_INFORMATION).ShowModal()
	Mixin.setMixin('mainframe', 'OnOptionRegister', OnOptionRegister)

	def OnOptionUnRegister(win, event):
		try:
			key = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, '*\\shell', _winreg.KEY_ALL_ACCESS)
			_winreg.DeleteKey(key, 'NewEdit\\command')
			_winreg.DeleteKey(key, 'NewEdit')
			wx.MessageDialog(win, tr('Successful!'), tr("Message"), wx.OK | wx.ICON_INFORMATION).ShowModal()
		except:
			error.traceback()
			wx.MessageDialog(win, tr('Unregister from explore context menu failed!'), tr("Error"), wx.OK | wx.ICON_INFORMATION).ShowModal()
	Mixin.setMixin('mainframe', 'OnOptionUnRegister', OnOptionUnRegister)

