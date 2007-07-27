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
#	$Id: Preference.py 176 2005-11-22 02:46:37Z limodou $

from modules import Mixin
from modules.Debug import debug
import copy
import pickle
import os.path
from modules.EasyGui import obj2ini

class Preference(Mixin.Mixin):
	__mixinname__ = 'preference'
#	preflist = [
#		('generic', 100, 'check', 'utf8_encoding_auto_detect', True, 'UTF-8 encoding auto detect', None),
#		('generic', 200, 'num', 'int', 100, 'int value', None),
#		('generic', 150, 'choice', 'select1', 'one', 'combox1', ['two', 'one', 'three']),
#		('generic', 150, 'choice', 'select2', 3, 'combox2', ['two', 'one', 'three']),
#		('generic', 300, 'text', 'name', 'limodou','enter your name',  None),
#		('generic', 100, 'num', 'recent_files_num', 10, 'Max number of recent files:', None),
#		('HTML', 100, 'check', 'html', False, 'Html format', None),
#	]
	preflist = []
	defaultfile = os.path.abspath('newedit.ini')

	def __init__(self):
		self.initmixin()
		self.callplugin('init', self)
		self.preflist.sort()

	def clone(self):
		return copy.copy(self)

	def save(self, filename=''):
		if not filename:
			filename = self.defaultfile
#		pickle.dump(self, open(filename, 'w'))
		obj2ini.dump(self, filename)

	def load(self, filename=''):
#		if not filename:
#			filename = self.defaultfile
#		if os.path.exists(filename):
#			obj = pickle.load(open(filename))
#			for k, v in obj.__dict__.items():
#				if hasattr(self, k):
#					setattr(self, k, v)
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