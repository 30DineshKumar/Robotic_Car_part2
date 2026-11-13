import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import TransformStamped, Twist
from tf2_ros import TransformBroadcaster


class DriveRobot(Node):
    def __init__(self):
        super().__init__('drive_robot')
        self.joint_pub = self.create_publisher(JointState, 'joint_states', 10)
        self.tf_broadcaster = TransformBroadcaster(self)
        self.cmd_sub = self.create_subscription(Twist, 'cmd_vel', self.cmd_callback, 10)
        self.timer = self.create_timer(0.1, self.update)

        self.wheel_angle = 0.0
        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0

        self.linear_speed = 0.0   # set by command
        self.angular_speed = 0.0  # set by command

    def cmd_callback(self, msg):
        self.linear_speed = msg.linear.x
        self.angular_speed = msg.angular.z

    def update(self):
        dt = 0.1
        now = self.get_clock().now().to_msg()

        # --- Move the body based on manual commands ---
        self.yaw += self.angular_speed * dt
        self.x += self.linear_speed * math.cos(self.yaw) * dt
        self.y += self.linear_speed * math.sin(self.yaw) * dt

        # --- Spin wheels proportional to forward speed ---
        self.wheel_angle += self.linear_speed * dt * 5.0

        joint_msg = JointState()
        joint_msg.header.stamp = now
        joint_msg.name = ['left_wheel_joint', 'right_wheel_joint']
        joint_msg.position = [
                              self.wheel_angle,
                              self.wheel_angle
                              ]
        
        self.joint_pub.publish(joint_msg)

        t = TransformStamped()
        t.header.stamp = now
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_link'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        t.transform.rotation.z = math.sin(self.yaw / 2.0)
        t.transform.rotation.w = math.cos(self.yaw / 2.0)
        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = DriveRobot()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        try:
            node.destroy_node()
        except BaseException:
            pass
        try:
            if rclpy.ok():
                rclpy.shutdown()
        except BaseException:
            pass


if __name__ == '__main__':
    main()