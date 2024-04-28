import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion

def odom_callback(msg):
    # Extract the position (x, y) coordinates
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    
    # Extract the orientation in quaternion
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    
    # Convert quaternion to Euler angles (roll, pitch, yaw)
    (roll, pitch, yaw) = euler_from_quaternion(orientation_list)
    
    # Log the coordinates and yaw
    rospy.loginfo("X: {:.2f}, Y: {:.2f}, Yaw: {:.4f}".format(x, y, yaw))

def listener():
    rospy.init_node('odom_yaw_listener', anonymous=True)  # Initialize the node
    rospy.Subscriber('/odom', Odometry, odom_callback)    # Subscribe to the odometry topic
    rospy.spin()  # Keep the program from exiting until the node is shut down

if __name__ == '__main__':
    listener()