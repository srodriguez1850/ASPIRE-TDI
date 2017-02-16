#!/usr/bin/env python

import os, sys, rospy
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

# --------------
# Node Functions
# --------------

def handle_requestHLM(req):
	# Main request handling, look up XT, and send a request to LLM
	# Use sendTo_LLH here!
	print 'HLM handling request.'
	return 0

def requestHLM_server():
	# Startup code for the HLM server. Takes inputs from II, requests the LLH, and returns completion code.

	# Initialize node
	rospy.init_node('requestHLM_server')

	# Initialize database of High Level Tasks (Actions/Fixes)
	# Declare and initialize dictionaries
	global A_db, F_db
	A_db = {}
	F_db = {}

	init_database('actions.db', A_db)
	#init_database('fixes.db', F_db)

	#print 'A_db:'
	#print A_db

	# Wait for LLH service to start so we don't hang
	rospy.wait_for_service('requestLLH')
	# Create a handle to request LLH
	global sendTo_LLH
	sendTo_LLH = rospy.ServiceProxy('requestLLH', requestLLH)

	# Start HLM service
	s = rospy.Service('requestHLM', requestHLM, handle_requestHLM)
	print 'HLM ready to handle requests.'

	# Test request here
	print 'HLM sending test request.'
	response = sendTo_LLH(A_db['bring_obj_to_user'])
	print 'HLM received ' + str(response.StatusCode)

	# Prevent exiting
	rospy.spin()

# ----
# Main
# ----

if __name__ == '__main__':
	requestHLM_server()


# Current requestHLM.srv

# string Query -> information of the world (maybe dictionary?)
# ---
# int64 StatusCode -> 0 for good, 1 for error

# Consider adding an interrupt signal, to catch any preempting (may have to be received from Naira's)