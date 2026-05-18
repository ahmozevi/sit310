this is the one i think is the best
#!/usr/bin/env python3

import rospy
from duckietown_msgs.msg import Twist2DStamped
from duckietown_msgs.msg import FSMState
 
class Drive_Square:
    def __init__(self):
        # Initialize global class variables
        self.cmd_msg = Twist2DStamped()
        self.has_run = False

        # Initialize ROS node
        rospy.init_node('drive_square_node', anonymous=True)
        
        # Initialize Pub/Subs
        self.pub = rospy.Publisher('/deakinbot/car_cmd_switch_node/cmd', Twist2DStamped, queue_size=1)
        rospy.Subscriber('/deakinbot/fsm_node/mode', FSMState, self.fsm_callback, queue_size=1)

        rospy.sleep(2)
        
    # Robot only moves when lane following is selected on the Duckiebot joystick app
    def fsm_callback(self, msg):
        rospy.loginfo("State: %s", msg.state)
        if msg.state == "NORMAL_JOYSTICK_CONTROL":
            self.stop_robot()
        elif msg.state == "LANE_FOLLOWING" and not self.has_run:
            self.has_run = True
            self.move_robot()
 
    # Sends zero velocities to stop the robot
    def stop_robot(self):
        self.cmd_msg.header.stamp = rospy.Time.now()
        self.cmd_msg.v = 0.0
        self.cmd_msg.omega = 0.0
        self.pub.publish(self.cmd_msg)
 
    # Spin forever but listen to message callbacks
    def run(self):
        rospy.spin()

    # Move forward continuously for a duration
    def move_forward(self, speed, duration):
        rospy.loginfo("Moving forward")

        rate = rospy.Rate(10)
        start_time = rospy.Time.now().to_sec()

        while rospy.Time.now().to_sec() - start_time < duration:
            self.cmd_msg.header.stamp = rospy.Time.now()
            self.cmd_msg.v = speed
            self.cmd_msg.omega = 0.0
            self.pub.publish(self.cmd_msg)
            rate.sleep()

        self.stop_robot()
        rospy.sleep(0.5)

    # Turn continuously for a duration
    def turn_left(self, speed, duration):
        rospy.loginfo("Turning")

        rate = rospy.Rate(10)
        start_time = rospy.Time.now().to_sec()

        while rospy.Time.now().to_sec() - start_time < duration:
            self.cmd_msg.header.stamp = rospy.Time.now()
            self.cmd_msg.v = 0.0
            self.cmd_msg.omega = speed
            self.pub.publish(self.cmd_msg)
            rate.sleep()

        self.stop_robot()
        rospy.sleep(0.5)

    # Robot drives around the loop map using open-loop timing and then stops
    def move_robot(self):

        straight_speed = 0.30
        straight_time = 4.15

        turn_speed = 1.5
        turn_time = 2.25

        for i in range(4):
            rospy.loginfo("Starting side %d", i + 1)
            self.move_forward(straight_speed, straight_time)
            self.turn_left(turn_speed, turn_time)

        rospy.loginfo("Finished full open-loop lap")
        self.stop_robot()


if __name__ == '__main__':
    try:
        duckiebot_movement = Drive_Square()

        # Automatic start when running script directly with python3.
        # This keeps testing simple while still keeping the original FSM callback structure.
        duckiebot_movement.move_robot()

        duckiebot_movement.run()
    except rospy.ROSInterruptException:
        pass
