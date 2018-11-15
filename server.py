#!/usr/bin/env python

#Christopher Campos, chc25
#CS356-006 Programming Assignment 3
#HTTP server

#References: 
# TCP Communication - https://wiki.python.org/moin/TcpCommunication
# calendar.timegm function - https://docs.python.org/3/library/calendar.html#calendar.timegm
# formatdate function - https://docs.python.org/3.6/library/email.util.html
# MIMEtype - https://docs.python.org/3.6/library/mimetypes.html
# Python File I/O: https://docs.python.org/3/tutorial/inputoutput.html
# Python SL: socket module: https://docs.python.org/3/library/socket.html
# Python getopt: https://docs.python.org/3.1/library/getopt.html
# HTTP protocol message info/structure was taken from assignment description

#imports
import socket, sys, time, datetime, os.path, getopt, calendar, mimetypes
from email.utils import formatdate

#define server parameters..for now
S_IP = '0.0.0.0' 	#bind to any IP
S_PORT = 12000		#default port is 8080
BUFFER_SIZE = 8192 # 8K buffer size for TCP 

#Print welcome message
print("----------------------------")
print("SIMPLE HTTP SERVER")
print("BY Christopher Campos")
print("CS356 Programming Assignment 3")
print("----------------------------\n")

# Time stamp fix - do not use floating point numbers for Unix epoch
#os.stat_float_times(False)

#Process command line arguments	
opts, args = getopt.getopt(sys.argv[1:], 'p:i:')
for opt, arg in opts:
	if '-p' in opt:
		S_PORT = int(arg)
	elif '-i' in opt:
		S_IP = arg

#create a socket and bind
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((S_IP, S_PORT))
sock.listen(1)

print("The server is ready to listen on", S_IP + ":" + str(S_PORT))

try:
	while True:
		#define some parameters
		filename = ""
		req_type = "NONE"
		response = ""
		conditional = False
		cond_time = 0
		
		#accept an incoming connection
		conn, addr = sock.accept()
	
		#receive data...we'll have to decide what to do here
		data = conn.recv(BUFFER_SIZE)
		
		if not data: continue;
		
		#decode the message
		client_msg = data.decode()

		print("Received data:")
		print(client_msg)
		
		#split the string by '\r\n' so we can analyze
		#the response line by line
		
		cli_msg_sp = client_msg.split('\r\n')
		
		#get the request info from the client
		line0 = cli_msg_sp[0]
		line0_split = line0.split()
		if line0_split[0] == "GET":
			filename = "." + line0_split[1]
			req_type = "GET"
		else:
			print("Received an unsupported request", line0_split[0])
			continue
		
		#Get the current time
		date = formatdate(timeval=None, localtime=False, usegmt=True)
		
		#Try to open the file
		#if it fails we have a 404 error
		try:
			f_o = open(filename, "rb")
		except IOError:
			#send a 404 error if it fails
			response = "HTTP/1.1 404 Not Found\r\nDate: " + date + "\r\n\r\n" 
			print("Sending response...")
			print(response)
			resp_encode = response.encode()
			conn.send(resp_encode)
			conn.close()
			continue
			
		#check for conditional get/ if-modified-since
		for line in cli_msg_sp:
			if line.find("If-Modified-Since:") != -1:
				cline_split = line.split(' ', 1)
				t_tmp = time.strptime(cline_split[1], "%a, %d %b %Y %H:%M:%S %Z")
				#using calendar.timegm function as mktime gives epoch in local time
				ifmod_time = calendar.timegm(t_tmp)
				file_mod_time = os.path.getmtime(filename)
				if (file_mod_time <= ifmod_time):
					conditional = True
		
		if conditional:
			#Send a 304 response to the client, meaning that the cached file version of the client
			#is the most up to date.
			response = "HTTP/1.1 304 Not Modified\r\nDate: " + date + "\r\n\r\n"
			print("Sending response...")
			print(response)
			#Send response and end the connection
			resp_encode = response.encode()
			conn.send(resp_encode)
			conn.close()
			f_o.close()
			continue
		else:
			#Send the response and the requested file data to the client
			# last_mod_time is the last modified time of the file
			# f_size is size of the file in bytes
			# f_type is the mime type of the file. If it is text we will set the encoding to UTF-8
			secs = os.path.getmtime(filename)
			f_size = os.path.getsize(filename)
			t = time.gmtime(secs)
			f_type = mimetypes.guess_type(filename)[0]
			last_mod_time = time.strftime("%a, %d %b %Y %H:%M:%S %Z", t)
			response = "HTTP/1.1 200 OK\r\nDate: " + date + "\r\n"
			response += "Last-Modified: " + last_mod_time + "\r\n"
			response += "Content-Length: " + str(f_size) + "\r\n"
			response += "Content-Type: " + f_type
			if "text" in f_type:
				response += "; charset=UTF-8\r\n\r\n"
			else:
				response += "\r\n\r\n"
			print("Sending response and file data...")
			print(response)
			#Encode the text response to byte form
			resp_encode = response.encode()
			#Add the file data to the response (binary form)
			resp_encode += f_o.read()
			#Send the response and end the connection
			conn.send(resp_encode)
			conn.close()
			f_o.close()
			continue

#Exception handling		
except KeyboardInterrupt: 
	print("Shutting down server...\n")
	sock.shutdown(2)
	sock.close()
except Exception as e:
	print(e)
	print("An error occurred. Shutting down server...\n")
	sock.shutdown(2)
	sock.close()
	
	
	
