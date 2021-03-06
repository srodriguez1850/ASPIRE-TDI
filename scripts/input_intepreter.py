#!/usr/bin/env python

import rospy
import tdi_constants
import os
import sys
from aspire_tdi.srv import *

import socket, select

# ----------------
# Helper Functions
# ----------------
def handshake(conn):
	rospy.logdebug('Shaking hand')
	buf_in = conn.recv(tdi_constants.BUFFER_LEN).strip()
	if buf_in == 'SYN':
		conn.send('SYN_ACK\n')
		rospy.logdebug('Received SYN, sent SYN_ACK')
		buf_in = conn.recv(tdi_constants.BUFFER_LEN).strip()
		if buf_in == 'ACK':
			rospy.loginfo('Connection with client established')
			return True
		else:
			return False
	else:
		return False

# --------------
# Node Functions
# --------------

def input_interpreter():
	# Startup code for I2. Receives input from the world, passes it into HLM.

	# Initialize node
	rospy.init_node('input_interpreter', log_level=tdi_constants.ROSPY_LOG_LEVEL)

	# Wait for LLH service to start so we don't hang
	rospy.wait_for_service('requestHLM')
	# Create a handle to request LLH
	global sendTo_HLM
	sendTo_HLM = rospy.ServiceProxy('requestHLM', requestHLM)

	if tdi_constants.ENABLE_CONSOLE_INPUT:
		while True:
			cmdin = str(raw_input('CONSOLE_INPUT_TO_TDI: '))
			if cmdin == '':
				sendTo_HLM('cmd:move_to_position_debug/nargs:3/arg1:0.0/arg2:0.0/arg3:0.0')
			else:
				sendTo_HLM(cmdin)

	# Set up server socket to receive request from client device
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((tdi_constants.HOST, tdi_constants.PORT))
	server_socket.listen(1)
	rospy.loginfo('Server started on port ' + str(tdi_constants.PORT))
	while True:
		#accept one connect
		connection, client_address = server_socket.accept()
		try:
			rospy.loginfo('Connection request from' + str(client_address))
			if handshake(connection) != True:
				continue
			while True:
			#start receiving data
				data = connection.recv(tdi_constants.BUFFER_LEN)
				if data:
					#deal with data(parse and store it) here
					rospy.logdebug('Received from client: ' + str(data.strip()))
					world_data = data.strip().split("/")
					#print world_data,
					rospy.logdebug('Sending ACK')
					connection.send("ACK\n")
					sendTo_HLM(data.strip())
				else:
					rospy.logwarn(str(client_address) + ' connection terminated: No more data')
					break
		except Exception as e:
			rospy.logerr(str(client_address) + ' connection interrupted: Exception thrown')
			rospy.logerr(e)
			if (type(e) is KeyboardInterrupt):
				sys.exit()
		finally:
			connection.shutdown(socket.SHUT_RDWR)
			connection.close()

		# Prevent exiting
	rospy.spin()

# ----
# Main
# ----

if __name__ == '__main__':
	input_interpreter()



# Queue should be here to implement queueing actions
