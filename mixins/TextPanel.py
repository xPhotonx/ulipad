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
#	$Id: TextPanel.py 176 2005-11-22 02:46:37Z limodou $

import MyPanel
from modules import Mixin
import DocumentBase

class TextPanel(MyPanel.SashPanel, DocumentBase.PanelBase, Mixin.Mixin):

	__mixinname__ = 'textpanel'
	documenttype = 'edit'

	def __init__(self, parent, filename):
		self.initmixin()

		MyPanel.SashPanel.__init__(self, parent)
		DocumentBase.PanelBase.__init__(self, parent, filename)
		self.document.panel = self
		self.callplugin('new_window', self.parent, self.document, self)

	def createDocument(self):
		from mixins.Editor import TextEditor
		return TextEditor(self.top, self.parent, self.filename, self.documenttype)