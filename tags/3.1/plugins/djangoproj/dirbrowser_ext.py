#   Programmer: limodou
#   E-mail:     limodou@gmail.com
#
#   Copyleft 2005 limodou
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

from modules import Mixin
import wx
import os
from modules import common
from modules.Debug import error

def other_popup_menu(dirwin, projectname, menus):
    item = dirwin.tree.GetSelection()
    if not item.IsOk(): return
    if projectname == 'django' and dirwin.get_node_filename(item) == os.path.join(dirwin.getCurrentProjectHome(), 'apps'):
        menus.extend([ (None,
            [
                (500, '', '-', wx.ITEM_SEPARATOR, None, ''),
                (510, 'IDPM_DJANGO_STARTAPP', tr('Create New Application'), wx.ITEM_NORMAL, 'OnDjangoFunc', ''),
#                (520, 'IDPM_DJANGO_INSTALLAPP', tr('Install Application'), wx.ITEM_NORMAL, 'OnDjangoFunc', ''),
            ]),
        ])
Mixin.setPlugin('dirbrowser', 'other_popup_menu', other_popup_menu)

def OnDjangoFunc(win, event):
    _id = event.GetId()
    try:
        if _id == win.IDPM_DJANGO_STARTAPP:
            OnDjangoStartApp(win)
#        elif _id == win.IDPM_DJANGO_INSTALLAPP:
#            OnDjangoInstallApp(win)
    except:
        error.traceback()
        common.showerror(win, tr("There is some wrong as executing the menu."))
Mixin.setMixin('dirbrowser', 'OnDjangoFunc', OnDjangoFunc)

def OnDjangoStartApp(win):
    appname = get_django_name(win)
    if appname:
        oldpath = os.getcwd()
        try:
            os.chdir(os.path.join(win.getCurrentProjectHome(), 'apps'))
            os.system('django-admin.py startapp %s' % appname)
            win.OnRefresh(None)
            common.showmessage(win, tr('Completed!'))
        finally:
            os.chdir(oldpath)

#def OnDjangoInstallApp(win):
#    appname = get_django_name(win)
#    if appname:
#        oldpath = os.getcwd()
#        try:
#            path = win.getProjectHome()
#            module = os.path.basename(path)
#            settings_file = os.path.join(path, 'settings.py')
#            text = file(settings_file).read()
#            text = text.replace('#@INSTALLED_APPS', "#@INSTALLED_APPS\n....'%s.apps.%s'," % (module, appname))
#            file(settings_file, 'w').write(text)
#            os.system('django-admin.py install %s' % appname)
#            common.showmessage(win, tr('Completed!'))
#        finally:
#            os.chdir(oldpath)
#
def get_django_name(win):
    elements = [
    ('string', 'appname', '', tr('Django application name:'), None),
    ]
    from modules.EasyGui import EasyDialog
    easy = EasyDialog.EasyDialog(win, title=tr('Input'), elements=elements)
    appname = None
    if easy.ShowModal() == wx.ID_OK:
        values = easy.GetValue()
        appname = values['appname']
        if not appname:
            common.showerror(win, tr("Django application name cannot be empty."))
    easy.Destroy()
    return appname