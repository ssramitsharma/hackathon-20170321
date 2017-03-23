#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

youBotOn = False
startX=0.0
startY=0.0

def stopYouBot():
    twist = Twist()

    twist.linear.x = 0
    twist.linear.y = 0
    twist.angular.z = 0

    youBot_publisher.publish(twist)

def move_callback(message):
    command = message.data.lower()
    twist = Twist()

    rospy.loginfo("Swith is %s" %("ON" if youBotOn else "OFF"))

    if  command == "forward":
        rospy.loginfo("Moving forward ...")
        twist.linear.x = rospy.get_param("/x_vel", 0.1)
        twist.linear.y = 0

    elif command == "backward":
        rospy.loginfo("Moving backward ...")
        twist.linear.x = rospy.get_param("/x_vel", 0.1) * -1.0
        twist.linear.y = 0

    elif command == "left":
        rospy.loginfo("Moving left ...")
        twist.linear.x = 0
        twist.linear.y = rospy.get_param("/y_vel",0.1)
        twist.angular.z = rospy.get_param("/theta_val", 0)

    elif command == "right":
        rospy.loginfo("Moving right ...")
        twist.linear.x = 0
        twist.linear.y = rospy.get_param("/y_vel",0.1) * -1.0
        twist.angular.z = rospy.get_param("/theta_val", 0)

    if youBotOn:
        youBot_publisher.publish(twist)
    else:
        rospy.loginfo("youBot is off")

def trigger_callback(message):
    global youBotOn
    command = message.data.lower()

    if command == "e_start":
        rospy.loginfo("Turning on ...")
        youBotOn = True

    elif command == "e_stop":
        rospy.loginfo("Turning off ...")
        youBotOn = False

        stopYouBot()

def odom_callback(message):
    global startX
    global startY

    currentX = message.pose.pose.position.x
    currentY = message.pose.pose.position.y

    distance = (((currentX - startX) ** 2) + ((currentY - startY) ** 2)) ** 0.5

    targetDistance = rospy.get_param("/distance", 0.5)

    if(distance >= targetDistance):
        startX = currentX
        startY = currentY

        stopYouBot()


def main():
    global youBot_publisher

    rospy.init_node('controller')
    rospy.Subscriber('/input', String, move_callback)

    rospy.Subscriber('/event_in', String, trigger_callback)

    rospy.Subscriber("/odom", Odometry, odom_callback)

    youBot_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        rate.sleep()
    pass

if __name__ == '__main__':
    main()
