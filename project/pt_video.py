#!/usr/bin/env python
# Andrew Blanford
# ECE 590
# Capture camera video stream and output to ach channel


import pt_ach
import ach
import sys 
import time
from ctypes import *
import cv2.cv as cv
import cv2
import numpy as np

cfg = pt_ach.PT_USER_CONFIG()

c = ach.Channel(pt_ach.USER_CONFIG_CHAN)
v = ach.Channel(pt_ach.ROBOT_VID_CHAN)

cv.NamedWindow("pt_video", cv.CV_WINDOW_AUTOSIZE)
capture = cv2.VideoCapture(0)
nx = 160
ny = 120

while True:
   c.get(cfg, wait=False, last=True)
   ret, vid = capture.read()
   vid2 = cv2.resize(vid,(nx,ny))
   cv2.imshow("pt_video", vid2)
   cv2.waitKey(20)
   if cfg.flag[0] == 1:
      v.put(vid2)


   time.sleep(0.1)
