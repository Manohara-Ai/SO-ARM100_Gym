#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os

class ImageRecorder(Node):
    def __init__(self):
        super().__init__('image_recorder')
        self.bridge = CvBridge()
        
        self.cwd = os.getcwd()
        
        self.width = 640
        self.height = 480
        
        self.arm_out = cv2.VideoWriter(
            os.path.join(self.cwd, 'arm_training.mp4'), 
            cv2.VideoWriter_fourcc(*'mp4v'), 
            20, 
            (self.width, self.height)
        )
        
        self.top_out = cv2.VideoWriter(
            os.path.join(self.cwd, 'overhead_training.mp4'), 
            cv2.VideoWriter_fourcc(*'mp4v'), 
            20, 
            (self.width, self.height)
        )

        self.sub_arm = self.create_subscription(
            Image, '/arm_camera/image_raw', self.arm_callback, 10)
        
        self.sub_top = self.create_subscription(
            Image, '/overhead_camera/image_raw', self.top_callback, 10)
        
        self.get_logger().info(f"Data recording initialized. Files will save to: {self.cwd}")

    def arm_callback(self, msg):
        try:
            cv_img = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            cv_img = cv2.resize(cv_img, (self.width, self.height))
            self.arm_out.write(cv_img)
        except Exception as e:
            self.get_logger().error(f"Error in arm_callback: {e}")

    def top_callback(self, msg):
        try:
            cv_img = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            cv_img = cv2.resize(cv_img, (self.width, self.height))
            self.top_out.write(cv_img)
        except Exception as e:
            self.get_logger().error(f"Error in top_callback: {e}")

    def stop_recording(self):
        self.arm_out.release()
        self.top_out.release()
        self.get_logger().info("Video files successfully released and saved.")

def main(args=None):
    rclpy.init(args=args)
    node = ImageRecorder()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.stop_recording()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()