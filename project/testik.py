
import pt_ik as ik
import math

thetaJS = [0.0, 0.0]

# start position
goal =  [0.0, 0.0, .124]

thetaJS = ik.getIK(goal, thetaJS)
print thetaJS

# pt unit end effector can only be in sphere
RADIUS = .0455
HEIGHT = .0785
thetaX = 0.0
thetaY = 0.0

cmd = [1.57, 1.0]


thetaX = thetaX + cmd[0]
thetaY = thetaY + cmd[1]
# x
goal[0] = RADIUS * math.cos(thetaX) * math.sin(thetaY)
# y
goal[1] = RADIUS * math.sin(thetaX) * math.sin(thetaY)
# z
goal[2] = RADIUS * math.cos(thetaY) + HEIGHT

print goal

   # get the new angles
thetaJS = ik.getIK(goal, thetaJS)

print thetaJS
