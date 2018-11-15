Simple HTTP client and Server
CS356-006 Programming Assignment 3
By Christopher Campos
This project contains two separate Python programs:
    - server.py, which is an HTTP server
    - client.py, which is an HTTP client
    
The server.py program operates as a simple HTTP server. The working directory is the directory where the program is located. By default, it binds to any IP, and runs on port 8080. These options can be changed by passing arguments
    python server.py (-i [ipaddr] -p [port])
    where -i takes in the IP address to where the server will bind to, and
    argument -p takes in the port that the server will listen on.
The server program only supports GET requests. It supports sending text and image files.
    
The client.py program acts as a simple HTTP server for use with the server program. It takes in exactly one argument:
    python client.py localhost:12000/filename.html
    The argument is a string consisting of the IP/hostname, followed by the port number, followed by the requested file on the server.
This program will perform two requests on the server: first, a GET request. If a 200 response with the file data is received it will download and save the file. If a 404 request is received it will tell the user and exit.
After, the program will send a conditional GET request echoing the last modified time given in the first GET request. The file should not have changed since then so we should receive a 304 response.

All test cases (for HTTP client and browser) are working.

References:
# TCP Communication - https://wiki.python.org/moin/TcpCommunication
# calendar.timegm function - https://docs.python.org/3/library/calendar.html#calendar.timegm
# formatdate function - https://docs.python.org/3.6/library/email.util.html
# MIMEtype - https://docs.python.org/3.6/library/mimetypes.html
# Python File I/O: https://docs.python.org/3/tutorial/inputoutput.html
# Python SL: socket module: https://docs.python.org/3/library/socket.html
# Python getopt: https://docs.python.org/3.1/library/getopt.html
# HTTP protocol message info/structure was taken from assignment description
