#!/usr/bin/env python
import rospy
from amr_msgs.msg import Ranges
from sensor_msgs.msg import Range
from geometry_msgs.msg import Twist

def sonar_callback(msg):
#    print msg
    global velocity_publisher
    left, right = msg.ranges[3].range, msg.ranges[4].range
    print left," ",right
    rospy.logwarn(left)
#    rospy.logerr(msg)
    '''
        Data Processing
    '''
    twist = Twist()
    twist.linear.x = (left+right)/2*0.5
    twist.linear.y = 0.0
    twist.angular.z = (left-right)
    
    velocity_publisher.publish(twist)

def main():
    global velocity_publisher
    rospy.init_node('controller')
    
    rospy.Subscriber('/sonar_pioneer', Ranges, sonar_callback)
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
#        rospy.logwarn("Running the node, time {}".format(rospy.get_time()))
        rate.sleep()
    pass


if __name__ == '__main__':
    main()
