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
#	$Id: mPlugins.py 176 2005-11-22 02:46:37Z limodou $

__doc__ = 'Plugins manage'

from modules import Mixin
import wx
from modules import common

menulist = [ ('IDM_TOOL',
	[
		(130, 'IDM_TOOL_PLUGINS_MANAGE', tr('Plugins Manage...'), wx.ITEM_NORMAL, 'OnDocumentPluginsManage', 'Manages plugins.'),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

def OnDocumentPluginsManage(win, event):
	from PluginDialog import PluginDialog

	dlg = PluginDialog(win)
	answer = dlg.ShowModal()
	dlg.Destroy()
Mixin.setMixin('mainframe', 'OnDocumentPluginsManage', OnDocumentPluginsManage)

plugin_imagelist = {
	'uncheck':	common.unicode_abspath('images/uncheck.gif'),
	'check':	common.unicode_abspath('images/check.gif'),
}

def afterinit(win):
	win.plugin_imagelist = plugin_imagelist
	win.plugin_initfile = common.get_app_filename(win, 'plugins/__init__.py')
Mixin.setPlugin('mainframe', 'afterinit', afterinit)