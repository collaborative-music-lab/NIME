#define ARRAY_SIZE(x)   (sizeof(x) / sizeof(x[0]))

#include <WiFi.h>
#include <WiFiUdp.h>

const byte LED_PIN = 22;
byte led_val = 0;
byte wifiEnable = 1;
byte serialEnable = 1;

byte WifiSend();

void setup() {
  if( serialEnable)SerialSetup();
  if( wifiEnable ) WiFiSetup();
  MsgsSetup();
}

void loop() {
  led_val = !led_val;
  digitalWrite(LED_PIN, led_val);

  static byte testVal[] = {0,1,2 };
  //byte state = WifiSend( testVal, ARRAY_SIZE(testVal) );
  
 WiFiLoop();
 
  testVal[0]++;
  delay( 200 ); 
}
