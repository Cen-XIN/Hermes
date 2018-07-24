/*
 * Move with "Precision"?
 * 2018-07-23
 * Copyright (c) Cen XIN
 */

// For controlling wheels
int E1 = 5;   // Pin 5 = PWM control for Motor 2
int M1 = 4;   // Pin 4 = Direction control for Motor 2
int E2 = 6;   // Pin 6 = PWM control for Motor 1                     
int M2 = 7;   // Pin 7 = Direction control for Motor 1

// For parsing commands
String cmd = "";
char car_direction = 0;
int car_speed = 0;
int car_distance = 0;

// For recording distances (ISR)
const byte interruptPin_left = 2;
const byte interruptPin_right = 3;
volatile int state_left = 0;
volatile int state_right = 0;

void parse_cmd() {
  int i, j;
  int dist_digit, temp = 1;
  if (cmd.length() <= 0) {
    return;
  }
  dist_digit = cmd.length() - 4;
  for (i = 0; cmd[i] != '\0'; i++) {
    //Serial.println(cmd[i]);
    if (i == 0) {
      car_direction = cmd[i];
    } else if (i == 2) {
      car_speed = int(cmd[i] - 48);
    } else if (i >= 4) {
      cmd[i] -= 48;
      for (j = 0; j < dist_digit - 1; j++) {
        temp *= 10;
      }
      temp *= int(cmd[i]);
      car_distance += temp;
      temp = 1;
      dist_digit--;
    }
  }
}

void change_left() {
  state_left++;
}

void change_right() {
  state_right++;
}

void setup() {
  Serial.begin(9600);

  for (int i = 4; i <= 7; i++) //Pin 4 to 7 are used
      pinMode(i, OUTPUT);

  pinMode(interruptPin_left, INPUT_PULLUP);
  pinMode(interruptPin_right, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin_left), change_left, CHANGE);
  attachInterrupt(digitalPinToInterrupt(interruptPin_right), change_right, CHANGE);
}

void loop() {
  while (Serial.available() > 0) {// Reveive the command as String
    cmd += char(Serial.read());
    delay(2);
  }
  
  parse_cmd();

  if (cmd.length() > 0) {
    switch(car_direction) {
      case 'w':
        digitalWrite(M1, LOW);
        digitalWrite(M2, LOW);
        switch(car_speed) {
          case 1:
            analogWrite(E1, 150);
            analogWrite(E2, 150);
            break;
          case 2:
            analogWrite(E1, 200);
            analogWrite(E2, 200);
            break;
          case 3:
            analogWrite(E1, 255);
            analogWrite(E2, 255);
            break;
          default:
            analogWrite(E1, 0);
            analogWrite(E2, 0);
            break;
        }
        break;
      case 's':
        digitalWrite(M1, HIGH);
        digitalWrite(M2, HIGH);
        switch(car_speed) {
          case 1:
            analogWrite(E1, 150);
            analogWrite(E2, 150);
            break;
          case 2:
            analogWrite(E1, 200);
            analogWrite(E2, 200);
            break;
          case 3:
            analogWrite(E1, 255);
            analogWrite(E2, 255);
            break;
          default:
            analogWrite(E1, 0);
            analogWrite(E2, 0);
            break;
        }
        break;
      default:
        digitalWrite(M1, HIGH);
        digitalWrite(M2, HIGH);
        analogWrite(E1, 0);
        analogWrite(E2, 0);
        break;
    }
    cmd = "";
  }
  
  if ((state_left/384.0)*20.7 > car_distance || (state_right/384.0)*20.7 > car_distance) {
    analogWrite(E1, 0);
    analogWrite(E2, 0);
    car_direction = 0;
    car_speed = 0;
    car_distance = 0;
    state_left = 0;
    state_right = 0;
  }
}
