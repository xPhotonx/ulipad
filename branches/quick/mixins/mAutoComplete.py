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
#	$Id: mAutoComplete.py 475 2006-01-16 09:50:28Z limodou $

import wx
import inspect
import sets
import re
import sys
import os
from modules import Mixin
from modules.Debug import error
from modules import common

CALLTIP_AUTOCOMPLETE = 2

def pref_init(pref):
	pref.python_calltip = True
	pref.python_autocomplete = True
Mixin.setPlugin('preference', 'init', pref_init)

def add_pref(preflist):
    preflist.extend([
        (tr('Python'), 120, 'check', 'python_calltip', tr("Enable calltip"), None),
        (tr('Python'), 130, 'check', 'python_autocomplete', tr("Enable auto completion"), None),
    ])
Mixin.setMixin('preference', 'add_pref', add_pref)

def editor_init(win):
	win.AutoCompSetIgnoreCase(True)
	win.AutoCompStops(' .,;:([)]}\'"\\<>%^&+-=*/|`')
	win.AutoCompSetAutoHide(False)
	win.calltip_times = 0
	win.calltip_column = 0
	win.calltip_line = 0
	win.namespace = {}
Mixin.setPlugin('editor', 'init', editor_init)

def on_idle(win, event):
	if not win.app.wxApp.IsActive():
		if win.AutoCompActive():
			win.AutoCompCancel()
Mixin.setPlugin('editor', 'on_idle', on_idle)

def on_key_down(win, event):
	key = event.GetKeyCode()
	control = event.ControlDown()
	#shift=event.ShiftDown()
	alt=event.AltDown()
	if key == wx.WXK_RETURN and not control and not alt:
		if not win.AutoCompActive():
			if win.calltip.active or win.calltip_times > 0:
				win.calltip_times = 0
				win.calltip.cancel()
		else:
			event.Skip()
			return True
	elif key == wx.WXK_ESCAPE:
		win.calltip.cancel()
		win.calltip_times = 0
Mixin.setPlugin('editor', 'on_key_down', on_key_down, Mixin.HIGH, 1)

def on_key_up(win, event):
	curpos = win.GetCurrentPos()
	line = win.GetCurrentLine()
	column = win.GetColumn(curpos)
	if win.calltip.active and win.calltip_type == CALLTIP_AUTOCOMPLETE:
		if column < win.calltip_column or line != win.calltip_line:
			win.calltip_times = 0
			win.calltip.cancel()
Mixin.setPlugin('editor', 'on_key_up', on_key_up)

def on_char(win,event):
	key = event.KeyCode()
	control = event.ControlDown()
	alt=event.AltDown()
	if win.languagename != 'python':
		return False

	# GF We avoid an error while evaluating chr(key), next line.
	if key > 255:
		return False

	# if document has selected text, then skip
	if win.GetSelectedText():
		return False

	# GF No keyboard needs control or alt to make '(', ')' or '.'
	# GF Shift is not included as it is needed in some keyboards.
	if chr(key) in ['(',')','.'] and not control and not alt:
		if win.AutoCompActive():
			win.AutoCompCancel()
		pos=win.GetCurrentPos()
		if key == ord('(') and win.pref.python_calltip:
			# ( start tips
			if win.calltip.active and win.calltip_type == CALLTIP_AUTOCOMPLETE:
				win.calltip_times += 1
				win.AddText('(')
			else:
				obj=getWordObject(win)
				win.AddText('(')
				if not obj:
					return True
				tip=getargspec(obj)
				doc = obj.__doc__
				if doc:
					tip += doc
				if tip:
					if win.AutoCompActive():
						win.AutoCompCancel()
					win.calltip_times = 1
					win.calltip_type = CALLTIP_AUTOCOMPLETE
					tip = tip.rstrip() + tr('\n\n(Press ESC to close)')
					win.calltip.show(pos, tip.replace('\r\n','\n'))

					#save position
					curpos = win.GetCurrentPos()
					win.calltip_column = win.GetColumn(curpos)
					win.calltip_line = win.GetCurrentLine()
				else:
					win.AddText(')')
					win.GotoPos(win.GetCurrentPos() - 1)
		elif key == ord(')'):
			# ) end tips
			win.AddText(')')
			if win.calltip.active:
				win.calltip_times -= 1
				if win.calltip_times == 0:
					win.calltip.cancel()
		elif key == ord('.') and win.pref.python_autocomplete:
			# . Code completion
			if win.calltip.active:
				win.calltip.cancel()
			autoComplete(win, object=1)
		else:
			return False
		return True
	else:
		return False
