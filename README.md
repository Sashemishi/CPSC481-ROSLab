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
  
## How to run the programs

### Running the Hello World program
1. navigate to ROS directory
2. build the programs using the command: colcon build
3. source install/setup.bash
4. ros2 run hello_pkg hello
5. Ctr + C to end the program

### Running the Traveler Program
Open Termina1 (Simulator):
1. navigate to ROS directory
2. ros2 run turtlesim turtlesim_node
Open Terminal2 (Controller):
1. navigate to ROS directory
2. colcon build
3. source install/setup.bash
4. ros2 run traveler_pkg traveler
