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
#   $Id: mHelp.py 1731 2006-11-22 03:35:50Z limodou $

import wx
from modules import Mixin
from modules import Version
from modules import common
from modules.HyperLinksCtrl import HyperLinkCtrl, EVT_HYPERLINK_LEFT
from modules import Globals

homepage = 'http://wiki.woodpecker.org.cn/moin/UliPad'
blog = 'http://www.donews.net/limodou'
email = 'limodou@gmail.com'
author = 'limodou'
maillist = 'http://groups.google.com/group/ulipad'

class AboutDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, size = (400, 340), style = wx.DEFAULT_DIALOG_STYLE, title = tr('About'))

#        self.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False))
#
        box = wx.BoxSizer(wx.VERTICAL)
        t = wx.StaticText(self, -1, label=tr('UliPad Version %s') % Version.version)
        font = t.GetFont()
        font.SetPointSize(20)
        t.SetFont(font)
        box.Add(t, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        t = wx.StaticText(self, -1, label=tr('Author: %s (%s)') % (author, email))
        font.SetPointSize(12)
        t.SetFont(font)
        box.Add(t, 0, wx.ALIGN_CENTER|wx.BOTTOM, 10)
        line = wx.StaticLine(self, -1, size=(-1, -1))
        box.Add(line, 0, wx.ALIGN_CENTER|wx.BOTTOM, 10)
        t = wx.StaticText(self, -1, label=tr('If you have any question please contact me !'))
        box.Add(t, 0, wx.ALIGN_CENTER|wx.BOTTOM, 10)

        self.ID_HOMEPAGE = wx.NewId()
        self.homepage = HyperLinkCtrl(self, self.ID_HOMEPAGE, "The UliPad project homepage", URL=homepage)
        box.Add(self.homepage, 0, wx.ALIGN_CENTER|wx.BOTTOM, 10)

        self.ID_MAILLIST = wx.NewId()
        self.maillist = HyperLinkCtrl(self, self.ID_MAILLIST, "The UliPad maillist", URL=maillist)
        box.Add(self.maillist, 0, wx.ALIGN_CENTER|wx.BOTTOM, 10)

        self.ID_BLOG = wx.NewId()
        self.blog = HyperLinkCtrl(self, self.ID_BLOG, "My Blog", URL=blog)
        box.Add(self.blog, 0, wx.ALIGN_CENTER|wx.BOTTOM, 10)

        self.ID_EMAIL = wx.NewId()
        self.email = HyperLinkCtrl(self, self.ID_EMAIL, "Contact me", URL='mailto:'+email)
        box.Add(self.email, 0, wx.ALIGN_CENTER|wx.BOTTOM, 10)

        btnOK = wx.Button(self, wx.ID_OK, tr("OK"))
        btnOK.SetDefault()
        box.Add(btnOK, 0, wx.ALIGN_CENTER|wx.ALL, 10)

        self.SetSizer(box)
        self.SetAutoLayout(True)

        box.Fit(self)

        EVT_HYPERLINK_LEFT(self.homepage, self.ID_HOMEPAGE, self.OnLink)
        EVT_HYPERLINK_LEFT(self.maillist, self.ID_MAILLIST, self.OnLink)
        EVT_HYPERLINK_LEFT(self.blog, self.ID_BLOG, self.OnLink)
        EVT_HYPERLINK_LEFT(self.email, self.ID_EMAIL, self.OnLink)

    def OnLink(self, event):
        eid = event.GetId()
        mainframe = Globals.mainframe
        if eid == self.ID_HOMEPAGE:
            mainframe.OnHelpProject(event)
        elif eid == self.ID_MAILLIST:
            mainframe.OnHelpMaillist(event)
        elif eid == self.ID_BLOG:
            mainframe.OnHelpMyBlog(event)
        elif eid == self.ID_EMAIL:
            mainframe.OnHelpEmail(event)

def add_mainframe_menu(menulist):
    menulist.extend([ ('IDM_HELP', #parent menu id
        [
            (100, 'wx.ID_HELP', tr('UliPad Help Document') + '\tF1', wx.ITEM_NORMAL, 'OnHelpIndex', tr('UliPad help document')),
            (200, '-', '', wx.ITEM_SEPARATOR, '', ''),
            (210, 'wx.ID_HOME', tr('Visit Project Homepage'), wx.ITEM_NORMAL, 'OnHelpProject', tr('Visit Project Homepage: %s') % homepage),
            (220, 'IDM_HELP_MAILLIST', tr('Visit maillist'), wx.ITEM_NORMAL, 'OnHelpMaillist', tr('Visit Project Maillist: %s') % maillist),
            (230, 'IDM_HELP_MYBLOG', tr('Visit My Blog'), wx.ITEM_NORMAL, 'OnHelpMyBlog', tr('Visit My blog: %s') % blog),
            (240, 'IDM_HELP_EMAIL', tr('Contact Me'), wx.ITEM_NORMAL, 'OnHelpEmail', tr('Send email to me mailto:%s') % email),
            (900, 'wx.ID_ABOUT', tr('About...'), wx.ITEM_NORMAL, 'OnHelpAbout', tr('About this program')),
        ]),
    ])
Mixin.setPlugin('mainframe', 'add_menu', add_mainframe_menu)

def OnHelpIndex(win, event):
    import webbrowser

    webbrowser.open('file:///'+common.get_app_filename(win, 'doc/index.htm'), 1)
Mixin.setMixin('mainframe', 'OnHelpIndex', OnHelpIndex)

def OnHelpAbout(win, event):
    AboutDialog(win).ShowModal()
Mixin.setMixin('mainframe', 'OnHelpAbout', OnHelpAbout)

def OnHelpProject(win, event):
    import webbrowser

    webbrowser.open(homepage, 1)
Mixin.setMixin('mainframe', 'OnHelpProject', OnHelpProject)

def OnHelpMaillist(win, event):
    import webbrowser

    webbrowser.open(maillist, 1)
Mixin.setMixin('mainframe', 'OnHelpMaillist', OnHelpMaillist)

def OnHelpEmail(win, event):
    import webbrowser

    webbrowser.open('mailto:%s' % email)
Mixin.setMixin('mainframe', 'OnHelpEmail', OnHelpEmail)

def OnHelpMyBlog(win, event):
    import webbrowser

    webbrowser.open(blog, 1)
Mixin.setMixin('mainframe', 'OnHelpMyBlog', OnHelpMyBlog)
