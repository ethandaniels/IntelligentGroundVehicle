
#import necessary libraries
import math #includes all the maths
import serial #serial communication extension
import os #allows for os manipulation (read/write)
import sys #system specific variables used by the interpreter
import time #enter sandman
import pykalman #imports kalman filter
#import RPi.GPIO as GPIO #initalizes the GPIO pins on PI (can only run with on PI)

### Serial Setup ###
port = "/dev/ttyUSB0" #initalizing serial read port
ser = serial.Serial()
ser.port = port
ser.close()

#declare variables for reading in serial ports
ser2 = serial.Serial('/dev/ttyACM0',115200) # Read for GPS / Serial 2
ser3 = serial.Serial('/dev/ttyACM1',115200) # Read for Compass / Serial 3

#set important serial cmmunciation fields
ser.baudrate = 19200
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.timeout = 1
ser.open()
ser.flushInput()
ser.flushOutput()

### GPIO setup ###
#GPIO.setmode(GPIO.BOARD) #Used to be BCM, Board is more consistent bc by pin

### Declare variables ###
lat1 = 41.676635		# Value from compass
lon1 = -71.266044 		# Value from compass
lat2 = 41.6768143		# INPUT DESIRED LOCATION HERE
lon2 = -71.2656901 		# INPUT DESIRED LOCATION HERE
x = 0.0					# For beta calculation
y = 0.0					# For beta calculation
ml = 192				# Value for left motor
mr = 66					# Value for right motor
beta = 0.0				# beta value for desired heading
state = 0				# Variable for state
distance = 0.0 			# Variable for distance calculation
comp = 0.0				# IGV Compass reading
R = 6372.795477598 		# Radius of Earth (km)

#would desire to have IMU through GPIO, in this case we would have multiple
#functions just to read compass and other DOFs
### Read in compass heading ###
def getCompass():

	# Read in string
	read_compass=ser3.readline()

	# Concatenate to floats
	comp = float(read_compass)

	print ("comp: ", comp)
	return comp

### Read in GPS Coordinates ###
def getGPS():

	# Read in string and split
	read_serial2=ser2.readline()
	x = read_serial2.split()

	# Concatenate to floats
	lat1 = float(x[0])
	lon1 = -1*float(x[1])

	print ("lat1: ", lat1, "lon1: ", lon1)
	return lat1, lon1

### Using IMU and GPS to correct with Kalman filter
def getKalmanCorrect(currLat, currLon, #other IMU variables):


try:
    #main solution code
    getKalmanCorrect()

    #this is placeholder until algorithm is developed
    while counter < 9000000:
        # count up to 9000000 - takes ~20s
        counter += 1
    print "Target reached: %d" % counter

except KeyboardInterrupt:
    # code that needs to run before the program
    # will exit when user presses CTRL+C
    print "\n", counter #prints value of counter

except:
    # this catches ALL other exceptions including errors.
    # When enables won't get any error messages for debugging
    # implement once code is working
    print "Other error or exception occurred!"

finally:
    GPIO.cleanup() # this ensures a clean exit
	print "GPIO is cleaned, smooth exit"
