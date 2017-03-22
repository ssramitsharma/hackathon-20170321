#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

youBotOn = False

def move_callback(message):
    global lastTwist
    command = message.data.lower()
    twist = Twist()

    rospy.loginfo("Swith is %s" %("ON" if youBotOn else "OFF"))

    if  command == "forward":
        rospy.loginfo("Moving forward ...")
        twist.linear.x = rospy.get_param("/x_vel", 0.1)
        twist.linear.y = rospy.get_param("/y_vel",0)

    elif command == "backward":
        rospy.loginfo("Moving backward ...")
        twist.linear.x = rospy.get_param("/x_vel", 0.1) * -1.0
        twist.linear.y = rospy.get_param("/y_vel",0) * -1.0

    elif command == "left":
        rospy.loginfo("Moving left ...")
        twist.linear.x = rospy.get_param("/x_vel", 0.1)
        twist.linear.y = rospy.get_param("/y_vel",0)
        twist.angular.z = rospy.get_param("/theta_val", 0.2)

    elif command == "right":
        rospy.loginfo("Moving right ...")
        twist.linear.x = rospy.get_param("/x_vel", 0.1)
        twist.linear.y = rospy.get_param("/y_vel",0)
        twist.angular.z = rospy.get_param("/theta_val", 0.2) * -1.0

    lastTwist = twist

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

        youBot_publisher.publish(lastTwist)
    elif command == "e_stop":
        rospy.loginfo("Turning off ...")
        youBotOn = False

        twist = Twist()

        twist.linear.x = 0
        twist.linear.y = 0
        twist.angular.z = 0

        youBot_publisher.publish(twist)


def main():
    global youBot_publisher
    global lastTwist

    lastTwist = Twist()

    lastTwist.linear.x=0
    lastTwist.angular.z=0

    rospy.init_node('controller')
    rospy.Subscriber('/input', String, move_callback)

    rospy.Subscriber('/event_in', String, trigger_callback)

    youBot_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        rate.sleep()
    pass

if __name__ == '__main__':
    main()
