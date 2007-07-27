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
#	$Id: mIcon.py 93 2005-10-11 02:51:02Z limodou $

import wx
import os
from modules import Mixin
from modules import common

iconfile = common.unicode_abspath(os.path.abspath('newedit.ico'))
def init(win):
	icon = wx.EmptyIcon()
	icon.LoadFile(iconfile, wx.BITMAP_TYPE_ICO)
	win.SetIcon(icon)
Mixin.setPlugin('mainframe', 'init', init)

