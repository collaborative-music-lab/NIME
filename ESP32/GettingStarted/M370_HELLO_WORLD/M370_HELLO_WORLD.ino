/* 370_HELLO_WORLD
 *  
 *  Test that your ESP32 is setup and ready to go.
 *  
 *  Open the Serial Monitor (Tools->Serial Monitor or click the button on the top right)
 *  Press a button and monitor the values in the serial monitor
 *  
 *  n.b. this patch is only intended for monitoring inside the Arduino IDE
 *   
 * _______
 * 
 * version history
 * 20_01_20: created
 */

const byte SERIAL_ENABLE = 1;

//some version of M370.h will be included in all your firmware
//it declares global variables and objects 
#include "M370.h"

Sensor button_0( BUTTON_0,"/button/0" );
Sensor button_1( BUTTON_1,"/button/1" );
Sensor analog_0( espPin[0],"/analog/0" );
Sensor analog_1( espPin[1],"/analog/1" );


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
