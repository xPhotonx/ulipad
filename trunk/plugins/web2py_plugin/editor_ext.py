#   Programmer: ygao
#   E-mail:     ygao2004@gmail.com
#
#   Copyleft ygao
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
import os
import re
from modules import Mixin
import wx
from modules import common
from modules.Debug import error
regex_def=re.compile('^def\s+(?P<name>(?:[a-zA-Z0-9]\w*)|(?:_[a-zA-Z0-9]\w*))\(')

def get_controller(win):
    controller = None
    line = win.GetCurrentLine()
    def_match = regex_def.match(win.GetLine(line))
    if def_match:
        controller = def_match.groups('name')[0]
        return controller
    if  win.syntax_info:
        obj = win.syntax_info.guess(line)
        if  len(obj) > 0:
            controller = obj[0].name
            return controller

def get_view(win):
    path = common.getProjectHome(win.filename)
    if not os.path.exists(os.path.join(path, "web2py.py")):
        common.showerror(win, tr("setting web2py project is not correctly"))
        return
    if "controllers" in win.filename:
        app = os.path.dirname(os.path.dirname(win.filename))
        if  os.path.split(win.filename)[1] == 'default.py':
            view = os.path.join(app, "views", "default", get_controller(win) + ".html")
        elif os.path.split(win.filename)[1] == 'appadmin.py':
            view = os.path.join(app, "views", "appadmin" + ".html") 
        else:
            view = os.path.join(app, "views", os.path.splitext(os.path.split(win.filename)[1])[0], get_controller(win) + ".html")
        return view
    
def dynamic_menu(win):
    view = get_view(win)
    if os.path.exists(view):
        return tr('&Goto %s view ') % get_controller(win)
    else:
        return tr('&Create %s view') % get_controller(win)
    
def other_popup_menu(editor, projectname, menus):
    if editor.languagename == 'python' and 'web2py' in common.getProjectName(editor.filename) and "controllers" in editor.filename:
        menus.extend([(None, #parent menu id
            [
                (30, 'IDPM_WEB2PY_PROJECT', tr('&Web2py'), wx.ITEM_NORMAL, '', ''),
                (35, 'IDPM_WEB2PY_PROJECT_CONTROLLERS_VIEW', dynamic_menu(editor), wx.ITEM_NORMAL, 'OnWeb2pyProjectFunc', tr('Create a view or open view.')),
                
                (40, '', '-', wx.ITEM_SEPARATOR, None, ''),
            ]),
            ('IDPM_WEB2PY_PROJECT',
            [
##                (100, 'IDPM_WEB2PY_PROJECT_CONTROLLERS_VIEW', dynamic_menu(editor), wx.ITEM_NORMAL, 'OnWeb2pyProjectFunc', tr('Create a view or open view.')),
                (110, '', '-', wx.ITEM_SEPARATOR, None, ''),
            ]),
        ])
Mixin.setPlugin('editor', 'other_popup_menu', other_popup_menu)

def OnWeb2pyProjectFunc(win, event):
    _id = event.GetId()
    
    try:
        if _id == win.IDPM_WEB2PY_PROJECT_CONTROLLERS_VIEW:
            OnWeb2pyProjectControllersView(win)
    except:
        error.traceback()
        common.showerror(win, tr("There is some wrong as executing the menu."))
Mixin.setMixin('editor', 'OnWeb2pyProjectFunc', OnWeb2pyProjectFunc)

def OnWeb2pyProjectControllersView(win):
    view = get_view(win)
    if os.path.exists(view):
        win.mainframe.editctrl.new(view)
    else:
        open(view, 'w').close()
        win.mainframe.editctrl.new(view).SetText("{{extend 'layout.html'}}\n")
        
