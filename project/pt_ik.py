#!/usr/bin/evn python 
# Andrew Blanford
# ECE 590

import sys
import math
import numpy as np
import pt_fk as fk
import pt_ach
import ach


def getDist(e, g):
	"euclidian distance between two points"
	return math.sqrt((e[0] - g[0])**2 + (e[1] - g[1])**2)


def getFK(theta):
	return fk.getFK(theta)

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
	while (a < 0):
		a += twoPi
	while (a > twoPi):
		a -= twoPi
	return a

# g = goal
# theta = current angles
# return new angles
def getIK(g, theta):
   # current position 
   e = getFK(theta)
   # target error 1% of arm length
   err = .01
   # delta theta
   thetaStep = .01
   # path step size - half of error
   step = err / 2

   iterations = 0

   # iterate until e is close enough to g
   while (getDist(e, g) > err):
      J = getJ(theta, thetaStep)
      Jp = np.linalg.pinv(J)
      dE = np.transpose(getNextPointDelta(e, g, step))
      dTheta = Jp * dE
      theta = np.squeeze(np.asarray(theta + np.transpose(dTheta)))
      e = getFK(theta)
      iterations += 1

   print iterations
   return map(rangeCheck, theta)


# setup ach
ref = pt_ach.PT_REF()
cmd = pt_ach.PT_REF()
#ref_out = ach.Channel(pt_ach.ROBOT_PT_DRIVE_CHAN)
#ref.flush()
#ref_in = ach.Channel(pt_ach.COMMAND_CHAN)

# zero the controls before we start
ref.ref[0] = 0
ref.ref[1] = 0
#ref_out.put(ref)

# joint space angles
#[pan, tilt, end]
thetaJS = [0.0, 0.0, 0.0]

# start position
goal =  [0.0, 0.0, .124]

# pt unit end effector can only be in sphere
RADIUS = .0455
HEIGHT = .0785
thetaX = 0.0
thetaY = 0.0

#while True:
#   ref_in.get(cmd, wait=True, last=True)

   # adjust the goal position
#   thetaX = thetaX + cmd.ref[0]
#   thetaY = thetaY + cmd.ref[1]
   # x
#   goal[0] = RADIUS * math.cos(thetaX) * math.sin(thetaY)
   # y
#   goal[1] = RADIUS * math.sin(thetaX) * math.sin(thetaY)
   # z
#   goal[2] = RADIUS * math.cos(thetaY) + HEIGHT

   # get the new angles
#   thetaJS = getIK(goal, thetaJS)

#   print thetaJS

#   ref.ref[0] = thetaJS[0]
#   ref.ref[1] = thetaJS[1]
#   ref_out.put(ref)

