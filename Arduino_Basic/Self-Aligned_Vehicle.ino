/*
 * Self-Aligned Vehicle
 * 2018-07-24
 * Copyright (c) Cen XIN
 */

#include <SparkFun_MAG3110.h>

//Pin 4 = Direction control for Motor 2
//Pin 5 = PWM control for Motor 2
//Pin 6 = PWM control for Motor 1
//Pin 7 = Direction control for Motor 1
int E1 = 5;  
int M1 = 4; 
int E2 = 6;                      
int M2 = 7;  

int car_speed = 100;

MAG3110 mag = MAG3110(); //Instantiate MAG3110

void setup() {
  Serial.begin(9600);
  for (int i = 4; i <= 7; i++) //Pin 4 to 7 are used
    pinMode(i, OUTPUT);

  digitalWrite(M1, LOW);
  digitalWrite(M2, HIGH);

  mag.initialize(); //Initialize the MAG3110
}

void loop() {
  int x, y, z;
  int head;

  if(!mag.isCalibrated()) //If we're not calibrated
  {
    if(!mag.isCalibrating()) //And we're not currently calibrating
    {
      Serial.println("Entering calibration mode");
      mag.enterCalMode(); //This sets the output data rate to the highest possible and puts the mag sensor in active mode
    }
    else
    {
      //Must call every loop while calibrating to collect calibration data
      //This will automatically exit calibration
      //You can terminate calibration early by calling mag.exitCalMode();
      mag.calibrate(); 
    }
  }
  else
  {
    Serial.println("Calibrated!");
  }
  mag.readMag(&x, &y, &z);
  Serial.print("Heading: ");
  head = mag.readHeading();
  head = abs(head);
  Serial.println(head);

  if (head > 95) {
    digitalWrite(M1, HIGH);
    digitalWrite(M2, LOW);    
    car_speed = 120;
  } else if (head < 85) {
    digitalWrite(M1, LOW);
    digitalWrite(M2, HIGH); 
    car_speed = 120;     
  } else {
    car_speed = 0;
  }

  analogWrite(E1, car_speed);
  analogWrite(E2, car_speed);
  
  delay(100);
}
