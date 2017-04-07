#!/usr/bin/env python

import rospy, sys, socket, select
from aspire_tdi.srv import *

# ----------------
# Helper Functions
# ----------------
HOST = '' 
sockets = []
BUFFER_LEN = 4096 
PORT = 4000
# --------------
# Node Functions
# --------------

def input_interpreter():
	# Startup code for I2. Receives input from the world, passes it into HLM.

	# Initialize node
	rospy.init_node('input_interpreter')

	# Wait for LLH service to start so we don't hang
	rospy.wait_for_service('requestHLM')
	# Create a handle to request LLH
	global sendTo_HLM
	sendTo_HLM = rospy.ServiceProxy('requestHLM', requestHLM)

        # Set up server socket to receive request from client device
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(10)
        print "Server started on port " + str(PORT)
        while True:
          #accept one connect
          connection, client_address = server_socket.accept()
          try:
            print "Connection from" + str(client_address)

            while True:
              #start receiving data
              data = connection.recv(BUFFER_LEN)
              if data:
                #deal with data(parse and store it) here
                print "I2 received from client: " + str(data)
                response = sendTo_HLM(str(data))
                print "I2 received from HLM: " + str(response.StatusCode)
              else:
                print "No more data"
                break
          finally:
            connection.close()

        # Prevent exiting
	rospy.spin()

# ----
# Main
# ----

if __name__ == '__main__':
	input_interpreter()
