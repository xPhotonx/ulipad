#	Programmer:	limodou
#	E-mail:		chatme@263.net
#
#	Copyleft 2004 limodou
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
#	$Id: Mixin.py 176 2005-11-22 02:46:37Z limodou $

import types
from Debug import debug

__mixinset__ = {}	#used to collect all mixins and plugins
HIGH = 1	#plugin high
MIDDLE = 2
LOW = 3

class Mixin:
	__mixinname__ = ''	#mixin interface name, all subclass need define its own __mixinname__

	def __init__(self):
		self.initmixin()

	def initmixin(self):
		debug.info('[Mixin] Dealing class [%s]' % self.__class__.__name__)
		if self.__class__.__name__ == 'Mixin':	#don't dealing Mixin class itself
			return
		if hasattr(self.__class__, '__mixinflag__'):
			if self.__class__.__mixinflag__ >= 1:	#having executed mixin
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
			for name in mixins.keys():
				setProperty(self.__class__, name, mixins[name])
			setProperty(self.__class__, '__plugins__', plugins)
		else:
			setProperty(self.__class__, '__plugins__', {})

	def callplugin(self, name, *args, **kwargs):
		if not self.__plugins__.has_key(name):
			#debug.error('[Mixin] The plugin [%s] has not been implemented yet!' % name)
			return

		for nice, f in self.__plugins__[name]:
			#debug.info("[Mixin] Call plugin [%s]" % name)
			f(*args, **kwargs)

	def execplugin(self, name, *args, **kwargs):
		"""If some function return True, then all invokes return. So if you want the next function will
		process coninuely, you should return False or None"""
		if not self.__plugins__.has_key(name):
			#debug.error('[Mixin] The plugin [%s] has not been implemented yet!' % name)
			return None

		for nice, f in self.__plugins__[name]:
			v = f(*args, **kwargs)
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

#def searchpackage(packagename):
#	module=__import__(packagename)
#	if hasattr(module, '__all__'):
#		for i in module.__all__:
#			debug.info('[Mixin] Dealing module [%s]' % i)
#			__import__(packagename+'.'+i)

def setMixin(mixinname, name, value):
	if __mixinset__.has_key(mixinname):
		mixins = __mixinset__[mixinname][0]
	else:
		__mixinset__[mixinname] = ({}, {})
		mixins = __mixinset__[mixinname][0]

	t = type(value)
	if t in (types.DictType, types.TupleType, types.ListType):
		if mixins.has_key(name):
			if t == types.DictType :
				mixins[name].update(value)
			elif t == types.ListType:
				mixins[name].extend(value)
			else:
				mixins[name] += value
		else:
			mixins[name] = value
	else:
		mixins[name] = value

def setPlugin(mixinname, name, value, kind=MIDDLE, nice=-1):
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
		plugins[name].sort()
	else:
		plugins[name] = [(nice, value)]

def setProperty(obj, name, value):
	t = type(value)
	if t in (types.DictType, types.TupleType, types.ListType):
		if hasattr(obj, name):
			oldvalue = getattr(obj, name)
			if t == types.DictType :
				oldvalue.update(value)
			elif t == types.ListType:
				oldvalue.extend(value)
			else:
				setattr(obj, name, oldvalue + value)
		else:
			setattr(obj, name, value)
	else:
		setattr(obj, name, value)

def printMixin():
	debug.info("[Mixin] Printing mixin set...")
	for name, value in __mixinset__.items():
		mixins, plugins = value
		debug.info("\tname=%s" % name)
		debug.info("\t   |----mixin")
		keys = mixins.keys()
		keys.sort()
		for k in keys:
			f = mixins[k]
			if callable(f):
				debug.info("\t          |%s\t%s.%s" % (k, f.__module__, f.__name__))
			else:
				debug.info("\t          |%s" % k)
		debug.info("\t   |----plugin")
		keys = plugins.keys()
		keys.sort()
		for k in keys:
			debug.info("\t          |%s" % k)
			for nice, f in plugins[k]:
				debug.info("\t\t          %d %s.%s" % (nice, f.__module__, f.__name__))