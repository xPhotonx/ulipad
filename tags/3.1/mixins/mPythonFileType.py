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
#	$Id: mPythonFileType.py 176 2005-11-22 02:46:37Z limodou $

from modules import Mixin
import wx
import FiletypeBase

class PythonFiletype(FiletypeBase.FiletypeBase):

	__mixinname__ = 'pythonfiletype'
	menulist = [ (None,
		[
			(890, 'IDM_PYTHON', 'Python', wx.ITEM_NORMAL, None, ''),
		]),
	]
	toollist = []		#your should not use supperclass's var
	toolbaritems= {}

filetype = [('python', PythonFiletype)]
Mixin.setMixin('changefiletype', 'filetypes', filetype)