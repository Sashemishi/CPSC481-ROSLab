#!/usr/bin/env python3
"""
traveler.py
-----------
ROS 2 node that controls turtle1 in turtlesim to draw a rectangle
with a diagonal line inside it, using NO hardcoded coordinate points.

Uses proportional control for turning (slows down near target angle)
and pose odometry for precise distance — no timing, no drift.
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time


class Traveler(Node):

    # Shape dimensions — no coordinates, just relative size
    WIDTH  = 4.0
    HEIGHT = 2.0
    SPEED  = 1.0   # linear speed (units/sec)

    def __init__(self):
        super().__init__('traveler')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.pose = None
        self.create_subscription(Pose, '/turtle1/pose', self._pose_cb, 10)

        self.get_logger().info('Waiting for pose...')
        while self.pose is None:
            rclpy.spin_once(self, timeout_sec=0.1)
        self.get_logger().info('Pose received.')

    def _pose_cb(self, msg):
        self.pose = msg

    def _spin(self):
        rclpy.spin_once(self, timeout_sec=0.01)

    @staticmethod
    def _angle_diff(target, current):
        """Shortest signed angle from current to target."""
        d = target - current
        while d >  math.pi: d -= 2 * math.pi
        while d < -math.pi: d += 2 * math.pi
        return d

    def turn_to(self, target_theta):
        """
        Proportional controller: turn speed scales with remaining angle.
        Slows down as it approaches target → no overshoot.
        """
        MAX_SPEED = 1.5   # rad/sec max
        MIN_SPEED = 0.3   # rad/sec min (keeps moving when close)
        TOLERANCE = 0.003 # ~0.17 degrees — very tight

        msg = Twist()
        while True:
            self._spin()
            diff = self._angle_diff(target_theta, self.pose.theta)
            if abs(diff) < TOLERANCE:
                break
            # Proportional gain: faster when far, slower when close
            speed = max(MIN_SPEED, min(MAX_SPEED, abs(diff) * 2.0))
            msg.angular.z = speed if diff > 0 else -speed
            self.publisher_.publish(msg)

        self.publisher_.publish(Twist())
        time.sleep(0.2)

    def move_forward(self, distance):
        """Move forward by distance using start-pose odometry."""
        start_x = self.pose.x
        start_y = self.pose.y

        msg = Twist()
        msg.linear.x = self.SPEED

        while True:
            self._spin()
            traveled = math.sqrt((self.pose.x - start_x) ** 2 +
                                 (self.pose.y - start_y) ** 2)
            if traveled >= distance:
                break
            self.publisher_.publish(msg)

        self.publisher_.publish(Twist())
        time.sleep(0.2)

    def run_path(self):
        """
        Draw a rectangle (WIDTH x HEIGHT) then a diagonal.
        All angles derived from math — no hardcoded coordinates.

        Heading convention (turtlesim):
          East  =  0          (right)
          South = -pi/2       (down)
          West  =  pi or -pi  (left)
          North =  pi/2       (up)
        """
        W = self.WIDTH
        H = self.HEIGHT

        EAST  =  0.0
        SOUTH = -math.pi / 2.0
        WEST  =  math.pi
        NORTH =  math.pi / 2.0

        # Diagonal: from top-left going down-right = negative angle from East
        DIAG     = -math.atan2(H, W)
        DIAG_LEN =  math.sqrt(W**2 + H**2)

        # --- Rectangle ---
        self.get_logger().info('Top edge →')
        self.turn_to(EAST);  self.move_forward(W)

        self.get_logger().info('Right edge ↓')
        self.turn_to(SOUTH); self.move_forward(H)

        self.get_logger().info('Bottom edge ←')
        self.turn_to(WEST);  self.move_forward(W)

        self.get_logger().info('Left edge ↑')
        self.turn_to(NORTH); self.move_forward(H)

        # --- Diagonal ---
        self.get_logger().info('Diagonal ↘')
        self.turn_to(DIAG);  self.move_forward(DIAG_LEN)

        self.get_logger().info('Done!')


def main(args=None):
    rclpy.init(args=args)
    node = Traveler()
    node.run_path()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()