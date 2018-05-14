/*Ethan T. Daniels | IGV 2017-2018 | 5 1-D LIDARs
 * This code outputs the distance in cm to obstacles from the given LIDARs. This uses PWM read connections/

  EXAMPLE HOOKUP
  Connections:
  LIDAR-Lite 5 Vdc (red) to Arduino 5v
  LIDAR-Lite Ground (black) to Arduino GND
  LIDAR-Lite Mode control (yellow) to Arduino digital input (pin 3)
  LIDAR-Lite Mode control (yellow) to 1 kOhm resistor lead 1
  1 kOhm resistor lead 2 to Arduino digital output (pin 2)
  
  680uF capacitor (+) to Arduino 5v
  680uF capacitor (-) to Arduino GND
*/

unsigned long pulseWidth1, pulseWidth2, pulseWidth3, pulseWidth4, pulseWidth5;
int lightTrig;
int lightsOn = LOW;

void setup()
{
  Serial.begin(9600); // Start serial communications

  //Trigger Pins
  pinMode(2, OUTPUT);
  digitalWrite(2, LOW); //sets continuous read
  pinMode(3, OUTPUT); 
  digitalWrite(3, LOW);
  pinMode(4, OUTPUT); 
  digitalWrite(4, LOW); 
  pinMode(5, OUTPUT); 
  digitalWrite(5, LOW);
  pinMode(6, OUTPUT);
  digitalWrite(6, LOW); 
  
  pinMode(13, INPUT); //monitor pin LIDAR 1
  pinMode(12, INPUT); //monitor pin LIDAR 2
  pinMode(11, INPUT); //monitor pin LIDAR 3
  pinMode(10, INPUT); //monitor pin LIDAR 4 
  pinMode(9, INPUT); //monitor pin LIDAR 5

  pinMode(8, OUTPUT); //Autonomous mode light ouput 
  digitalWrite(8, LOW); //start with lights off
}

void pulseCheck(unsigned long pulseNum)
{
  pulseNum = pulseNum /10;
  if(pulseNum<1)
  {
    pulseNum = 999;
    Serial.print(String(pulseNum));
  }
  else if(pulseNum<10)
  {
    Serial.print('0');
    Serial.print('0');
    Serial.print(String(pulseNum));
  }
  else if(pulseNum<100)
  {
    Serial.print('0');
    Serial.print(String(pulseNum));
  }
  else
  {
    pulseNum = 999;
    Serial.print(String(pulseNum));
  }
  Serial.print(" ");
}

//main loop
void loop()
{
  pulseWidth1 = pulseIn(13, HIGH); // Count how long the pulse is high in microseconds
  pulseWidth2 = pulseIn(12, HIGH);
  pulseWidth3 = pulseIn(11, HIGH);
  pulseWidth4 = pulseIn(10, HIGH);
  pulseWidth5 = pulseIn(9, HIGH); 

  pulseCheck(pulseWidth1);
  pulseCheck(pulseWidth2);
  pulseCheck(pulseWidth3);
  pulseCheck(pulseWidth4);
  pulseCheck(pulseWidth5);
  Serial.println();
  delay(100);
}

