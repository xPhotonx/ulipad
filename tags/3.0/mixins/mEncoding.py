#	Programmer:	limodou
#	E-mail:		chatme@263.net
#
#	Copyleft 2004 limodou
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
#	$Id: mEncoding.py 93 2005-10-11 02:51:02Z limodou $

from modules import Mixin
import wx
from modules import i18n
from modules import Resource
import EncodingDialog
import os.path
from modules import common

def init(pref):
	pref.select_encoding = False
Mixin.setPlugin('preference', 'init', init)

preflist = [
	(tr('General'), 160, 'check', 'select_encoding', tr('Show encoding selection dialog as openning or saving file.'), None),
]
Mixin.setMixin('preference', 'preflist', preflist)

encoding_resfile = common.unicode_abspath('resources/encodingdialog.xrc')

def getencoding(win, mainframe):
	ret = None
	if win.pref.select_encoding:
		filename = i18n.makefilename(encoding_resfile, mainframe.app.i18n.lang)
		dlg = Resource.loadfromresfile(filename, win, EncodingDialog.EncodingDialog, 'EncodingDialog', mainframe)
		answer = dlg.ShowModal()
		if answer == wx.ID_OK:
			ret = dlg.GetValue()
			dlg.Destroy()
	return ret
Mixin.setPlugin('mainframe', 'getencoding', getencoding)

menulist = [ ('IDM_DOCUMENT',
	[
		(125, 'IDM_DOCUMENT_CHANGE_ENCODING', tr('Change Encoding...'), wx.ITEM_NORMAL, 'OnDocumentChangeEncoding', tr("Chanages current document's saving encoding.")),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

def OnDocumentChangeEncoding(win, event):
	ret = ''
	filename = i18n.makefilename(encoding_resfile, win.app.i18n.lang)
	dlg = Resource.loadfromresfile(filename, win, EncodingDialog.EncodingDialog, 'EncodingDialog', win)
	answer = dlg.ShowModal()
	if answer == wx.ID_OK:
		ret = dlg.GetValue()
		dlg.Destroy()
		win.document.locale = ret
		win.SetStatusText(win.document.locale, 4)
		win.document.modified = True
		win.editctrl.showTitle(win.document)
Mixin.setMixin('mainframe', 'OnDocumentChangeEncoding', OnDocumentChangeEncoding)

