/* 370_I2C
 *  
 * Testing I2C
 *  
 *   
 * _______
 * 
 * version history
 * 20_01_20: created
 */

const byte SERIAL_ENABLE = 1; //enables communication over USB

//some version of M370.h will be included in all your firmware
//it declares global variables and objects 
#include "M370.h"

//we can choose how fast to send analog sensors here
const int analogSendRate = 100;

//Sensor objects can have multiple kinds of arguments:
//argument 1 is the physical pin on the PCB
//argument 2 is the OSC address of the sensor
//argument 3 (optional) is how fast the data is sent in MS
//argument 4 is oversampling (val from 1 to 32)
//argument 5 is have to process oversampling 
Sensor button_0( BUTTON_0,"/button/0", 25, 16, MIN );
Sensor button_1( BUTTON_1,"/button/1", 25, 16, MIN );
Sensor analog_0( p0,"/analog/0", analogSendRate, 8, MEDIAN );
Sensor analog_1( p1,"/analog/1", analogSendRate, 8, MEDIAN );
Sensor analog_2( p2,"/analog/2", analogSendRate, 8, MEDIAN );
Sensor analog_3( p3,"/analog/3", analogSendRate, 8, MEDIAN );
Sensor analog_4( p4,"/analog/4", analogSendRate, 8, MEDIAN );
Sensor analog_5( p5,"/analog/5", analogSendRate, 8, MEDIAN );
Sensor analog_6( p6,"/analog/6", analogSendRate, 8, MEDIAN );
Sensor analog_7( p7,"/analog/7", analogSendRate, 8, MEDIAN );
Sensor analog_8( p8,"/analog/8", analogSendRate, 8, MEDIAN );
Sensor analog_9( p9,"/analog/9", analogSendRate, 8, MEDIAN );


/*********************************************
SETUP
*********************************************/
void setup() {
  //For now we will be using a USB cable to send data to our PC using Serial
  if( SERIAL_ENABLE) SerialSetup();

  button_0.setup();
  button_1.setup();
  analog_0.setup();
  analog_1.setup();
  analog_2.setup();
  analog_3.setup();
  analog_4.setup();
  analog_5.setup();
  analog_6.setup();
  analog_7.setup();
  analog_8.setup();
  analog_9.setup();
  
}

/*********************************************
LOOP
*********************************************/
void loop() {
  curMillis = millis();
  button_0.loop();
  button_1.loop();
  analog_0.loop();
  analog_1.loop();
  analog_2.loop();
  analog_3.loop();
  analog_4.loop();
  analog_5.loop();
  analog_6.loop();
  analog_7.loop();
  analog_8.loop();
  analog_9.loop();

  CheckSerial();
}
