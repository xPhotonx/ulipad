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
#   $Id: Mixin.py 486 2006-01-17 12:08:32Z limodou $

import types

__mixinset__ = {}   #used to collect all mixins and plugins
HIGH = 1    #plugin high
MIDDLE = 2
LOW = 3
MUST_FUNC = False
ENABLE = True

log = None

class Mixin:
    __mixinname__ = ''  #mixin interface name, all subclass need define its own __mixinname__

    def __init__(self):
        self.initmixin()

    def initmixin(self):
        from Debug import debug
        debug.info('[Mixin] Dealing class [%s]' % self.__class__.__name__)
        if self.__class__.__name__ == 'Mixin':  #don't dealing Mixin class itself
            return
        if hasattr(self.__class__, '__mixinflag__'):
            if self.__class__.__mixinflag__ >= 1:   #having executed mixin
                return
            else:
                self.__class__.__mixinflag__ = 1
        else:
            setattr(self.__class__, '__mixinflag__', 1)
        if not self.__mixinname__:
            debug.warn('[Mixin] The class [%s] has not a mixinname defined' % self.__class__.__name__)
            return
        
        if __mixinset__.has_key(self.__mixinname__):
            debug.info('[Mixin] Mixinning class [%s]' % self.__class__.__name__)
            mixins, plugins = __mixinset__[self.__mixinname__]
            items = {}
            for name, value in mixins.items():
                if not value[0]:
                    setProperty(self.__class__, name, value[1])
                else:
                    items[name] = value[1]
            setattr(self.__class__, '__mixins__', items)
            setattr(self.__class__, '__plugins__', plugins)
        else:
            setattr(self.__class__, '__mixins__', {})
            setattr(self.__class__, '__plugins__', {})
        setattr(self.__class__, '__one_plugins__', {})

    def callplugin_once(self, name, *args, **kwargs):
        if self.__one_plugins__.get(name, 0) < 1:
            self.__one_plugins__[name] = 1
            self.callplugin(name, *args, **kwargs)

    def callplugin(self, name, *args, **kwargs):
        if not self.__plugins__.has_key(name):
            #debug.error('[Mixin] The plugin [%s] has not been implemented yet!' % name)
            return

        items = self.__plugins__[name]
        items.sort()
        for i in range(len(items)):
            #debug.info("[Mixin] Call plugin [%s]" % name)
            nice, f = items[i]
            f = import_func(f)
            if callable(f):
                items[i] = (nice, f)
            try:
                f(*args, **kwargs)
            except SystemExit:
                raise
            except:
                if log:
                    log.traceback()
                else:
                    raise

    def execplugin_once(self, name, *args, **kwargs):
        if self.__one_plugins__.get(name, 0) < 1:
            self.__one_plugins__[name] = 1
            return self.callplugin(name, *args, **kwargs)

    def execplugin(self, name, *args, **kwargs):
        """If some function return True, then all invokes return. So if you want the next function will
        process coninuely, you should return False or None"""
        if not self.__plugins__.has_key(name):
            #debug.error('[Mixin] The plugin [%s] has not been implemented yet!' % name)
            return None

        items = self.__plugins__[name]
        items.sort()
        for i in range(len(items)):
            nice, f = items[i]
            f = import_func(f)
            if callable(f):
                items[i] = (nice, f)
            try:
                v = f(*args, **kwargs)
            except SystemExit:
                raise
            except:
                if log:
                    log.traceback()
                    continue
                else:
                    raise
            if v:
                if type(v) == types.TupleType:
                    r = v[1:]
                    if len(r) == 1:
                        return r[0]
                    else:
                        return r
                else:
                    return v
        return None
    
    def __getattr__(self, name):
        if self.__mixins__.has_key(name):
            f = import_func(self.__mixins__[name])
            self.__mixins__[name] = f
            setProperty(self.__class__, name, f)
            return getattr(self, name)
        else:
            raise AttributeError, name

#def searchpackage(packagename):
#   module=__import__(packagename)
#   if hasattr(module, '__all__'):
#       for i in module.__all__:
#           debug.info('[Mixin] Dealing module [%s]' % i)
#           __import__(packagename+'.'+i)

def setMixin(mixinname, name, value):
    if not ENABLE:
        return
    
    if MUST_FUNC and not callable(value):
        print "name=%s, value=%r" % (name, value)
        raise Exception, 'The value should be a callable object'
    
    if __mixinset__.has_key(mixinname):
        mixins = __mixinset__[mixinname][0]
    else:
        __mixinset__[mixinname] = ({}, {})
        mixins = __mixinset__[mixinname][0]

    if MUST_FUNC:
        mixins[name] = (1, value)
    else:
        if isinstance(value, (dict, tuple, list)):
            if mixins.has_key(name):
                if isinstance(value, dict):
                    mixins[name][1].update(value)
                    mixins[name] = (0, mixins[name][1])
                elif isinstance(value, list):
                    mixins[name][1].extend(value)
                    mixins[name] = (0, mixins[name][1])
                else:
                    mixins[name] = (0, mixins[name][1] + value)
            else:
                mixins[name] = (0, value)
        else:
            mixins[name] = (0, value)

def setPlugin(mixinname, name, value, kind=MIDDLE, nice=-1):
    if not ENABLE:
        return
    
    if MUST_FUNC and not callable(value):
        print "name=%s, value=%r" % (name, value)
        raise Exception, 'The value should be a callable object'
    
    if __mixinset__.has_key(mixinname):
        plugins = __mixinset__[mixinname][1]
    else:
        __mixinset__[mixinname] = ({}, {})
        plugins = __mixinset__[mixinname][1]

    if nice == -1:
        if kind == MIDDLE:
            nice = 500
        elif kind == HIGH:
            nice = 100
        else:
            nice = 900
    if plugins.has_key(name):
        plugins[name].append((nice, value))
    else:
        plugins[name] = [(nice, value)]

def setProperty(obj, name, value):
    if isinstance(value, (dict, tuple, list)):
        if hasattr(obj, name):
            oldvalue = getattr(obj, name)
            if isinstance(value, dict):
                oldvalue.update(value)
            elif isinstance(value, list):
                oldvalue.extend(value)
            else:
                setattr(obj, name, oldvalue + value)
        else:
            setattr(obj, name, value)
    else:
        setattr(obj, name, import_func(value))
        
def import_func(info):
    if isinstance(info, str):
        mod, func = info.rsplit('.', 1)
        info = getattr(__import__(mod, '', '', ['']), func)
    return info

def printMixin():
    from Debug import debug
    debug.info("[Mixin] Printing mixin set...")
    for name, value in __mixinset__.items():
        mixins, plugins = value
        debug.info("\tname=%s" % name)
        debug.info("\t   |----mixin")
        keys = mixins.keys()
        keys.sort()
        for k in keys:
            t, f = mixins[k]
            if callable(f):
                debug.info("\t          |%s\t%s.%s" % (k, f.__module__, f.__name__))
            else:
                debug.info("\t          |%s %s" % (k, f))
        debug.info("\t   |----plugin")
        keys = plugins.keys()
        keys.sort()
        for k in keys:
            debug.info("\t          |%s" % k)
            for nice, f in plugins[k]:
                if callable(f):
                    debug.info("\t\t          %d %s.%s" % (nice, f.__module__, f.__name__))
                else:
                    debug.info("\t\t          %d %s" % (nice, f))

def setlog(logobj):
    global log
    log = logobj