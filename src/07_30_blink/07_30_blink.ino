#define ARRAY_SIZE(x)   (sizeof(x) / sizeof(x[0]))

#include <WiFi.h>
#include <WiFiUdp.h>

const byte LED_PIN = 22;
byte led_val = 0;
byte wifiEnable = 1;
byte serialEnable = 1;

byte WifiSend();

void setup() {
  pinMode(LED_PIN, OUTPUT);
  
  Serial.begin( 115200 );
  digitalWrite(LED_PIN, 1);
  delay(200);
  digitalWrite(LED_PIN, 0);
  delay(200);
}

void loop() {
  led_val = !led_val;
  digitalWrite(LED_PIN, led_val);

  delay( 200 ); 
}
