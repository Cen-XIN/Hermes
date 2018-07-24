/*
 * How Far?
 * 2018-07-23
 * Copyright (c) Cen XIN
 */

const byte interruptPin_left = 2;
const byte interruptPin_right = 3;
volatile int state_left = 0;
volatile int state_right = 0;

void setup() {
  pinMode(interruptPin_left, INPUT_PULLUP);
  pinMode(interruptPin_right, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin_left), change_left, CHANGE);
  attachInterrupt(digitalPinToInterrupt(interruptPin_right), change_right, CHANGE);
  
  Serial.begin(9600);
}

void loop() {
  delay(100);       
  Serial.print("Left State = ");
  Serial.print((state_left/384.0)*20.7);
  Serial.print(" cm   Right State = ");
  Serial.print((state_right/384.0)*20.7);
  Serial.println(" cm");
}

void change_left() {
  state_left++;
}

void change_right() {
  state_right++;
}

