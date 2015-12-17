#!/usr/bin/evn python 
# Andrew Blanford
# ECE 590

import pt_fk as fk
import pt_ik as ik
import pt_ach
import ach

# setup ach
ref = pt_ach.PT_REF()
cmd = pt_ach.PT_REF()
state = pt_ach.PT_REF()
ref_out = ach.Channel(pt_ach.ROBOT_PT_DRIVE_CHAN)
ref_out.flush()
ref_in = ach.Channel(pt_ach.COMMAND_CHAN)
s = ach.Channel(pt_ach.ROBOT_STATE_CHAN)

# joint space angles
#[pan, tilt]
thetaJS = [0.0, 0.0]

# start position
# [x, y, z, theta_x, theta_y, theta_z]
goal =  fk.getFK(thetaJS)

# pt unit end effector can only be in sphere
RADIUS = .0455
HEIGHT = .0785
thetaX = 0.0
thetaY = 0.0

# zero the controls before we start
ref.ref[0] = thetaJS[0]
ref.ref[1] = thetaJS[1]
ref_out.put(ref)

while True:
   ref_in.get(cmd, wait=True, last=True)

   dPan = cmd.ref[0]
   dTilt = cmd.ref[1]

   # get the current goal position using current state
   s.get(state, wait=False, last=True)
   thetaJS[0] = state.ref[0]
   thetaJS[1] = state.ref[1]
   print 'State:', thetaJS
   goal = fk.getFK(thetaJS)

   # adjust the goal position theta_y and theta_z orientations
   goal[4] += dTilt
   goal[5] += dPan

   # find the new joint space thetas
   thetaJS = ik.getIK(goal, thetaJS)   
   print 'Theta: ', thetaJS

   # send the values 
   ref.ref[0] = thetaJS[0]
   ref.ref[1] = thetaJS[1]
   ref_out.put(ref)


