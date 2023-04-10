/* m370_lbr.h
 * 
 * Header file for 21M.370 ESP32 library
 * 
 * Sections:
 * - sublibrary  includees
 * - pin mappings
 * - global variables
 * - function prototypes if necessary
 * - object definitions
 * 
 * NOTE:
 * ESP32 pins 21 and 22 used for I2C
 * - pin 22 is also built in LED on ESP32
 */

 //array of analog pins 
 // array of ESPpins

#ifndef m370_lbr_h
#define m370_lbr_h
 
#include <Arduino.h>
#include <Wire.h>
// #include <WiFi.h>
// #include <WiFiUdp.h>

#include "pinDefsv5.h"
#include "src/m370_communication.h"
#include "src/m370_digitalInput.h"
#include "src/LSM6.h"
#include "src/Esp32Encoder.h"

void  debug(String name, int val){
	Serial.print(name);
	Serial.print(" ");
	Serial.println(val);
}

void  debug2(String name, int val1, int val2){
	Serial.print(name);
	Serial.print(" ");
	Serial.print(val1);
	Serial.print(" ");
	Serial.println(val2);
}
void  debug3(String name, int val1, int val2,int val3){
	Serial.print(name);
	Serial.print(" ");
	Serial.print(val1);
	Serial.print(" ");
	Serial.print(val2);
	Serial.print(" ");
	Serial.println(val3);
}

#endif
