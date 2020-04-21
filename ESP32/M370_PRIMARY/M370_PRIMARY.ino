/* M370_PRIMARY
 *  
 *  Main m370 firmware for ESP32
 * _______
 * 
 * version history
 * 20_04_20: added analog debugging - prints analogRead values to console
 * 20_04_20: added support for wifi
 * 20_04_12: added ultrasonic support
 *           commented out MPR121 on line 88. 
 *           You can uncomment if you want to use it
 *           may cause your ESP32 to crash - but try it!
 * 20_04_01: added MPR121 functions
 * 20_03_25: added array notation and input
 * 20_01_20: created
 */

#include <Wire.h>
#include "Adafruit_MPR121.h"
#include "NewPing.h"
#include <WiFi.h>
#include <WiFiUdp.h>

byte SERIAL_ENABLE = 1; //enables communication over USB
byte WIFI_ENABLE = 0; //enables communication over USB

// WiFi network name and password:
const char * ssid = "MLE";
const char * password = "mitmusictech";

const byte SERIAL_DEBUG = 0; //for debugging serial communication over USB
const byte WIFI_DEBUG = 0; //for debuggiing wifi communiication
const byte ANALOG_DEBUG = 0; //for debuggiing analog inputs using arduino console 

//some version of M370.h will be included in all your firmware
//it declares global variables and objects 
#include "M370.h"

/*********************************************
CAPACITIVE SETUP
*********************************************/
//declare MPR121 object
Adafruit_MPR121 _MPR121 = Adafruit_MPR121();

byte chargeCurrent = 63; //from 0-63, def 63
byte chargeTime = 1; //from 0-7, def 1
byte NUM_ELECTRODES = 0;
int capSenseInterval = 100;

Cap capSense[12] ={
  Cap ( capSenseInterval ),
  Cap ( capSenseInterval ),
  Cap ( capSenseInterval ),
  Cap ( capSenseInterval ), //4
  Cap ( capSenseInterval ), 
  Cap ( capSenseInterval ),
  Cap ( capSenseInterval ),
  Cap ( capSenseInterval ),//8
  Cap ( capSenseInterval ),
  Cap ( capSenseInterval ),
  Cap ( capSenseInterval ),
  Cap ( capSenseInterval ) //12
};

/*********************************************
ANALOG SETUP
*********************************************/
//we can choose how fast to send analog sensors here
int analogSendRate = 250;

//Sensor objects can have multiple kinds of arguments:
//argument 1 is the physical pin on the PCB
//argument 2 is the OSC address of the sensor
//argument 3 (optional) is how fast the data is sent in MS
//argument 4 is oversampling (val from 1 to 32)
//argument 5 is how to process oversampling 
const byte numSensors = 12;

Sensor sensors[12] = {
  Sensor ( p0,"/analog/0", analogSendRate, 8, MEAN ),
  Sensor ( p1,"/analog/1", analogSendRate, 8, MEAN ),
  Sensor ( p2,"/analog/2", analogSendRate, 8, MEAN ),
  Sensor ( p3,"/analog/3", analogSendRate, 8, MEAN ),
  Sensor ( p4,"/analog/4", analogSendRate, 8, MEAN ),
  Sensor ( p5,"/analog/5", analogSendRate, 8, MEAN ),
  Sensor ( p6,"/analog/6", analogSendRate, 8, MEAN ),
  Sensor ( p7,"/analog/7", analogSendRate, 8, MEAN ),
  Sensor ( p8,"/analog/8", analogSendRate, 8, MEAN ),
  Sensor ( p9,"/analog/9", analogSendRate, 8, MEAN ),
  Sensor ( BUTTON_0,"/button/0", 250, 16, MIN ),
  Sensor ( BUTTON_1,"/button/1", 250, 16, MIN)
};


/*********************************************
SETUP
*********************************************/
void setup() {
  //Be sure to select  either USB or WiFi using enables at top of script
  SerialSetup();
  WiFiSetup();

  //MPR121setup(); <- UNCOMMENT TO USE MPR121
  //MPR121test(); //comment out for normal use
  
  for(byte i=0;i< numSensors; i++) sensors[i].setup();
  
}

/*********************************************
LOOP
*********************************************/
void loop() {
  curMillis = millis();
  
  for(byte i=0;i < numSensors; i++) sensors[i].loop();
  //for(byte i=0;i < NUM_ELECTRODES; i++) capSense[i].loop(i);

  //sendCapValues();
  WiFiLoop();
  CheckSerial();
  
  //testData();
  if(WIFI_DEBUG) pingMe();
}

/*********************************************
ADDITIONAL FUNCTIONS
*********************************************/

void sendCapValues(){
  static uint32_t timer = 0;
  int interval = 50;

  if(millis()-timer>interval){
    timer = millis();
  
    totalCapacitance = 4096;
    //make sure totalCap >= 0
    for(byte i=0;i < NUM_ELECTRODES; i++) totalCapacitance += (capSense[i].outVal-4096);
    SlipOutByte(101);
    SlipOutInt(totalCapacitance);
    SerialOutSlip();
  }
}
