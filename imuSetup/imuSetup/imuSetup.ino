/* Ethan T. Daniels || Roger Willams University Intellegent Ground Vehicle 2017-2018

   The purpose of this program is to read in raw data from the BNO055 9DOF sensor, create serial outputs for
   data handoff to RPi, and to create an accurate reading of the compass functionality.

   Connections
   ===========
   Connect SCL to analog 5
   Connect SDA to analog 4
   Connect VDD to 3.3V DC
   Connect GROUND to common ground

   Last Edit: 8/2/2017 20:34:07
*/
#include <Wire.h>
#include <math.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

/* Set the delay between fresh samples */
#define BNO055_SAMPLERATE_DELAY_MS (100)
Adafruit_BNO055 bno = Adafruit_BNO055();

void setup(void)
{
  Serial.begin(9600);

  //Initalize the sensor
  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }

  delay(1000);
  bno.setExtCrystalUse(true);

  //Note: Calibration status values: 0=uncalibrated, 3=fully calibrated
}

//Arduino loop function, triggered after setup is complete
void loop()
{
  //Quaternion variables
  double qX, qY, qZ, qW;
  //Gyro variables (rad/s)
  double gX, gY, gZ;
  //Euler variables (degrees)
  double eX, eY, eZ;
  //Magnetometer varaibles (uT)
  double mX, mY, mZ;
  //Linear Acceleration varaibles (m/s^2)
  double lX, lY, lZ;

  //Display calibration status for each sensor.
  uint8_t system, gyro, accel, mag = 0;
  bno.getCalibration(&system, &gyro, &accel, &mag);
  Serial.print("CALIBRATION: Sys=");
  Serial.print(system, DEC);
  Serial.print(" Gyro=");
  Serial.print(gyro, DEC);
  Serial.print(" Accel=");
  Serial.print(accel, DEC);
  Serial.print(" Mag=");
  Serial.println(mag, DEC);

  delay(300); //delay 3 seconds after calibration

  readQuats(&qX, &qY, &qZ, &qW);
  readGyro(&gX, &gY, &gZ);
  readEuler(&eX, &eY, &eZ);
  readMag(&mX, &mY, &mZ);
  readLinAcc(&lX, &lY, &lZ);
  readComp(&mX, &mY, &mZ, &eZ, &eY);

  delay(BNO055_SAMPLERATE_DELAY_MS);
}
