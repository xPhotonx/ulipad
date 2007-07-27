#	Programmer:	limodou
#	E-mail:		limodou@gmail.com
#
#	Copyleft 2005 limodou
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
#	$Id: mModuleInfo.py 93 2005-10-11 02:51:02Z limodou $

from modules import Mixin
import wx
import os.path
from modules import common

menulist = [ ('IDM_HELP', #parent menu id
	[
		(102, 'IDM_HELP_MODULES', tr('Extended Modules Info'), wx.ITEM_NORMAL, 'OnHelpModules', tr('Extended modules infomation')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

def OnHelpModules(win, event):
    from ModulesInfo import show_modules_info
    show_modules_info(win)
Mixin.setMixin('mainframe', 'OnHelpModules', OnHelpModules)


