#   Programmer: limodou
#   E-mail:     limodou@gmail.coms
#
#   Copyleft 2004 limodou
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
#   $Id: mSnippets.py,v 1.8 2004/11/27 15:52:08 limodou Exp $

from modules import Mixin
import wx
import os.path
from modules import common
import images

menulist = [
    ('IDM_WINDOW',
    [
        (190, 'IDM_WINDOW_WIZARD', tr('Open Wizard Window'), wx.ITEM_NORMAL, 'OnWindowWizard', tr('Opens wizard window.'))
    ]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

popmenulist = [ (None,
    [
        (140, 'IDPM_WIZARDWINDOW', tr('Open Wizard Window'), wx.ITEM_NORMAL, 'OnWizardWindow', tr('Opens wizard window.')),
    ]),
]
Mixin.setMixin('notebook', 'popmenulist', popmenulist)

toollist = [
	(550, 'wizard'),
]
Mixin.setMixin('mainframe', 'toollist', toollist)

#order, IDname, imagefile, short text, long text, func
toolbaritems = {
	'wizard':(wx.ITEM_NORMAL, 'IDM_WINDOW_WIZARD', images.getWizardBitmap(), tr('wizard'), tr('Opens wizard window.'), 'OnWindowWizard'),
}
Mixin.setMixin('mainframe', 'toolbaritems', toolbaritems)

def createWizardWindow(win):
    if not win.panel.getPage(tr('Wizard')):
        from WizardPanel import WizardPanel

        page = WizardPanel(win.panel.createNotebook('left'), win)
        win.panel.addPage('left', page, tr('Wizard'))
Mixin.setMixin('mainframe', 'createWizardWindow', createWizardWindow)

def OnWindowWizard(win, event):
    win.createWizardWindow()
    win.panel.showPage(tr('Wizard'))
Mixin.setMixin('mainframe', 'OnWindowWizard', OnWindowWizard)

def OnWizardWindow(win, event):
    win.mainframe.createWizardWindow()
    win.panel.showPage(tr('Wizard'))
Mixin.setMixin('notebook', 'OnWizardWindow', OnWizardWindow)
