#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2

class DepthEstimationNode:
    def __init__(self):
        rospy.init_node('depth_node', anonymous=True)

        self.bridge = CvBridge()

        # Subscriber
        self.sub = rospy.Subscriber(
            '/camera_frames',
            Image,
            self.image_callback
        )

        # Publisher
        self.pub = rospy.Publisher(
            '/depth_data',
            String,
            queue_size=10
        )

        # Haar Cascade
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

        # Constants (adjust if needed)
        self.KNOWN_FACE_WIDTH = 14.0  # cm
        self.FOCAL_LENGTH = 600       # estimated

        rospy.loginfo("Depth Estimation Node Started")

    def estimate_distance(self, face_width_pixels):
        if face_width_pixels == 0:
            return 0
        return (self.KNOWN_FACE_WIDTH * self.FOCAL_LENGTH) / face_width_pixels

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        depth_data = ""

        for (x, y, w, h) in faces:
            distance = self.estimate_distance(w)
            depth_data += "face:{:.2f};".format(distance)

        self.pub.publish(depth_data)


if __name__ == '__main__':
    try:
        node = DepthEstimationNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
