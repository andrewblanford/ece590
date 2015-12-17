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
import numpy as np

def integralLimit(i):
   MAX = 1.0
   MIN = -1.0
   result = i
   if (i > MAX):
      result = MAX
   if (i < MIN):
      result = MIN
   return result

tgt = pt_ach.PT_REF()
cmd = pt_ach.PT_REF()
tim = pt_ach.PT_TIME()
cfg = pt_ach.PT_USER_CONFIG()

ref_in = ach.Channel(pt_ach.TARGET_POSITION_CHAN)
ref_out = ach.Channel(pt_ach.COMMAND_CHAN)
ref_out.flush()
t = ach.Channel(pt_ach.ROBOT_TIME_CHAN)
c = ach.Channel(pt_ach.USER_CONFIG_CHAN)

tLast = 0
xErrLast = 0
yErrLast = 0
xIntegral = 0.0
yIntegral = 0.0

while True:
   # wait for new target position
   [status, framesize] = ref_in.get(tgt, wait=True, last=True)
   if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
       pass
   else:
       raise ach.AchException( ref_in.result_string(status) )

   [status, framesize] = t.get(tim, wait=False, last=True)
   if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
       pass
   else:
       raise ach.AchException( t.result_string(status) )

   [status, framesize] = c.get(cfg, wait=False, last=True)
   if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
       pass
   else:
       raise ach.AchException( c.result_string(status) )

   # Def:
   # tgt.ref[0] = location x
   # tgt.ref[1] = location y
   # tim.sim[0] = Sim Time
   # cmd.ref[0] = theta x
   # cmd.ref[1] = theta y
   kp = cfg.pid[0]
   ki = cfg.pid[1]
   kd = cfg.pid[2]

   tNow = tim.sim[0]
   dt = tNow - tLast 
 
   # get current x and y
   xLoc = tgt.ref[0]
   yLoc = tgt.ref[1]

   # get desired x and y
   xDes = cfg.des[0]
   yDes = cfg.des[1]

   # calculate error
   xErr = xDes - xLoc
   yErr = yDes - yLoc
   print 'err', xErr, 'last', xErrLast

   # accumlate error
   xIntegral += xErr * dt
   yIntegral += yErr * dt
   xIntegral = integralLimit(xIntegral)
   yIntegral = integralLimit(yIntegral)
   print 'xint', xIntegral

   print 'dt', dt
   # if dt large, reset 
   if dt > .5:
      xIntegral = 0.0
      yIntegral = 0.0
      xErrLast = 0.0
      yErrLast = 0.0

   # perform pid operation
   xCmd = (kp * xErr) + (ki * xIntegral) + (kd * ((xErr - xErrLast) / dt))
   yCmd = (kp * yErr) + (ki * yIntegral) + (kd * ((yErr - yErrLast) / dt))

   # save current error and time
   xErrLast = xErr
   yErrLast = yErr
   tLast = tNow

   # set commands
   cmd.ref[0] = xCmd
   cmd.ref[1] = yCmd
   print 'cmd', cmd.ref[0], cmd.ref[1]
   ref_out.put(cmd);
