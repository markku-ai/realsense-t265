#!/usr/bin/python
# -*- coding: utf-8 -*-

import pyrealsense2 as rs

from pprint import pprint
import numpy as np
import cv2

# Get realsense pipeline
pipe = rs.pipeline()

# Configure the pipeline
cfg = rs.config()
cfg.enable_stream(rs.stream.pose) # Positional data (translation, rotation, velocity etc)
cfg.enable_stream(rs.stream.fisheye, 1) # Left camera
cfg.enable_stream(rs.stream.fisheye, 2) # Right camera

# Prints a list of available streams, not all are supported by each device
print('Available streams:')
pprint(dir(rs.stream))

# Start the configured pipeline
pipe.start(cfg)

try:
    for _ in range(10000):
        frames = pipe.wait_for_frames()

        left = frames.get_fisheye_frame(1)
        left_data = np.asanyarray(left.get_data())

        right = frames.get_fisheye_frame(2)
        right_data = np.asanyarray(right.get_data())

        cv2.imshow('left', left_data)
        cv2.imshow('right', right_data)

        pose = frames.get_pose_frame()
        if pose:
            data = pose.get_pose_data()
            print('\nFrame number: ', pose.frame_number)
            print('Position: ', data.translation)
            print('Velocity: ', data.velocity)
            print('Acceleration: ', data.acceleration)
            print('Rotation: ', data.rotation)

        cv2.waitKey(50)

finally:
    pipe.stop()
