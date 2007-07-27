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
