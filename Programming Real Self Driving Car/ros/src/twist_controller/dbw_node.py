#!/usr/bin/env python
from geometry_msgs.msg import PoseStamped
import rospy
from std_msgs.msg import Bool
from styx_msgs.msg import Lane
from dbw_mkz_msgs.msg import ThrottleCmd, SteeringCmd, BrakeCmd, SteeringReport
from geometry_msgs.msg import TwistStamped
import math
import numpy as np
from twist_controller import Controller

'''
You can build this node only after you have built (or partially built) the `waypoint_updater` node.

You will subscribe to `/twist_cmd` message which provides the proposed linear and angular velocities.
You can subscribe to any other message that you find important or refer to the document for list
of messages subscribed to by the reference implementation of this node.

One thing to keep in mind while building this node and the `twist_controller` class is the status
of `dbw_enabled`. While in the simulator, its enabled all the time, in the real car, that will
not be the case. This may cause your PID controller to accumulate error because the car could
temporarily be driven by a human instead of your controller.

We have provided two launch files with this node. Vehicle specific values (like vehicle_mass,
wheel_base) etc should not be altered in these files.

We have also provided some reference implementations for PID controller and other utility classes.
You are free to use them or build your own.

Once you have the proposed throttle, brake, and steer values, publish it on the various publishers
that we have created in the `__init__` function.

'''

