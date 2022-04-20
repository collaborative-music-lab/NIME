#ifndef _pinDefs_h
#define _pinDefs_h

#include  "Arduino.h"


//array of analog pins 
 // array of ESPpins
const byte espPin[] = {27,33,32,14,4,0,15,13,36,39, //analog inputs
  18,19,23,21,22,5, //SPI and I2C digital inputs
  2,12,34,35,25,26 //alternate  analog  inputs
  };
//virtual pin addresses for _MPR121
const byte capPins[] = {64,65,66,67,68,69,70,71,72,73,74,75};

//main row of input pins
const byte p0 = 27;
const byte p1 = 33;
const byte p2 = 32;
const byte p3 = 14;
const byte p4 = 4;
const byte p5 = 0;
const byte p6 = 15;
const byte p7 = 13;

//special analog pins with (possibly) lower noise?
const byte p8 = 36;
const byte p9 = 39;
//alternate names
const byte AN0 = 36;
const byte AN1 = 39;

//MUX and SPI control pins
const byte pMISO = 19;
const byte pMOSI = 23;
const byte pCLK = 18;
const byte pCS0 = 2; //also present on MIDI jack
const byte pCS1 = 12;
const byte MUX_PINS[] = {18,19,23};
const  byte pSDA=21;
const  byte pSCL=22;

//LED and buttons on PCB
const byte LED = 13;
const byte BUTTON_0 = 34;
const byte BUTTON_1 = 35;

//3.5mm jacks
const byte euroGate = 0;
const byte euroClock= 2;
const byte dac1 = 25; //tip
const byte dac2 = 26; //ring
const byte dac1in = 36;
const byte dac2in = 39;
const byte MIDI = 5; //tip
const byte MIDI_5v = 2; //must be set high for MIDI use
//note this jack puts out 5v due to level translator

#endif
