#ifndef _pinDefs_h
#define _pinDefs_h

#include  "Arduino.h"

//array of analog pins 
 // array of ESPpins
const byte espPin[] = {32,36,39,35,33,34, //analog inputs 0-5
  13,14,25,26,27,4,0,15, //digital pins 6-13
  18,19,23,2,12,21,22, //SPI and I2C digital inputs
  5,16,17 //MIDI, UART
  };

//analog input pins - no pullup resistor
const byte p0 = 32;
const byte p1 = 36;
const byte p2 = 39;
const byte p3 = 35;
const byte p4 = 33;
const byte p5 = 34;

//digital input pins
const byte p6 = 13;
const byte p7 = 14;
const byte p8 = 25;
const byte p9 = 26;
const byte p10 = 27;
const byte p11 = 4;
const byte p12 = 0;
const byte p13 = 15;

//MUX and SPI control pins
const byte pMISO = 19;
const byte pMOSI = 23;
const byte pCLK = 18;
const byte pCS0 = 2; 
const byte pCS1 = 12;
const byte MUX_PINS[] = {18,19,23};
const  byte pSDA=21;
const  byte pSCL=22;

#endif
