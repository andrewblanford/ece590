#!/usr/bin/evn python 
# Andrew Blanford
# ECE 590
# HW6
# functions for visual servo

import cv2.cv as cv
import cv2
import numpy as np

# returns dictionary 
# xR, yR, xL, yL, depth, found
def findTarget(imgL, imgR, lower, upper):
    'Find a target in the lower/upper range and get the x, y and depth'
    numRows = imgR.shape[0]
    numCols = imgR.shape[1]

    # use cv funtion to find the yellow mask
    maskR = cv2.inRange(imgR, lower, upper)
    maskL = cv2.inRange(imgL, lower, upper)

    # find the CG
    # add up all the mask values > 0 and track accumlated positions
    txR = 0
    tyR = 0
    aR = 0
    txL = 0
    tyL = 0
    aL = 0
    for x in range(numCols):
        for y in range(numRows):
            if maskR[y, x] > 0:
                txR += x
                tyR += y
                aR = aR + 1
            if maskL[y, x] > 0:
                txL += x
                tyL += y
                aL = aL + 1

    # camera parameters
    f = .085
    b = .4
    ps = .000280
    xR = 0.0
    xL = 1.0
    yL = 0
    yR = 0
    depth = 0.0
    found = False
    if aR > 0 and aL > 0: 
        xR = txR / aR
        yR = tyR / aR
        xL = txL / aL
        yL = tyL / aL
        dX = abs(xR - xL)
        depth = (f * b) / (dX * ps)
        found = True

    return {'found':found, 'xR':xR, 'yR':yR, 'xL':xL, 'yL':yL, 'depth':depth}

def getCenteringCommand(error):
    kp = .001
    kd = .1
    #c = (kp * error) + (kd * ((error - eLast) / (tNow - tLast)))
    c = kp * error
    #eLast = error
    # clamp c 
    #c / (numCols / 2)
    if c > .8:
        c = .8
    if c < -.8: 
        c = -.8
    return c

def getApproachCommand(error):
    kp = .12
    c = (kp * error)
    # clamp c 
    if c > .5:
        c = .5
    if c < -.5: 
        c = -.5
    return c

