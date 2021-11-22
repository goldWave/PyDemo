# -*- coding: utf-8 -*-

import socket
import threading
import time

HOST='127.0.0.1'
PORT=5967
bufsize = 1024
address = (HOST,PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(address)
s.listen(1)
print('Waiting for connecting...')


def tcplink(sock, addr):
	print("accept new connecting from %s:%s..." % addr)
	sock.send(b'Welcome.')
	while True:
		data = sock.recv(bufsize)
		# time.sleep(1)
		if not data or data.decode('utf-8') == 'exit':
			break
		sock.send(("hello , %s" % data.decode('utf-8')).encode('utf-8'))
	sock.close()
	print('connection from %s:%s closed' % addr)

is_exit_all = False


while True:
	print('waiting for connection...')
	sock, addr = s.accept()
	# t = threading.Thread(target=tcplink, args=(sock, addr))
	print("accept new connecting from %s:%s..." % addr)
	sock.send(b'Welcome.')
	while True:
		data = sock.recv(bufsize)
		print(' 收到---->%s' % data.decode('utf-8') )
		# time.sleep(1)
		if not data or data.decode('utf-8') == 'exit':
			break
		if data.decode('utf-8') == 'exitall':
			is_exit_all = True
			break

		sock.send(("hello 已收到, %s" % data.decode('utf-8')).encode('utf-8'))
	sock.close()

	print('connection from %s:%s closed' % addr)
	if is_exit_all == True:
		break


s.close()