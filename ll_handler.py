#!/usr/bin/env python

import rospy
from aspire_tdi.srv import *

# ----------------
# Helper Functions
# ----------------



# --------------
# Node Functions
# --------------

def handle_requestLLH(req):
	# Main request handling, take subtask, send it to the drones
	# Use sendTo_DC here!
	print 'LLH handling request.'
	return 0

def requestLLH_server():
	# Startup code for the LLH server. Takes XT from HLM, determines tasks to request to the DC, and returns completion for the whole task.

	# Initialize node
	rospy.init_node('requestLLH_server')

	# Wait for DC service to start so we don't hang
	rospy.wait_for_service('requestDC')
	# Create a handle to requestDC
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
	requestLLH_server()