#!/usr/bin/env python
# Andrew Blanford
# IPC definitions and constants

from ctypes import Structure,c_uint16,c_double,c_ubyte,c_uint32,c_int16

EXAMPLE_CHAN_1 = 'example-chan-1'
EXAMPLE_CHAN_2 = 'example-chan-2'
EXAMPLE_CHAN_3 = 'example-chan-3'

class E_VALUE(Structure):
   _pack_ = 1
   _fields_ = [("value", c_double*1),
               ("time", c_double*1)]

class E_SERVO(Structure):
   _pack_ = 1
   _fields_ = [("command", c_double*2)]
