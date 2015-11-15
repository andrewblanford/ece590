#!/usr/bin/env python
# Andrew Blanford
# Process 2
# triggered by proc 1
# input: value from 1
# output: value multiplied by 2.5 
# input channel: output of proc 1
# output channel: 'example-chan-2'

import ipc
import ach
import sys
import time
from ctypes import *
import socket

value1 = ipc.E_VALUE()
value2 = ipc.E_VALUE()

v1 = ach.Channel(ipc.EXAMPLE_CHAN_1)
v2 = ach.Channel(ipc.EXAMPLE_CHAN_2)


while True:
   v1.get(value1, wait=True, last=True)
   value2.value[0] = value1.value[0] * 2.5
   value2.time[0] = time.time()
   v2.put(value2)
   
