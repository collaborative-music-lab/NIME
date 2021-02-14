#include "SparkFunLSM6DS3.h"

LSM6DS3 IMU;

void setup() {
  Serial.begin(115200);
  IMU.begin();
  
}

void loop() {
  int val = IMU.readRawAccelZ();
  Serial.println(val);
  delay(100);

}
