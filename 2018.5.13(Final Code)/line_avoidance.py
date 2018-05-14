## Owen Graig & Ethan Daniels | IGV 2017-2018 | Line Detection and Processing

### IMPORTS ###
import cv2
import numpy as np
import serial
import time
from sabertooth2x60 import Sabertooth #Motor Control

### OBJECTS ###
saber = Sabertooth()
class Lines(object):
	def getSlope(self):
		#Starts openCV with external camera
		cap = cv2.VideoCapture(0) ## MIGHT HAVE TO BE MOVED ABOUT
		_,frame =cap.read()
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		# gaussian smooth over standard deviation, reduce noise
		ret,thresh1 = cv2.threshold(gray ,200,255,cv2.THRESH_BINARY)
		#gaussian = cv2.GaussianBlur(gray, (5,5), 3)
		#hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
		edges = cv2.Canny(thresh1,100,255,apertureSize = 3)
		minLineLength = 1000
		maxLineGap = 10
		lines = cv2.HoughLinesP(edges,1,np.pi/180,40,minLineLength,maxLineGap)
                try:
                    for x in range(0, len(lines)):
                                    for x1,y1,x2,y2 in lines[x]:
                                                    cv2.line(frame,(x1,y1),(x2,y2),(255,0,0),5)
                    if x2-x1 == 0.:
                                    slope = 0 #cant divide by zero, output zero insteaad
                    else:
                                    slope = (float(y2)-float(y1))/(float(x2)-float(x1))
                    print('slope = ', slope)
                    #cv2.imshow('hough',frame) ## THIS DOESNT WORK, WHO CARES.. We dont need to see it
                    #print('x1 =',x1)
                    #print('y1 =',y1)
                    #print('x2 =',x2)
                    #print('y2 =',y2)
                    cv2.destroyAllWindows()
                    return slope

                except TypeError: #there is no line seen
                    print('No line found!')

                    cv2.destroyAllWindows()
                    return 0
	# Creates an average of lines
	def avgOUT(self):
		newSlope = 0
		for i in range(0,1):
                                time.sleep(0.25)
				newSlope = newSlope + self.getSlope()
				print('newSlope = ', newSlope)
		avgSlope = newSlope / 1
		print('Average Slope = ', avgSlope)
		return avgSlope

	# Acts based on the resultant average
	def saber_act(self):
		#saber.stop()
		#time.sleep(0.2) # Pre Processing Time
		line = self.avgOUT()
		#saber.stop()
		#time.sleep(0.4) # Post Processing Time
		# turn right
		if(line < -0.3):
			saber.turnRight()
			time.sleep(0.2)
		# turn left
		elif(line > 0.3):
			saber.turnLeft()
			time.sleep(0.2)

		# go straight
		else:
			saber.driveStraight()
			time.sleep(0.5)
