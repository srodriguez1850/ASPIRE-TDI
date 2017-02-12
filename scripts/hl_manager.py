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
	# Declare dictionaries
	A_db = {}
	#F_db = {}

	# Initialize dictionaries
	init_database('actions.db', A_db)
	#init_database('fixes.db', F_db)
	#print 'A_db:'
	#print A_db

	# Wait for LLH service to start so we don't hang
	rospy.wait_for_service('requestLLH')
	# Create a handle to request LLH
	sendTo_LLH = rospy.ServiceProxy('requestLLH', requestLLH)

	# Start HLM service
	s = rospy.Service('requestHLM', requestHLM, handle_requestHLM)
	print 'HLM ready to handle requests.'

	# Prevent exiting
	rospy.spin()

# ----
# Main
# ----

if __name__ == '__main__':
	requestHLM_server()