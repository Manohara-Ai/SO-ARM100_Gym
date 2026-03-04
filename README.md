# SO-ARM100 Reinforcement Learning System

The **SO-ARM100 Reinforcement Learning System** provides a complete **ROS 2–based Reinforcement Learning ecosystem** for training policies on the SO-ARM100 robotic manipulator.

---

# Workspace Structure Assumption

This project assumes the following ROS 2 workspace layout:

```
~/ros2_ws/
├── src/
│   └── SO-ARM100_Gym/
├── build/
├── install/
└── log/
```

If you do not already have a workspace:

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
```

---

# Included Packages

- `so_arm100_gym_description` - URDF/SDF robot models and mesh files.

- `so_arm100_gym_gazebo` - Gazebo Sim plugins and world configurations.

- `so_arm100_gym_application` - Holds ros2 specific code and configurations.

- `so_arm100_gym_bringup` - Holds launch files and high level utilities.

---

# System Requirements

| Component | Version |
|-----------|----------|
| OS | Ubuntu 22.04 LTS |
| ROS 2 | [Humble Hawksbill](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html) |
| Gazebo | [Harmonic (8.10.0)](https://gazebosim.org/docs/latest/ros_installation/#gazebo-harmonic-with-ros-2-humble) |
| Python | 3.10.x |

Using other versions may require modifications.

---

# Installation

## 1. Clone Repository (Inside src/)

```bash
cd ~/ros2_ws/src
git clone https://github.com/Manohara-Ai/SO-ARM100_Gym.git
```

---

## 2. Install ROS 2 Dependencies

All commands below must be run from the workspace root:

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
```

Initialize rosdep (only once per system):

```bash
sudo rosdep init
rosdep update
```

Install dependencies:

```bash
rosdep install --from-paths src --ignore-src -r -i -y --rosdistro humble
```

---

## 3. Install Build Tools

```bash
sudo apt update
sudo apt install -y python3-colcon-common-extensions
```

---

## 4. Gazebo Harmonic Configuration

ROS 2 Humble does not default to Gazebo Harmonic.

Ensure Gazebo Harmonic is installed.

Export the version before building or launching:

```bash
export GZ_VERSION=harmonic
```

(Optional) Add to your ~/.bashrc:

```bash
echo "export GZ_VERSION=harmonic" >> ~/.bashrc
```

---

# Build Instructions

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
colcon build
```

If build issues occur:

```bash
cd ~/ros2_ws
rm -rf build/ install/ log/
colcon build
```

---

# Source the Workspace

Every new terminal must run:

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
```

(Optional) Add to ~/.bashrc:

```bash
echo -e "source /opt/ros/humble/setup.bash\nsource ~/ros2_ws/install/setup.bash" >> ~/.bashrc
```

---

# Running the Simulation

## Launch Gazebo + RL Stack

```bash
ros2 launch so_arm100_gym_bringup so_arm100.launch.py
```

## Launch with RVIZ

```bash
ros2 launch so_arm100_gym_bringup so_arm100.launch.py rviz:=true
```

---

# Development Workflow

After modifying any package:

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash
```

---

# Known Issue: Gazebo Hanging at "Requesting world names"

Gazebo may hang at:

```
Requesting world names
```

Possible causes:
- Stale build artifacts
- Plugin load timing issue
- Corrupted install space

Recommended fix:

```bash
cd ~/ros2_ws
rm -rf build/ install/ log/
colcon build
source install/setup.bash
```

Then relaunch the simulation.

---

# Contributing

1. Fork the repository  
2. Create a feature branch:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit changes:
   ```bash
   git commit -m "Add AmazingFeature"
   ```
4. Push branch:
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request

---

# Future Work

- Multi-agent reinforcement learning  
- Dual-arm coordination  
- Cooperative grasping  
- Object handover tasks  
- Hardware deployment support  

---
