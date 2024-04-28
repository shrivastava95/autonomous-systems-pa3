import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion
from math import atan2, sqrt, tan, pi, fabs
import numpy as np

class RobotController:
    def __init__(self, target_x, target_y):
        self.target_x = target_x
        self.target_y = target_y
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        rospy.Subscriber('/odom', Odometry, self.odom_callback)

    def odom_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        orientation_q = msg.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = euler_from_quaternion(orientation_list)

        # Calculate line equation parameters
        m = tan(yaw)
        b = y - m * x

        # Calculate perpendicular distance from the target to the line
        A = m
        B = -1
        C = b
        distance = fabs(A * self.target_x + B * self.target_y + C) / sqrt(A**2 + B**2)

        # Command to publish
        command = Twist()
        if distance > 2.0:  # Threshold distance to consider realignment
            # Determine rotation direction
            theta = atan2(self.target_y - y, self.target_x - x)
            delta_theta = theta - yaw
            command.angular.z = 0.3 if delta_theta > 0 else -0.3
            command.angular.z *= float(np.sqrt(min(distance, 10.0))) * 0.1
        else:
            # Move forward if aligned properly
            command.linear.x = 0.5

        self.pub.publish(command)

def listener():
    rospy.init_node('go_to_point_line_dist', anonymous=True)
    controller = RobotController(5.0, 5.0)
    rospy.spin()

if __name__ == '__main__':
    listener()