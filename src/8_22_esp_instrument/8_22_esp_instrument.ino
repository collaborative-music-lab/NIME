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

int runAvgBuf0[64];
int runAvgBuf1[64];
int runAvgBuf2[64];

int curTime = 0;
int lastTimeBtn0 = 0;
int lastTimeBtn1 = 0;
int lastTimeBtn2 = 0;
int lastTimeFdr0 = 0;
int lastTimeFdr1 = 0;
int lastTimeFdr2 = 0;

int oversample(int adcPin, int numSamples) {
  int total = 0;
  for (int i = 0; i < numSamples; i++) {
    total += analogRead(adcPin);
  }
  return total / numSamples;
}

int runningAverage(int adcPin, int buf[], int bufferSize) {
  int avgs = 0;
  static int index;
  int curReading = analogRead(adcPin);
  if (index >= bufferSize) {
    index = 0;
  }
  buf[index] = curReading;
  for (int i = 0; i < bufferSize; i++) {
    avgs = avgs + buf[i];
  }
  index++;
  return avgs / bufferSize;
}

void setup() {
  if( serialEnable)SerialSetup();
  if( wifiEnable ) WiFiSetup();
  MsgsSetup();
 
}

void loop() {
  curTime = millis();
  pinMode(btnPin0, INPUT_PULLUP);
  pinMode(btnPin1, INPUT_PULLUP);
  pinMode(btnPin2, INPUT_PULLUP);
  potValue0 = runningAverage(potPin0, runAvgBuf0, 64);
  potValue1 = runningAverage(potPin1, runAvgBuf1, 64);
  potValue2 = runningAverage(potPin2, runAvgBuf2, 64);
  btnValue0 = digitalRead(btnPin0);
  btnValue1 = digitalRead(btnPin1);
  btnValue2 = digitalRead(btnPin2);
  sendButtonMessage(0, 0, btnValue0, 100, lastTimeBtn0);
  sendButtonMessage(0, 1, btnValue1, 400, lastTimeBtn1);
  sendButtonMessage(0, 2, btnValue2, 1000,lastTimeBtn2);
  sendFaderMessage(0, 0, potValue0, 50, lastTimeFdr0);
  sendFaderMessage(0, 1, potValue1, 400, lastTimeFdr1);
  sendFaderMessage(0, 2, potValue2, 1000, lastTimeFdr2);
}
