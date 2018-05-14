### IMPORTS ###
import time #sandman
import sys, traceback #for exception handeling
#from sabertooth2x60 import Sabertooth #Motor Control
from GPS_edit import GPS #Navio GPS
import math #minor in mathematics
import serial

### OBJECTS ###
gps = GPS() #gps object

### COMPASS ###
import logging
import sys
import time
from Adafruit_BNO055 import BNO055

### COMPASS SHIT ###
bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)
# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status, self_test, error = bno.get_system_status()

### VARIABLES ###
#motor 1(left)
right_crawl = chr(70)
right_slow = chr(85)
right_fast = chr(100)
right_ulta = chr(127)
right_back = chr(50)
right_back_crawl = chr(58)

#motor 2(right)
left_crawl = chr(198)
left_slow = chr(213)
left_fast = chr(228)
left_ulta = chr(255)
left_back = chr(178)
left_back_crawl = chr(184)

### SERIAL SETUP ###
#variables for serial port
port = "/dev/ttyUSB0"
baudrate = 9600
timeout = 1
ser = serial.Serial()

#setup serial port
ser.port = port
ser.baudrate = baudrate
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.timeout = timeout
print "serial has been setup"

def turnRight():
    ser.write(left_slow)
    ser.write(right_back_crawl)

def turnLeft():
    ser.write(right_slow)
    ser.write(left_back_crawl)

def driveStraight():
    ser.flushInput()
    ser.flushOutput()
    count = 0
    while(count < 25):
        ser.write(left_slow)
        ser.write(right_slow)
        count = count+1
        print count
    stop()
    ser.flushInput()
    ser.flushOutput()

def stop():
    ser.write(chr(0))

#get current heading, (IF NORTH WAS SET PROPERLY)
def readCompass():
    # Read the Euler angles for heading, roll, pitch (all in degrees).
    heading, roll, pitch = bno.read_euler()
    # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
    sys, gyro, accel, mag = bno.get_calibration_status()
    x,y,z = bno.read_magnetometer()

    return heading

def calculateBearing(currLat,currLon,desLat,desLon):
        currLat = math.radians(currLat)
        currLon = math.radians(currLon)
        desLat = math.radians(desLat)
        desLon = math.radians(desLon)
        diffLong = desLon - currLon

        x = math.sin(diffLong) * math.cos(desLat)
        y = math.cos(currLat) * math.sin(desLat) - (math.sin(currLat) *
            math.cos(desLat) * math.cos(diffLong))

        inital_bearing = math.atan2(x,y)
        inital_bearing = math.degrees(inital_bearing)
        compass_bearing = (inital_bearing + 360) % 360

        return compass_bearing

#Calculate distance to the target
def haversine(currLat,currLon,desLat,desLon):
    #approx radius of the earf
    R = 6371000

    currLat = math.radians(currLat)
    currLon = math.radians(currLon)
    desLat = math.radians(desLat)
    desLon = math.radians(desLon)

    dlon = desLon-currLon
    dlat = desLat-currLat
    a = math.sin(dlat/2)**2 + math.cos(currLat) * math.cos(desLat) * math.sin(dlon / 2)**2
    c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    distance = R*c # In meters

    return distance

def turnTo(desiredHeading):
    currHeading = readCompass()
    thres=4 #degree turning threshold

    #will turn to one direction based on current currHeading
    while not(currHeading >= desiredHeading - thres and currHeading <= desiredHeading + thres):
        currHeading = readCompass()
        if(currHeading < desiredHeading):
            print "Turn Right"
            turnRight()
            #time.sleep(0.2)
            print currHeading
            currHeading = readCompass()
        stop()
        #time.sleep(1)
        if(currHeading > desiredHeading):
            print "Turn Left"
            turnLeft()
            #time.sleep(0.2)
            print currHeading
            currHeading = readCompass()
        stop()
        #time.sleep(1)
        #opening the serial port for communication
        ser.flushInput()
        ser.flushOutput()
    return

def main():
    #opening the serial port for communication
    ser.open()
    ser.write(chr(0))
    ser.flushInput()
    ser.flushOutput()
    count = 0
    while(count < 250):
        ser.write(left_slow)
        ser.write(right_slow)
        count = count+1
        print count
###motor 1(left)
##right_crawl = chr(70)
##right_slow = chr(85)
##right_fast = chr(100)
##right_ulta = chr(127)
##right_back = chr(50)
##right_back_crawl = chr(58)
##
###motor 2(right)
##left_crawl = chr(198)
##left_slow = chr(213)
##left_fast = chr(228)
##left_ulta = chr(255)
##left_back = chr(178)
##left_back_crawl = chr(184)
    ser.write(chr(0))
    time.sleep(0.2)
    ser.flushInput()
    ser.flushOutput()
    print "stop command"
    

def gpsGO():
    #opening the serial port for communication
    ser.open()
    ser.flushInput()
    ser.flushOutput()
    
    desLat = 41.6766657
    desLon = -71.2664577

    stop()
    currLon = float(gps.gpsData('lon'))
    currLat = float(gps.gpsData('lat'))
    #calculate bearing and disatnce from target point
    beta = calculateBearing(currLat,currLon,desLat, desLon)
    print "START Desired Angle: {}".format(beta)
    distance = haversine(currLat,currLon,desLat,desLon)
    print "START Distance to target: {}".format(distance)

    #turnTo(beta)

    while not(distance < 1):
        currLon = float(gps.gpsData('lon'))
        currLat = float(gps.gpsData('lat'))
        #calculate bearing and disatnce from target point
        beta = calculateBearing(currLat,currLon,desLat, desLon)
        print "Desired Angle: {}".format(beta)
        distance = haversine(currLat,currLon,desLat,desLon)
        print "Distance to target: {}".format(distance)
        time.sleep(0.5)

        if(distance > 10):
            turnTo(beta)
            ser.flushInput()
            ser.flushOutput()
            driveStraight()

    stop()
    ser.close()

if __name__ == '__main__':
    gpsGO()
    #main()
