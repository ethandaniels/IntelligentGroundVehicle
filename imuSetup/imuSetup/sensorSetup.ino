//might not even need Quats
void readQuats(double *x, double *y, double *z, double *w)
{
  imu::Quaternion quat = bno.getQuat();

  float quatX = quat.x();
  double nearestQuatX = roundf(quatX * 100) / 100; //rounds to tenths palce
  *x = nearestQuatX;

  float quatY = quat.y();
  double nearestQuatY = roundf(quatY * 100) / 100;
  *y = nearestQuatY;

  float quatZ = quat.z();
  double nearestQuatZ = roundf(quatZ * 100) / 100;
  *z = nearestQuatZ;

  float quatW = quat.w();
  double nearestQuatW = roundf(quatW * 100) / 100;
  *w = nearestQuatW;
}

//Read the Gyroscope!
void readGyro(double *x, double *y, double *z)
{
  imu::Vector<3> gyro = bno.getVector(Adafruit_BNO055::VECTOR_GYROSCOPE);

  float gyroX = gyro.x();
  double nearestGyroX = roundf(gyroX *100) / 100;
  *x = nearestGyroX;

  float gyroY = gyro.y();
  double nearestGyroY = roundf(gyroY *100) / 100;
  *y = nearestGyroY;

  float gyroZ = gyro.z();
  double nearestGyroZ = roundf(gyroZ *100) / 100;
  *z = nearestGyroZ;
}

//reads the euler degree values (standard 0-359º, adding one for ease of use as we will convert to rads)
void readEuler(double *x, double *y, double *z)
{
  //creating an instance of getVector class
  imu::Vector<3> eul = bno.getVector(Adafruit_BNO055::VECTOR_EULER);

  //creates all varaibles to return the magnemoeter values of each direction
  float eulX = eul.x();
  double nearestEulX = roundf(eulX * 100) / 100; //rounds to tenths palce
  *x = nearestEulX+1;

  float eulY = eul.y();
  double nearestEulY = roundf(eulY * 100) / 100;
  *y = nearestEulY+1;


  float eulZ = eul.z();
  double nearestEulZ = roundf(eulZ * 100) / 100;
  *z = nearestEulZ+1;
}


//reads the magnetic field around the bot, main compass module [uT]
void readMag(double *x, double *y, double *z)
{
  //creating an instance of getVector class
  imu::Vector<3> mag = bno.getVector(Adafruit_BNO055::VECTOR_MAGNETOMETER);

  //creates all varaibles to return the magnemoeter values of each direction
  float magX = mag.x();
  double nearestMagX = roundf(magX * 100) / 100; //rounds to tenths palce
  *x = nearestMagX;

  float magY = mag.y();
  double nearestMagY = roundf(magY * 100) / 100;
  *y = nearestMagY;


  float magZ = mag.z();
  double nearestMagZ = roundf(magZ * 100) / 100;
  *z = nearestMagZ;
}

//Read the Linear Acceleration!
//this will read the speed of the bot. It excludes gravity forces
void readLinAcc(double *x, double *y, double *z)
{
  imu::Vector<3> linAcc = bno.getVector(Adafruit_BNO055::VECTOR_LINEARACCEL);

  float accX = linAcc.x();
  double nearestAccX = roundf(accX *100) / 100; //rounds to tenths place
  *x = nearestAccX;

  float accY = linAcc.y();
  double nearestAccY = roundf(accY *100) / 100;
  *y = nearestAccY;

  float accZ = linAcc.z();
  double nearestAccZ = roundf(accZ *100) / 100;
  *z = nearestAccZ;
}
