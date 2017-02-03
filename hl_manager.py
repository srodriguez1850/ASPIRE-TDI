#!/usr/bin/env python

import rospy
from std_msgs.msg import String

# ------------------
# Callback Functions
# ------------------

def callback(data):
	rospy.loginfo(rospy.get_caller_id() + ' HL: I heard %s', data.data)

# -----------
# Node Source
# -----------

# TODO: clean up and comment like ll_handler.py

def hl_handler():
	rospy.init_node('HL_manager', anonymous=False)
	#toII_pub = 
	toLLH_pub = rospy.Publisher('HLM_to_LLH', String, queue_size=10)
	rospy.Subscriber('LLH_to_HLM', String, callback)
	rate = rospy.Rate(1)
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
