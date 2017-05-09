#!/usr/bin/env python

# import rospy, sys, socket, select
from signal import *
import socket, select
# from aspire_tdi.srv import *

# ----------------
# Definitions
# ----------------
HOST = '' 
sockets = []
BUFFER_LEN = 4096 
PORT = 4000

# ----------------
# Helper Functions
# ----------------
def handshake(conn):
	print "Shaking hand"
	buf_in = conn.recv(BUFFER_LEN).strip()
	if buf_in == "SYN":
		conn.send("SYN_ACK\n")
		print "Received SYN, sent SYN_ACK,",
		buf_in = conn.recv(BUFFER_LEN).strip()
		if buf_in == "ACK":
			print "received ACK, connection established."
			return True
		else:
			return False
	else:
		return False

# --------------
# Node Functions
# --------------

def input_interpreter():
    # Set up server socket to receive request from client device
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print "Server started on port " + str(PORT)
    while True:
    #accept one connect
    	connection, client_address = server_socket.accept()
    	try:
	    	print "Connection request from" + str(client_address)
	    	if handshake(connection) != True:
	    		continue
    		while True:
    		#start receiving data
	    		data = connection.recv(BUFFER_LEN)
    			if data:
	    			#deal with data(parse and store it) here
    				print "Received from client: " + str(data.strip()) + " -",
    				world_data = data.strip().split("/")
    				print world_data,
    				print "-> Sending ACK"
    				connection.send("ACK\n")
    			else:
	    			print "No more data"
    				break
    	except:
    		print "Shutdown requested"
    	finally:
    		connection.shutdown(socket.SHUT_RDWR)
	    	connection.close()

# ----
# Main
# ----

if __name__ == '__main__':
	input_interpreter()

#192.168.1.107