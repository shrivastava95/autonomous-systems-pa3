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
threshold_distance_to_target = 0.3  # Set the stopping threshold

class RobotController:
    def __init__(self, alpha_beta, target_x, target_y):
        self.target_x = target_x
        self.target_y = target_y
        self.forwardvel = np.clip(np.random.beta(*alpha_beta) * max_speed, 0, max_speed) if alpha_beta is not None else max_speed
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        rospy.Subscriber('/odom', Odometry, self.odom_callback)

    def odom_callback(self, msg):
        global threshold_distance_realignment
        global thresh_small
        global thresh_large
        global threshold_distance_to_target

        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        orientation_q = msg.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = euler_from_quaternion(orientation_list)

        # Calculate distance to target
        distance_to_target = sqrt((self.target_x - x)**2 + (self.target_y - y)**2);        # self.forwardvel = 0.25;

        # print(f'distance: {distance_to_target:.2f}')
        if distance_to_target < threshold_distance_to_target:
            # Stop the bot by publishing a zero velocity Twist message
            stop_command = Twist()
            stop_command.linear.x = 0
            stop_command.angular.z = 0
            self.pub.publish(stop_command)

            # Wait a bit for the message to take effect
            rospy.sleep(1)

            rospy.signal_shutdown("Target reached")  # Stop the node if target is close enough
            return

        # Calculate line equation parameters
        m = tan(yaw)
        b = y - m * x

        # Calculate perpendicular distance from the target to the line
        A = m
        B = -1
        C = b
        perpendicular_distance = fabs(A * self.target_x + B * self.target_y + C) / sqrt(A**2 + B**2)

        # Command to publish
        command = Twist()

        # Determine rotation direction
        theta = atan2(self.target_y - y, self.target_x - x)
        delta_theta = theta - yaw
        if delta_theta > pi:
            while delta_theta > pi:
                delta_theta -= 2*pi
        elif delta_theta < -pi:
            while delta_theta < -pi:
                delta_theta += 2*pi

        if perpendicular_distance > threshold_distance_realignment or abs(delta_theta) > 1.5:
            command.angular.z = 0.5 if delta_theta > 0 else -0.5
        else:
            # Move forward if aligned properly
            command.angular.z = 0.1 if delta_theta > 0 else -0.1
            command.linear.x = self.forwardvel

        self.pub.publish(command)

def listener(args):
    target_location = args.target
    alpha_beta = args.alphabeta
    rospy.init_node('go_to_point_line_dist', anonymous=True)
    controller = RobotController(alpha_beta, target_location[0], target_location[1])
    rospy.spin()

import argparse

def main():
    parser = argparse.ArgumentParser(description='Robot navigation to a specified point.')
    parser.add_argument('--target', nargs=2, type=float, help='Target coordinates as x and y values')
    parser.add_argument('--alphabeta', nargs=2, type=float, help='Alpha and Beta values for varying the velocity', default=None)
    args = parser.parse_args()

    if args.target:
        listener(args)
    else:
        print("Error: Please provide the target coordinates using --target option.")


if __name__ == "__main__":
    main()
