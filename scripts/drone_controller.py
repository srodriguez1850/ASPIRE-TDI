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

def DC_server():
	# Startup code for the HLM server. Takes input from LLH, sends them to the drones, and returns completion per subtask.

	# Initialize node
	rospy.init_node('drone_controller')

	# Start DC service
	s = rospy.Service('requestDC', requestDC, handle_requestDC)
	print 'DC ready to handle requests.'

	# Prevent exiting
	rospy.spin()

# ----
# Main
# ----

if __name__ == '__main__':
	DC_server()




# Current requestDC.srv

# string Subtask -> subtask ID to execute (a string for now)
# ---
# int64 StatusCode -> 0 for good, 1 for error

# Consider adding an interrupt signal, to catch any preempting (may have to be received from Naira's)