#!/usr/bin/env python
# Andrew Blanford
# Process 3
# runs at 50 hz
# input: value from proc 2 
# output:r = (z^-1 * (L-1.0) + c) / L   
#  and     t = time (in seconds with better then millisecond resolution)
# z^-1 is previous r
# c is zero order hold of proc 2
# input channel: output of 2
# output channel: 'example-chan-3'

import ipc
import ach
import sys
import time
from ctypes import *
import socket

L = 40

value2 = ipc.E_VALUE()
value3 = ipc.E_VALUE()

v2 = ach.Channel(ipc.EXAMPLE_CHAN_2)
v3 = ach.Channel(ipc.EXAMPLE_CHAN_3)
v3.flush()

rLast = 0

while True:
   t1 = time.time();
   v2.get(value2, wait=False, last=True)
   # zero order hold is continuation of current value for sample period
   c = value2.value[0]
   r = (rLast * (L - 1.0) + c) / L
   rLast = r
   value3.value[0] = r
   value3.time[0] = t1
   v3.put(value3)
   t2 = time.time()
   time.sleep(max((0.02 - (t2 - t1)), 0))
   
