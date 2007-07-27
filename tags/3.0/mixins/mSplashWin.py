
#   Programmer: limodou
#   E-mail:     chatme@263.net
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
#   $Id: mSplashWin.py 93 2005-10-11 02:51:02Z limodou $

import wx
from modules import common
from modules import Mixin
import time

preflist = [
    (tr('General'), 190, 'check', 'splash_on_startup', tr('Show splash window on startup'), None),
]
Mixin.setMixin('preference', 'preflist', preflist)

splashimg = common.unicode_abspath('images/splash.jpg')

def beforegui(app):
    app.splashwin = None
    if app.pref.splash_on_startup:
        app.splashwin = wx.SplashScreen(wx.Image(splashimg).ConvertToBitmap(), 
            wx.SPLASH_CENTRE_ON_SCREEN|wx.SPLASH_NO_TIMEOUT, 0, None, -1)
Mixin.setPlugin('app', 'beforegui', beforegui)

def init(pref):
    pref.splash_on_startup = True
Mixin.setPlugin('preference', 'init', init)

def show(mainframe):
    if mainframe.app.splashwin:
        wx.FutureCall(1000, mainframe.app.splashwin.Destroy)
Mixin.setPlugin('mainframe', 'show', show)