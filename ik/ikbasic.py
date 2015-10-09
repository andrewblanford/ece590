#!/usr/bin/evn python 
# Andrew Blanford
# ECE 590

import sys
import math
import numpy as np

def getDist(e, g):
	"euclidian distance between two points"
	return math.sqrt((e[0] - g[0])**2 + (e[1] - g[1])**2)


def getFK(theta):
	"2-d robot specific FK algo"
	armLen = [0.3, 0.2, 0.1]
	x = (armLen[0] * math.cos(theta[0])) \
		+ (armLen[1] * math.cos(theta[0] + theta[1])) \
		+ (armLen[2] * math.cos(theta[0] + theta[1] + theta[2]))
	y = (armLen[0] * math.sin(theta[0])) \
		+ (armLen[1] * math.sin(theta[0] + theta[1])) \
		+ (armLen[2] * math.sin(theta[0] + theta[1] + theta[2]))
	e = [x, y]
	return e

def getJ(theta, dTheta):
	"compute jacobian given current angles and desired change"
	e = getFK(theta)
	jac = np.zeros(shape=(len(e), len(theta)))
	for i in range(len(e)):
		for j in range(len(theta)):
			thetaNew = theta
			# make a small change in j-th variable
			thetaNew[j] = thetaNew[j] + dTheta
			# recompute position give that
			eNew = getFK(thetaNew)
			# find the change 
			de = np.asmatrix(eNew) - np.asmatrix(e)
			jac[i, j] = de[0, i]/dTheta
	return jac

def getNextPointDelta(e, g, step):
	"compute the next point along the path"
	# assumes straight line between e and g
	m = np.asmatrix(g) - np.asmatrix(e)
	m = m / np.linalg.norm(m)
	return m * step

def rangeCheck(a):
	"limit the angle to 0 - 2pi"
	twoPi = 2 * math.pi
	if (a < 0):
		a += twoPi
	if (a > twoPi):
		a -= twoPi
	return a


# 3-DoF
theta = [0.0, 0.0, 0.0]
# goal position
g = [0.0, 0.15]
# current position
e = getFK(theta)
# target error 1% of arm length
err = .006
# delta theta
thetaStep = .01
# path step size - half of error
step = err / 2

# iterate until e is close enough to g
while (getDist(e, g) > err):
	J = getJ(theta, thetaStep)
	Jp = np.linalg.pinv(J)
	dE = np.transpose(getNextPointDelta(e, g, step))
	dTheta = Jp * dE
	theta = np.squeeze(np.asarray(theta + np.transpose(dTheta)))
	e = getFK(theta)

print "Final Angles: ", map(rangeCheck, theta)
print "Final Pos: ", e
