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
#	$Id: FiletypeBase.py 176 2005-11-22 02:46:37Z limodou $

__doc__ = 'Filetype base class'

from modules import Mixin
from modules import dynamicmenu
from modules import maketoolbar

class FiletypeBase(Mixin.Mixin):
	__mixinname__ = 'filetypebase'

	menulist = []
	toollist = []
	toolbaritems= {}

	def __init__(self, name):
		self.initmixin()
		self.name = name

	def enter(self, mainframe, document):
		if document and document.languagename == self.name:
			dynamicmenu.menuInsert(mainframe, self.menulist)
			maketoolbar.inserttookbar(mainframe, mainframe.toollist, self.toollist, self.toolbaritems)
			self.doenter(mainframe, document)
			self.callplugin('on_enter', mainframe, document)
			return True

	def doenter(self, mainframe, document):
		pass

	def leave(self, mainframe, filename, languagename):
		if languagename == self.name:
			dynamicmenu.menuRemove(mainframe, self.menulist)
			maketoolbar.removetoolbar(mainframe, mainframe.toollist, self.toollist, self.toolbaritems)
			self.doleave(mainframe, filename, languagename)
			self.callplugin('on_leave', mainframe, filename, languagename)
			return True

	def doleave(self, mainframe, filename, languagename):
		pass