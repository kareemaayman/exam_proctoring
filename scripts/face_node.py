#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2

class FaceDetectionNode:
    def __init__(self):
        rospy.init_node('face_node', anonymous=True)

        self.bridge = CvBridge()

        # Subscriber
        self.sub = rospy.Subscriber(
            '/camera_frames',
            Image,
            self.image_callback
        )

        # Publisher
        self.pub = rospy.Publisher(
            '/face_data',
            String,
            queue_size=10
        )

        # Load Haar Cascade
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

        rospy.loginfo("Face Detection Node Started")

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        face_data = ""

        for (x, y, w, h) in faces:
            face_data += "{},{},{},{};".format(x, y, w, h)

        self.pub.publish(face_data)


if __name__ == '__main__':
    try:
        node = FaceDetectionNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
