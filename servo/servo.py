#!/usr/bin/evn python
# Andrew Blanford
# Program to communicate with the dynamixel AX-12A servo
# some of the voodoo below for manipulating bytes in packet 
# came from here: https://www.cs.duke.edu/~mac/dynamixel.py

import sys
import serial
import time
import math

WRITE_CMD 	= [0x03]
READ_CMD 	= [0x04]

portName = "/dev/ttyUSB0"

serialPort = serial.Serial(portName, 1000000)
serialPort.open()

def computeChecksum(data):
	"compute checksum of data as ~(id + len + data) & 0xFF"
	# only want the lower byte so truncate
	return (~sum(data)) & 0xFF

def sendPacket(id, data):
	"send a packet of data to id"
	# assemble the payload
	# id, size of data (plus id byte)
	payload = [id, len(data) + 1] + data
	# add header and checksum to payload
	# convert everything chr (bytes) and send
	msg = "".join(map(chr, [0xFF, 0xFF] + payload + [computeChecksum(payload)]))
	serialPort.write(msg)
	serialPort.flushOutput()
	# done sending
	return

def setPosition(id, position):
	"set the servo position for servo id, position in encoder ticks"
	# TODO: check position for valid range
	# msg = write register command
	# + position address = 0x1E
	# + position LSB
	# + position MSB
	msg = WRITE_CMD + [0x1E, position & 0xFF, position >> 8]
	sendPacket(id, msg)
	return

def setPositionRadians(id, position):
	"set the position using radians"
	return setPosition(id, rad2tick(position))

def rad2tick(rads):
	"convert radians to servo encoder ticks, where 0 is the center position"
	# add 150 to center the angle around the servo center point
	r = math.radians(150.0) + rads
	# 0x3FF = 300 degrees
	# floor and convert to int
	return int(math.floor(r * 0x3FF / math.radians(300.0)))

def tick2rad(ticks):
	"convert servo encoder ticks to radians, where 0 is the center position"
	# convert to radians 0x3FF = 300 degrees
	r = ticks * (math.radians(300.0) / 0x3FF)
	# subtract 150 degrees to get back to original angle
	return r - math.radians(150.0)

TIME_STEP = .01
amp = 90
freq = .5
elapsed = 0;
while (True):
	pos = amp * math.sin(2 * math.pi * freq * elapsed)
	print "Pos (", elapsed, "): ", pos
	setPositionRadians(13, math.radians(pos))
	elapsed += TIME_STEP
	time.sleep(TIME_STEP)
