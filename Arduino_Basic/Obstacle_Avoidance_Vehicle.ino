/*
 * Obstacle Avoidance Vehicle
 * 2018-07-24
 * Copyright (c) Cen XIN
 */

#include <NewPing.h>

#define TRIGGER_PIN  12  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     11  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 400 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

char cmd = 'x';

// For controlling wheels
int E1 = 5;   // Pin 5 = PWM control for Motor 2
int M1 = 4;   // Pin 4 = Direction control for Motor 2
int E2 = 6;   // Pin 6 = PWM control for Motor 1                     
int M2 = 7;   // Pin 7 = Direction control for Motor 1

void setup() {
  Serial.begin(9600);

  for (int i = 4; i <= 7; i++) //Pin 4 to 7 are used
      pinMode(i, OUTPUT);
}

void loop() {
  int dist;

  if (Serial.available()) {
    cmd = Serial.read();
    
    switch(cmd) {
      case 'w':
        analogWrite(E1, 180);
        analogWrite(E2, 180);
        cmd = 'o';
        break;
      case 'o':
        break;
      default:
        analogWrite(E1, 0);
        analogWrite(E2, 0);
        break;
    }
  }
  
  delay(100);
  dist = sonar.ping_cm();
  Serial.println(dist);
  
  if (sonar.ping_cm() > 0 && sonar.ping_cm() < 30 && cmd == 'o') {
    analogWrite(E1, 200);  
    analogWrite(E2, 0);
    delay(1000);
  } else {
    if (cmd == 'x') {
      delay(100);
    } else {
      analogWrite(E1, 180);
      analogWrite(E2, 180);    
      cmd = 'o';
    }  
  }
}
