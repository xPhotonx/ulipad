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
#	$Id: mUnicode.py 176 2005-11-22 02:46:37Z limodou $

__doc__ = 'encoding selection and unicode support'

from modules import Mixin
import wx
import wx.stc
#from modules import DetectUTF_8
from MyUnicodeException import MyUnicodeException
from modules.Debug import error

def init(pref):
	pref.auto_detect_utf8 = True
Mixin.setPlugin('preference', 'init', init)

preflist = [
	(tr('Document'), 170, 'check', 'auto_detect_utf8', tr('Auto detect UTF-8 encoding'), None),
]
Mixin.setMixin('preference', 'preflist', preflist)

def init(win):
	win.locale = win.defaultlocale
Mixin.setPlugin('editor', 'init', init)

def openfileencoding(win, stext, encoding):
	text = stext[0]

	if not encoding:
		if win.mainframe.pref.auto_detect_utf8:
			encoding = 'utf-8'
		else:
			encoding = win.defaultlocale
	try:
		s = unicode(text, encoding)
		win.locale = encoding
	except:
		if win.mainframe.pref.auto_detect_utf8 and encoding == 'utf-8':
			encoding = win.defaultlocale
			try:
				s = unicode(text, encoding)
				win.locale = encoding
			except:
				error.traceback()
				raise MyUnicodeException(win, tr("Cann't convert file encoding [%s] to unicode!\nThe file cann't be openned!") % encoding,
					tr("Unicode Error"))
		else:
			error.traceback()
			raise MyUnicodeException(win, tr("Cann't convert file encoding [%s] to unicode!\nThe file cann't be openned!") % encoding,
				tr("Unicode Error"))
	stext[0] = s
Mixin.setPlugin('editor', 'openfileencoding', openfileencoding)

def savefileencoding(win, stext, encoding):
	text = stext[0]

	if not encoding:
		encoding = win.locale

	oldencoding = win.locale
	if encoding:
		try:
			s = text.encode(encoding)
			win.locale = encoding
		except:
			error.traceback()
			raise MyUnicodeException(win, tr("Cann't convert file to [%s] encoding!\nThe file cann't be saved!") % encoding,
				tr("Unicode Error"))
	else:
		s = text
	stext[0] = s
Mixin.setPlugin('editor', 'savefileencoding', savefileencoding)