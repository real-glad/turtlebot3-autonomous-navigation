# TurtleBot3 Autonomous Navigation using ROS 2 and Nav2

An autonomous mobile robot navigation project developed using ROS 2 Jazzy, Gazebo Harmonic, and Navigation2 (Nav2).

The project uses a TurtleBot3 Burger simulated in an obstacle-filled environment. A custom occupancy grid map is generated using SLAM and subsequently used for localisation and autonomous navigation.

## Features

- TurtleBot3 Burger simulation in Gazebo Harmonic.
- 2D mapping using Cartographer SLAM.
- Saved occupancy grid map for navigation.
- Autonomous path planning and obstacle avoidance using Nav2.
- AMCL-based robot localisation.
- Custom Python action client for programmatic navigation goals.
- Modular ROS 2 launch files.

## System Requirements

- Ubuntu 24.04 LTS
- ROS 2 Jazzy
- Gazebo Harmonic
- TurtleBot3 Burger
- Navigation2
- TurtleBot3 Gazebo, Navigation2 and Cartographer packages.

## Dependencies

Install the required packages:

```bash
sudo apt update

sudo apt install \
  ros-jazzy-navigation2 \
  ros-jazzy-nav2-bringup \
  ros-jazzy-turtlebot3 \
  ros-jazzy-turtlebot3-gazebo \
  ros-jazzy-turtlebot3-navigation2 \
  ros-jazzy-turtlebot3-cartographer \
  ros-jazzy-ros-gz
```

## Repository Structure

```text
antropi_assign/
├── src/
│   └── antropi_navigation/
│       ├── config/
│       │   └── nav2_params.yaml
│       ├── launch/
│       │   ├── simulation.launch.py
│       │   └── navigation.launch.py
│       ├── maps/
│       │   ├── turtlebot3_world.pgm
│       │   └── turtlebot3_world.yaml
│       ├── src/
│       │   └── goal_sender.py
│       ├── CMakeLists.txt
│       └── package.xml
├── .gitignore
└── README.md
```

## Build Instructions

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd antropi_assign
```

Source ROS 2:

```bash
source /opt/ros/jazzy/setup.bash
```

Build the workspace:

```bash
colcon build --symlink-install
source install/setup.bash
```

## Running the Simulation

### Terminal 1: Launch Gazebo

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 launch antropi_navigation simulation.launch.py
```

### Terminal 2: Launch Navigation2

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 launch antropi_navigation navigation.launch.py
```

### Initialise Robot Localisation

Once RViz opens:

1. Select **2D Pose Estimate**.
2. Set the approximate initial position and orientation of the robot on the map.
3. Wait for AMCL to establish localisation.

The robot is now ready for autonomous navigation.

## Sending Navigation Goals

Navigation goals can be sent through RViz using the **Nav2 Goal** tool.

Alternatively, the custom Python action client can send goals programmatically through the Nav2 `NavigateToPose` action interface.

Example:

```bash
ros2 run antropi_navigation goal_sender.py --ros-args \
  -p x:=1.0 \
  -p y:=0.5 \
  -p yaw:=1.57 \
  -p use_sim_time:=true
```

Parameters:

| Parameter | Description |
|---|---|
| `x` | Target X coordinate in metres |
| `y` | Target Y coordinate in metres |
| `yaw` | Target orientation in radians |
| `frame_id` | Reference frame (default: `map`) |

The action client sends a goal to Nav2 and reports navigation feedback and the final result.

## Navigation Architecture

```text
                 RViz / Python Goal Client
                            |
                            v
                  NavigateToPose Action
                            |
                            v
                    Navigation2 Stack
                   /        |        \
                  /         |         \
             Planner    Controller    AMCL
                  \         |         /
                   \        |        /
                    Velocity Commands
                            |
                            v
                       Gazebo Robot
                            |
                   LiDAR / Odometry
                            |
                            v
                     ROS 2 Interfaces
```

## Testing

The following behaviours were tested:

- Navigation to different target locations.
- Obstacle avoidance around cylindrical obstacles.
- Consecutive navigation goals without restarting the simulation.
- Programmatic goal submission using the Python action client.

## Technologies Used

- ROS 2 Jazzy
- Gazebo Harmonic
- Navigation2
- AMCL
- Cartographer
- Python
- CMake
- RViz2

## License

Apache-2.0
