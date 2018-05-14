import serial
import time
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0.1) #this tty address may change
time.sleep(1)
class Lights(object): 
    def lightsOn(self):
        ser.write('1')
    def lightsOff(self):
        ser.write('0')
        #print('Lights should be off!')



# Example Code Use

#time.sleep(3)

#w = Lights()

#w.lightsOn()

#time.sleep(3)

#w.lightsOff()
