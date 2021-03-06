#!/usr/bin/env python

import rospy
import tdi_constants
import os
import sys
from aspire_tdi.srv import *

from collections import deque

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
	rospy.loginfo('LLH handling request')
	rospy.logdebug(str(req))

	args = deque(req.Args)
	step = 0

	for i in req.ExecTimeline:
		subtask_info = S_db[str(i)].split("-")
		si_subtask = subtask_info[0]
		si_numargs = int(subtask_info[1])

		l_thisTask_args = []
		for j in range(0, si_numargs):
			l_thisTask_args.append(args.popleft())

		resp = sendTo_DC(si_subtask, l_thisTask_args)
		if resp.RespCode != 0:
			return step + 1
		step += 1

	return 0

def LLH_server():
	# Startup code for the LLH server. Takes XT from HLM, determines tasks to request to the DC, and returns completion for the whole task.

	# Initialize node
	rospy.init_node('low_level_handler', log_level=tdi_constants.ROSPY_LOG_LEVEL)

	# Initialize database of Subtasks
	global S_db
	S_db = {}
	init_database('subtasks.db', S_db)

	rospy.logdebug('S_db: ' + str(S_db))

	# Wait for DC service to start so we don't hang
	rospy.wait_for_service('requestDC')
	# Create a handle to requestDC
	global sendTo_DC
	sendTo_DC = rospy.ServiceProxy('requestDC', requestDC)

	# Start LLH service
	s = rospy.Service('requestLLH', requestLLH, handle_requestLLH)
	rospy.loginfo('LLH service ready')

	# Prevent exiting
	rospy.spin()

# ----
# Main
# ----

if __name__ == '__main__':
	LLH_server()


# Current requestLLH.srv

# int64[] ExecTimeline -> list of subtask IDs to execute
# string[] Args -> argument of subtasks, incrementally, in order (must parse)
# ---
# int64 RespCode -> 0 for good, N for error in subtask N

# Consider adding an interrupt signal, to catch any preempting (may have to be received from Naira's)