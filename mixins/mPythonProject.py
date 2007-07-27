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
#   $Id: DirBrowser.py 262 2005-12-14 04:11:44Z limodou $

import sys
from modules import Mixin
from modules.Debug import error

def add_project(project_names):
    project_names.extend(['python'])
Mixin.setPlugin('dirbrowser', 'add_project', add_project)

def project_begin(dirwin, project_names, path):
    if 'python' in project_names:
        sys.path.insert(0, path)
Mixin.setPlugin('dirbrowser', 'project_begin', project_begin)

def project_end(dirwin, project_names, path):
    if 'python' in project_names:
        try:
            sys.path.remove(path)
        except:
            error.traceback()
Mixin.setPlugin('dirbrowser', 'project_end', project_end)
