#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */
# /*
# Copyright (c) 2015, Andrew Blanford
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
import pt_ach
import ach
import sys
import time
from ctypes import *
import socket
import cv2.cv as cv
import cv2
import numpy as np

# ach setup
ref = pt_ach.PT_REF()
tim = pt_ach.PT_TIME()
cfg = pt_ach.PT_USER_CONFIG()
r = ach.Channel(pt_ach.TARGET_POSITION_CHAN)
r.flush()
v = ach.Channel(pt_ach.ROBOT_VID_CHAN)
t = ach.Channel(pt_ach.ROBOT_TIME_CHAN)
c = ach.Channel(pt_ach.USER_CONFIG_CHAN)

# CV setup 
cv.NamedWindow("wctrl", cv.CV_WINDOW_AUTOSIZE)

newx = 160 #320
newy = 120 #240

nx = 160
ny = 120

while True:
    # Get Frame
    img = np.zeros((newx,newy,3), np.uint8)
    c_image = img.copy()
    vid = cv2.resize(c_image,(newx,newy))
    [status, framesize] = v.get(vid, wait=False, last=True)
    if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
        vid2 = cv2.resize(vid,(nx,ny))
        # for robot color is already RGB
        img = vid2
        # need to convert for sim 
        if cfg.flag[0] == 0:
           img = cv2.cvtColor(vid2,cv2.COLOR_BGR2RGB)
        cv2.imshow("wctrl", img)
        cv2.waitKey(10)
    else:
        raise ach.AchException( v.result_string(status) )


    [status, framesize] = t.get(tim, wait=False, last=True)
    if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
        pass
    else:
        raise ach.AchException( v.result_string(status) )

     
    [status, framesize] = c.get(cfg, wait=False, last=True)
    if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
        pass
    else:
        raise ach.AchException( v.result_string(status) )

    # Def:
    # ref.ref[0] = target x
    # ref.ref[1] = target y
    # tim.sim[0] = Sim Time
    # img        = cv image in BGR format

    # image height and width
    numRows = img.shape[0]
    numCols = img.shape[1]

    # lower and upper range in BGR format
    lower = np.array([cfg.tgt[2], cfg.tgt[1], cfg.tgt[0]], np.uint8)
    upper = np.array([cfg.tgt[5], cfg.tgt[4], cfg.tgt[3]], np.uint8)
#    print "lower", lower
#    print "upper", upper
    # use cv funtion to find the blue mask
    mask = cv2.inRange(img, lower, upper)
    cv2.imshow("mask", mask)

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
    if a > 0:
        # find position in image frame
        x = tx / a
        y = ty / a
        # compute offset from center
        offsetX = (x - (numCols/2))
        offsetY = -(y - (numRows/2))
        # normalize
        x = float(offsetX) / (numCols/2)
        y = float(offsetY) / (numRows/2)
        # use the normalized x/y
        ref.ref[0] = x
        ref.ref[1] = y    
        print "x", x, "y", y
        # Sets target reference
        r.put(ref);

    # Sleeps
    time.sleep(0.1)   
