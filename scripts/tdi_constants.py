import rospy

# -----------
# Definitions
# -----------
HOST = '' 
sockets = []
BUFFER_LEN = 4096 
PORT = 4000

# -------
# Options
# -------
ENABLE_CONSOLE_INPUT = 0
ROSPY_LOG_LEVEL = rospy.DEBUG
HOME_COORD = [0.0, 0.0, 0.5]
