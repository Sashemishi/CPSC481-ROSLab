# Traveler Project - ROS Basic Navigation
Group 7
- Gilbert Banuelos
- Matthew Choi
- Owen Keyser
- Peter Afif

## Overview
package containts two ROS programs:
1. hello.py - prints "Hello World"
2. traveler program - controls turtle1 in turtlesim to navigate the given path

Both prgrams were developed on:
- ROS2 Humble
- Ubuntu 22.04
- Python
  
# How to Run the Traveler Program

## Open Terminal 1 (The Simulator):
* ros2 run turtlesim turtlesim_node

## Open Terminal 2 (The Controller):
* cd ~/Documents/ROS/CPSC481-ROSLab
* colcon build --packages-select hello_pkg
* source install/setup.bash
* ros2 run hello_pkg traveler

# Navigation Strategy:
The robot uses a timed state machine to alternate between linear translation and angular rotation. It monitors its current Euclidean distance from the initial start_pose and terminates when that distance falls below a specific threshold.
