import numpy as np
import argparse
import cv2


# define the range of colors we want to track~!!!!
colorLow = (29,86,6)
colorHigh = (64,255,255)

# referencing the webcam for our video camera
camera = cv2.VideoCapture(0)

while 1:
	# ret is boolean for successful frame read
	ret, frame = camera.read()

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask over the color green or something
	# erode and dilate clean up the border of our colorful thing
	mask = cv2.inRange(hsv, colorLow, colorHigh)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# finds the contour in the mask an initializes the storage for ball location
	cnts = cvs.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	if len(cnts) > 0:
		# finds the biggest contour and then makes a circle to 
		# fit around it

		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))