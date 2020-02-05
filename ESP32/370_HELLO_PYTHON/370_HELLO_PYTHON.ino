/* 370_HELLO_PYTHON
 *  
 *  Test communication between your ESP32 and python.
 *  
 *  The associated python script with this is:
 *  370_HELLO_ESP32
 *  
 *  Upload this firmware to your ESP32 and it will automatically begin
 *  streaming the following data to python:
 *  - button 0 and button 1
 *  - analog inputs 0 and 1
 *  
 *  Python will print these values to the Python console
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

//Sensor objects can have multiple kinds of arguments:
//argument 1 is the physical pin on the PCB
//argument 2 is the OSC address of the sensor
//argument 3 (optional) is how fast the data is sent in MS
Sensor button_0( BUTTON_0,"/button/0" );
Sensor button_1( BUTTON_1,"/button/1" );
Sensor analog_0( p0,"/analog/0", 250 );
Sensor analog_1( p1,"/analog/1", 250 );


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
}
