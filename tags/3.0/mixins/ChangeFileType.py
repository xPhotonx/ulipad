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
#	$Id: ChangeFileType.py 93 2005-10-11 02:51:02Z limodou $

from modules import Mixin

class ChangeFileType(Mixin.Mixin):
	__mixinname__ = 'changefiletype'
	filetypes = []	#(name, filetypeobjclass)

	def __init__(self):
		self.initmixin()
		self.objs = []

		for name, _class in self.filetypes:
			self.objs.append(_class(name))

	def enter(self, mainframe, document):
		for i, obj in enumerate(self.objs):
			if obj.enter(mainframe, document):
				break

	def leave(self, mainframe, filename, languagename):
		for obj in self.objs:
			if obj.leave(mainframe, filename, languagename):
				break

