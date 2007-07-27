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
#	$Id: mFtp.py 176 2005-11-22 02:46:37Z limodou $

__doc__ = 'ftp manage'

from modules import Mixin
import wx
from modules.Debug import error
import os.path
from modules import common

menulist = [ ('IDM_WINDOW',
	[
		(160, 'IDM_WINDOW_FTP', tr('Open Ftp Window'), wx.ITEM_NORMAL, 'OnWindowFtp', tr('Opens ftp window.')),
	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

ftp_imagelist = {
	'close':		common.unicode_abspath('images/folderclose.gif'),
	'document':		common.unicode_abspath('images/file.gif'),
	'parentfold':	common.unicode_abspath('images/parentfold.gif'),
}
ftp_resfile = common.unicode_abspath('resources/ftpmanagedialog.xrc')


def afterinit(win):
	win.ftp_imagelist = ftp_imagelist
	win.ftp_resfile = ftp_resfile
	win.ftp = None
Mixin.setPlugin('mainframe', 'afterinit', afterinit)

popmenulist = [ (None,
	[
		(150, 'IDPM_FTPWINDOW', tr('Open Ftp Window'), wx.ITEM_NORMAL, 'OnFtpWindow', tr('Opens ftp window.')),
	]),
]
Mixin.setMixin('notebook', 'popmenulist', popmenulist)

def createFtpWindow(win):
	page = win.panel.getPage('Ftp')
	if not page:
		from FtpClass import Ftp

		page = Ftp(win.panel.createNotebook('bottom'), win)
		win.panel.addPage('bottom', page, 'Ftp')
	win.ftp = page
Mixin.setMixin('mainframe', 'createFtpWindow', createFtpWindow)

def OnWindowFtp(win, event):
	win.createFtpWindow()
	win.panel.showPage('Ftp')
Mixin.setMixin('mainframe', 'OnWindowFtp', OnWindowFtp)

def OnFtpWindow(win, event):
	win.mainframe.createFtpWindow()
	win.panel.showPage('Ftp')
Mixin.setMixin('notebook', 'OnFtpWindow', OnFtpWindow)

def init(pref):
	pref.ftp_sites = []
	pref.sites_info = {}
	pref.last_ftp_site = 0
	pref.remote_paths = []
Mixin.setPlugin('preference', 'init', init)

def afterclosewindow(win):
	if win.ftp and win.ftp.alive:
		try:
			win.ftp.ftp.quit()
		except:
			error.traceback()
Mixin.setPlugin('mainframe', 'afterclosewindow', afterclosewindow)

popmenulist = [ (None, #parent menu id
	[
		(100, 'IDPM_OPEN', tr('Open'), wx.ITEM_NORMAL, 'OnOpen', tr('Open an file or directory.')),
		(110, 'IDPM_NEWFILE', tr('New File'), wx.ITEM_NORMAL, 'OnNewFile', tr('Create an new file.')),
		(120, 'IDPM_NEWDIR', tr('New Directory'), wx.ITEM_NORMAL, 'OnNewDir', tr('Create an new directory.')),
		(130, 'IDPM_DELETE', tr('Delete'), wx.ITEM_NORMAL, 'OnDelete', tr('Delete selected file or directory.')),
		(140, 'IDPM_RENAME', tr('Rename'), wx.ITEM_NORMAL, 'OnRename', tr('Rename selected file or directory.')),
		(150, '-', '', wx.ITEM_SEPARATOR, '', ''),
		(160, 'IDPM_REFRESH', tr('Refresh'), wx.ITEM_NORMAL, 'OnRefresh', tr('Refresh current directory.')),
		(170, '-', '', wx.ITEM_SEPARATOR, '', ''),
		(180, 'IDPM_UPLOAD', tr('Upload'), wx.ITEM_NORMAL, 'OnUpload', tr('Upload files.')),
		(190, 'IDPM_DOWNLOAD', tr('Download'), wx.ITEM_NORMAL, 'OnDownload', tr('Download files.')),
	]),
]
Mixin.setMixin('ftpclass', 'popmenulist', popmenulist)

def OnOpen(win, event):
	win.OnEnter(event)
Mixin.setMixin('ftpclass', 'OnOpen', OnOpen)

def OnNewFile(win, event):
	win.newfile()
Mixin.setMixin('ftpclass', 'OnNewFile', OnNewFile)

def OnNewDir(win, event):
	win.newdir()
Mixin.setMixin('ftpclass', 'OnNewDir', OnNewDir)

def OnDelete(win, event):
	win.delete()
Mixin.setMixin('ftpclass', 'OnDelete', OnDelete)

def OnRename(win, event):
	win.rename()
Mixin.setMixin('ftpclass', 'OnRename', OnRename)

def OnUpload(win, event):
	win.upload()
Mixin.setMixin('ftpclass', 'OnUpload', OnUpload)

def OnDownload(win, event):
	win.download()
Mixin.setMixin('ftpclass', 'OnDownload', OnDownload)

#ftp(siteno):fullpathfilename
def readfiletext(win, filename, stext):
	import re

	re_ftp = re.compile('^ftp\((\d+)\):')
	b = re_ftp.search(filename)
	if b:
		siteno = int(b.group(1))
		filename = filename.split(':')[1]
		from FtpClass import readfile
		text = readfile(win.mainframe, filename, siteno)
		win.needcheckfile = False
		if text is not None:
			stext.append(text)
		else:
			stext.append(None)
		return True, True
Mixin.setPlugin('editor', 'readfiletext', readfiletext)

def writefiletext(win, filename, text):
	import re

	re_ftp = re.compile('^ftp\((\d+)\):')
	b = re_ftp.search(filename)
	if b:
		siteno = int(b.group(1))
		filename = filename.split(':', 1)[1]
		from FtpClass import writefile
		flag = writefile(win.mainframe, filename, siteno, text)
		return True, True, flag
Mixin.setPlugin('editor', 'writefiletext', writefiletext)

toollist = [
	(127, 'ftp'),
]
Mixin.setMixin('mainframe', 'toollist', toollist)

#order, IDname, imagefile, short text, long text, func
toolbaritems = {
	'ftp':(wx.ITEM_NORMAL, 'IDM_FILE_FTP', common.unicode_abspath('images/ftp.gif'), tr('open ftp window'), tr('Opens ftp window.'), 'OnWindowFtp'),
}
Mixin.setMixin('mainframe', 'toolbaritems', toolbaritems)

def getShortFilename(win):
	import re
	import os.path

	if win.title:
		return win.title

	re_ftp = re.compile('^ftp\((\d+)\):')
	b = re_ftp.search(win.filename)
	if b:
		return os.path.basename(win.filename.split(':', 1)[1])
	else:
		return os.path.basename(win.getFilename())
Mixin.setMixin('editor', 'getShortFilename', getShortFilename)