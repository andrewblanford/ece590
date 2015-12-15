#!/usr/bin/env python
# Andrew Blanford
# Real Camera Controller

import pt_ach
import ach
import sys
import time
from ctypes import *
import socket
import math
import servo

PAN_SERVO = 3
TILT_SERVO = 2

ref = pt_ach.PT_REF()
cfg = pt_ach.PT_USER_CONFIG()

r = ach.Channel(pt_ach.ROBOT_PT_DRIVE_CHAN)
c = ach.Channel(pt_ach.USER_CONFIG_CHAN)

while True:
   r.get(ref, wait=True, last=True)
   c.get(cfg, wait=False, last=True)

   if cfg.flag[0] == 1:
      servo.setPositionRadians(PAN_SERVO, ref.ref[0])
      servo.setPositionRadians(TILT_SERVO, ref.ref[1])
