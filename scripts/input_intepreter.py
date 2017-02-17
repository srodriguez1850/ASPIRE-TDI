#!/usr/bin/env python

import rospy
from aspire_tdi.srv import *

# ----------------
# Helper Functions
# ----------------



# --------------
# Node Functions
# --------------

def input_interpreter():
	# Startup code for I2. Receives input from the world, passes it into HLM.

	# Initialize node
	rospy.init_node('input_interpreter')

	# Wait for LLH service to start so we don't hang
	rospy.wait_for_service('requestHLM')
	# Create a handle to request LLH
	global sendTo_HLM
	sendTo_HLM = rospy.ServiceProxy('requestHLM', requestHLM)

	print 'I2 ready to receive requests.'

	# Prevent exiting
	rospy.spin()

# ----
# Main
# ----

if __name__ == '__main__':
	input_interpreter()