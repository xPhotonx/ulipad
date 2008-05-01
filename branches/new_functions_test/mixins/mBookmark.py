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
#   $Id: mBookmark.py 1665 2006-11-07 13:20:21Z limodou $

import wx
from modules import Mixin

def editor_init(win):
    win.margin_bookmark_type = 2
    win.SetMarginWidth(win.margin_bookmark_type, 20)
    win.SetMarginType(win.margin_bookmark_type, wx.stc.STC_MARGIN_SYMBOL)
    win.SetMarginSensitive(win.margin_bookmark_type, True)
    win.SetMarginMask(win.margin_bookmark_type, ~wx.stc.STC_MASK_FOLDERS)
    # the marker defined  in the mMarkerDefine.py by ygao
    
Mixin.setPlugin('editor', 'init', editor_init)

def add_mainframe_menu(menulist):
    menulist.extend([ ('IDM_SEARCH',
        [
            (180, '', '-', wx.ITEM_SEPARATOR, None, ''),
            (190, 'IDM_SEARCH_BOOKMARK_TOGGLE', tr('Toggle Marker') + '\tE=F9', wx.ITEM_NORMAL, 'OnSearchBookmarkToggle', tr('Set and clear marker at current line')),
            (200, 'IDM_SEARCH_BOOKMARK_CLEARALL', tr('Clear All Marker') + '\tE=Ctrl+Shift+F9', wx.ITEM_NORMAL, 'OnSearchBookmarkClearAll', tr('Clears all marker from the active document')),
            (210, 'IDM_SEARCH_BOOKMARK_NEXT', tr('Next Marker') + '\tE=F8', wx.ITEM_NORMAL, 'OnSearchBookmarkNext', tr('Goes to next marker position')),
            (220, 'IDM_SEARCH_BOOKMARK_PREVIOUS', tr('Previous Marker') + '\tE=Shift+F8', wx.ITEM_NORMAL, 'OnSearchBookmarkPrevious', tr('Goes to previous marker position')),
        ]),
    ])
Mixin.setPlugin('mainframe', 'add_menu', add_mainframe_menu)


def OnSearchBookmarkToggle(win, event):
    line = win.document.GetCurrentLine()
    win.document.toggle_mark(line, win.document.bookmark_number)
Mixin.setMixin('mainframe', 'OnSearchBookmarkToggle', OnSearchBookmarkToggle)


def OnSearchBookmarkClearAll(win, event):
    win.document.MarkerDeleteAll(win.document.bookmark_number)
Mixin.setMixin('mainframe', 'OnSearchBookmarkClearAll', OnSearchBookmarkClearAll)


def OnSearchBookmarkNext(win, event):
    line = win.document.GetCurrentLine()
    win.document.GotoBookmarkNext(line)
Mixin.setMixin('mainframe', 'OnSearchBookmarkNext', OnSearchBookmarkNext)

def GotoBookmarkNext(win, line):
    line = win.get_marker_next(line, win.bookmarker_mask)
    if line:
        win.goto(line)
        win.ScrollToLine(line - 20)
Mixin.setMixin('editor', 'GotoBookmarkNext',GotoBookmarkNext )
    
def OnSearchBookmarkPrevious(win, event):
    line = win.document.GetCurrentLine()
    win.document.GotoBookmarPrevious(line)
Mixin.setMixin('mainframe', 'OnSearchBookmarkPrevious', OnSearchBookmarkPrevious)

def GotoBookmarPrevious(win, line):
    line = win.get_marker_previous(line, win.bookmarker_mask)
    if line:
        win.goto(line)
        win.ScrollToLine(line - 20)
Mixin.setMixin('editor', 'GotoBookmarPrevious',GotoBookmarPrevious)


def OnMarginClick(self, event):
    if event.GetMargin() == self.margin_bookmark_type:
            line_clicked = self.LineFromPosition(event.GetPosition())
            self.toggle_mark(line_clicked, self.bookmark_number)
Mixin.setPlugin('editor', 'on_margin_click', OnMarginClick)