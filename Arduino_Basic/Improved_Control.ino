/*
 * Improved Control
 * 2018-07-25
 * Copyright (c) Cen XIN
 */

// For controlling wheels
int E1 = 5;   // Pin 5 = PWM control for Motor 2
int M1 = 4;   // Pin 4 = Direction control for Motor 2
int E2 = 6;   // Pin 6 = PWM control for Motor 1                     
int M2 = 7;   // Pin 7 = Direction control for Motor 1

// For parsing commands
String cmd = "";
char car_direction = 'x';
int car_degree = 0;
int car_speed = 0;
int is_cmd = 0;

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
  dist_digit = cmd.length() - 2;
  for (i = 0; cmd[i] != '\0'; i++) {
    if (i == 0) {
      car_direction = cmd[i];
    } else if (i >= 2) {
      cmd[i] -= 48;
      for (j = 0; j < dist_digit - 1; j++) {
        temp *= 10;
      }
      temp *= int(cmd[i]);
      car_degree += temp;
      temp = 1;
      dist_digit--;
    }
  }
  Serial.println(car_direction);
  Serial.println(car_degree);
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
    Serial.println("done...1");
    is_cmd = 1;
    switch(car_direction) {
      case 'a':
        Serial.println("done...2_1");
        digitalWrite(M1, LOW);
        digitalWrite(M2, HIGH);
        car_speed = 150;
        break;
      case 'd':
        Serial.println("done...2_2");   
        digitalWrite(M1, HIGH);
        digitalWrite(M2, LOW);
        car_speed = 150;
        break;
      case 'x':
        Serial.println("done...2_3");
        digitalWrite(M1, LOW);
        digitalWrite(M2, LOW);
        car_speed = 0;
        break;
      default:
        Serial.println("done...2_4"); 
        digitalWrite(M1, LOW);
        digitalWrite(M2, LOW);
        car_speed = 0;
        break;   
    }
    cmd = "";
  }

  Serial.println("done...3");

  if (is_cmd == 1) {
    Serial.println("done...if_1");
    analogWrite(E1, car_speed);
    analogWrite(E2, car_speed);
  }


  Serial.println("done...4");

  if (is_cmd == 1 && ((state_left/384.0)*360.0 > car_degree || (state_right/384.0)*360.0 > car_degree)) {
    delay(100);
    Serial.println("done...if_2");
    analogWrite(E1, 0);
    analogWrite(E2, 0);
    car_direction = 0;
    car_speed = 0;
    car_degree = 0;
    state_left = 0;
    state_right = 0;    
    is_cmd = 0;
  }
  Serial.println("done...5");
  delay(100);
}
