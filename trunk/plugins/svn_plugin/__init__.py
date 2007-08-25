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
#   $Id$

import wx
from modules import Mixin
import os

def pref_init(pref):
    pref.version_control_exe = ''
Mixin.setPlugin('preference', 'init', pref_init)

def add_pref(preflist):
    preflist.extend([
        (tr('Version'), 100, 'text', 'version_control_exe', tr('Select version control software'), None)
    ])
Mixin.setPlugin('preference', 'add_pref', add_pref)

def other_popup_menu(dirwin, projectname, menus):
    from modules import common
    
    item = dirwin.tree.GetSelection()
    if not item.IsOk(): return
    if not detect_svn(common.getCurrentDir(dirwin.get_node_filename(item))):
        return
    menus.extend([ (None,
        [
            (93, 'IDPM_VC_UPDATE', tr('Version Control: Update'), wx.ITEM_NORMAL, 'OnVC_DoCommand', ''),
            (94, 'IDPM_VC_CHECKOUT', tr('Version Control: Checkout'), wx.ITEM_NORMAL, 'OnVC_DoCommand', ''),
            (95, 'IDPM_VC_COMMIT', tr('Version Control: Commit'), wx.ITEM_NORMAL, 'OnVC_DoCommand', ''),
            (96, 'IDPM_VC_COMMANDS', tr('Version Control: Commands'), wx.ITEM_NORMAL, '', ''),
            (97, '', '-', wx.ITEM_SEPARATOR, None, ''),
        ]),
        ('IDPM_VC_COMMANDS',
        [
            (100, 'IDPM_VC_COMMANDS_LIST', tr('List'), wx.ITEM_NORMAL, 'OnVC_DoCommand', ''),
            (110, 'IDPM_VC_COMMANDS_SHOWLOG', tr('Show log'), wx.ITEM_NORMAL, 'OnVC_DoCommand', ''),
            (120, 'IDPM_VC_COMMANDS_STATUS', tr('Status'), wx.ITEM_NORMAL, 'OnVC_DoCommand', ''),
            (130, 'IDPM_VC_COMMANDS_DIFF', tr('Diff'), wx.ITEM_NORMAL, 'OnVC_DoCommand', ''),
            (145, '', '-', wx.ITEM_SEPARATOR, None, ''),
            (150, 'IDPM_VC_COMMANDS_ADD', tr('Add'), wx.ITEM_NORMAL, 'OnVC_DoCommand', ''),
            (160, 'IDPM_VC_COMMANDS_RENAME', tr('Rename'), wx.ITEM_NORMAL, 'OnVC_DoCommand', ''),
            (170, 'IDPM_VC_COMMANDS_DELETE', tr('Delete'), wx.ITEM_NORMAL, 'OnVC_DoCommand', ''),
            (180, 'IDPM_VC_COMMANDS_REVERSE', tr('Revert'), wx.ITEM_NORMAL, 'OnVC_DoCommand', ''),
            (190, '', '-', wx.ITEM_SEPARATOR, None, ''),
            (200, 'IDPM_VC_COMMANDS_EXPORT', tr('Export'), wx.ITEM_NORMAL, 'OnVC_DoCommand', ''),
            
        ]),
    ])
#    dir = common.getCurrentDir(dirwin.get_node_filename(item))
#    if os.path.isdir(dir) and os.path.exists(os.path.join(os.path.dirname(dir), '_project')):
#        menus.extend([ (None,
#        [
#            (520, 'IDPM_DJANGO_INSTALLAPP', tr('Install Application'), wx.ITEM_NORMAL, 'OnDjangoFunc', ''),
#        ]),
#    ])
Mixin.setPlugin('dirbrowser', 'other_popup_menu', other_popup_menu)

def OnVC_DoCommand(win, event):
    mapping = {
        'IDPM_VC_CHECKOUT':'checkout',
        'IDPM_VC_COMMIT':'commit',
        'IDPM_VC_UPDATE':'update',
        'IDPM_VC_COMMANDS_LIST':'list',
        'IDPM_VC_COMMANDS_STATUS':'status',
        'IDPM_VC_COMMANDS_SHOWLOG':'log',
        'IDPM_VC_COMMANDS_ADD':'add',
        'IDPM_VC_COMMANDS_RENAME':'rename',
        'IDPM_VC_COMMANDS_DELETE':'delete',
        'IDPM_VC_COMMANDS_REVERSE':'revert',
        'IDPM_VC_COMMANDS_DIFF':'diff',
        'IDPM_VC_COMMANDS_EXPORT':'export',
    }
    item = win.tree.GetSelection()
    if item.IsOk():
        path = win.get_node_filename(item)
    else:
        path = ''
    import SvnSupport as vc
    _id = event.GetId()
    for id, cmd in mapping.items():
        if _id == getattr(win, id, None):
            vc.do(win, cmd, path)
Mixin.setMixin('dirbrowser', 'OnVC_DoCommand', OnVC_DoCommand)

#functions
########################################################

def detect_svn(path):
    if os.path.exists(os.path.join(path, '.svn')):
        return True