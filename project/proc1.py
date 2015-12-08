#!/usr/bin/env python
# Andrew Blanford
# Process 1
# runs at 1 hz
# input: none
# output: value of -1 and 1 on alternating cycles 
# input channel: none
# output channel: 'example-chan-1'

import pt_ach
import ach
import sys
import time
from ctypes import *
import socket
import math

pt_ref = pt_ach.PT_REF()
pt_time = pt_ach.PT_TIME()

ref = ach.Channel(pt_ach.ROBOT_PT_DRIVE_CHAN)
ref.flush()
t = ach.Channel(pt_ach.ROBOT_TIME_CHAN)

TIME_STEP = .05
amp = 90
freq = .5
elapsed = 0;
while (True):
   t.get(pt_time, wait=True, last=True)
   before = pt_time.sim[0]

   pos = amp * math.sin(2 * math.pi * freq * elapsed)
   print "Pos (", elapsed, "): ", pos
   pt_ref.ref[1] = math.radians(pos)
   ref.put(pt_ref)


   t.get(pt_time, wait=True, last=True)
   after = pt_time.sim[0]

   time.sleep(TIME_STEP - max((after-before), 0))
   elapsed += TIME_STEP
