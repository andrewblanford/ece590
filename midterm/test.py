#!/usr/bin/env python


import time
import math
def filterTargetPos(target, elapsed, freq):
	return (target / 2) * (math.cos(2 * math.pi * freq * elapsed - math.pi) + 1)

targetx = math.asin(88.4/600.0)

targetz = math.acos(.5 * 400 / 300)

targetx2 = math.asin(88.4 / 400)
print "target theta: ", targetx, ", ", targetx2, (targetx2 - targetx)

TIME_STEP = .05

thetaAR = 0.0
elapsed = 0
freq = 20
while (elapsed < 10):
	# thetaAR = target * math.cos(2 * math.pi * freq * (elapsed - math.pi)) + target
	thetaAR = filterTargetPos(targetx, elapsed, freq)
	print elapsed, "\t", thetaAR
	elapsed += TIME_STEP 
	#time.sleep(TIME_STEP)
