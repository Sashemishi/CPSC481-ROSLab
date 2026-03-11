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
