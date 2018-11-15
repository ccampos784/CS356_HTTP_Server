#!/usr/bin/env python

#Christopher Campos, chc26
#CS 356-006 Programming Assignment 3
#HTTP Client

#References: 
# TCP Communication - https://wiki.python.org/moin/TcpCommunication
# calendar.timegm function - https://docs.python.org/3/library/calendar.html#calendar.timegm
# formatdate function - https://docs.python.org/3.6/library/email.util.html
# MIMEtype - https://docs.python.org/3.6/library/mimetypes.html
# Python File I/O: https://docs.python.org/3/tutorial/inputoutput.html
# Python SL: socket module: https://docs.python.org/3/library/socket.html
# Python getopt: https://docs.python.org/3.1/library/getopt.html
# HTTP protocol message info/structure was taken from assignment description

import socket, sys, time, datetime, os.path, getopt, calendar, mimetypes
from email.utils import formatdate

#define some parameters
TCP_IP = '127.0.0.1'
TCP_PORT = 12000
BUFFER_SIZE = 8192 # 8K buffer size for TCP 
FILENAME = "index.html"

# Time stamp fix - do not use floating point numbers for Unix epoch
os.stat_float_times(False)

#Process command line argument
#The format of the argument is as follows:
# localhost:12000/filename.html
try:
	url_arg = sys.argv[1]
except Exception:
	print("Invalid argument")
	exit(1)
	
if ':' in url_arg:
	TCP_IP = url_arg.split(":", 1)[0]
	TCP_PORT = int(url_arg.split(":", 1)[1].split("/", 1)[0])
else:
	TCP_IP = url_arg.split("/", 1)[0]
	TCP_PORT = 80
FILENAME = url_arg.split("/", 1)[1]

#Print welcome message
print("----------------------------")
print("SIMPLE HTTP CLIENT")
print("BY Christopher Campos")
print("CS356 Programming Assignment 3")
print("----------------------------\n")		

for i in range(2):
	if i == 0:
		MESSAGE = "GET /" + FILENAME + " HTTP/1.1\r\n" + "Host: " + TCP_IP + ":" + str(TCP_PORT) + "\r\n\r\n"
	else:
		print("Round 2: Sending a Conditional GET request...")
		MESSAGE = "GET /" + FILENAME + " HTTP/1.1\r\n" + "Host: " + TCP_IP + ":" + str(TCP_PORT) + "\r\n" + "If-Modified-Since: " + last_mod_time + "\r\n\r\n"
	
	#set up a socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	
	#send a request
	print("Sending request...")
	print(MESSAGE)
	request = MESSAGE.encode();
	s.send(request)

	#receive the response
	data = b''
	while True:
		tmp_d = s.recv(BUFFER_SIZE)
		if not tmp_d: break
		data += tmp_d

	s.close()
	#split the response and potential data
	response = data.split(b'\r\n\r\n', 1)[0]
	file_data = data.split(b'\r\n\r\n', 1)[1]
	last_mod_time = ""

	#Analyze the response
	response_split = response.decode().split("\r\n")
	print("Received response...")
	print(response.decode())
	if "200" in response_split[0]:
		#Get last modified time from response
		for line in response_split:
			if line.find("Last-Modified:") != -1:
				cline_split = line.split(' ', 1)
				last_mod_time = cline_split[1]
				print(last_mod_time)
			
		os.makedirs(os.path.dirname("./" + FILENAME), exist_ok=True)
		f_o = open(FILENAME, "wb+");
		print("\nSaving data to", FILENAME)
		f_o.write(file_data)
		f_o.close()
		#print out file
		f_o = open(FILENAME, "rb");
		print("File contents:")
		if "text" in mimetypes.guess_type(FILENAME)[0]:
			print(f_o.read().decode())
		else:
			print("This is not a text file, so contents will not be printed.")
		
		f_o.close()
	elif "404" in response_split[0]:
		print("\nReceived 404 error - file was not found")
		break
	elif "304" in response_split[0]:
		print("\nReceived 304 response - file has not been modified")
	else:
		print("\nReceived unhandled response type...exiting")
		break
exit(0)


#print ("received data:", data.decode())
