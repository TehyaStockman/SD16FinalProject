import numpy as np
import argparse
import cv2


# apparently this is needed for the trackbars
def nothing(x):
	pass


# define the range of colors we want to track~!!!!
colorLow = (29,86,6)
colorHigh = (64,255,255)

# referencing the webcam for our video camera
camera = cv2.VideoCapture(1)
cv2.namedWindow('image')
cv2.createTrackbar('LowR','image',0,255,nothing)
cv2.createTrackbar('LowG','image',0,255,nothing)
cv2.createTrackbar('LowB','image',0,255,nothing)
cv2.createTrackbar('R','image',0,255,nothing)
cv2.createTrackbar('G','image',0,255,nothing)
cv2.createTrackbar('B','image',0,255,nothing)

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
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	if len(cnts) > 0:
		# finds the biggest contour and then finds the smallest circle 
		# possible to enclose it
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)

		# finds the center of the circle using moments
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# ensures the thing it's detecting is not too small and a mistake
		if radius > 1:
			# draws a circle around our tracked thing. This is mostly for testing to see how 
			# this ends up working
			cv2.circle(frame, (int(x),int(y)), int(radius),(0,0,0),2)

	# displays the screen 
	cv2.imshow('Frame',frame)
	# if we press q key, everything quits
	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		break
	if key == ord('w'):
		cv2.destroyWindow('image')
	# trakcs the trackbar position and sets colors accordingly
	if key == ord('c'):
		colorLow = (cv2.getTrackbarPos('LowB','image'),cv2.getTrackbarPos('LowG','image'),cv2.getTrackbarPos('LowR','image'))
		colorHigh = (cv2.getTrackbarPos('B','image'),cv2.getTrackbarPos('G','image'),cv2.getTrackbarPos('R','image'))

camera.release()
cv2.destroyAllWindows()