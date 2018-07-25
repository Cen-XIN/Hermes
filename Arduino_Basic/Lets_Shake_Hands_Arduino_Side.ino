/*
 * Let's Shake Hands!
 * 2018-07-24
 * Copyright (c) Cen XIN
 */
char inByte;

void setup() {
  // initialize both serial ports:
  Serial.begin(9600);
  Serial3.begin(9600);
}
void loop() {
  if (Serial3.available()) {
    inByte = Serial3.read();
    Serial.println(inByte);
    if (inByte == 'a') {
      inByte = 'b';
      Serial3.write(inByte);
    }
  }
}
