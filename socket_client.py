# -*- coding: utf-8 -*-

import socket

HOST='127.0.0.1'
PORT=5967
bufsize = 1024
address = (HOST,PORT) 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('start')
s.connect(address)

print((s.recv(bufsize)).decode('utf-8'))

is_exit_all = False

while True:
	x = str(input("Please enter an str: "))
	
	print("input:" + x)
	if x == 'exit':
		break;

	if x == 'exitall':
		is_exit_all = True
		break;
		
	if x == '' or x == "\n":
		x = "empty"

	s.send(bytes(x, encoding='utf-8'))
	print((s.recv(bufsize)).decode('utf-8'))

if is_exit_all == True:
	s.send(b'exitall')	
else:
	s.send(b'exit')


s.close()

# x = str(input("Please enter an str: "))
# print(x)