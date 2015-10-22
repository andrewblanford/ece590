#!/usr/bin/evn python 
# Andrew Blanford
# ECE 590
# test MDS robot functions

import math
import mdsfk as mds

# define some random angles
theta = [0, math.radians(90), 0, 0, 0, 0, 0]

# get the transform
t = mds.getT(theta, True)
print t

# get the position / rotation
pos = mds.getPos(t)
print "x: ", pos['x']
print "y: ", pos['y']
print "z: ", pos['z']
print "tx: ", pos['tx']
print "ty: ", pos['ty']
print "tz: ", pos['tz']

# do FK
print mds.getFK(theta, True)
