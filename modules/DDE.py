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
#	$Id: DDE.py 475 2006-01-16 09:50:28Z limodou $

from socket import *
import threading
from Debug import error
import wx

ADDR = '127.0.0.1'
PORT = 50000

server = None
g_port = PORT

def init(port):
	global g_port

	if port == 0:
		port = PORT
	g_port = port
	server = socket(AF_INET, SOCK_STREAM)
	try:
		server.bind((ADDR, port))
	except:
#		traceback.print_exc()
		server = None
		return server
	return server

def start(server, app=None):
	server.listen(1)
#	print 'server starting'
	while True:
		conn = server.accept()[0]
		try:
			data = conn.recv(256)
			if data:
				data = data.decode('utf-8')
				lines = data.splitlines()
				cmd = lines[0]
				if cmd == 'data':
#					print 'data'
					if app:
						wx.CallAfter(app.frame.openfiles, lines[1:])
				elif cmd == 'stop':
#					print 'stop'
					break
		except:
			error.traceback()
#			traceback.print_exc()
			pass


def sendraw(cmd, data):
	try:
		sendSock = socket(AF_INET, SOCK_STREAM)
		sendSock.connect((ADDR, g_port))
		data = data.encode('utf-8')
		sendSock.send(cmd+'\n'+data)
		sendSock.close()
	except:
		error.traceback()

def stop():
	sendraw('stop', '')

def senddata(data):
	sendraw('data', data)

def run(app=None, port=PORT):
	server = init(port)
	if server:
		t = threading.Thread(target=start, args=(server, app,), name='dde')
		t.setDaemon(True)
		t.start()
		return True
	else:
		return False