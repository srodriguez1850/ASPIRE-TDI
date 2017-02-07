#!/usr/bin/env python

import rospy
from std_msgs.msg import String

# ----------------
# Helper Functions
# ----------------

def init_database(file, db):
	# Initialize a dictionary using I/O
	f = open(file, 'r')
	for line in f:
		line = line.split('/')
		db[line[0]] = [int(s) for s in line[1].split(',')]
	f.close()

# ------------------
# Callback Functions
# ------------------

def callback(data):
	rospy.loginfo(rospy.get_caller_id() + ' HL: I heard %s', data.data)

# -----------
# Node Source
# -----------

def hl_handler():

	# Initialize the node with False parameter to reject duplicate nodes
	rospy.init_node('HL_manager', anonymous=False)

	# Initialize database of High Level Tasks (Actions/Fixes/Interrupts)
	# Declare dictionaries
	A_db = {}
	#F_db = {}
	#I_db = {}

	# Initialize dictionaries
	init_database('actions.db', A_db)
	#init_database('fixes.db', F_db)
	#init_database('interrupts.db', I_db)


	# Initialize Publisher topics (senders)
	#toII_pub = rospy.Publisher('HLM_to_II', String, queue_size=10)
	toLLH_pub = rospy.Publisher('HLM_to_LLH', String, queue_size=10)

	# Initialize Subscriber topics (receivers)
	rospy.Subscriber('LLH_to_HLM', String, callback)
	#rospy.Subscriber('II_to_HLM', String, callback)

	# Initialize rate
	rate = rospy.Rate(1)

	# Run node
	while not rospy.is_shutdown():
		histr = 'Hi from HL'
		#rospy.loginfo(histr)
		toLLH_pub.publish(histr)
		rate.sleep()

# -----------------------
# Main and Error Handling
# -----------------------

if __name__ == '__main__':
	try:
		hl_handler()
	except rospy.ROSInterruptException:
		pass
