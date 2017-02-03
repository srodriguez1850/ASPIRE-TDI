# Task Delegation Interface for ASPIRE (UIUC)

Updated: 25JAN17

Tutorial to setup the ROS environment [here](http://wiki.ros.org/ROS/Tutorials/InstallingandConfiguringROSEnvironment), requires Ubuntu 16.04 (Xenial) for ROS Kinetic Kame.

Create a package called aspire_tdi, with std_msgs, roscpp and rospy as dependencies. Inside, make a folder called src, and link it to Git (clone the repository to the folder with a '.' as the 4th parameter so it ignores the root folder) with,

```
git clone [repository URL] .
```

This repository contains all catkin makefiles; to compile, in the catkin_ws directory, run
```
catkin_make
```

Can be written in either C++ or Python, but let's maintain Python for now for consistency.

To start up ROS (in background beacuse it blocks), run
```
roscore &
```
To execute a node, run
```
rosrun aspire_tdi [node_name]      (C++)
rosrun aspire_tdi [node_name].py   (Python)
```
