void setup() 
{
  Serial.begin(9600); // Start serial communications

  pinMode(8, OUTPUT); //Autonomous mode light ouput 
  digitalWrite(8, LOW); //start with lights off
}

void loop() 
{
  if (Serial.available() > 0) 
  {
    if(Serial.read() == '1')
    {
      digitalWrite(8, HIGH);
    }
    else
    {
      digitalWrite(8,LOW);
    }
  }
}
