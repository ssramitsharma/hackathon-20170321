#!/usr/bin/env python
import rospy
from amr_msgs.msg import Ranges
from sensor_msgs.msg import Range
from geometry_msgs.msg import Twist

def main():
    rospy.init_node('controller')


if __name__ == '__main__':
    main()
