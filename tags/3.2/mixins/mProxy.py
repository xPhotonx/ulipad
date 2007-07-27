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
#	$Id$

from modules import Mixin

def pref_init(pref):
    pref.use_proxy = False
    pref.proxy = ''
    pref.proxy_user = ''
    pref.proxy_password = ''
Mixin.setPlugin('preference', 'init', pref_init)

def add_pref(preflist):
    preflist.extend([
        (tr('General'), 200, 'check', 'use_proxy', tr('Use proxy'), None),
        (tr('General'), 210, 'text', 'proxy', tr('Proxy URL:'), None),
        (tr('General'), 220, 'text', 'proxy_user', tr('Proxy User:'), None),
        (tr('General'), 230, 'password', 'proxy_password', tr('Proxy Password:'), None),
    ])
Mixin.setPlugin('preference', 'add_pref', add_pref)

