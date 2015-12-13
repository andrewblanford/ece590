#!/usr/bin/env python
# Andrew Blanford
# IPC definitions and constants

from ctypes import Structure,c_uint16,c_double,c_ubyte,c_uint32,c_int16

ROBOT_PT_DRIVE_CHAN='robot-pt-drive'
ROBOT_TIME_CHAN='robot-time'
ROBOT_VID_CHAN='robot-vid-chan'
USER_CONFIG_CHAN='user-config-chan'
TARGET_POSITION_CHAN='target-position-chan'
COMMAND_CHAN='command-chan'

# [0] pan angle
# [1] tilt angle
class PT_REF(Structure):
   _pack_ = 1
   _fields_ = [("ref", c_double*2)]

class PT_TIME(Structure):
    _pack_ = 1
    _fields_ = [("sim",    c_double*1)]

# pid [kp, ki, kd]
# des [xDes, yDes]
# tgt lower [R, G, B] upper [R, G, B]
# flag 1 = robot, 0 = sim
class PT_USER_CONFIG(Structure):
   _pack_ = 1
   _fields_ = [("pid", c_double*3),
               ("des", c_double*2),
               ("tgt", c_ubyte*6),
               ("flag", c_ubyte*1)]


