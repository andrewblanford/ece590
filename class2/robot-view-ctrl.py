#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */
# /*
# Copyright (c) 2014, Daniel M. Lofaro <dan (at) danLofaro (dot) com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# */
import ipc
import ach
import sys
import time
from ctypes import *
import socket
import cv2.cv as cv
import cv2
import numpy as np

ref = ipc.E_SERVO()

# CV setup 
cv.NamedWindow("wctrl", cv.CV_WINDOW_AUTOSIZE)
#capture = cv.CaptureFromCAM(0)
capture = cv2.VideoCapture(0)

# added
##sock.connect((MCAST_GRP, MCAST_PORT))
newx = 320
newy = 240

nx = 640
ny = 480

r = ach.Channel(ipc.EXAMPLE_CHAN_1)
r.flush()

i=0
tLast = 0
eLastX = 0
eLastY = 0
cLastX = 0
cLastY = 0

print '======================================'
print '============= Robot-View ============='
print '========== Daniel M. Lofaro =========='
print '========= dan@danLofaro.com =========='
print '======================================'
while True:
    # Get Frame
    ret, vid = capture.read()

    vid2 = cv2.resize(vid,(nx,ny))
    #img = cv2.cvtColor(vid2,cv2.COLOR_BGR2RGB)
    img = vid2
    cv2.imshow("wctrl", img)
    cv2.waitKey(10)

#-----------------------------------------------------
#--------[ Do not edit above ]------------------------
#-----------------------------------------------------
    # Def:
    # ref.command[0] = yaw radians
    # ref.command[1] = pitch radians
    # img        = cv image in BGR format

    # image height and width
    numRows = img.shape[0]
    numCols = img.shape[1]

    # lower and upper range of blue in BGR format
    lower = np.array([100, 0, 0], np.uint8)
    upper = np.array([255, 100, 100], np.uint8)
    # use cv funtion to find the blue mask
    mask = cv2.inRange(img, lower, upper)

    # find the CG
    # add up all the mask values > 0 and track accumlated positions
    tx = 0
    ty = 0
    a = 0
    for x in range(numCols):
        for y in range(numRows):
            if mask[y, x] > 0:
                tx += x
                ty += y
                a = a + 1

    # compute final CG based on found points
    x = -1
    y = -1
    found = False
    # require a > 5 to avoid small blue noise
    if a > 5:
        x = tx / a
        y = ty / a
        found = True
        print "Found: ", found, "at", x, ",", y
    else: 
        print "Not found"

    tNow = time.time()
    if found:
        # compute offset from center (-1 to 1)
        x = (x - (numCols/2)) / (numCols/2))
        y = -((y - (numRows/2)) / (numRows/2))
        # get control output - base on x only
        xDes = 0
        yDes = 0
        kp = .2
        kd = .1
        eX = xDes - x
        eY = yDes - y
	print "e", eX eY
        cx = (kp * eX) + (kd * ((eX - eLastX) / (tNow - tLast)))
        cy = (kp * eY) + (kd * ((eY - eLastY) / (tNow - tLast)))
        cx = cx * (tNow - tLast) + cLastX
        cx = cy * (tNow - tLast) + cLastY
        cLastX = cx
        cLastY = cy
        eLastX = eX
        eLastY = eY
        print "C: ", cX, cY
      

        # set commands
        ref.command[0] = cX
        ref.command[1] = cY
    else: 
        # if not found, maximize e
        eLastX = 0
        eLastY = 0
        # search pattern - turn in place
        ref.ref[0] = 0
        ref.ref[1] = 0    
    tLast = tNow
    
    # Sets reference to robot
    r.put(ref);

    # Sleeps
    time.sleep(0.1)   
#-----------------------------------------------------
#--------[ Do not edit below ]------------------------
#-----------------------------------------------------
