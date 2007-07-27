#   Programmer: limodou
#   E-mail:     limodou@gmail.com
#
#   Copyleft 2006 limodou
#
#   Distributed under the terms of the GPL (GNU Public License)
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
#   $Id: MessageWindow.py 475 2006-01-16 09:50:28Z limodou $

__doc__ = 'message window'

import os
import wx
import wx.stc
from modules import Mixin
from modules import common
from modules import makemenu
from modules import Globals

class MessageWindow(wx.stc.StyledTextCtrl, Mixin.Mixin):
    __mixinname__ = 'messagewindow'
    popmenulist = [(None, #parent menu id
        [
            (100, 'IDPM_UNDO', tr('Undo') + '\tCtrl+Z', wx.ITEM_NORMAL, 'OnPopupEdit', tr('Reverse previous editing operation')),
            (110, 'IDPM_REDO', tr('Redo') + '\tCtrl+Y', wx.ITEM_NORMAL, 'OnPopupEdit', tr('Reverse previous undo operation')),
            (120, '', '-', wx.ITEM_SEPARATOR, None, ''),
            (130, 'IDPM_CUT', tr('Cut') + '\tCtrl+X', wx.ITEM_NORMAL, 'OnPopupEdit', tr('Deletes text from the document and moves it to the clipboard')),
            (140, 'IDPM_COPY', tr('Copy') + '\tCtrl+C', wx.ITEM_NORMAL, 'OnPopupEdit', tr('Copies text from the document to the clipboard')),
            (150, 'IDPM_PASTE', tr('Paste') + '\tCtrl+V', wx.ITEM_NORMAL, 'OnPopupEdit', tr('Pastes text from the clipboard into the document')),
            (160, '', '-', wx.ITEM_SEPARATOR, None, ''),
            (170, 'IDPM_SELECT_ALL', tr('Select All') + '\tCtrl+A', wx.ITEM_NORMAL, 'OnPopupEdit', tr('Selects all text.')),
        ]),
    ]
    imagelist = {
        'IDPM_UNDO':'undo.gif',
        'IDPM_REDO':'redo.gif',
        'IDPM_CUT':'cut.gif',
        'IDPM_COPY':'copy.gif',
        'IDPM_PASTE':'paste.gif',
    }

    def __init__(self, parent, mainframe):
        self.initmixin()

        wx.stc.StyledTextCtrl.__init__(self, parent, -1)
        self.parent = parent
        self.mainframe = mainframe
        self.SetMarginWidth(0, 0)
        self.SetMarginWidth(1, 0)
        self.SetMarginWidth(2, 0)
        font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, "face:%s,size:10" % font.GetFaceName())

        self.SetScrollWidth(1)
        self.maxline = 'WWWW'

        for key in MessageWindow.imagelist.keys():
            f = MessageWindow.imagelist[key]
            MessageWindow.imagelist[key] = common.getpngimage(os.path.join(Globals.workpath, 'images/%s' % f))

        self.popmenu = makemenu.makepopmenu(self, MessageWindow.popmenulist, MessageWindow.imagelist)

        wx.stc.EVT_STC_MODIFIED(self, self.GetId(), self.OnModified)
        wx.EVT_RIGHT_DOWN(self, self.OnPopUp)

        wx.EVT_UPDATE_UI(self, self.IDPM_UNDO, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_REDO, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_CUT, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_COPY, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(self, self.IDPM_PASTE, self.OnUpdateUI)

#        self.SetCaretForeground(')
        self.SetCaretLineBack('#FF8000')
        self.SetCaretLineVisible(True)
        
        self.callplugin('init', self)

    def SetText(self, text):
        ro = self.GetReadOnly()
        self.SetReadOnly(0)
        wx.stc.StyledTextCtrl.SetText(self, text)
        self.SetReadOnly(ro)

    def SetSelectedText(self, text):
        ro = self.GetReadOnly()
        self.SetReadOnly(0)
        self.SetTargetStart(self.GetSelectionStart())
        self.SetTargetEnd(self.GetSelectionEnd())
        self.ReplaceTarget(text)
        self.SetReadOnly(ro)

    def setWidth(self, text=''):
        if not text:
            text = self.maxline
        if self.GetWrapMode() == wx.stc.STC_WRAP_NONE:
            ll = self.TextWidth(wx.stc.STC_STYLE_DEFAULT, "W")*4
            line = text.expandtabs(self.GetTabWidth())
            current_width = self.GetScrollWidth()
            width = self.TextWidth(wx.stc.STC_STYLE_DEFAULT, line)
            if width>current_width:
                self.maxline = line
                self.SetScrollWidth(width + ll)

    def OnModified(self, event):
        self.setWidth(self.GetCurLine()[0])

    def canClose(self):
        return True
    
    def OnPopUp(self, event):
        other_menus = []
        if self.popmenu:
            self.popmenu.Destroy()
            self.popmenu = None
        self.callplugin('other_popup_menu', self, other_menus)
        import copy
        if other_menus:
            pop_menus = copy.deepcopy(MessageWindow.popmenulist + other_menus)
        else:
            pop_menus = copy.deepcopy(MessageWindow.popmenulist)
        self.popmenu = pop_menus = makemenu.makepopmenu(self, pop_menus, MessageWindow.imagelist)

        self.PopupMenu(self.popmenu, event.GetPosition())
        
    def OnPopupEdit(self, event):
        eid = event.GetId()
        if eid == self.IDPM_CUT:
            self.Cut()
        elif eid == self.IDPM_COPY:
            self.Copy()
        elif eid == self.IDPM_PASTE:
            self.Paste()
        elif eid == self.IDPM_SELECT_ALL:
            self.SelectAll()
        elif eid == self.IDPM_UNDO:
            self.Undo()
        elif eid == self.IDPM_REDO:
            self.Redo()

    def OnUpdateUI(self, event):
        eid = event.GetId()
        if eid == self.IDPM_CUT:
            event.Enable(not self.GetReadOnly() and bool(self.GetSelectedText()))
        elif eid == self.IDPM_COPY:
            event.Enable(bool(self.GetSelectedText()))
        elif eid == self.IDPM_PASTE:
            event.Enable(not self.GetReadOnly() and bool(self.CanPaste()))
        elif eid == self.IDPM_UNDO:
            event.Enable(bool(self.CanUndo()))
        elif eid == self.IDPM_REDO:
            event.Enable(bool(self.CanRedo()))
