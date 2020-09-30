# gazebo-line-follower
Simple Gazebo simulation of a line following robot (OpenCV, RoS, SciPy).

See `~/node/move_robot.py` for the implementation. First, we grayscale a frame from the robot's camera feed, then apply a binary mask. Finally, the center of mass of the binary mask is computed, and the robot's movement is adjusted.

Visit https://youtu.be/BuUYXrn7hKo for a video.

