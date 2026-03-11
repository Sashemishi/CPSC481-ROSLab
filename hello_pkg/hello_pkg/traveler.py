import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class Traveler(Node):
    def __init__(self):
        super().__init__('traveler')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        
        self.timer = self.create_timer(1.0, self.navigate)
        self.start_pose = None
        self.current_pose = None
        self.step = 0

    def pose_callback(self, msg):
        self.current_pose = msg
        if self.start_pose is None:
            self.start_pose = msg 

    def navigate(self):
        if self.current_pose is None:
            return

        msg = Twist()
        if self.step % 2 == 0:
            msg.linear.x = 2.0
            self.get_logger().info('Action: Moving Straight')
        else:
            msg.angular.z = 1.5708
            self.get_logger().info('Action: Turning')

        self.publisher_.publish(msg)
        self.step += 1

        if self.step > 4: 
            distance = math.sqrt((self.current_pose.x - self.start_pose.x)**2 + 
                                 (self.current_pose.y - self.start_pose.y)**2)
            if distance < 0.2:
                self.get_logger().info('Goal Reached: Returned to Start!')
                raise SystemExit

def main(args=None):
    rclpy.init(args=args)
    node = Traveler()
    try:
        rclpy.spin(node)
    except SystemExit:
        pass
    node.destroy_node()
    rclpy.shutdown()