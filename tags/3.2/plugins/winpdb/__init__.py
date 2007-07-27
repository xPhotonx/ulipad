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
#	$Id: mDosPrompt.py,v 1.1 2005/07/31 09:08:14 limodou Exp $

from modules import Mixin
import wx
import os.path
import os
import sys
import images

menulist = [('IDM_PYTHON', #parent menu id
		[
			(160, 'IDM_PYTHON_DEBUG', tr('Debug in WinPdb'), wx.ITEM_NORMAL, 'OnPythonDebug', tr('Debug the current program in WinPdb.')),
		]),
]
Mixin.setMixin('pythonfiletype', 'menulist', menulist)

toollist = [
	(2130, 'debug'),
]
Mixin.setMixin('pythonfiletype', 'toollist', toollist)

#order, IDname, imagefile, short text, long text, func
toolbaritems = {
	'debug':(wx.ITEM_NORMAL, 'IDM_PYTHON_DEBUG', images.getDebugBitmap(), tr('debug'), tr('Debug the current program in WinPdb.'), 'OnPythonDebug'),
}
Mixin.setMixin('pythonfiletype', 'toolbaritems', toolbaritems)

def OnPythonDebug(win, event):
	i_main, i_ext = os.path.splitext(sys.executable)
	if i_main.endswith('w'):
		i_main = i_main[:-1]
	cmd = os.path.normcase("%s %s/plugins/winpdb/_winpdb.py -t %s" % (i_main, win.app.workpath, win.document.filename))
	wx.Execute(cmd)
Mixin.setMixin('mainframe', 'OnPythonDebug', OnPythonDebug)