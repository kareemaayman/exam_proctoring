#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

class AlertNode:
    def __init__(self):
        rospy.init_node('alert_node')

        # Parameter
        self.alert_level = rospy.get_param('~alert_level', 'HIGH')

        # Subscriber
        rospy.Subscriber('/violation_event', String, self.callback)

        # Publisher
        self.pub = rospy.Publisher('/alert_status', String, queue_size=10)

        rospy.loginfo("Alert Node Started 🚨")

    def callback(self, msg):
        alert_text = f"🚨 ALERT: {msg.data} | Level: {self.alert_level}"

        rospy.loginfo(alert_text)

        alert_msg = String()
        alert_msg.data = alert_text

        self.pub.publish(alert_msg)

if __name__ == '__main__':
    node = AlertNode()
    rospy.spin()
