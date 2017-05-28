#!/usr/bin/env python

import rospy
import tdi_options
import os
import sys
import thread
from aspire_tdi.srv import *

import socket, select

# ----------------
# Helper Functions
# ----------------
def handshake(conn, addr):
	rospy.logdebug('Shaking hands with ' + str(addr))
	buf_in = conn.recv(tdi_options.BUFFER_LEN).strip()
	if buf_in == tdi_options.SYN_STR_FROM_CLIENT:
		conn.send(tdi_options.SYNACK_STR_TO_CLIENT)
		rospy.logdebug('Received SYN, sent SYN_ACK')
		buf_in = conn.recv(tdi_options.BUFFER_LEN).strip()
		if buf_in == tdi_options.ACK_STR_FROM_CLIENT:
			rospy.loginfo('Connection with ' + str(addr) + ' established')
			return True
		else:
			return False
	else:
		return False

def handle_client(conn, addr):
	buf = tdi_options.BUFFER_LEN
	rospy.logdebug('Spawning thread to handle ' + str(addr))
	# Handshake the client, if not valid, end the thread
	if handshake(conn, addr) != True:
		rospy.logwarn(str(addr) + ' not valid ASPIRE client, shutting thread')
		conn.shutdown(socket.SHUT_RDWR)
		conn.close()
		return
	# Listen for data, parse and send off to HLM
	while True:
		data = conn.recv(buf)
		if data:
			rospy.logdebug('Received from ' + str(addr) + ': ' + str(data.strip()))
			#c_data = data.strip().split("/")
			#print c_data,
			rospy.logdebug('Sending ACK to ' + str(addr))
			conn.send(tdi_options.ACTN_ACK_STR_TO_CLIENT)
			sendTo_HLM(data.strip())
		else:
			rospy.logwarn(str(addr) + ' connection terminated: No more data')
			conn.shutdown(socket.SHUT_RDWR)
			conn.close()
			break
	rospy.logdebug('Shutting thread handling ' + str(addr))

# --------------
# Node Functions
# --------------

def tdi_master():
	# Startup code for Master. Receives input from the world, passes it into HLM.

	# Initialize node
	rospy.init_node('input_interpreter', log_level=tdi_options.ROSPY_LOG_LEVEL)

	# Wait for LLH service to start so we don't hang
	rospy.wait_for_service('requestHLM')
	# Create a handle to request LLH
	global sendTo_HLM
	sendTo_HLM = rospy.ServiceProxy('requestHLM', requestHLM)

	if tdi_options.ENABLE_CONSOLE_INPUT:
		while True:
			cmdin = str(raw_input('CONSOLE_INPUT_TO_TDI: '))
			if cmdin == '':
				sendTo_HLM('cmd:move_to_position_debug/nargs:3/arg1:0.0/arg2:0.0/arg3:0.0')
			else:
				sendTo_HLM(cmdin)

	# Set up server socket to receive request from client device
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((tdi_options.HOST, tdi_options.PORT))
	server_socket.listen(tdi_options.MAX_CLIENTS)
	rospy.loginfo('Server started on port ' + str(tdi_options.PORT) + ' with max clients ' + str(tdi_options.MAX_CLIENTS))

	while True:
		# Accept connections
		connection, address = server_socket.accept()
		rospy.loginfo('Connection request from ' + str(address))
		try:
			thread.start_new_thread(handle_client, (connection, address,))
		except Exception as e:
			rospy.logerr('Unable to start thread: ' + e)
	rospy.spin()

# ----
# Main
# ----

if __name__ == '__main__':
	tdi_master()


# Queue should be here to implement queueing actions