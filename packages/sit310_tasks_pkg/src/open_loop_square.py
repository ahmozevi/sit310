#!/usr/bin/env python3

import rospy
import time
from duckietown_msgs.msg import WheelsCmdStamped


class OpenLoopSquare:
    def __init__(self):
        rospy.init_node("open_loop_square_node", anonymous=True)

        self.pub = rospy.Publisher(
            "/deakinbot/wheels_driver_node/wheels_cmd",
            WheelsCmdStamped,
            queue_size=1
        )

        rospy.sleep(2)

    def set_wheels(self, left, right, duration):
        msg = WheelsCmdStamped()
        msg.vel_left = left
        msg.vel_right = right

        start_time = time.time()

        while time.time() - start_time < duration and not rospy.is_shutdown():
            msg.header.stamp = rospy.Time.now()
            self.pub.publish(msg)
            rospy.sleep(0.1)

    def stop(self):
        self.set_wheels(0.0, 0.0, 1.0)

    def run_square(self):
        forward_time = 2.0
        turn_time = 1.0

        forward_speed = 0.3
        turn_speed = 0.25

        rospy.loginfo("Starting open loop square movement")

        for side in range(4):
            rospy.loginfo("Moving forward")
            self.set_wheels(forward_speed, forward_speed, forward_time)

            rospy.loginfo("Turning left")
            self.set_wheels(-turn_speed, turn_speed, turn_time)

        self.stop()
        rospy.loginfo("Open loop square movement finished")


if __name__ == "__main__":
    try:
        controller = OpenLoopSquare()
        controller.run_square()
    except rospy.ROSInterruptException:
        pass
