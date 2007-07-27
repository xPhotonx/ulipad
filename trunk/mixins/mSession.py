#   Programmer: limodou
#   E-mail:     limodou@gmail.com
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
#   $Id: mSession.py 1457 2006-08-23 02:12:12Z limodou $

import wx
import wx.stc
from modules import Mixin

def pref_init(pref):
    pref.load_session = True
    pref.sessions = []
    pref.last_tab_index = -1
    pref.screen_lines = 0
Mixin.setPlugin('preference', 'init', pref_init)

def add_pref(preflist):
    preflist.extend([
        (tr('General'), 130, 'check', 'load_session', tr('Auto load the files of last session'), None),
    ])
Mixin.setPlugin('preference', 'add_pref', add_pref)

def afterclosewindow(win):
    win.pref.sessions = []
    win.pref.last_tab_index = -1
    if win.pref.load_session:
        for document in win.editctrl.getDocuments():
            if document.documenttype != 'edit':
                continue
            if document.filename and document.savesession:
                win.pref.sessions.append(getStatus(document))
        win.pref.last_tab_index = win.editctrl.GetSelection()
    win.pref.save()
Mixin.setPlugin('mainframe', 'afterclosewindow', afterclosewindow)

def getStatus(document):
    """filename, pos, bookmarks"""
    bookmarks = []
    start = 0
    line = document.MarkerNext(start, 1)
    while line > -1:
        bookmarks.append(line)
        start = line + 1
        line = document.MarkerNext(start, 1)
    return document.filename, document.save_state(), bookmarks

def openPage(win):
    n = 0
    if win.mainframe.pref.load_session and not win.mainframe.app.skipsessionfile:
        for v in win.mainframe.pref.sessions:
            if len(v) == 4:
                filename, row, col, bookmarks = v
                state = row
            else:
                filename, state, bookmarks = v
            document = win.new(filename, delay=True)
            if document:
                n += 1
        index = win.mainframe.pref.last_tab_index
        if index > -1 and index < len(win.list):
            wx.CallAfter(win.switch, win.list[index], delay=False)
#            while index > -1:
#                if not win.switch(win.list[index], delay=False):
#                    index=len(win.list)-1
#                else:
#                    break

    return n > 0
Mixin.setPlugin('editctrl', 'openpage', openPage)
