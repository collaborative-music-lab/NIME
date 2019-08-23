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

#include <WiFi.h>
#include <WiFiUdp.h>

byte led_val = 0;
byte wifiEnable = 1;
byte serialEnable = 1;
byte WifiSend();


const byte LED_PIN = 22;
const int potPin0 = 37;
const int potPin1 = 38;
const int potPin2 = 34;
const int btnPin0 = 19;
const int btnPin1 = 22;
const int btnPin2 = 21;

int potValue0 = 0;
int potValue1 = 0;
int potValue2 = 0;
int btnValue0 = 0;
int btnValue1 = 0;
int btnValue2 = 0;

void setup() {
  if( serialEnable)SerialSetup();
  if( wifiEnable ) WiFiSetup();
  MsgsSetup();
  pinMode(btnPin0, INPUT_PULLUP);
  pinMode(btnPin1, INPUT_PULLUP);
  pinMode(btnPin2, INPUT_PULLUP);
}

void loop() {
  potValue0 = analogRead(potPin0);
  potValue1 = analogRead(potPin1);
  potValue2 = analogRead(potPin2);
  btnValue0 = digitalRead(btnPin0);
  btnValue1 = digitalRead(btnPin1);
  btnValue2 = digitalRead(btnPin2);
  sendButtonMessage(0, 0, btnValue0);
  sendButtonMessage(0, 1, btnValue1);
  sendButtonMessage(0, 2, btnValue2);
  sendFaderMessage(0, 0, potValue0);
  sendFaderMessage(0, 1, potValue1);
  sendFaderMessage(0, 2, potValue2);
  delay(50);
}
