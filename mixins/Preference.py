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
#   $Id: Preference.py 1457 2006-08-23 02:12:12Z limodou $

import copy
import os.path
from modules import Mixin
from modules.Debug import debug
from modules.EasyGuider import obj2ini
from modules import Globals

class Preference(Mixin.Mixin):
    __mixinname__ = 'preference'
    preflist = []

    def __init__(self):
        self.initmixin()
        self.defaultfile = os.path.join(Globals.workpath, 'ulipad.ini')
        #@add_pref preflist
        self.callplugin_once('add_pref', Preference.preflist)
        self.callplugin('init', self)
        self.preflist.sort()

    def clone(self):
        return copy.copy(self)

    def save(self, filename=''):
        if not filename:
            filename = self.defaultfile
#       pickle.dump(self, open(filename, 'w'))
        obj2ini.dump(self, filename)

    def load(self, filename=''):
#       if not filename:
#           filename = self.defaultfile
#       if os.path.exists(filename):
#           obj = pickle.load(open(filename))
#           for k, v in obj.__dict__.items():
#               if hasattr(self, k):
#                   setattr(self, k, v)
        if not filename:
            filename = self.defaultfile
        if os.path.exists(filename):
            obj2ini.load(filename, obj=self)

    def printValues(self):
        debug.info("[preference] member variable...")
        for k, v in self.__dict__.items():
            debug.info('\t', k,'=', v)
        debug.info('[preference] preference dialog member...')
        for v in self.preflist:
            debug.info('\t',v)
