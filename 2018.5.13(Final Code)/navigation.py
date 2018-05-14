############################
##navigation.py
##Ethan T. Daniels | IGV 2017-2017 | Roger Williams University
#!!! This will hold all navigation algorithms, including evasion !!!
#Example Sensor Calls:
#!!GPS!!
# gps.gpsData('lon')
# gps.gpsData('lat')

#!!IMU!!
# imu.getAcc()
# imu.getMag()
# imu.getGyro()
###########################
### IMPORTS ###
import time #sandman
import sys, traceback #for exception handeling
from sabertooth2x60 import Sabertooth #Motor Control
from GPS_edit import GPS #Navio GPS
import math #minor in mathematics
from line_avoidance import Lines # camera line detection data
from lidar_data import Lidar # lidar Data

### COMPASS ###
import logging
import sys
import time
from Adafruit_BNO055 import BNO055

### OBJECTS ###
gps = GPS() #gps object
saber = Sabertooth() #motor controller object
lines = Lines()
lidar = Lidar()
### COMPASS ###
bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)
# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status, self_test, error = bno.get_system_status()
#---------------------------------------------------------------
class Nav(object):
    #test line detection
    def lineAvoid(self):
        time.sleep(0.2)
        line = lines.avgOUT()

        # turn right
        if(line < 0):
                saber.turnRight()
                time.sleep(0.2)
        # turn left
        elif(line > 0):
                saber.turnLeft()
                time.sleep(0.2)
        # go straight
        else:
                saber.driveStraight()
                time.sleep(0.5)

    def testLidar(self):
        # test case incase there is failed reading
        try:
            [left1, left2, center, right2, right1] = lidar.lidarData()
            # typecasting variable
            left1 = float(left1)
            left2 = float(left2)
            center = float(center)
            right2 = float(right2)
            right1 = float(right1)

        except Exception:
            left1 = 1000
            left2 = 1000
            center = 1000
            right1 = 1000
            right2 = 1000

        # print LIDAR values
        print(left1)
        print(left2)
        print(center)
        print(right2)
        print(right1)
        print("-----------------------")

        # get image for slopes
        line = lines.avgOUT()
        print("-----------------------")

        # something ahead
        if(center < 100):
            # something to the left
            if(left1 < 75 or left2 < 75):
                saber.turnRight()
                time.sleep(0.5)
            # something to the right
            elif(right1 < 75 or right2 < 75):
                saber.turnLeft()
                time.sleep(0.5)
            else:
                # turn right
                if(line < 0):
                    print("line case")
                    saber.turnRight()
                    time.sleep(0.5)
                # turn left
                elif(line > 0):
                    print("line case")
                    saber.turnLeft()
                    time.sleep(0.5)
                else:
                    print("line case")
                    saber.turnRight()
                    time.sleep(0.5)

        elif(right1 < 35):
            saber.turnLeft()
            time.sleep(0.5)
        elif(left1 < 35):
            saber.turnRight()
            time.sleep(0.5)
        elif(right2 < 100):
            saber.turnLeft()
            time.sleep(0.5)
        elif(left2 < 100):
            saber.turnRight()
            time.sleep(0.5)


        # chicane case!!!
        elif(center > 400 and right1 < 40): # may have to adjust all distance value REMEMBER CHICANE EXIT
            if(line < 0 or line > 0):
                print("Chicane Case")
                saber.turnLeft()
                time.sleep(0.2)
            else:
                print("Chicane Case, null")
                saber.driveStraight()
                time.sleep(0.5)
        elif(center > 400 and left1 < 40):
            if(line < 0 or line > 0):
                saber.turnRight()
                time.sleep(0.5)
            else:
                print("Chicane Case, null")
                saber.driveStraight()
                time.sleep(0.5)
        else:
            # turn right
            if(line < 0):
                    saber.turnRight()
                    time.sleep(0.5)
                    print("line only case")
            # turn left
            elif(line > 0):
                    saber.turnLeft()
                    time.sleep(0.5)
                    print("line only case")
            else: # default state lines are okay
                saber.driveStraight()
                time.sleep(0.5)
                print("default else")
            saber.driveStraight()
            time.sleep(0.5)

    #get current heading, (IF NORTH WAS SET PROPERLY)
    def readCompass(self):
        # Read the Euler angles for heading, roll, pitch (all in degrees).
        heading, roll, pitch = bno.read_euler()
        # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
        sys, gyro, accel, mag = bno.get_calibration_status()
        x,y,z = bno.read_magnetometer()

        return heading

    #Turns the robot to specified angle
    def turnTo(self, desiredHeading):
        currHeading = self.readCompass()
        thres=8 #degree turning threshold
        #will turn to one direction based on current currHeading
        while not(currHeading >= desiredHeading - thres and currHeading <= desiredHeading + thres):
            currHeading = self.readCompass()
            if(currHeading < desiredHeading):
                print "Turn Right"
                saber.turnRight()
                print currHeading
                currHeading = self.readCompass()
            saber.stop()
            #time.sleep(0.5)
            if(currHeading > desiredHeading):
                print "Turn Left"
                saber.turnLeft()
                print currHeading
                currHeading = self.readCompass()
            saber.stop()
            #time.sleep(0.5)
        return

    #calcuate bearing to target | Output will be what we want to turn to
    #will read in currPos and desiredPos
    def calculateBearing(self,currLat,currLon,desLat,desLon):
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
    def haversine(self,currLat,currLon,desLat,desLon):
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

    #averaging GPS values
    def avgGPS(self):
        currLon = float(gps.gpsData('lon'))
        currLat = float(gps.gpsData('lat'))

        for i in range(0, 5):
            currLon += float(gps.gpsData('lon'))
        for i in range(0, 5):
            currLat += float(gps.gpsData('lat'))
        currLon = float(currLon/6)
        currLat = float(currLat/6)
        return currLon, currLat#call as currLon, currLat = avgGPS()

    #weighted filter based on average velocity of bot, its location before and after driving for some time

    def gpsFilter(self,t):
        #Get GPS
        prevLat = float(gps.gpsData('lat'))
        prevLon = float(gps.gpsData('lon'))
        #Converting into m
        prevLat = prevLat*(111111.111)
        prevLon = prevLon*(111111.111)

        #value between gps correction
        theta = 360-(self.readCompass())
        deltx = 0.6425*t*math.sin(theta)
        delty = 0.6425*t*math.cos(theta)

        #check new gps
        newLat = float(gps.gpsData('lat'))
        newLon = float(gps.gpsData('lon'))
        newLat = newLat*(111111.111)
        newLon = newLon*(111111.111)

        #value between gps readings
        delLat = newLat-prevLat
        delLon = newLon-prevLon

        #compare gps correction to delta gps readings
        currLat = ((deltx*.50)+(delLat*.50))+prevLat
        currLon = ((delty*.50)+(delLon*.50))+prevLon

        #convert from meters back to lat,lon unit
        currLat = currLat/111111.111
        currLon = currLon/111111.111

        return currLon, currLat

    def gpsGO(self, desLat, desLon):
        currLon = float(gps.gpsData('lon'))
        currLat = float(gps.gpsData('lat'))
        #calculate bearing and disatnce from target point
        beta = self.calculateBearing(currLat,currLon,desLat, desLon)
        print "START Desired Angle: {}".format(beta)
        distance = self.haversine(currLat,currLon,desLat,desLon)
        print "START Distance to target: {}".format(distance)

        while(distance > 1):
            currLon = float(gps.gpsData('lon'))
            currLat = float(gps.gpsData('lat'))
            #calculate bearing and disatnce from target point
            beta = self.calculateBearing(currLat,currLon,desLat, desLon)
            print "Desired Angle: {}".format(beta)
            distance = self.haversine(currLat,currLon,desLat,desLon)
            print "Distance to target: {}".format(distance)

            self.turnTo(beta)
            saber.driveStraight()

        #stop bot once reached positon
        saber.stop()
        print "\nDONE"
        print "\n\nHave reached location {} {} within 1m".format(desLat,desLon)

        #close and clear serial
        #saber.flush()
        #saber.close()
