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
#	$Id: mClassBrowser.py 154 2005-11-07 04:48:15Z limodou $

import wx
import os
from modules import Mixin
from modules import common

def mainframe_init(win):
	win.memo_win = None
Mixin.setPlugin('mainframe', 'init', mainframe_init)

def pref_init(pref):
	pref.easy_memo_lastpos = 0
Mixin.setPlugin('preference', 'init', pref_init)

def add_mainframe_menu(menulist):
    menulist.extend([('IDM_TOOL', #parent menu id
        [
            (140, 'IDM_TOOL_MEMO', tr('Easy Memo') + u'\tF12', wx.ITEM_CHECK, 'OnToolMemo', tr('Show Easy Memo windows, and you can write down everything what you want.')),
        ]),
    ])
Mixin.setPlugin('mainframe', 'add_menu', add_mainframe_menu)

def OnToolMemo(win, event):
	if win.memo_win:
		win.memo_win.Close()
		win.memo_win = None
	else:
		import Pad
		from modules import Globals
		pad = Pad.PAD(win, os.path.join(Globals.userpath, 'memo.txt'), tr('Easy Memo'))
		pad.Show()
		win.memo_win = pad
Mixin.setMixin('mainframe', 'OnToolMemo', OnToolMemo)

def add_tool_list(toollist, toolbaritems):
    toollist.extend([
        (600, 'memo'),
    ])
    
    #order, IDname, imagefile, short text, long text, func
    toolbaritems.update({
        'memo':(wx.ITEM_CHECK, 'IDM_TOOL_MEMO', common.unicode_abspath('images/memo.gif'), tr('easy memo'), tr('Show Easy Memo windows, and you can write down everything what you want.'), 'OnToolMemo'),
    })
Mixin.setPlugin('mainframe', 'add_tool_list', add_tool_list)

def afterinit(win):
	wx.EVT_UPDATE_UI(win, win.IDM_TOOL_MEMO, win.OnUpdateUI)
Mixin.setPlugin('mainframe', 'afterinit', afterinit)

def on_mainframe_updateui(win, event):
	eid = event.GetId()
	if eid == win.IDM_TOOL_MEMO:
		if win.memo_win:
			event.Check(True)
		else:
			event.Check(False)
Mixin.setPlugin('mainframe', 'on_update_ui', on_mainframe_updateui)
