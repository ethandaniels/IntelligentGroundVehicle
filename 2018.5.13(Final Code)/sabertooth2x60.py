#!/usr/bin/python
#sabertooth2x60.py
#Ethan Daniels | 2017.10.6
#Class implementing simplified Serial output
#with Saberooth 2x60 (Dimension Engineering)
import serial
import time

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

#opening the serial port for communication
ser.open()
ser.flushInput()
ser.flushOutput()

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

#ex of how to create an object of this class
#saber = Sabertooth()
class Sabertooth(object):
    #EX:how to have motor move
    #saber.drive(1,1)
    #Motor 1, 1 is full reverse, 64 is stop and 127 is full forward
    #Motor 2, 128 is full reverse, 192 is stop and 255 if full forward
    def drive(self, mtr, speed):
        ### Right Motor
        if mtr == 1:
            if speed == 1:
                ser.write(left_crawl)
            elif speed == 2:
                ser.write(left_slow)
            elif speed == 3:
                ser.write(left_fast)
            elif speed == 4:
                ser.write(left_back)
            elif speed ==5:
                ser.write(left_ulta)

        ### Right Motor
        elif mtr == 2:
            if speed == 1:
                ser.write(right_crawl)
            elif speed == 2:
                ser.write(right_slow)
            elif speed == 3:
                ser.write(right_fast)
            elif speed == 4:
                ser.write(right_back)
            elif speed == 5:
                ser.write(right_ulta)

    ### Basic movements ###
    def turnLeft(self):
        ser.write(right_slow)
        ser.write(left_back_crawl)

    def turnRight(self):
        ser.write(left_slow)
        ser.write(right_back_crawl)

    def driveStraight(self):
        ser.write(left_slow)
        ser.write(right_slow)

    def flush(self):
        ser.flushInput()
        ser.flushOutput()

    def close(self):
        ser.close()

    ### Stop States ###
    def stopRight(self):
        ser.write(chr(64))

    def stopLeft(self):
        ser.write(chr(192))

    #call to stop the robot
    def stop(self):
        ser.write(chr(0))
