#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */
# /*
# Copyright (c) 2013, Daniel M. Lofaro
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



import hubo_ach as ha
import ach
import sys
import time
import math
from ctypes import *

def filterTargetPos(target, elapsed, freq):
	return (target / 2) * (math.cos(2 * math.pi * freq * elapsed - math.pi) + 1)

# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)
#s.flush()
#r.flush()

# 20 Hz update rate
TIME_STEP = .05

# feed-forward will now be refered to as "state"
state = ha.HUBO_STATE()

# feed-back will now be refered to as "ref"
ref = ha.HUBO_REF()

# Get the current feed-forward (state) 
[statuss, framesizes] = s.get(state, wait=False, last=False)

freq = .2
elapsed = 0

# use this function to choose delay option
def delay(duration):
	return simDelay(duration)

# real time delay
def realDelay(duration):
	time.sleep(duration)
	return

# use sim time instead of sleep 
def simDelay(duration):
	s.get(state, wait=False, last=False)
	targetTime = state.time + duration
	while (state.time < targetTime):
		s.get(state, wait=True, last=False)
	return

# move arms out of the way
ref.ref[ha.RSR] = -.1
ref.ref[ha.LSR] = .1
r.put(ref)

# 1. Sway over right foot
def phase1():
	print "Phase 1"
	# asin(x / 2l)
	targetAR = math.asin(-88.4/600.0)
	thetaAR = state.joint[ha.RAR].pos
	elapsed = 0
	while(thetaAR > targetAR):
		s.get(state, wait=False, last=False)
		t1 = state.time
		thetaAR = filterTargetPos(targetAR, elapsed, freq)
		ref.ref[ha.RHR] = -thetaAR
		ref.ref[ha.RAR] = thetaAR
		ref.ref[ha.LHR] = -thetaAR
		ref.ref[ha.LAR] = thetaAR
		r.put(ref)
		elapsed += TIME_STEP
		s.get(state, wait=False, last=False)
		t2 = state.time
		delay(TIME_STEP - (t2 - t1))

# 2. raise left leg more than .2m
def phase2():
	print "Phase 2"
	# acos(.5 z / l)
	targetAP = math.acos(.5 * 300 / 300)
	thetaAP = state.joint[ha.LAP].pos
	elapsed = 0
	while (thetaAP < targetAP):
		s.get(state, wait=False, last=False)
		t1 = state.time
		thetaAP = filterTargetPos(targetAP, elapsed, freq)
		# print elapsed, "\t", thetaAP
		ref.ref[ha.LHP] = -thetaAP
		ref.ref[ha.LAP] = -thetaAP
		ref.ref[ha.LKN] = 2 * thetaAP
		r.put(ref)
		elapsed += TIME_STEP
		s.get(state, wait=False, last=False)
		t2 = state.time
		delay(TIME_STEP - (t2 - t1))
	
# 3 bend right knee .2m at .2Hz 2 times
def phase3():
	print "Phase 3"
	targetAP = math.acos(.5 * 400 / 300)
	thetaAP = state.joint[ha.RAP].pos
	# change in x position of CoM during bend
	baseAR = math.asin(-88.4/600)
	deltaAR = math.asin(-88.4 / 400) - baseAR
	elapsed = 0
	#print "AP start: ", thetaAP
	#print "AP target: ", targetAP
	while (elapsed < 10):
		s.get(state, wait=False, last=False)
		t1 = state.time
		thetaAP = filterTargetPos(targetAP, elapsed, freq)
		thetaAR = filterTargetPos(deltaAR, elapsed, freq) + baseAR
		# print elapsed, "\t", thetaAR
		# shift z
		ref.ref[ha.RHP] = -thetaAP
		ref.ref[ha.RAP] = -thetaAP
		ref.ref[ha.RKN] = 2 * thetaAP
		# shift x
		ref.ref[ha.RHR] = -thetaAR
		ref.ref[ha.RAR] = thetaAR
		ref.ref[ha.LHR] = -thetaAR
		ref.ref[ha.LAR] = thetaAR
		r.put(ref)
		elapsed += TIME_STEP
		s.get(state, wait=False, last=False)
		t2 = state.time
		delay(TIME_STEP - (t2 - t1))

# 4. Lower left leg back to double support
# return angle to 0
def phase4(): 
	print "Phase 4"
	baseAP = math.acos(.5 * 300 / 300)
	thetaAP = baseAP
	elapsed = 0
	while (thetaAP > 0):
		s.get(state, wait=False, last=False)
		t1 = state.time
		thetaAP = baseAP - filterTargetPos(baseAP, elapsed, freq)
		#print elapsed, "\t", thetaAP
		ref.ref[ha.LHP] = -thetaAP
		ref.ref[ha.LAP] = -thetaAP
		ref.ref[ha.LKN] = 2 * thetaAP
		r.put(ref)
		elapsed += TIME_STEP
		s.get(state, wait=False, last=False)
		t2 = state.time
		delay(TIME_STEP - (t2 - t1))
	
# 5. sway left now
def phase5():
	print "Phase 5"
	targetAR = math.asin(88.4/600.0)
	baseAR = math.asin(-88.4/600.0)
	thetaAR = baseAR
	deltaAR = targetAR - baseAR
	elapsed = 0
	while (thetaAR < targetAR):
		s.get(state, wait=False, last=False)
		t1 = state.time
		thetaAR = baseAR + filterTargetPos(deltaAR, elapsed, freq)
		ref.ref[ha.RHR] = -thetaAR
		ref.ref[ha.RAR] = thetaAR
		ref.ref[ha.LHR] = -thetaAR
		ref.ref[ha.LAR] = thetaAR
		r.put(ref)
		elapsed += TIME_STEP
		s.get(state, wait=False, last=False)
		t2 = state.time
		delay(TIME_STEP - (t2 - t1))

