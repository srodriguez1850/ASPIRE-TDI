#!/usr/bin/env python

import rospy
import tdi_options
import os
import sys
import thread

from Queue import *
from aspire_tdi.srv import *

import socket, select

# -------
# Classes
# -------
class tdi_info:
	def __init__(self):
		self.master_queue = Queue()
		self.devices_connected = []

	def add_request(self, r_in, conn, addr):
		d = self.format_request(r_in)
		d['conn_obj'] = conn
		d['conn_addr'] = addr
		rospy.logdebug('Adding request to master: ' + str(d))
		self.put_request(d)
		rospy.logdebug('Sending ACK to ' + str(addr))
		conn.send(tdi_options.ACTN_ACK_STR_TO_CLIENT)

	def format_request(self, r_in):
		d = {}
		d['raw_request'] = r_in.strip()
		for i in r_in.strip().split('/'):
			v = i.split(':')
			d[v[0]] = v[1]
		return d

	def put_request(self, d_in):
		self.master_queue.put(d_in)

	def get_request(self):
		rospy.logdebug('Retrieving request')
		return self.master_queue.get()

	def print_queue(self):
		for item in self.master_queue:
			print item

	def do_requests(self):
		while True:
			while not self.master_queue.empty():
				curr_request = self.get_request()
				rospy.logdebug('^ ' + str(curr_request))
				rospy.logdebug('Handling request')
				resp = sendTo_HLM(curr_request['raw_request'])
				rospy.logdebug('Response: ' + str(resp.RespCode))
				rospy.logdebug('Requests remaining: ' + str(self.master_queue.qsize()))
				self.broadcast_info()
		rospy.logerr('Request handler stopped unexpectedly')

	def broadcast_info(self):
		queue_str = 'MASTER_QUEUE=' + str(self.master_queue.qsize()) + '/'
		for req in list(self.master_queue.queue):
			queue_str += req['cmd'] + '/'
		rospy.logdebug(queue_str)
		queue_str += '\n'

		for d in self.devices_connected:
			rospy.logdebug('Broadcasting master queue to ' + str(d['conn_addr']))
			#d['conn_obj'].send(queue_str)

	def broadcast_devices(self):
		devices_str = 'DEVICES=' + str(len(self.devices_connected)) + '/'
		for d in devices_connected:
			devices_str += d['device_name'] + '|'
			devices_str += d['device_type'] + '|'
			devices_str += d['device_model'] + '|'
		rospy.logdebug(devices_str)
		devices_str += '\n'

		for d in devices_connected:
			rospy.logdebug('Broadcasting devices to ' + str(d['conn_addr']))
			#d['conn_obj'].send(devices_str)


	def run_requests(self):
		rospy.loginfo('Starting master request runner')
		thread.start_new_thread(self.do_requests, ())

# ----------------
# Helper Functions
# ----------------
def print_tdi_options():
	if tdi_options.ENABLE_CONSOLE_INPUT:
		rospy.logwarn('ENABLE_CONSOLE_INPUT is enabled')
	if tdi_options.DISABLE_TDI_BRIDGE:
		rospy.logwarn('TdiBridge service is disabled')
		if tdi_options.DELAY_ACTION:
			rospy.logwarn('DELAY_ACTION is enabled, ' + str(tdi_options.DELAY_ACTION_AMOUNT) + ' second delay')

def handshake(conn, addr):
	rospy.logdebug('Shaking hands with ' + str(addr))
	buf_in = conn.recv(tdi_options.BUFFER_LEN).strip()
	if buf_in == tdi_options.SYN_STR_FROM_CLIENT:
		conn.send(tdi_options.SYNACK_STR_TO_CLIENT)
		rospy.logdebug('Received SYN, sent SYN_ACK')
		buf_in = conn.recv(tdi_options.BUFFER_LEN).strip()
		if buf_in == tdi_options.ACK_STR_FROM_CLIENT:
			rospy.loginfo('Connection with ' + str(addr) + ' established')
			device = {}
			#device['device_name']
			#device['device_type']
			#device['device_model']
			#device['device_uuid']
			#device['os']
			#device['os_version']
			device['conn_obj'] = conn
			device['conn_addr'] = addr
			master.devices_connected.append(device)
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
			master.add_request(data, conn, addr)
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
	rospy.init_node('tdi_master', log_level=tdi_options.ROSPY_LOG_LEVEL)
	# Print options so we know
	print_tdi_options()

	# Initialize master, start new thread to run requests
	global master
	master = tdi_info()
	master.run_requests()

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
			elif cmdin == 'show_queue':
				master.print_queue()
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