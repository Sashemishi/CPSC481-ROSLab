# Traveler

## Build
```bash
cd ~/ros2_ws
colcon build --packages-select hello_pkg
source install/setup.bash
```

## Run
**Terminal 1:**
```bash
ros2 run turtlesim turtlesim_node
```

**Terminal 2:**
```bash
ros2 run hello_pkg traveler
```