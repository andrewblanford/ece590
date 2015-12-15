
import pt_ik as ik
import pt_fk as fk
import math

thetaJS = [0, 0]
print fk.getFK(thetaJS)

# start position
goal =  [0.0, 0.0, .124, 0, 0, 0]

thetaJS = ik.getIK(goal, thetaJS)
print thetaJS

# pt unit end effector can only be in sphere
RADIUS = .0455
HEIGHT = .0785
thetaX = 0.0
thetaY = 0.0

cmd = [.1, .1]


thetaX = thetaX + cmd[0]
thetaY = thetaY + cmd[1]
# x
#goal[0] = RADIUS * math.cos(thetaX) * math.sin(thetaY)
# y
#goal[1] = RADIUS * math.sin(thetaX) * math.sin(thetaY)
# z
#goal[2] = RADIUS * math.cos(thetaY) + HEIGHT

goal[4] = thetaY
goal[5] = thetaX

print goal

   # get the new angles
thetaJS = ik.getIK(goal, thetaJS)

print thetaJS

print fk.getFK(thetaJS)

i = 0
dPan = .1
thetaJS = [0, 0]

while i < 1.5:
   print 'i: ', i
   goal = fk.getFK(thetaJS)
   print 'Goal: ', goal
   goal[4] = 0
   goal[5] += dPan
   thetaJS = ik.getIK(goal, thetaJS)   
   print 'Result: ', thetaJS
   i += dPan
