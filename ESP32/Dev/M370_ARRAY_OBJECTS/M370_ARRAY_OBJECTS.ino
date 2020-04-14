/* 370_ARRAY_OBJECTS
 *  
 * Instantiates sensors as an array, and enables changing settings remotely: 
 * - enable (0/1)
 * - data rate (MS)
 * - oversampling (TODO)
 * - data type/processing (TODO)
 *   
 * _______
 * 
 * version history
 * 21_03_25: added array notation and input
 * 20_01_20: created
 */

const byte SERIAL_ENABLE = 1; //enables communication over USB
const byte SERIAL_DEBUG = 0;

//some version of M370.h will be included in all your firmware
//it declares global variables and objects 
#include "M370.h"

//we can choose how fast to send analog sensors here
int analogSendRate = 25;

//Sensor objects can have multiple kinds of arguments:
//argument 1 is the physical pin on the PCB
//argument 2 is the OSC address of the sensor
//argument 3 (optional) is how fast the data is sent in MS
//argument 4 is oversampling (val from 1 to 32)
//argument 5 is how to process oversampling 
const byte numSensors = 12;

Sensor sensors[12] = {
  Sensor ( p0,"/analog/0", analogSendRate, 2, MEAN ),
  Sensor ( p1,"/analog/1", analogSendRate, 2, MEAN ),
  Sensor ( p2,"/analog/2", analogSendRate, 2, MEAN ),
  Sensor ( p3,"/analog/3", analogSendRate, 2, MEAN ),
  Sensor ( p4,"/analog/4", analogSendRate, 2, MEAN ),
  Sensor ( p5,"/analog/5", analogSendRate, 2, MEAN ),
  Sensor ( p6,"/analog/6", analogSendRate, 2, MEAN ),
  Sensor ( p7,"/analog/7", analogSendRate, 2, MEAN ),
  Sensor ( p8,"/analog/8", analogSendRate, 2, MEAN ),
  Sensor ( p9,"/analog/9", analogSendRate, 2, MEAN ),
  Sensor ( BUTTON_0,"/button/0", 25, 16, MIN ),
  Sensor ( BUTTON_1,"/button/1", 25, 16, MIN) 
};


/*********************************************
SETUP
*********************************************/
void setup() {
  //For now we will be using a USB cable to send data to our PC using Serial
  if( SERIAL_ENABLE) SerialSetup();

  for(byte i=0;i< numSensors; i++) sensors[i].setup();
  
}

/*********************************************
LOOP
*********************************************/
void loop() {
  curMillis = millis();
  
  for(byte i=0;i < numSensors; i++) sensors[i].loop();

  CheckSerial();
}