Mixin.setPlugin('editor', 'on_char', on_char)

def afteropenfile(win, filename):
	win.namespace = {}
Mixin.setMixin('editor', 'afteropenfile', afteropenfile)

def getWordObject(win, word=None, whole=None):
	if not word:
		word = getWord(win, whole=whole)
	try:
		return evaluate(win, word)
	except:
		error.traceback()
		return None
Mixin.setMixin('editor', 'getWordObject', getWordObject)

def getWord(win, whole=None):
	pos=win.GetCurrentPos()
	line = win.GetCurrentLine()
	linePos=win.PositionFromLine(line)
	txt = win.GetLine(line)
	start=win.WordStartPosition(pos,1)
	i = start - 1
	while i >= 0:
		if win.getChar(i) in win.mainframe.getWordChars() + '.':
			start -= 1
			i -= 1
		else:
			break
	if whole:
		end=win.WordEndPosition(pos,1)
	else:
		end=pos
	return txt[start-linePos:end-linePos]


def evaluate(win, word):
	try:
		obj = eval(word, win.namespace)
		return obj
	except:
		import_document(win)
		try:
			obj = eval(word, win.namespace)
			return obj
		except:
			return None

def autoComplete(win, object=0):
	import wx.py.introspect as intro

	word = getWord(win)
	if object:
		win.AddText('.')
		word += '.'

	words = getAutoCompleteList(intro, win, word)
	if words:
		win.AutoCompShow(0, " ".join(words))
	else:
		words = getWords(win, word)
		if words:
			win.AutoCompShow(0, " ".join(words))

def getAutoCompleteList(modules, win, command='', includeMagic=1,
						includeSingle=1, includeDouble=1):
	"""Return list of auto-completion options for command.

	The list of options will be based on the locals namespace."""
	attributes = []
	# Get the proper chunk of code from the command.
	object = None
	if command.endswith('.'):
		root = command[:-1]
	else:
		root = command
	try:
		object = eval(root, win.namespace)
	except:
		error.traceback()
		import_document(win)
		try:
			object = eval(root, win.namespace)
		except:
			error.traceback()
			pass
	if object:
		attributes = modules.getAttributeNames(object, includeMagic,
									   includeSingle, includeDouble)
	return attributes

def import_document(win):
	dir = common.encode_string(os.path.dirname(win.filename))
	if dir not in sys.path:
		sys.path.insert(0, dir)
	r = re.compile(r'^\s*from\s+.*$|^\s*import\s+.*$', re.M)
	result = r.findall(win.GetText())
	result = [s.strip() for s in result]
	for line in result:
		if line.startswith('from'):
			try:
				exec(line) in win.namespace
			except:
				error.traceback()
		elif line.startswith('import'):
			try:
				exec(line) in win.namespace
			except:
				error.traceback()


def getWords(win, word=None, whole=None):
	if not word:
		word = win.getWord(whole=whole)
	if not word:
		return []
	else:
		word = word.replace('.', r'\.')
		words = list(sets.Set([x for x in re.findall(r"\b" + word + r"(\w+)\b", win.GetText())]))
		words.sort(lambda x, y:cmp(x.upper(), y.upper()))
		return words

def getargspec(func):
	"""Get argument specifications"""
	try:
		func=func.im_func
	except:
		error.traceback()
		pass
	try:
		return inspect.formatargspec(*inspect.getargspec(func))+'\n\n'
	except:
		error.traceback()
		pass
	try:
		return inspect.formatargvalues(*inspect.getargvalues(func))+'\n\n'
	except:
		error.traceback()
		return ''
