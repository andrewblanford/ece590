#!/usr/bin/env python
# Andrew Blanford
# User Config process
# output: PT_USER_CONFIG on change  
# input channel: user input

import pt_ach
import ach
import sys
import time
from ctypes import *
import socket
import math

def printMenu(config):
   print '\n**********************'
   print '1. Change PID Gain'
   print '\tKp =', config.pid[0]
   print '\tKi =', config.pid[1]
   print '\tKd =', config.pid[2]
   print '2. Change desired position'
   print '\txDes =', config.des[0]
   print '\tyDes =', config.des[1]
   print '3. Change Target Color'
   print '\tLower Range'
   print '\tR =', config.tgt[0]
   print '\tG =', config.tgt[1]
   print '\tB =', config.tgt[2]
   print '\tUpper Range'
   print '\tR =', config.tgt[3]
   print '\tG =', config.tgt[4]
   print '\tB =', config.tgt[5]
   print '4. Toggle Robot/Sim'
   if (config.flag[0]):
      print '\tUsing Robot'
   else:
      print '\tUsing Sim'
   print '**********************\n'

def changeGain(config):
   p = float(raw_input('Kp: ') or config.pid[0])
   i = float(raw_input('Ki: ') or config.pid[1])
   d = float(raw_input('Kd: ') or config.pid[2])
   config.pid[0] = p
   config.pid[1] = i
   config.pid[2] = d

def changeDes(config):
   x = float(raw_input('Normalized X position (-1.0:1.0): ') or config.des[0])
   y = float(raw_input('Normalized Y position (-1.0:1.0): ') or config.des[1])
   config.des[0] = x
   config.des[1] = y

def changeTarget(config):
   r = int(raw_input('Enter Lower Red Value   (0-255): ') or config.tgt[0])
   g = int(raw_input('Enter Lower Green Value (0-255): ') or config.tgt[1])
   b = int(raw_input('Enter Lower Blue Value  (0-255): ') or config.tgt[2])
   config.tgt[0] = r
   config.tgt[1] = g
   config.tgt[2] = b
   r = int(raw_input('Enter Upper Red Value   (0-255): ') or config.tgt[3])
   g = int(raw_input('Enter Upper Green Value (0-255): ') or config.tgt[4])
   b = int(raw_input('Enter Upper Blue Value  (0-255): ') or config.tgt[5])
   config.tgt[3] = r
   config.tgt[4] = g
   config.tgt[5] = b

pt_config = pt_ach.PT_USER_CONFIG()

c = ach.Channel(pt_ach.USER_CONFIG_CHAN)
c.flush()

# default PID constants
pt_config.pid[0] = .1
pt_config.pid[1] = 0
pt_config.pid[2] = 0

# default desired point = 0,0
pt_config.des[0] = 0
pt_config.des[1] = 0

# default target color = red
pt_config.tgt[0] = 100
pt_config.tgt[1] = 0
pt_config.tgt[2] = 0
pt_config.tgt[3] = 255
pt_config.tgt[4] = 50
pt_config.tgt[5] = 50

# default flat = sim
pt_config.flag[0] = 0

c.put(pt_config)

while (True):
   printMenu(pt_config)
   i = int(raw_input('menu option: '))
   if i == 1:
      changeGain(pt_config)
   elif i == 2:
      changeDes(pt_config)
   elif i == 3:
      changeTarget(pt_config)
   elif i == 4:
      if (pt_config.flag[0]):
         pt_config.flag[0] = 0
      else:
         pt_config.flag[0] = 1
   else:
      print 'Input', i, 'not understood'
   
   # look at option and update config

   c.put(pt_config)
