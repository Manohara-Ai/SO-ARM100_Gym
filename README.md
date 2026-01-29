# SO-ARM100 Teleoperation System

The **SO-ARM100 Teleop System** provides a complete **ROS 2–based teleoperation ecosystem** for controlling the SO-ARM100 robotic arm using a **WebXR interface**.  

---

## Included Packages

- **`so_arm100_teleop_description`**  
  URDF/SDF robot models and mesh files for the SO-ARM100.

- **`so_arm100_teleop_gazebo`**  
  Custom Gazebo Sim plugins and world configurations.

- **`so_arm100_teleop_application`**  
  WebXR frontend, HTTPS server, and a secure WebSocket ↔ ROS 2 bridge.

- **`so_arm100_teleop_bringup`**  
  Launch files and parameters to start the complete teleoperation stack.

---

## Installation

### Clone the Repository

```bash
cd ~/ros2_ws/src
git clone <your-repo-link>
```

---

### Generate HTTPS Certificates (Required for WebXR)

WebXR requires a **secure HTTPS context**.

```bash
cd ~/ros2_ws/src/so_arm100_teleop/so_arm100_teleop_application/scripts
chmod +x generate_cert.sh
chmod +x run_wireless.sh
./generate_cert.sh
```

---

## System Requirements

This project has been developed and tested on the following environment.  
Using other versions may require modifications.

| Component | Version |
|----------|---------|
| Operating System | Ubuntu 22.04 LTS (Jammy Jellyfish) |
| ROS 2 Distro | Humble Hawksbill |
| Gazebo | Fortress (6.17.0) |
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
sudo apt install -y python3-colcon-common-extensions websockets
pip install ikpy
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
ros2 launch so_arm100_teleop_bringup so_arm100.launch.py
```

```bash
ros2 launch so_arm100_teleop_bringup so_arm100.launch.py record:=true
```

Note: If recording fails, run:

```bash
chmod +x src/so_arm100_teleop/so_arm100_teleop_application/src/record_data.py
```

---

### Launch the Teleoperation Server

```bash
cd ~/ros2_ws
./src/so_arm100_teleop/so_arm100_teleop_application/scripts/run_wireless.sh
```

---

## Control Logic Overview

- Move the **right VR controller** to control the arm end-effector position using **Inverse Kinematics (IK)**.
- Gripper control using the **Index Trigger**:
  - Fully released: open gripper (`-0.2 rad`)
  - Fully pressed: close gripper (`2.0 rad`)

---

## Visual Feedback

The WebXR interface provides two live camera streams:

- **Arm-Mounted Camera**: First-person view from the gripper.
- **Overhead Camera**: Wide-angle workspace view.

Note: The robot currently tracks **position only**. Wrist orientation is not yet supported.

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

1. VR control stabilization with smoothing and workspace scaling  
2. Refactoring `so_arm100_teleop_application` into modular ROS 2 nodes  
3. Reinforcement Learning training support in Gazebo  
4. Hardware deployment on physical SO-ARM100 using the same ROS 2 bridge

---

## Known Issue: Gazebo "Requesting world names"

Gazebo may occasionally hang at **"Requesting world names"** due to stale build artifacts or startup race conditions.

**Workaround:**  
Rebuild the workspace and relaunch the simulation.

---
