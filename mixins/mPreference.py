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
#	$Id: mPreference.py 93 2005-10-11 02:51:02Z limodou $

from modules import Mixin
import wx

menulist = [ (None,
	[
		(600, 'IDM_OPTION', tr('Option'), wx.ITEM_NORMAL, None, ''),
	]),
	('IDM_OPTION',
	[
		(100, 'IDM_OPTION_PREFERENCE', tr('Preference...'), wx.ITEM_NORMAL, 'OnOptionPreference', tr('Setup program preferences')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

def beforegui(win):
	import Preference

	win.pref = Preference.Preference()
	win.pref.load()
	win.pref.printValues()
Mixin.setPlugin('app', 'beforegui', beforegui, Mixin.HIGH)

def OnOptionPreference(win, event):
	import PrefDialog

	dlg = PrefDialog.PrefDialog(win)
	dlg.ShowModal()
Mixin.setMixin('mainframe', 'OnOptionPreference', OnOptionPreference)

