#  RoboDriver-ROS2 (Part 2: Robot Driver)

A ROS 2 Python package (`my_robot_driver`) that brings a two-wheeled robot to life in **RViz2**. It listens to velocity commands on `/cmd_vel`, updates the robot's position and heading, spins the wheels, and publishes joint states and TF transforms.

[RViz Demo]
<br><br>
<img width="1211" height="889" alt="Screenshot From 2026-11-13 17-12-34" src="https://github.com/user-attachments/assets/d38d3a20-9324-4552-9639-7ac0e36742b1" />


## ✨ Features

- 🎮 **Velocity control**: subscribes to `/cmd_vel` (`geometry_msgs/Twist`)
- 🧭 **Pose tracking**: integrates linear and angular speed into x, y and yaw
- 🛞 **Wheel animation**: publishes `left_wheel_joint` and `right_wheel_joint`
- 🔗 **TF broadcasting**: publishes the robot transform with `tf2_ros`
- ⏱️ **10 Hz update loop**

## 🧰 Tech Stack

- Python 3
- ROS 2 (`rclpy`)
- `sensor_msgs`, `geometry_msgs`, `tf2_ros`
- RViz2

## 📁 Project Structure

```
my_robot_driver/
├── my_robot_driver/
│   ├── __init__.py
│   └── drive_robot.py        # Main driver node
├── resource/
│   └── my_robot_driver
├── test/
│   ├── test_copyright.py
│   ├── test_flake8.py
│   ├── test_mypy.py
│   ├── test_pep257.py
│   └── test_xmllint.py
├── package.xml
├── setup.py
└── setup.cfg
```

## ⚙️ Prerequisites

- ROS 2 (Humble / Jazzy / Lyrical)
- `colcon` build tools
- RViz2
- Part 1 package (`my_robot_description`) built and sourced

## 🚀 Installation

```bash
cd ~/ros2_ws/src
git clone https://github.com/30DineshKumar/Robotic_Car_part_1.git
git clone https://github.com/30DineshKumar/<part-2-repo-name>.git

cd ~/ros2_ws
colcon build
source install/setup.bash
```

**Terminal 3**: send a velocity command:

```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
"{linear: {x: 0.5}, angular: {z: 0.3}}"
```

Or drive with the keyboard:


## 📡 Topics

| Topic           | Type                     | Direction | Description                 |
|-----------------|--------------------------|-----------|-----------------------------|
| `/cmd_vel`      | `geometry_msgs/Twist`    | Subscribe | Linear and angular velocity |
| `/joint_states` | `sensor_msgs/JointState` | Publish   | Left and right wheel angles |
| `/tf`           | `tf2_msgs/TFMessage`     | Publish   | Robot pose transform        |

## 🧠 How It Works

Every 0.1 s the node updates the robot state:

```
yaw += angular_speed * dt
x   += linear_speed * cos(yaw) * dt
y   += linear_speed * sin(yaw) * dt
wheel_angle += linear_speed * dt * 5.0
```

The wheel angles go into a `JointState` message and the pose goes out as a TF transform, so RViz shows the robot moving.

## 🚧 Future Improvements

- Separate left and right wheel speeds (true differential drive)
- Publish `nav_msgs/Odometry`
- Add a single launch file to start everything

## 📄 License

Apache-2.0

##  Author

**Dinesh Kumar**
GitHub: [@30DineshKumar](https://github.com/30DineshKumar)
