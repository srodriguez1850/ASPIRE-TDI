#!/usr/bin/env python

import rospy
from aspire_tdi.srv import *

# ----------------
# Helper Functions
# ----------------



# --------------
# Node Functions
# --------------

def handle_requestDC(req):
	# Main request handling, take subtask, send it to the drones
	# Talk to Naira's group, here is where we collaborate with them!
	print 'DC handling request.'
	return 0

def requestDC_server():
	# Startup code for the HLM server. Takes input from LLH, sends them to the drones, and returns completion per subtask.

	# Initialize node
	rospy.init_node('requestDC_server')

	# Start DC service
	s = rospy.Service('requestDC', requestDC, handle_requestDC)
	print 'DC ready to handle requests.'

	# Prevent exiting
	rospy.spin()

# ----
# Main
# ----

if __name__ == '__main__':
	requestDC_server()