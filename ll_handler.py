#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def ll_handler():
	pub = rospy.Publisher('timeline', String, queue_size=10)
	rospy.init_node('ll_handler', anonymous=True)
	rate = rospy.Rate(5)
	while not rospy.is_shutdown():
		somestr = 'hello'
		rospy.loginfo(somestr)
		pub.publish(somestr)
		rate.sleep()

if __name__ == '__main__':
	try:
		ll_handler()
	except rospy.ROSInterruptException:
		pass

