
#import necessary libraries
import math #includes all the maths
import serial #serial communication extension
import os #allows for os manipulation (read/write)
import sys #system specific variables used by the interpreter
import time #enter sandman
import numpy as np

#start time variable
tNot = time.time()
dT = 0.1 #Time step between filter steps

#The state tranisition matrix, three standard kinematics equations
A = np.array([[1, dT, 0.5 * (dT**2)], #position
              [0, 1, dT], #velocity
              [0, 0, 1]]) #acceleration

#Model that predicts what changes occur to the bot based on commands
#This will most liekly stay zero unless we have odometers that are near 98% accurate
Bk = np.array([[0,0,0],
			  [0,0,0],
			  [0,0,0]])

#Model that represents the sensors, hard to determine. May or may not change
H = np.array([[1,0,0],
              [0,0,0],
              [0,0,1]])

#Initial State
x = np.array([[0.0,0.0,0.0]]).T

#Initial Uncertainty
P = np.array([[100.0,0,0],
              [0,10.0,0],
              [0,0,1.0]])


#kalman filter to correct x position (lat). measuremnts should be in [m]
def kalmanX ():
	#current time variable
	tk = time.time() - tNot

	#read in GPS values
	currLat = lat
	previousLat = lat_1

	#read in current accelerometer values
	ax = accX

	#convert lat into meters

	#1. Project the state ahead
	Yk= np.matmul(A,Yk_1)+Bk

	return Yk
	Yk_1 = Yk
	lat_1 = lat
