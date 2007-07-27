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
#	$Id$

from modules import Mixin

def mainframe_init(win):
    win.input_assistant = None
Mixin.setPlugin('mainframe', 'init', mainframe_init)

def on_char(win, event):
    if not win.mainframe.input_assistant:
        from InputAssistant import InputAssistant

        win.mainframe.input_assistant = i = InputAssistant()
    else:
        i = win.mainframe.input_assistant
    return i.run(win, event)
Mixin.setPlugin('editor', 'on_char', on_char, nice=10)

def init(pref):
	pref.auto_extend = True
Mixin.setPlugin('preference', 'init', init)

preflist = [
	(tr('Document'), 260, 'check', 'auto_extend', tr('Enable auto extend'), None),
]
Mixin.setMixin('preference', 'preflist', preflist)