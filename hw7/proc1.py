#!/usr/bin/env python
# Andrew Blanford
# Process 1
# runs at 1 hz
# input: none
# output: value of -1 and 1 on alternating cycles 
# input channel: none
# output channel: 'example-chan-1'

import ipc
import ach
import sys
import time
from ctypes import *
import socket

value = ipc.E_VALUE()

v = ach.Channel(ipc.EXAMPLE_CHAN_1)
v.flush()

i = -1

while True:
   t1 = time.time();
   value.value[0] = i
   value.time[0] = t1
   v.put(value)
   i = i * -1
   t2 = time.time()
   time.sleep(max((1.0 - (t2 - t1)), 0))
   
