import rospy

# -------
# Options
# -------

# Debugging
ENABLE_CONSOLE_INPUT = 0
ROSPY_LOG_LEVEL = rospy.DEBUG
DISABLE_TDI_BRIDGE = 1
DELAY_ACTION = 1
DELAY_ACTION_AMOUNT = 3 # in seconds

# Localization
HOME_COORD = [0.0, 0.0, 0.5]

# Networking
HOST = ''
SOCKETS = []
BUFFER_LEN = 4096
PORT = 4000
MAX_CLIENTS = 2
SYN_STR_FROM_CLIENT = 'ASPIREv0.1.0-SYN'
SYNACK_STR_TO_CLIENT = 'ASPIRE_TDI-SYNACK\n'
ACK_STR_FROM_CLIENT = 'ASPIREv0.1.0-ACK'
ACTN_ACK_STR_TO_CLIENT = 'ASPIRE-ACTNACK\n'