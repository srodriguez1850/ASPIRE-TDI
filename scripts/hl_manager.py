#!/usr/bin/env python

import rospy
import tdi_options
import os
import sys
from aspire_tdi.srv import *

# ----------------
# Helper Functions
# ----------------

def init_database(file, db):
	# Initialize a dictionary using I/O
	f = open(os.path.join(sys.path[0], file), 'r')
	for line in f:
		line = line.split('/')
		db[line[0]] = [int(s) for s in line[1].split(',')]
	f.close()

def deconstruct_query(query):
	d = {}
	for i in query.split('/'):
		v = i.split(':')
		d[v[0]] = v[1]
	return d

def construct_argument_list(data):
	l = []
	for i in range(0, int(data['nargs'])):
		l.append(data['arg' + str(i + 1)])
	return l


# --------------
# Node Functions
# --------------

def handle_requestHLM(req):
	# Main request handling, look up XT, and send a request to LLM
	# Use sendTo_LLH here!
	rospy.loginfo('HLM handling request')
	rospy.logdebug(str(req))

	query_data = deconstruct_query(req.Query)
	r_command = A_db[query_data["cmd"]]
	r_args = construct_argument_list(query_data)

	response = sendTo_LLH(r_command, r_args)

	if response.RespCode == 0:
		return 0
	else:
		return response.RespCode

def HLM_server():
	# Startup code for the HLM server. Takes inputs from II, requests the LLH, and returns completion code.

	# Initialize node
	rospy.init_node('high_level_manager', log_level=tdi_constants.ROSPY_LOG_LEVEL)

	# Initialize database of High Level Tasks (Actions/Fixes)
	# Declare and initialize dictionaries
	global A_db, F_db
	A_db = {}
	F_db = {}

	init_database('actions.db', A_db)
	#init_database('fixes.db', F_db)

	rospy.logdebug('A_db: ' + str(A_db))
	#rospy.logdebug('F_db: ' + F_db)

	# Wait for LLH service to start so we don't hang
	rospy.wait_for_service('requestLLH')
	# Create a handle to request LLH
	global sendTo_LLH
	sendTo_LLH = rospy.ServiceProxy('requestLLH', requestLLH)

	# Start HLM service
	s = rospy.Service('requestHLM', requestHLM, handle_requestHLM)
	rospy.loginfo('HLM service ready')

	# Prevent exiting
	rospy.spin()

# ----
# Main
# ----

if __name__ == '__main__':
	HLM_server()


# Current requestHLM.srv

# string Query -> command query
# ---
# int64 RespCode -> 0 for good, 1 for error

# Consider adding an interrupt signal, to catch any preempting (may have to be received from Naira's)