class DBWNode(object):
    def __init__(self):
        rospy.init_node('dbw_node')

        vehicle_mass = rospy.get_param('~vehicle_mass', 1736.35)
        fuel_capacity = rospy.get_param('~fuel_capacity', 13.5)
        brake_deadband = rospy.get_param('~brake_deadband', .1)
        decel_limit = rospy.get_param('~decel_limit', -5)
        accel_limit = rospy.get_param('~accel_limit', 1.)
        wheel_radius = rospy.get_param('~wheel_radius', 0.2413)
        wheel_base = rospy.get_param('~wheel_base', 2.8498)
        steer_ratio = rospy.get_param('~steer_ratio', 14.8)
        max_lat_accel = rospy.get_param('~max_lat_accel', 3.)
        max_steer_angle = rospy.get_param('~max_steer_angle', 8.)


        config = {
            'vehicle_mass': vehicle_mass,
            'fuel_capacity': fuel_capacity,
            'brake_deadband': brake_deadband,
            'decel_limit': decel_limit,
            'accel_limit': accel_limit,
            'wheel_radius': wheel_radius,
            'wheel_base': wheel_base,
            'steer_ratio': steer_ratio,
            'max_lat_accel': max_lat_accel,
            'max_steer_angle': max_steer_angle
        }

        self.steer_pub = rospy.Publisher('/vehicle/steering_cmd',
                                         SteeringCmd, queue_size=1)
        self.throttle_pub = rospy.Publisher('/vehicle/throttle_cmd',
                                            ThrottleCmd, queue_size=1)
        self.brake_pub = rospy.Publisher('/vehicle/brake_cmd',
                                         BrakeCmd, queue_size=1)

        # Create `TwistController` object
        self.controller = Controller(**config)

        self.dbw_enabled = False
        self.current_vel = None
        self.target_vel = None
        self.final_waypoints = None
        self.current_pose = None
        self.previous_loop_time = rospy.get_rostime()


        # Subscribe to all the topics you need to
        self.twist_sub = rospy.Subscriber('/twist_cmd', TwistStamped, self.twist_cb, queue_size=1)
        self.velocity_sub = rospy.Subscriber('/current_velocity', TwistStamped, self.current_vel_cb, queue_size=1)
        self.dbw_sub = rospy.Subscriber('/vehicle/dbw_enabled', Bool, self.dbw_enabled_cb, queue_size=1)
        self.final_wp_sub = rospy.Subscriber('final_waypoints', Lane, self.final_waypoints_cb, queue_size=1)
        self.pose_sub = rospy.Subscriber('/current_pose', PoseStamped, self.current_pose_cb, queue_size=1)

        self.loop()

    def loop(self):
        rate = rospy.Rate(50)  # 50Hz
        while not rospy.is_shutdown():
            # Get predicted throttle, brake, and steering using `twist_controller`
            # You should only publish the control commands if dbw is enabled
            if (self.current_vel is not None) and (self.target_vel is not None) and (self.final_waypoints is not None):
                current_time = rospy.get_rostime()
                ros_duration = current_time - self.previous_loop_time
                duration_in_seconds = ros_duration.secs + (1e-9 * ros_duration.nsecs)
                self.previous_loop_time = current_time

                current_linear_vel = self.current_vel.twist.linear.x
                target_linear_vel = self.target_vel.twist.linear.x

                target_angular_vel = self.target_vel.twist.angular.z
                cross_track_error = self.get_cross_track_error(self.final_waypoints, self.current_pose)

                throttle, brake, steering = self.controller.control(target_linear_vel,
                                                                    target_angular_vel,
                                                                    current_linear_vel,
                                                                    cross_track_error,
                                                                    duration_in_seconds)
                # reset controller
                if (not self.dbw_enabled
                        or abs(self.current_vel.twist.linear.x) < 1e-5
                        and abs(self.target_vel.twist.linear.x) < 1e-5):
                   self.controller.reset()

                if self.dbw_enabled:
                    self.publish(throttle, brake, steering)
            rate.sleep()

    def publish(self, throttle, brake, steer):
        tcmd = ThrottleCmd()
        tcmd.enable = True
        tcmd.pedal_cmd_type = ThrottleCmd.CMD_PERCENT
        tcmd.pedal_cmd = throttle
        self.throttle_pub.publish(tcmd)

        scmd = SteeringCmd()
        scmd.enable = True
        scmd.steering_wheel_angle_cmd = steer
        self.steer_pub.publish(scmd)

        bcmd = BrakeCmd()
        bcmd.enable = True
        bcmd.pedal_cmd_type = BrakeCmd.CMD_TORQUE
        bcmd.pedal_cmd = brake
        self.brake_pub.publish(bcmd)

    def get_cross_track_error(self,final_waypoints, current_pose):
        origin = final_waypoints[0].pose.pose.position
        waypoints_matrix = self.get_waypoints_2d(final_waypoints)

        # Convert the coordinates [x,y] in the world view to the car's coordinate

        # Shift the points to the origin
        shifted_matrix = waypoints_matrix - np.array([origin.x, origin.y])

        # Derive an angle by which to rotate the points
        offset = 11
        angle = np.arctan2(shifted_matrix[offset, 1], shifted_matrix[offset, 0])
        rotation_matrix = np.array([
                [np.cos(angle), -np.sin(angle)],
                [np.sin(angle), np.cos(angle)]
            ])
        rotated_matrix = np.dot(shifted_matrix, rotation_matrix)

        # Fit a 2 degree polynomial to the waypoints
        degree = 2
        coefficients = np.polyfit(rotated_matrix[:, 0], rotated_matrix[:, 1], degree)

        # Transform the current pose of the car to be in the car's coordinate system
        shifted_pose = np.array([current_pose.pose.position.x - origin.x, current_pose.pose.position.y - origin.y])
        rotated_pose = np.dot(shifted_pose, rotation_matrix)

        expected_y_value = np.polyval(coefficients, rotated_pose[0])
        actual_y_value = rotated_pose[1]

        return expected_y_value - actual_y_value

    def get_waypoints_2d(self,waypoints):
        return [[w.pose.pose.position.x, w.pose.pose.position.y] for w in waypoints]

    def twist_cb(self, msg):
        self.target_vel = msg

    def current_vel_cb(self, msg):
        self.current_vel = msg

    def dbw_enabled_cb(self, msg):
        rospy.logwarn("DBW_ENABLED %s" % msg)
        self.dbw_enabled = msg.data

    def final_waypoints_cb(self, msg):
        self.final_waypoints = msg.waypoints

    def current_pose_cb(self, msg):
        self.current_pose = msg


if __name__ == '__main__':
    DBWNode()