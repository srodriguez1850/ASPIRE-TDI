#!/usr/bin/env python

import rospy
from std_msgs.msg import String

# ------------------
# Callback Functions
# ------------------

def callback(data):
	rospy.loginfo(rospy.get_caller_id() + ' LL: I heard %s', data.data)

# -----------
# Node Source
# -----------

def ll_handler():

	# Initialize the node with False parameter to reject duplicate nodes
	rospy.init_node('LL_handler', anonymous=False)

	# Initialize Publisher topics (senders)
	#toDC_pub = rospy.Publisher('LLH_to_DC', String, queue_size=10)
	toHLM_pub = rospy.Publisher('LLH_to_HLM', String, queue_size=10)

	# Initialize Subscriber topics (receivers)
	rospy.Subscriber('HLM_to_LLH', String, callback)
	#rospy.Subscriber('DC_to_LLH', String, callback)

	# Initialize rate
	rate = rospy.Rate(1)

	# Run node
	while not rospy.is_shutdown():
		histr = 'Hi from LL'
		#rospy.loginfo(histr)
		toHLM_pub.publish(histr)
		rate.sleep()

# -----------------------
# Main and Error Handling
# -----------------------

if __name__ == '__main__':
	try:
		ll_handler()
	except rospy.ROSInterruptException:
		pass

