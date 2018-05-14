import serial
import time
ser = serial.Serial('/dev/ttyACM1', 9600, timeout=0.1) #this tty address may change
time.sleep(0.1)
class Lidar(object): #import Lidar from lidarLights
    # get lidar data
    def lidarData(self):
        ser.flushInput()
        time.sleep(.8) # if this is lower an exception will be created due to data not being parsed properly
        data = ser.readline() #read the LIDAR data in
        data = data.split()
        return data

# There is exception handling built into the navigation file if the arduino does not send the poper amount
# though this exception will essentially make the robot not see anything and as a result rely on line detection
# meaning the robot will hit something. 

# Example Code Use
#w = Lidar()
#print "test output"
#w.lidarData()
#[left1, left2, center, right2, right1] = w.lidarData()
#print(left1)
#print(right1)
