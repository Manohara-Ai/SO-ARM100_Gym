#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import Joy
from std_msgs.msg import Float64
import ikpy.chain
import numpy as np
import os
from ament_index_python.packages import get_package_share_directory

class GazeboTeleopBridge(Node):
    def __init__(self):
        super().__init__('gazebo_teleop_bridge')
        
        # 1. Load URDF and Setup IK Chain
        description_pkg = get_package_share_directory('so_arm100_teleop_description')
        urdf_path = os.path.join(description_pkg, 'models', 'so_arm100', 'so_arm100.urdf')

        # We define the chain. Note: we tell IKPy which joints it CANNOT move for IK
        self.arm_chain = ikpy.chain.Chain.from_urdf_file(urdf_path, base_elements=["base"])
        
        # Active mask: False for base/fixed, True for arm joints, False for gripper
        # Adjust indices if your URDF structure results in more/fewer links in the chain
        self.active_mask = [False] + [True] * 5 + [False] 

        self.joint_names = [
            'shoulder_pan', 'shoulder_lift', 'elbow_flex', 
            'wrist_flex', 'wrist_roll', 'gripper_joint'
        ]

        # 2. Setup Gazebo Publishers
        self.pubs = {
            name: self.create_publisher(Float64, f'/model/so_arm100/joint/{name}/0/cmd_pos', 10)
            for name in self.joint_names
        }

        # 3. Subscribers
        # Listen for Controller Position (IK)
        self.create_subscription(PoseStamped, '/quest/right_hand/pose', self.pose_callback, 10)
        # Listen for Trigger/Buttons (Gripper)
        self.create_subscription(Joy, '/quest/right_hand/inputs', self.joy_callback, 10)

        # Gripper Limits from your URDF
        self.GRIPPER_OPEN = -0.2
        self.GRIPPER_CLOSED = 2.0

        self.get_logger().info("✅ Gazebo Bridge Active: Arm (IK) + Gripper (Trigger)")

    def joy_callback(self, msg):
        """Map Quest Trigger (axes[0]) to Gripper Joint"""
        if len(msg.axes) > 0:
            trigger_val = msg.axes[0]  # 0.0 (released) to 1.0 (squeezed)
            
            # Linear map trigger (0->1) to joint (-0.2 -> 2.0)
            target_pos = self.GRIPPER_OPEN + (trigger_val * (self.GRIPPER_CLOSED - self.GRIPPER_OPEN))
            
            gripper_msg = Float64()
            gripper_msg.data = float(target_pos)
            self.pubs['gripper_joint'].publish(gripper_msg)

    def pose_callback(self, msg):
        """Solve Inverse Kinematics for the arm joints"""
        target_pos = [
            msg.pose.position.x,
            msg.pose.position.y,
            msg.pose.position.z
        ]

        # Solve IK using the active mask to ignore the gripper joint
        ik_joints = self.arm_chain.inverse_kinematics(target_pos)

        # Map IK results to publishers (excluding gripper_joint which is handled by joy_callback)
        for i, name in enumerate(self.joint_names):
            if name != 'gripper_joint' and (i + 1) < len(ik_joints):
                cmd = Float64()
                cmd.data = float(ik_joints[i + 1])
                self.pubs[name].publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = GazeboTeleopBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()