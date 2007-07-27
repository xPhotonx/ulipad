#   Programmer:     limodou
#   E-mail:         limodou@gmail.com
# 
#   Copyleft 2006 limodou
# 
#   Distributed under the terms of the GPL (GNU Public License)
# 
#   UliPad is free software; you can redistribute it and/or modify
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
#   $Id$

import wx
import re
from modules import Mixin
from modules import common
from modules import Globals

def other_popup_menu(win, menus):
    menus.extend([(None, #parent menu id
        [
            (180, '', '-', wx.ITEM_SEPARATOR, None, ''),
            (190, 'IDPM_GOGO', tr('Goto error line'), wx.ITEM_NORMAL, 'OnGoto', tr('Goto the line that occurs the error.')),
        ]),
    ])
Mixin.setPlugin('messagewindow', 'other_popup_menu', other_popup_menu)

r = re.compile('File\s+"(.*?)",\s+line\s+(\d+)')
def OnGoto(win, event):
    line = win.GetCurLine()[0]
    b = r.search(common.encode_string(line, common.defaultfilesystemencoding))
    if b:
        filename, lineno = b.groups()
        Globals.mainframe.editctrl.new(filename)
        wx.CallAfter(Globals.mainframe.document.goto, int(lineno))
Mixin.setMixin('messagewindow', 'OnGoto', OnGoto)

def messagewindow_init(win):
    wx.EVT_LEFT_DCLICK(win, win.OnGoto)
Mixin.setPlugin('messagewindow', 'init', messagewindow_init)
