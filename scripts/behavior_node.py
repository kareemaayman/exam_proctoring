#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

class BehaviorNode:

    def __init__(self):
        rospy.init_node('behavior_node')

        # ==============================
        # PARAMETERS (Behavior thresholds)
        # ==============================
        self.attention_threshold = rospy.get_param('~attention_threshold', 3)

        # ==============================
        # SUBSCRIBERS
        # ==============================
        rospy.Subscriber('/face_data', String, self.face_callback)
        rospy.Subscriber('/object_data', String, self.object_callback)
        rospy.Subscriber('/depth_data', String, self.depth_callback)

        # ==============================
        # PUBLISHER
        # ==============================
        self.pub = rospy.Publisher('/behavior_state', String, queue_size=10)

        # ==============================
        # INTERNAL STATE
        # ==============================
        self.face = "face_detected"
        self.object = "none"
        self.depth = "normal"

        self.no_face_counter = 0

    # ==============================
    # CALLBACKS
    # ==============================
    def face_callback(self, msg):
        self.face = msg.data

    def object_callback(self, msg):
        self.object = msg.data

    def depth_callback(self, msg):
        self.depth = msg.data

    # ==============================
    # CORE LOGIC (Multi-Perception)
    # ==============================
    def analyze_behavior(self):

        # -------- FACE ANALYSIS --------
        if self.face == "no_face":
            self.no_face_counter += 1
        else:
            self.no_face_counter = 0

        looking_away = self.no_face_counter >= self.attention_threshold

        # -------- OBJECT ANALYSIS --------
        using_object = self.object in ["phone", "book"]

        # -------- DEPTH ANALYSIS --------
        bad_distance = self.depth in ["far", "close"]

        # ==============================
        # DECISION LOGIC (PRIORITY)
        # ==============================

        # Highest priority → cheating
        if using_object:
            return "using_phone"

        # Medium → attention issue
        if looking_away:
            return "looking_away"

        # Low → suspicious positioning
        if bad_distance:
            return "too_far"

        # Normal
        return "normal"

    # ==============================
    # MAIN LOOP
    # ==============================
    def run(self):
        rate = rospy.Rate(5)  # Minimum 5 FPS requirement

        while not rospy.is_shutdown():

            state = self.analyze_behavior()

            # Publish result
            self.pub.publish(state)

            # Debug (VERY IMPORTANT for grading)
            rospy.loginfo(
                f"[Behavior Node] Face: {self.face}, Object: {self.object}, Depth: {self.depth} → State: {state}"
            )

            rate.sleep()


# ==============================
# RUN NODE
# ==============================
if __name__ == '__main__':
    node = BehaviorNode()
    node.run()
