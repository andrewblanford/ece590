#!/usr/bin/env python
# Andrew Blanford
# IPC definitions and constants

from ctypes import Structure,c_uint16,c_double,c_ubyte,c_uint32,c_int16

ROBOT_PT_DRIVE_CHAN='robot-pt-drive'
ROBOT_TIME_CHAN='robot-time'
ROBOT_VID_CHAN='robot-vid-chan'

# [0] pan angle
# [1] tilt angle
class PT_REF(Structure):
   _pack_ = 1
   _fields_ = [("ref", c_double*2)]

class PT_TIME(Structure):
    _pack_ = 1
    _fields_ = [("sim",    c_double*1)]
