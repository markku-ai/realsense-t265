#!/usr/bin/python
import pyrealsense2 as rs
import numpy as np
import cv2
import os

pipe = rs.pipeline()

cfg = rs.config()
cfg.enable_stream(rs.stream.fisheye, 1)
cfg.enable_stream(rs.stream.fisheye, 2)

pipe.start(cfg)

left_path = './data/left'
right_path = './data/right'
os.makedirs(left_path)
os.makedirs(right_path)

cv2.namedWindow('left', cv2.WINDOW_NORMAL)
cv2.namedWindow('right', cv2.WINDOW_NORMAL)

try:
    for i in range(200):
        frames = pipe.wait_for_frames()

        left = frames.get_fisheye_frame(1)
        left_data = np.asanyarray(left.get_data())

        right = frames.get_fisheye_frame(2)
        right_data = np.asanyarray(right.get_data())

        cv2.imshow('left', left_data)
        cv2.imshow('right', right_data)

        cv2.imwrite('%s/%d.jpg' % (left_path, i), left_data)
        cv2.imwrite('%s/%d.jpg' % (right_path, i), right_data)

        cv2.waitKey(500)

finally:
    pipe.stop()
