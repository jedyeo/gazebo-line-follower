#! /usr/bin/env python

import rospy
import numpy as np
import cv2
from scipy.ndimage.measurements import center_of_mass
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

# Constants
TURN_LEFT_SPD = 0.1
TURN_RIGHT_SPD = 0.125
STRAIGHT_SPD = 0.25
ANGULAR_VEL = 1.25
OFFSET_Y = 500

# Global Variable that holds previous CoM
prev = (400, 400)


def callback(data):
    global prev

    try:
        # Process grayscale and binary mask
        img_grayscale = bridge.imgmsg_to_cv2(data, 'mono8')
        _, img_bin = cv2.threshold(img_grayscale, 128, 1, cv2.THRESH_BINARY_INV)

        # Compute center of mass of bottom 300 rows
        coords_bin = center_of_mass(img_bin[-300:])
        y = coords_bin[0] + OFFSET_Y
        x = coords_bin[1]

        # if CoM is NaN, take previous iteration's value of CoM
        if np.isnan(x) or np.isnan(y):
            x = prev[0]
            y = prev[1]
        else:
            prev = (x, y)
    
        print((x,y))

        # new Twist object
        move = Twist()

        # turn left or right or go straight
        if x < 350:
            move.linear.x = TURN_LEFT_SPD
            move.angular.z = ANGULAR_VEL
            pub.publish(move)
        elif x >= 350 and x <= 450:
            move.linear.x = STRAIGHT_SPD
            move.angular.z = 0
            pub.publish(move)
        else:
            move.linear.x = TURN_RIGHT_SPD
            move.angular.z = -1 * ANGULAR_VEL
            pub.publish(move)

    except CvBridgeError as e:
        print(e)


if __name__ == '__main__':
    bridge = CvBridge()
    rospy.init_node('move_robot')
    rospy.Subscriber('/robot/camera/image_raw', Image, callback)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    rate = rospy.Rate(2)
    rospy.spin()