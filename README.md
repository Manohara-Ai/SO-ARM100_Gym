# SO-ARM100 Reinforcement Learning System

The **SO-ARM100 Reinforcement Learning System** provides a complete **ROS 2–based Reinforcement Learning ecosystem** for training policies on the SO-ARM100 robotic manipulator.  

---

## Included Packages

- **`so_arm100_gym_description`**  
  URDF/SDF robot models and mesh files for the SO-ARM100.

- **`so_arm100_gym_gazebo`**  
  Custom Gazebo Sim plugins and world configurations.

- **`so_arm100_gym_application`**  
  Reinforcement Learning interface layer.

- **`so_arm100_gym_bringup`**  
  Launch files and parameters to start the complete RL stack.

---

## Installation

### Clone the Repository

```bash
cd ~/ros2_ws/src
git clone https://github.com/Manohara-Ai/SO-ARM100_Gym
```

---

## System Requirements

This project has been developed and tested on the following environment.  
Using other versions may require modifications.

| Component | Version |
|----------|---------|
| Operating System | Ubuntu 22.04 LTS (Jammy Jellyfish) |
| ROS 2 Distro | Humble Hawksbill |
| Gazebo | Harmonic (8.10.0) |
| Python | 3.10.x |

---

## Usage

### Install ROS 2 Dependencies

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
sudo rosdep init
rosdep update
rosdep install --from-paths src --ignore-src -r -i -y --rosdistro humble
```

---

### Install Python Dependencies

```bash
sudo apt update
sudo apt install -y python3-colcon-common-extensions 
```

---

Note: To use Gazebo Harmonic (non-default pairing for ROS 2 Humble), ensure Harmonic is installed and run:
```bash
export GZ_VERSION=harmonic 
```

---

### Build the Workspace
```bash
colcon build
```

---

### Source the Workspace

```bash
source ~/ros2_ws/install/setup.bash
```

---

### Launch the Simulation

```bash
ros2 launch so_arm100_gym_bringup so_arm100.launch.py
```

Note: If you want to launch with RVIZ, run:
```bash
ros2 launch so_arm100_gym_bringup so_arm100.launch.py rviz:=true
```

---

## Contributing

1. Fork the project  
2. Create a feature branch:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit changes:
   ```bash
   git commit -m "Add AmazingFeature"
   ```
4. Push the branch:
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request

---

## Future Work

Extend the framework to support multi-agent reinforcement learning for coordinated dual-arm manipulation tasks such as cooperative grasping and object handover.

---

## Known Issue: Gazebo "Requesting world names"

Gazebo may occasionally hang at **"Requesting world names"** due to stale build artifacts or startup race conditions.

**Workaround:**  
Rebuild the workspace and relaunch the simulation.

---
