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
#	$Id: mPreference.py 475 2006-01-16 09:50:28Z limodou $

import wx
from modules import Mixin

def add_mainframe_menu(menulist):
    menulist.extend([ (None,
        [
            (600, 'IDM_OPTION', tr('Option'), wx.ITEM_NORMAL, None, ''),
        ]),
        ('IDM_OPTION',
        [
            (100, 'IDM_OPTION_PREFERENCE', tr('Preference...'), wx.ITEM_NORMAL, 'OnOptionPreference', tr('Setup program preferences')),
        ]),
    ])
Mixin.setPlugin('mainframe', 'add_menu', add_mainframe_menu)

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