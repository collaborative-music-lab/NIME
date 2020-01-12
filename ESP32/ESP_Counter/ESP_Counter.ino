void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  static byte count = 48;

  Serial.write(count);
  count++;
  delay(250);
}
