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
#	$Id: mChangeFileType.py 93 2005-10-11 02:51:02Z limodou $

__doc__ = 'Process changing file type event'

from modules import Mixin
import wx

def on_document_enter(win, document):
	win.mainframe.changefiletype.enter(win.mainframe, document)
Mixin.setPlugin('editctrl', 'on_document_enter', on_document_enter)

def on_document_leave(win, filename, languagename):
	win.mainframe.changefiletype.leave(win.mainframe, filename, languagename)
Mixin.setPlugin('editctrl', 'on_document_leave', on_document_leave)

def afterinit(win):
	import ChangeFileType

	win.changefiletype = ChangeFileType.ChangeFileType()
Mixin.setPlugin('mainframe', 'afterinit', afterinit)


