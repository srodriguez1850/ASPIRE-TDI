#!/usr/bin/env python

import rospy
import tdi_constants
import os
import sys
from aspire_tdi.srv import *
from crazyflie_demo.srv import tdiBridge


# ----------------
# Helper Functions
# ----------------

def send_command_to_bridge(cmd, args):
	# move_to_location has 3 arguments
	if (cmd == 'move_to_location' and len(args) == 3):
		return sendTo_ASPIRE(1, args).RespCode
	elif (cmd == 'move_to_home' and len(args) == 0):
		return sendTo_ASPIRE(1, strlist(tdi_constants.HOME_COORD)).RespCode
	else:
		rospy.logerr('Unrecognized command, not sent to bridge')
		return 1

def strlist(list):
	out = []
	for e in list:
		out.append(str(e))
	return out

# --------------
# Node Functions
# --------------

def handle_requestDC(req):
	# Main request handling, take subtask, send it to the drones
	# Talk to Naira's group, here is where we collaborate with them!
	rospy.loginfo('DC handling request')
	rospy.logdebug(str(req))
	return send_command_to_bridge(req.Subtask, req.Args)

def DC_server():
	# Startup code for the HLM server. Takes input from LLH, sends them to the drones, and returns completion per subtask.

	# Initialize node
	rospy.init_node('drone_controller', log_level=tdi_constants.ROSPY_LOG_LEVEL)

	#Wait for  service to start so we don't hang
	rospy.wait_for_service('/crazyflie/tdiBridge')
	# Create a handle to requestDC
	global sendTo_ASPIRE
	sendTo_ASPIRE = rospy.ServiceProxy('/crazyflie/tdiBridge', tdiBridge)

	# Start DC service
	s = rospy.Service('requestDC', requestDC, handle_requestDC)
	rospy.loginfo('DC service ready')

	# Prevent exiting
	rospy.spin()

# ----
# Main
# ----

if __name__ == '__main__':
	DC_server()




# Current requestDC.srv

# string Subtask -> subtask ID to execute (a string for now)
# string[] Args -> arguments for the subtask
# 
# ---
# int64 RespCode -> 0 for good, 1 for error

# Consider adding an interrupt signal, to catch any preempting (may have to be received from Naira's)