/*general_protocol
 * 
 * arduino sketch for use with an ESP32, sending data to a PC
 * or a raspberry pi.
 * 
 * Ian Hattwick
 * Fred Kelly
 * Massachusetts Institute of Technology, 2019
 * _______
 * 
 * define whether to send data over serial or wifi using wifiEnable and serialEnable
 * - these will be set by physical switches later
 * - the same data is sent over both interfaces (except for the debugging serial
 *   information)
 *   
 * _______
 * 
 * version history
 * 07_30: test patch, sends test data over both wifi and serial
 */

//generic function for finding the size of an array
#define ARRAY_SIZE(x)   (sizeof(x) / sizeof(x[0]))

#include <WiFi.h>
#include <WiFiUdp.h>

const byte LED_PIN = 22;
byte led_val = 0;
byte wifiEnable = 1;
byte serialEnable = 1;

byte WifiSend();

void setup() {
  pinMode( LED_PIN, OUTPUT);
  
  if( serialEnable)SerialSetup();
  if( wifiEnable ) WiFiSetup();
  MsgsSetup();
}

void loop() {
  led_val = !led_val;
  digitalWrite(LED_PIN, led_val);

  static uint16_t testVal[64] = {0,1,2 };
  
  byte state = WifiSend( testVal, ARRAY_SIZE(testVal) );
  byte serialSstate = SerialSend( testVal, ARRAY_SIZE( testVal) );
  
 //WiFiLoop();
 
  testVal[0]++;
  delay( 200 ); 
}
