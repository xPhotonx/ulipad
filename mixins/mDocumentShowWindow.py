

import wx
from modules import Mixin

def add_mainframe_menu(menulist):
    menulist.extend([('IDM_WINDOW', #parent menu id
        [
            (210, 'IDM_WINDOW_Document_Show', tr('Open Document_Show Window')+u'\tCtrl+9', wx.ITEM_NORMAL, 'OnWindowDocument_Show', tr('Open the Document_Show window.')),
        ]),
    ])
Mixin.setPlugin('mainframe', 'add_menu', add_mainframe_menu)

def add_notebook_menu(popmenulist):
    popmenulist.extend([ (None,
        [
            (190, 'IDPM_Document_ShowWINDOW', tr('Open Document Show Window'), wx.ITEM_NORMAL, 'OnNDocu_showWindow', tr('Opens the Document Show window.')),
        ]),
    ])
Mixin.setPlugin('notebook', 'add_menu', add_notebook_menu)

def pref_init(pref):
    pass
Mixin.setPlugin('preference', 'init', pref_init)

def add_pref(preflist):
    pass
Mixin.setPlugin('preference', 'add_pref', add_pref)

document_show_pagename = tr('Document_Show')

def create_document_show_window(win):
    if not win.panel.getPage(document_show_pagename):
        from DocumentShowWindow import DocumentShowWindow

        page = DocumentShowWindow(win.panel.createNotebook('right'), win)
        win.panel.addPage('right', page, document_show_pagename)
    win.document_show_window = win.panel.getPage(document_show_pagename)
    win.panel.showPage(document_show_pagename)
    win.panel.showWindow("right", True)

Mixin.setMixin('mainframe', 'create_document_show_window', create_document_show_window)
Mixin.setPlugin('mainframe', 'afterinit', create_document_show_window)

def OnWindow_Document_Show(win, event):
    win.create_document_show_window()
    win.panel.showPage(document_show_pagename)
    win.document_show_window.Show()
Mixin.setMixin('mainframe', 'OnWindowDocument_Show', OnWindow_Document_Show)

def OnNDocu_showWindow(win, event):
    win.mainframe.create_document_show_window()
    win.panel.showPage(document_show_pagename)
    win.mainframe.document_show_window.Show()
Mixin.setMixin('notebook', 'OnNDocu_showWindow', OnNDocu_showWindow)

def on_document_enter1(win, editor):
    win.mainframe.document_show_window.show("document will show here!")
Mixin.setPlugin('editctrl', 'on_document_enter', on_document_enter1)
