#!/usr/bin/evn python
# Andrew Blanford
# program to receive ipc commands for servo motor

import servo
import ipc
import ach
import sys
import time
import math
from ctypes import *
import socket

YAW_SERVO = 3
PITCH_SERVO = 2

r = ach.Channel(ipc.EXAMPLE_CHAN_1)

ref = ipc.E_SERVO()

while True:
   r.get(ref, wait=True, last=True)
   print "Got command: ", ref.command[0], ref.command[1]
   servo.setPositionRadians(YAW_SERVO, math.radians(ref.command[0]))
   servo.setPositionRadians(PITCH_SERVO, math.radians(ref.command[1]))



