#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose


class GoalSender(Node):

    def __init__(self):
        super().__init__('goal_sender')

        # Goal parameters
        self.declare_parameter('x', 0.0)
        self.declare_parameter('y', 0.0)
        self.declare_parameter('yaw', 0.0)
        self.declare_parameter('frame_id', 'map')

        self.x = self.get_parameter('x').value
        self.y = self.get_parameter('y').value
        self.yaw = self.get_parameter('yaw').value
        self.frame_id = self.get_parameter('frame_id').value

        # Nav2 action client
        self.action_client = ActionClient(
            self,
            NavigateToPose,
            'navigate_to_pose'
        )

        self.get_logger().info('Goal Sender initialized.')

    def send_goal(self):

        self.get_logger().info(
            'Waiting for Nav2 NavigateToPose action server...'
        )

        if not self.action_client.wait_for_server(timeout_sec=10.0):
            self.get_logger().error(
                'NavigateToPose action server unavailable!'
            )
            return False

        # Construct navigation goal
        goal_msg = NavigateToPose.Goal()

        goal_msg.pose = PoseStamped()
        goal_msg.pose.header.frame_id = self.frame_id
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()

        goal_msg.pose.pose.position.x = self.x
        goal_msg.pose.pose.position.y = self.y
        goal_msg.pose.pose.position.z = 0.0

        # Convert yaw into quaternion
        goal_msg.pose.pose.orientation.x = 0.0
        goal_msg.pose.pose.orientation.y = 0.0
        goal_msg.pose.pose.orientation.z = math.sin(self.yaw / 2.0)
        goal_msg.pose.pose.orientation.w = math.cos(self.yaw / 2.0)

        self.get_logger().info(
            f'Sending goal: x={self.x:.2f}, '
            f'y={self.y:.2f}, yaw={self.yaw:.2f}'
        )

        self.send_goal_future = self.action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        self.send_goal_future.add_done_callback(
            self.goal_response_callback
        )

        return True

    def goal_response_callback(self, future):

        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error('Navigation goal rejected.')
            rclpy.shutdown()
            return

        self.get_logger().info('Navigation goal accepted!')

        self.result_future = goal_handle.get_result_async()

        self.result_future.add_done_callback(
            self.result_callback
        )

    def feedback_callback(self, feedback_msg):

        feedback = feedback_msg.feedback

        distance = feedback.distance_remaining

        self.get_logger().info(
            f'Distance remaining: {distance:.2f} m',
            throttle_duration_sec=2.0
        )

    def result_callback(self, future):

        result = future.result()

        if result.status == 4:
            self.get_logger().info(
                'SUCCESS: Navigation goal reached!'
            )
        else:
            self.get_logger().error(
                f'Navigation failed. Status: {result.status}'
            )

        rclpy.shutdown()


def main(args=None):

    rclpy.init(args=args)

    node = GoalSender()

    try:
        if node.send_goal():
            rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Navigation client interrupted.')
    finally:
        if rclpy.ok():
            rclpy.shutdown()

        node.destroy_node()


if __name__ == '__main__':
    main()
