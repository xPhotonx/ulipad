#   Programmer: limodou
#   E-mail:     limodou@gmail.com
#
#   Copyleft 2006 limodou
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
#   $Id: mDDESupport.py 486 2006-01-17 12:08:32Z limodou $

__doc__ = 'simulate DDE support'

import sys
from modules import DDE
from modules import Mixin
from modules import dict4ini

def app_init(app, filenames):
#    print app.ddeflag
    if app.ddeflag:
        x = dict4ini.DictIni('config.ini')
        port = x.server.get('port', 0)
        if not DDE.run(app, port):
#            print "send data", '\n'.join(filenames)
            DDE.senddata('\n'.join(filenames))
            sys.exit(0)
Mixin.setPlugin('app', 'dde', app_init, Mixin.HIGH, 0)

def afterclosewindow(win):
    if win.app.ddeflag:
        DDE.stop()
Mixin.setPlugin('mainframe', 'afterclosewindow', afterclosewindow)

def openfiles(win, files):
    if files:
        for filename in files:
            win.editctrl.new(filename)
        win.Show()
        win.Raise()
Mixin.setMixin('mainframe', 'openfiles', openfiles)