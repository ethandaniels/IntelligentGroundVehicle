##############################################################
##AccelGyroMag_edit.py | Ethan T. Daniels | 2017.11.24
##This will be a test for invoking function calls for values
##Uses standard framework from example code

#!!! This only uses one IMU as of current !!! 

##Future: try to create object types for which imu is
##being requested for use? 
##############################################################

import spidev
import time
import argparse 
import sys
import navio.mpu9250
import navio.util

#checking the Navio hardware
navio.util.check_apm()

#!!! Choosing what IMU to use, naming 'imu' object to it
#imu = navio.mpu9250.MPU9250()
imu = navio.lsm9ds1.LSM9DS1()

#initalize the sensor for use
imu.initialize()

#creating a class to output this data
class IMU(object):
    
    def getGyro(self):
        imu.read_gyro()
        return imu.gyroscope_data
    def getAcc(self):
        imu.read_acc()
        return imu.accelerometer_data
    def getMag(self):
        imu.read_mag()
        return imu.magnetometer_data
