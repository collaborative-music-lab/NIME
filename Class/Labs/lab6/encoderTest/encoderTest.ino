#include "pinDefsv5.h"

byte a = p13;
byte b= p12;
byte sw = p10;

void setup() {
  Serial.begin(115200);

  pinMode(a, INPUT);
  pinMode(b, INPUT);
  pinMode(sw, INPUT);
  
}

void loop() {
  Serial.print(digitalRead(a));
  Serial.print("\t");
  Serial.print(digitalRead(b));
  Serial.print("\t");
  Serial.print(digitalRead(sw));
  Serial.println("\t");
  delay(50);
}
