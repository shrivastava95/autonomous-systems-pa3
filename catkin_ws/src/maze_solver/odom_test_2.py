import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion
from math import atan2, sqrt, tan, pi, fabs
import numpy as np

from graphdata import graph, get_id_from_name

max_speed = 0.25

threshold_distance_realignment = 2.0
factor = 1.5
thresh_small = threshold_distance_realignment / factor
thresh_large = threshold_distance_realignment * factor

class RobotController:
    def __init__(self, target_x, target_y):
        self.target_x = target_x
        self.target_y = target_y
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        rospy.Subscriber('/odom', Odometry, self.odom_callback)

    def odom_callback(self, msg):
        global threshold_distance_realignment
        global thresh_small
        global thresh_large

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

        # Determine rotation direction
        theta = atan2(self.target_y - y, self.target_x - x)
        delta_theta = theta - yaw

        if distance > threshold_distance_realignment or abs(delta_theta) > 1.5:  # Threshold distance to consider realignment
            # print(f'distance: {distance:.3f}  delta_theta: {delta_theta:.2f}')
            command.angular.z = 0.5 if delta_theta > 0 else -0.5
            # command.angular.z *= np.sign(delta_theta) * min(0.5, max(abs(delta_theta), 0.09))
        else:
            # Move forward if aligned properly
            command.angular.z = 0.1 if delta_theta > 0 else -0.1
            command.linear.x = max_speed

        self.pub.publish(command)


def listener():
    rospy.init_node('go_to_point_line_dist', anonymous=True)
    controller = RobotController(*graph[get_id_from_name['main_gate']]['position'])
    rospy.spin()


listener()