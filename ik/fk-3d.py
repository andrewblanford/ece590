#!/usr/bin/evn python 
# Andrew Blanford
# ECE 590

import numpy as np
import sys
import math

l1 = .24551
l2 = .282575
l3 = .3127375
l4 = .0635

# kinematic configruation
leftkin = [
[[0, l1, 0],  [0, 1, 0]],
[[0, 0, 0],   [1, 0, 0]],
[[0, 0, 0],   [0, 0, 1]],
[[0, 0, -l2], [0, 1, 0]],
[[0, 0, -l3], [0, 0, 1]],
[[0, 0, 0],   [1, 0, 0]],
[[0, 0, -l4], [0, 0, 0]]]
rightkin = [
[[0, -l1, 0], [0, 1, 0]],
[[0, 0, 0],   [1, 0, 0]],
[[0, 0, 0],   [0, 0, 1]],
[[0, 0, -l2], [0, 1, 0]],
[[0, 0, -l3], [0, 0, 1]],
[[0, 0, 0],   [1, 0, 0]],
[[0, 0, -l4], [0, 0, 0]]]

def getPi(kin, i):
	"return kinematic config for joint i"
	return np.asmatrix(kin[i][0]).getT()

def getRi(kin, i, theta):
	"get the rotation matrix"
	axis = kin[i][1]
	t = theta * axis[0]
	rx = np.matrix(
		[[1, 0, 0],
		[0, math.cos(t), -math.sin(t)],
		[0, math.sin(t), math.cos(t)]])
	t = theta * axis[1]
	ry = np.matrix(
		[[math.cos(t), 0, math.sin(t)],
		[0, 1, 0],
		[-math.sin(t), 0, math.cos(t)]])
	t = theta * axis[2]
	rz = np.matrix(
		[[math.cos(t), -math.sin(t), 0],
		[math.sin(t), math.cos(t), 0],
		[0, 0, 1]])
	return rx*ry*rz

def getTi(Ri, Pi):
	"build transform for joint"
	b = np.matrix([0, 0, 0, 1])
	Ti = np.bmat([[Ri, Pi], [b]])
	return Ti

def getT(theta, left):
	"input angles and left/right, return transform"
	kin = leftkin
	if (not left):
		kin = rightkin
	result = np.identity(4)
	for i in range(len(kin)):
		Pi = getPi(kin, i)
		# not sure which theta here???
		Ri = getRi(kin, i, theta[i])
		Ti = getTi(Ri, Pi)
		result = result * Ti
	return result


def getPos(T):
	x = T[0, 3]
	y = T[1, 3]
	z = T[2, 3]
	# since R is in upper left of T, can use same index
	thetax = math.atan2(T[2, 1], T[2, 2])
	thetay = math.atan2((-T[2, 0]), (T[2, 1]**2 + T[2, 2]**2))
	thetaz = math.atan2(T[1, 0], T[0, 0])
	print "x: ", x
	print "y: ", y
	print "z: ", z
	print "x: ", thetax
	print "y: ", thetay
	print "z: ", thetaz
	return

theta = [0, 0, 0, math.radians(-90), 0, 0, 0]

t = getT(theta, True)
print t

getPos(t)

