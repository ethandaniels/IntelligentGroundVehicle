#Ethan T. Daniels
#IGV 2017-2018 RWU
import xbox #controller IO
import time #sandman
import RPi.GPIO as GPIO #for IO
import sys, traceback #for exception handeling
from sabertooth2x60 import Sabertooth #Motor Control
from AccelGyroMag_edit import IMU #Navio IMU
from GPS_edit import GPS #Navio GPS
from navigation import Nav #Includes all nav algs
import numpy
import RPi.GPIO as GPIO
from line_avoidance import Lines
from light_trig import Lights
#from serial_lights import Lights

nav = Nav() #object for navigation functions
gps = GPS() #gps object
imu = IMU() #imu object
saber = Sabertooth() #motor controller object
joy = xbox.Joystick() #xbox controller object
lines = Lines()
lights = Lights()
#GPIO.setmode(GPIO.BOARD)

# Show connection status
if joy.connected():
    print "Connected"
    print "\n\nClick the back button to exit."

    saber.flush()
    print "\nSerial has been flushed"

else:
    print "\nDisconnected"
    saber.stop()
    GPIO.cleanup()

#Run forever until back button  is pressed, or an exception is made
def main():
    try:
        while not joy.Back():
            lights.lightsOff()
            if joy.A():
               print "\CurrLon Curr Lat"
               currLon = float(gps.gpsData('lon'))
               currLat = float(gps.gpsData('lat'))
               print currLon
               print currLat
               lights.lightsOff()

            if joy.B():
                lights.lightsOn()
                print "\nGPS waypoint navigation"
                #Hawkworks TREE Destination
                desLat1 = 41.6766209
                desLon1 = -71.2664265

                #Hawkworks DRAIN Destination
                desLat2 = 41.6766479
                desLon2 = -71.2660617
                ### Get user input for desiried position ###
                #desLat = input("Please provide the lat (##.#######): ")
                #desLon = input("Please provide the lon (##.#######): ")

                nav.gpsGO(desLat1,desLon1)
                time.sleep(2)
                nav.gpsGO(desLat2,desLon2)
                time.sleep(2)
                lights.lightsOff()

            # Test Turning
            if joy.Y():
                lines.avgOUT()
            if joy.X():
                #saber.driveStraight()
                lights.lightsOn()
                #nav.lineAvoid()
                nav.testLidar()
                #lines.avgOUT()


            #Analog Stick Control

            ### LEFT STICK ###
            if joy.leftY() == 0:
                saber.stopLeft() #stop (dead position)
            if joy.leftY() > .1:
                saber.drive(1,1) #slow movement left
            if joy.leftY() > .7:
                saber.drive(1,2) #med movement left
            if joy.leftY() < 0:
                saber.drive(1,4) #back movment left

            ### RIGHT STICK ###
            if joy.rightY() == 0:
                saber.stopRight() #stop (dead position)
            if joy.rightY() > .1:
                saber.drive(2,1) #slow movement right
            if joy.rightY() > .7:
                saber.drive(2,2) #med movement right
            if joy.rightY() < 0:
                saber.drive(2,4) #back movment right

            ### FAST MODE ###
            if joy.rightTrigger() > .9 and joy.leftTrigger() > .9:
                ## Left
                if joy.leftY() > .8:
                    saber.drive(1,5) #fast movement left
                ## Right
                if joy.rightY() > .8:
                    saber.drive(2,5) #fast movement right

        # Close out when done
        joy.close()
        #stop the motors
        saber.stop()
        #clean the serial
        saber.flush()
        saber.close()
        #lights.Off()

    #User Keyboard Inturrupt
    except KeyboardInterrupt:
        print "\nShutdown requested...exiting"
        #stop the motors
        saber.stop()
        #clean the serial
        saber.flush()
        saber.close()
        # Close out when done
        joy.close()
        #lights.Off()

    #Some crash
    except Exception:
        traceback.print_exc(file=sys.stdout)
        #stop the motors
        saber.stop()
        #clean the serial
        saber.flush()
        saber.close()
        # Close out when done
        joy.close()
        #lights.Off()
    sys.exit(0)

if __name__ == '__main__':
    main()