# 6. move into ballet stance
# part 1 raise leg off ground
def phase6a(): 
	print "phase 6a - raise right leg"
	# acos(.5 z / l)
	targetAP = math.acos(.5 * 500 / 300)
	thetaAP = state.joint[ha.RAP].pos
	elapsed = 0
	while (thetaAP < targetAP):
		s.get(state, wait=False, last=False)
		t1 = state.time
		thetaAP = filterTargetPos(targetAP, elapsed, freq)
		# print elapsed, "\t", thetaAP
		ref.ref[ha.RHP] = -thetaAP
		ref.ref[ha.RAP] = -thetaAP
		ref.ref[ha.RKN] = 2 * thetaAP
		r.put(ref)
		elapsed += TIME_STEP
		s.get(state, wait=False, last=False)
		t2 = state.time
		delay(TIME_STEP - (t2 - t1))

# 6b. bend forward 60 degrees
# 60 is a guess at "almost" parallel while still leaving room for 
# knee bend movement at the hip
def phase6b():
	print "Phase 6b - bend forward on left leg"
	targetHP = math.radians(60)
	thetaHP = 0
	elapsed = 0
	while (thetaHP < targetHP):
		s.get(state, wait=False, last=False)
		t1 = state.time
		thetaHP = filterTargetPos(targetHP, elapsed, freq)
		ref.ref[ha.LHP] = -thetaHP
		r.put(ref)
		elapsed += TIME_STEP
		s.get(state, wait=False, last=False)
		t2 = state.time
		delay(TIME_STEP - (t2 - t1))

# bend left knee .1m at .2Hz 2 times
def phase7():
	print "Phase 7 - left knee bends"
	# acos(.5 z / l)
	targetAP = math.acos(.5 * 500 / 300)
	thetaAP = state.joint[ha.LAP].pos
	# change in x position of CoM during bend
	baseAR = math.asin(88.4/600)
	deltaAR = math.asin(88.4 / 400) - baseAR
	baseHP = state.joint[ha.LHP].pos
	elapsed = 0
	while (elapsed < 10):
		s.get(state, wait=False, last=False)
		t1 = state.time
		thetaAP = filterTargetPos(targetAP, elapsed, freq)
		thetaAR = filterTargetPos(deltaAR, elapsed, freq) + baseAR
		# print elapsed, "\t", thetaAR
		# shift z
		ref.ref[ha.LHP] = -thetaAP + baseHP
		ref.ref[ha.LAP] = -thetaAP
		ref.ref[ha.LKN] = 2 * thetaAP
		# shift x
		ref.ref[ha.RHR] = -thetaAR
		ref.ref[ha.RAR] = thetaAR
		ref.ref[ha.LHR] = -thetaAR
		ref.ref[ha.LAR] = thetaAR
		r.put(ref)
		elapsed += TIME_STEP
		s.get(state, wait=False, last=False)
		t2 = state.time
		delay(TIME_STEP - (t2 - t1))

# 8a. return to vertical hip bend
def phase8a():
	print "Phase 8a - stand up"
	targetHP = 0.0
	baseHP = math.radians(60)
	thetaHP = baseHP
	elapsed = 0
	while (thetaHP > targetHP):
		s.get(state, wait=False, last=False)
		t1 = state.time
		thetaHP = baseHP - filterTargetPos(baseHP, elapsed, freq)
		ref.ref[ha.LHP] = -thetaHP
		r.put(ref)
		elapsed += TIME_STEP
		s.get(state, wait=False, last=False)
		t2 = state.time
		delay(TIME_STEP - (t2 - t1))

# 8b. lower right leg back to ground
def phase8b():
	print "Phase 8b - lower right leg"
	baseAP = math.acos(.5 * 500 / 300)
	thetaAP = baseAP
	elapsed = 0
	while (thetaAP > 0):
		s.get(state, wait=False, last=False)
		t1 = state.time
		thetaAP = baseAP - filterTargetPos(baseAP, elapsed, freq)
		#print elapsed, "\t", thetaAP
		ref.ref[ha.RHP] = -thetaAP
		ref.ref[ha.RAP] = -thetaAP
		ref.ref[ha.RKN] = 2 * thetaAP
		r.put(ref)
		elapsed += TIME_STEP
		s.get(state, wait=False, last=False)
		t2 = state.time
		delay(TIME_STEP - (t2 - t1))

# 9 sway back to center
def phase9():
	print "Phase 9"
	targetAR = 0.0
	baseAR = state.joint[ha.RAR].pos
	thetaAR = baseAR
	deltaAR = targetAR - baseAR
	elapsed = 0
	while(thetaAR > targetAR):
		s.get(state, wait=False, last=False)
		t1 = state.time
		thetaAR = baseAR + filterTargetPos(deltaAR, elapsed, freq)
		ref.ref[ha.RHR] = -thetaAR
		ref.ref[ha.RAR] = thetaAR
		ref.ref[ha.LHR] = -thetaAR
		ref.ref[ha.LAR] = thetaAR
		r.put(ref)
		elapsed += TIME_STEP
		s.get(state, wait=False, last=False)
		t2 = state.time
		delay(TIME_STEP - (t2 - t1))

# sway right
phase1()
# lift left leg
phase2()
# do right knee bends
phase3()
# lower left leg
phase4()
# sway left
phase5()
# assume ballet stance
phase6a()
phase6b()
# do left knee bends
phase7()
# return to standing
phase8a()
phase8b()
# sway center
phase9()


# Close the connection to the channels
r.close()
s.close()


