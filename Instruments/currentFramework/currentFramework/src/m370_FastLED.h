/*
m370_FastLED

uses FastLED library to communicate with addresable RGB leds.
 * 
 requires the fastLED library be installed
 - in arduino, go to sketch->include library->manage library and search for FastLED by Daniel Garcia

 */

#ifndef M370FASTLED_h
#define M370FASTLED_h
#include "Arduino.h"
#include <FastLED.h>


/************************
**LED class
************************/

CRGB leds[NUM_LEDS];

void beginLeds(){

	FastLED.addLeds<WS2811, DATA_PIN, RGB>(leds, NUM_LEDS);

}

void writeOneLed(byte num,byte r, byte g, byte b){
	leds[num] = CRGB(r,g,b);
}

void showLeds(){
	FastLED.show();
}



// class m370_FastLED{
// 	public:
// 	m370_FastLED();
// 	m370_FastLED(comModes _mode); //communication mode as enum : {SERIAL, AP_WIFI, STA_WIFI, APandSERIAL, STAandSERIAL};
// 	m370_FastLED(comModes _mode, uint16_t size); //buffer sizes in bytes, def:64

	
// 	private:
// 	void Init(uint16_t size);
// 	void pack(byte val);
// 	void slipOut(byte val);
	
// };

#endif
