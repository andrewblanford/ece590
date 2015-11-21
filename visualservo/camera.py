import ach
import sys
import time
from ctypes import *
import socket
import cv2.cv as cv
import cv2
import numpy as np

capture = cv2.VideoCapture(0)
cv.NamedWindow("test", cv.CV_WINDOW_AUTOSIZE)
frame = capture.read()

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
cv2.imshow("test", hsv)
