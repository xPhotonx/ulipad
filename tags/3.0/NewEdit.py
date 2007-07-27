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
#   $Id: NewEdit.py 71 2005-09-29 06:39:27Z limodou $

__appname__ = 'NewEdit'
__author__ = 'limodou'

import getopt
import sys
import wx
import os
import locale
import os.path
import codecs
from modules import common
from modules import Mixin
from modules import Debug
from modules import i18n
from modules import IniFile

workpath = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.insert(0, workpath)
sys.path.insert(0, os.path.join(workpath, 'modules'))
sys.path.insert(0, os.path.join(workpath, 'plugins'))
curpath = os.getcwd()
os.chdir(workpath)

#install i18n package
i18n = i18n.I18n('./lang', keyfunc='tr')
ini = IniFile.IniFile()
if ini.has_option('language', 'default'):
    language = ini.get('language', 'default', '')
    i18n.install(language)

#import mixins
try:
    import mixins
except:
    Debug.error.traceback()
    print "There are some errors as importing mimxins, Please see the error.txt."
    sys.exit(0)

class wxApp(wx.App):
    def OnInit(self):
        return True

app = None

class App(Mixin.Mixin):
    __mixinname__ = 'app'
    
    def __init__(self):
        global app
        
        app = self
        import __builtin__
        __builtin__.__dict__['app'] = app
        
        self.initmixin()
        
        self.appname = __appname__
        self.author = __author__
        
        self.wxApp = wxApp(0)
        self.frame = self.init()
        self.frame.Show()
        self.wxApp.SetTopWindow(self.frame)
        self.wxApp.MainLoop()
        
    def init(self, showSplash=True, load=True): 

        #add modules path to sys.path
        self.workpath = workpath
        self.curpath = curpath
        self.i18n = i18n

        self.processCommandLineArguments()

        if self.psycoflag:
            try:
                import psyco
                psyco.full()
            except:
                pass
        
        #change workpath
        self.userpath = self.workpath
        if self.multiuser:
            self.userpath = common.getHomeDir()
            
        Debug.debug = Debug.Debug(os.path.join(self.userpath, 'debug.txt'))
        Debug.error = Debug.Debug(os.path.join(self.userpath, 'error.txt'))

        #-----------------------------------------------------------------------------

        self.callplugin('start', self, self.files)

        #-----------------------------------------------------------------------------

        self.CheckPluginDir()
        
        try:
            import plugins
        except:
            common.showerror(None, tr('There is something wrong as importing plugins.'))

        #-----------------------------------------------------------------------------

        #before running gui
        self.callplugin("beforegui", self)

        Mixin.printMixin()

        return self.execplugin('getmainframe', self, self.files)

    def processCommandLineArguments(self):
        #process command line
        try:
            opts, args = getopt.getopt(sys.argv[1:], "e:vunsfm", [])
        except getopt.GetoptError:
            self.Usage()
            sys.exit(2)
        self.defaultencoding = common.defaultencoding   #defaultencoding in common.py
        
        self.ddeflag = True
        self.psycoflag = False
        self.skipsessionfile = False
        self.multiuser = False
        
        for o, a in opts:
            if o == '-e':       #encoding
                defaultencoding = a
            elif o == '-v':     #version
                self.Version()
                sys.exit()
            elif o == '-u':     #usage
                self.Usage()
                sys.exit()
            elif o == '-n':     #no dde
                self.ddeflag = False
            elif o == '-s':
                self.psycoflag = True
            elif o == '-f':
                self.skipsessionfile = True
            elif o == '-m':
                self.multiuser = True
        files = args
        
        self.files = [common.decode_string(os.path.join(self.curpath, f)) for f in files]

    def quit(self):
        self.wxApp.ProcessIdle()
        self.wxApp.Exit()

    def Usage(self):
        print """Usage %s -u|-v|-n|[-e encoding]|-s|-f|-m files ...
    
        -u Show this message
        -v Show version information
        -n Disable DDE support
        -e encoding Set default encoding which will be used in NewEdit
        -s Enable psyco speed support
        -f Skip last session files
        -m Multi user mode, data file will be saved in user home directory
    """ % sys.argv[0]
    
    def Version(self):
        from modules import Version
    
        print """%s Copyleft GPL
Author: %s
Version: %s""" % (__appname__, __author__, Version.version)

    def CheckPluginDir(self):
        pluginpath = os.path.join(self.workpath, 'plugins')
        if not os.path.exists(pluginpath):
            os.mkdir(pluginpath)
        if not os.path.exists(os.path.join(pluginpath, '__init__.py')):
            file(os.path.join(pluginpath, '__init__.py'), 'w').write("""#   Programmer: limodou
#   E-mail:     limodou@gmail.com
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

__doc__ = 'Plugins __init__.py'

""")


App()