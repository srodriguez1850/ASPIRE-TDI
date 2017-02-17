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
		db[line[0]] = line[1].strip()
	f.close()

# --------------
# Node Functions
# --------------

def handle_requestLLH(req):
	# Main request handling, take subtask, send it to the drones
	# Use sendTo_DC here!
	print 'LLH handling request.'
	print 'XT: ' + str(req.Timeline)

	step = 0

	for i in req.Timeline:
		resp = sendTo_DC(S_db[str(i)])
		if resp.StatusCode != 0:
			return step + 1
		step += 1

	return 0

def LLH_server():
	# Startup code for the LLH server. Takes XT from HLM, determines tasks to request to the DC, and returns completion for the whole task.

	# Initialize node
	rospy.init_node('low_level_handler')

	# Initialize database of Subtasks
	global S_db
	S_db = {}
	init_database('subtasks.db', S_db)

	print S_db

	# Wait for DC service to start so we don't hang
	rospy.wait_for_service('requestDC')
	# Create a handle to requestDC
	global sendTo_DC
	sendTo_DC = rospy.ServiceProxy('requestDC', requestDC)

	# Test request to DC (this will go to handle_requestLLH)
	# print 'Test request to DC.'
	# response = sendTo_DC(0)
	# print 'Should be 0 -> ' + str(response.CompletionCode)

	# Start LLH service
	s = rospy.Service('requestLLH', requestLLH, handle_requestLLH)
	print 'LLH ready to handle requests.'

	# Prevent exiting
	rospy.spin()

# ----
# Main
# ----

if __name__ == '__main__':
	LLH_server()


# Current requestLLH.srv

# int64[] Timeline -> list of subtask IDs to execute
# ---
# int64 StatusCode -> 0 for good, N for error in subtask N

# Consider adding an interrupt signal, to catch any preempting (may have to be received from Naira's)