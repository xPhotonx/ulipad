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
#	$Id: SnippetClass.py 481 2006-01-17 05:54:13Z limodou $

__doc__ = 'parse XML formatted snippets'

from xml.dom.minidom import parse, getDOMImplementation
import os.path
import codecs

class SnippetCatalog:
	def __init__(self, xmlfile):
		if not os.path.exists(xmlfile):
			WriteSnippetCatalog(xmlfile)
		self.dom = parse(xmlfile)
		self.root = self.dom.documentElement  #or self.root = self.dom.firstChild

	def __iter__(self):
		self.iter = self.listnode(self.root)
		return self.iter

	def next(self):
		return self.iter.next()

	def listnode(self, node, level=0):
		for i in node.childNodes:
			if i.nodeType == i.ELEMENT_NODE:
				if i.nodeName == 'item':
					caption = getTagText(i, 'caption')
					id = i.getAttribute('id')
					yield level, caption, int(id)
					for v in self.listnode(i, level+1):
						yield v

	def getmaxid(self):
		maxid = getTagText(self.root, 'maxid')
		return int(maxid)

class SnippetCode:
	def __init__(self, xmlfile):
		if not os.path.exists(xmlfile):
			WriteSnippetCode(xmlfile)
		self.dom = parse(xmlfile)
		self.root = self.dom.documentElement

	def __iter__(self):
		return self.listnode()

	def listnode(self):
		for i in self.root.childNodes:
			if i.nodeType == i.ELEMENT_NODE:
				if i.nodeName == 'item':
					abbr = getTagText(i, 'abbr')
					author =getTagText(i, 'author')
					description = getTagText(i, 'description')
					date = getTagText(i, 'date')
					version = getTagText(i, 'version')
					code = getTagText(i, 'code')
					yield abbr, description, author, version, date, code

def WriteSnippetCatalog(xmlfile, maxid=0, items=()):
	impl = getDOMImplementation()
	dom = impl.createDocument(None, 'catalog', None)
	root = dom.documentElement
	root.appendChild(makeEasyTag(dom, 'maxid', str(maxid)))
	stack = [root]
	lastlevel = 0
	lastnode = root
	for v in items:
		level, caption, id = v
		if level < lastlevel:
			stack = stack[:level+1]
		elif level > lastlevel:
			stack.append(lastnode)
		parent = stack[level]
		lastlevel = level
		lastnode = makeCatalogNode(dom, caption, id)
		parent.appendChild(lastnode)

	domcopy = dom.cloneNode(True)
	Indent(domcopy, domcopy.documentElement)
	f = file(xmlfile, 'wb')
	writer = codecs.lookup('utf-8')[3](f)
	domcopy.writexml(writer, encoding = 'utf-8')
	domcopy.unlink()

def WriteSnippetCode(xmlfile, items=()):
	impl = getDOMImplementation()
	dom = impl.createDocument(None, 'data', None)
	root = dom.documentElement
	for v in items:
		node = makeCatalogCode(dom, *v)
		root.appendChild(node)

	domcopy = dom.cloneNode(True)
	Indent(domcopy, domcopy.documentElement)
	f = file(xmlfile, 'wb')
	writer = codecs.lookup('utf-8')[3](f)
	domcopy.writexml(writer, encoding = 'utf-8')
	domcopy.unlink()

def Indent(dom, node, indent = 0):
	# Copy child list because it will change soon
	children = node.childNodes[:]
	# Main node doesn't need to be indented
	if indent:
		text = dom.createTextNode('\n' + '\t' * indent)
		node.parentNode.insertBefore(text, node)
	if children:
		# Append newline after last child, except for text nodes
		if children[-1].nodeType == node.ELEMENT_NODE:
			text = dom.createTextNode('\n' + '\t' * indent)
			node.appendChild(text)
		# Indent children which are elements
		for n in children:
			if n.nodeType == node.ELEMENT_NODE:
				Indent(dom, n, indent + 1)

def makeCatalogNode(dom, caption, id):
	caption_node = makeEasyTag(dom, 'caption', caption)
	item_node = dom.createElement('item')
	item_node.setAttribute('id', id)
	item_node.appendChild(caption_node)
	return item_node

def makeCatalogCode(dom, abbr, description, author, version, date, code):
	item_node = dom.createElement('item')
	item_node.appendChild(makeEasyTag(dom, 'abbr', abbr))
	item_node.appendChild(makeEasyTag(dom, 'description', description, 'cdata'))
	item_node.appendChild(makeEasyTag(dom, 'author', author))
	item_node.appendChild(makeEasyTag(dom, 'version', version))
	item_node.appendChild(makeEasyTag(dom, 'date', date))
	item_node.appendChild(makeEasyTag(dom, 'code', code, 'cdata'))
	return item_node

def makeEasyTag(dom, tagname, value, type='text'):
	tag = dom.createElement(tagname)
	if value.find(']]>') > -1:
		type = 'text'
	if type == 'text':
		value = value.replace('&', '&amp;')
		value = value.replace('<', '&lt;')
		text = dom.createTextNode(value)
	elif type == 'cdata':
		text = dom.createCDATASection(value)
	tag.appendChild(text)
	return tag

def getTagText(root, tag):
	node = root.getElementsByTagName(tag)[0]
	rc = ""
	for node in node.childNodes:
		if node.nodeType in ( node.TEXT_NODE, node.CDATA_SECTION_NODE):
			rc = rc + node.data
	return rc

if __name__ == '__main__':
	s = SnippetCatalog('d:/project/newedit/src/snippets/catalog.xml')
	for level, name, id in s:
		print level, name, id

#	s = SnippetData('d:/project/newedit/src/snippets/snippet1.xml')
#	for abbr, description, author, version, date, code in s:
#		print abbr, description, author, version, date, code