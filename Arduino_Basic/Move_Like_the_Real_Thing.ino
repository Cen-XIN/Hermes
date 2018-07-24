/*
 * Move Like the Real Thing
 * 2018-07-23
 * Copyright (c) Cen XIN
 */
 
//Pin 4 = Direction control for Motor 2
//Pin 5 = PWM control for Motor 2
//Pin 6 = PWM control for Motor 1
//Pin 7 = Direction control for Motor 1
int E1 = 5;  
int M1 = 4; 
int E2 = 6;                      
int M2 = 7;  

void setup() {
  Serial.begin( 9600 );
  for (int i = 4; i <= 7; i++) //Pin 4 to 7 are used
      pinMode(i, OUTPUT);
}

void loop() {
  if (Serial.available()) {
        char input = Serial.read();
        switch(input){
          case 'w':
            digitalWrite(M1, LOW);
            digitalWrite(M2, LOW);
            analogWrite(E1, 255); 
            analogWrite(E2, 255);
            break;
          case 's':
            digitalWrite(M1, HIGH);
            digitalWrite(M2, HIGH);
            analogWrite(E1, 255); 
            analogWrite(E2, 255);
            break;
          case 'a':   
            analogWrite(E1, 191);
            analogWrite(E2, 0);
            break;
          case 'd':
            analogWrite(E1, 0);
            analogWrite(E2, 191);
            break;
          case 'x':
            analogWrite(E1, 0);
            analogWrite(E2, 0);
            break;
          default:
            analogWrite(E1, 0);
            analogWrite(E2, 0);
            break;
        }
     }
}

