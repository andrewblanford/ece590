#!/usr/bin/env python
# Andrew Blanford
# Process 4
# triggered by proc 3
# input: value from 1, 2, 3
# output: csv file
# input channel: output of proc 1, 2, 3
# output channel: none

import ipc
import ach
import sys
import time
from ctypes import *
import socket
import csv



value1 = ipc.E_VALUE()
value2 = ipc.E_VALUE()
value3 = ipc.E_VALUE()

v1 = ach.Channel(ipc.EXAMPLE_CHAN_1)
v2 = ach.Channel(ipc.EXAMPLE_CHAN_2)
v3 = ach.Channel(ipc.EXAMPLE_CHAN_3)

# open a file
csvfile = open('result.csv', 'w')
fieldnames = ['time', 'proc1', 'proc2', 'proc3']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()

# loop 8 seconds based on proc3 @50Hz
i = 0
while i < 400:
   # trigger on 3
   v3.get(value3, wait=True, last=True)
   # grab the other 2 values 
   v1.get(value1, wait=False, last=True)
   v2.get(value2, wait=False, last=True)
   # put in file
   writer.writerow({'time': value3.time[0],
                    'proc1': value1.value[0],
                    'proc2': value2.value[0],
                    'proc3': value3.value[0]})
   i += 1

csvfile.close()
sys.exit()

   
