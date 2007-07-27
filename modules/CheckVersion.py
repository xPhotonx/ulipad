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
#	$Id: CheckVersion.py 93 2005-10-11 02:51:02Z limodou $

import wx
import sys

def check():
	wxversion = "%d%d" % (wx.MAJOR_VERSION, wx.MINOR_VERSION)
	if (wxversion >= '24') and wx.USE_UNICODE and sys.version_info[:2] == (2, 3):
		return True
	else:
		raw_input("""You must install wxPython 2.4 Unicode above and Python 2.3 version.
Please install them first before running NewEdit.

Press Enter to exit the program ...""")
		return False

if __name__ == '__main__':
	print check()

