#!/usr/bin/evn python 
# Andrew Blanford
# ECE 590
# FK based on MDS robot arm

import numpy as np
import sys
import math

# Arm lengths
l1 = .24551
l2 = .282575
l3 = .3127375
l4 = .0635

# kinematic configruation - Left 
leftkin = [
[[0, l1, 0],  [0, 1, 0]],
[[0, 0, 0],   [1, 0, 0]],
[[0, 0, 0],   [0, 0, 1]],
[[0, 0, -l2], [0, 1, 0]],
[[0, 0, -l3], [0, 0, 1]],
[[0, 0, 0],   [1, 0, 0]],
[[0, 0, -l4], [0, 0, 0]]]
# kinematic configuration - Right
rightkin = [
[[0, -l1, 0], [0, 1, 0]],
[[0, 0, 0],   [1, 0, 0]],
[[0, 0, 0],   [0, 0, 1]],
[[0, 0, -l2], [0, 1, 0]],
[[0, 0, -l3], [0, 0, 1]],
[[0, 0, 0],   [1, 0, 0]],
[[0, 0, -l4], [0, 0, 0]]]

# get the position vector from the kinematic table
# kin - left or right kinematic information
# i - joint index
def getPi(kin, i):
	"return kinematic config for joint i"
	return np.asmatrix(kin[i][0]).getT()

# get the rotation matrix for a specific joint
# kin - left or right kinematic information
# i - joint index
# theta - angle of joint i
def getRi(kin, i, theta):
	"get the rotation matrix"
	axis = kin[i][1]
	# rotation about x
	t = theta * axis[0]
	rx = np.matrix(
		[[1, 0, 0],
		[0, math.cos(t), -math.sin(t)],
		[0, math.sin(t), math.cos(t)]])
	# rotation about y
	t = theta * axis[1]
	ry = np.matrix(
		[[math.cos(t), 0, math.sin(t)],
		[0, 1, 0],
		[-math.sin(t), 0, math.cos(t)]])
	# rotation about z
	t = theta * axis[2]
	rz = np.matrix(
		[[math.cos(t), -math.sin(t), 0],
		[math.sin(t), math.cos(t), 0],
		[0, 0, 1]])
	return rx*ry*rz

# assemble the complete transformation matrix (4x4)
# Ri - rotation matrix 3x3
# Pi - position vector 3x1
def getTi(Ri, Pi):
	"build transform for joint"
	b = np.matrix([0, 0, 0, 1])
	Ti = np.bmat([[Ri, Pi], [b]])
	return Ti

# get the final transform of all DoF
# theta - angle vector for all angles in kinematic chain
# left - true for left arm, false for right arm
def getT(theta, left):
	"input angles and left/right, return transform"
	# choose kinematic config
	kin = rightkin
	if (left):
		kin = leftkin
	# calculate and multiply in each transform for each link
	result = np.identity(4)
	for i in range(len(kin)):
		Pi = getPi(kin, i)
		Ri = getRi(kin, i, theta[i])
		Ti = getTi(Ri, Pi)
		result = result * Ti
	return result


# Get the position and orientation from transform
# returns dictionary using
# position: x, y, z
# orientation: tx, ty, tz for theta values
def getPos(T):
	"compute the full x,y,z position and orientation given the transform"
	x = T[0, 3]
	y = T[1, 3]
	z = T[2, 3]
	# since R is in upper left of T, can use same index
	thetax = math.atan2(T[2, 1], T[2, 2])
	thetay = math.atan2((-T[2, 0]), (T[2, 1]**2 + T[2, 2]**2))
	thetaz = math.atan2(T[1, 0], T[0, 0])
	# return in dictionary format t* are theta values
	return {'x':x, 'y':y, 'z':z, 'tx':thetax, 'ty':thetay, 'tz':thetaz}

# left = true, right = false
def getFK(theta, left):
	"computer FK given current angles and left / right"
	t = getT(theta, left)
	pos = getPos(t)
	return [pos['x'], pos['y'], pos['z']]
	
