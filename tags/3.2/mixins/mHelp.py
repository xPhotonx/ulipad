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
#	$Id: mHelp.py 481 2006-01-17 05:54:13Z limodou $

import wx
from modules import Mixin
from modules import Version
from modules import common

homepage = 'http://wiki.woodpecker.org.cn/moin/NewEdit'
blog = 'http://www.donews.net/limodou'
email = 'limodou@gmail.com'
author = 'limodou'

class AboutDialog(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, -1, size = (400, 240), style = wx.DEFAULT_DIALOG_STYLE, title = tr('About'))

		box = wx.BoxSizer(wx.VERTICAL)
		t = wx.StaticText(self, -1, label=tr('NewEdit Version %s') % Version.version)
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
		t = wx.StaticText(self, -1, label=tr('If you have any question please contact me !\nThe NewEdit project homepage is : \n    %s\nMy Blog is : \n    %s') % (homepage, blog))
		font.SetPointSize(10)
		t.SetFont(font)
		box.Add(t, 0, wx.ALIGN_CENTER|wx.BOTTOM, 10)
		btnOK = wx.Button(self, wx.ID_OK, tr("OK"), size=(60, -1))
		btnOK.SetDefault()
		box.Add(btnOK, 0, wx.ALIGN_CENTER|wx.ALL, 10)

		self.SetSizer(box)
		self.SetAutoLayout(True)

def add_mainframe_menu(menulist):
    menulist.extend([ ('IDM_HELP', #parent menu id
        [
            (100, 'IDM_HELP_INDEXT', tr('NewEdit Help Document') + '\tF1', wx.ITEM_NORMAL, 'OnHelpIndex', tr('NewEdit help document')),
            (110, 'IDM_HELP_PROJECT', tr('Visit Project Homepage'), wx.ITEM_NORMAL, 'OnHelpProject', tr('Project Homepage %s') % homepage),
            (120, 'IDM_HELP_MYBLOG', tr('Visit My Blog'), wx.ITEM_NORMAL, 'OnHelpMyBlog', tr('My Blog %s') % blog),
            (130, 'IDM_HELP_EMAIL', tr('Contact Me'), wx.ITEM_NORMAL, 'OnHelpEmail', tr('Send email to me mailto:%s') % email),
            (900, 'IDM_HELP_ABOUT', tr('About...'), wx.ITEM_NORMAL, 'OnHelpAbout', tr('About this program')),
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

def OnHelpEmail(win, event):
	import webbrowser

	webbrowser.open('mailto:%s' % email)
Mixin.setMixin('mainframe', 'OnHelpEmail', OnHelpEmail)

def OnHelpMyBlog(win, event):
	import webbrowser

	webbrowser.open(blog, 1)
Mixin.setMixin('mainframe', 'OnHelpMyBlog', OnHelpMyBlog)

