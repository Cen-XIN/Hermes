/*
 * Serial Blink
 * 2018-07-23
 * Copyright (c) Cen XIN
 */

int delay_time = 1000;

void func(int delay_time) {
  digitalWrite(13, HIGH);
  delay(delay_time);

  digitalWrite(13, LOW);
  delay(delay_time);
}

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
}

void loop() {
  char c;
  if (Serial.available()) {
    c = Serial.read();
    if (c == 'w') {
      delay_time -= 100;
      if (delay_time < 100) {
        delay_time = 100;
      }
    } else if (c == 's') {
      delay_time += 100;
      if (delay_time > 10000) {
        delay_time = 10000;
      }
    } else {
      Serial.println("Wrong command!");
    }
  }
  func(delay_time);
}
