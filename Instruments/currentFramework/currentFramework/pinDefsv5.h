#ifndef _pinDefsv4_h
#define _pinDefsv4_h

#include  "Arduino.h"

 // array of ESPpins
const byte espPin[] = {32,36,39,35,33,34, //analog inputs
  13,14,25,26,27,0,15,4, //digital inputs
  19,23,18,2,12, //SPI
  21,22, //I2C
  16,17, //UART 2
  5 //MIDI
  };


//main row of input pins
const byte p0 = 32;
const byte p1 = 36;
const byte p2 = 39;
const byte p3 = 35;
const byte p4 = 33;
const byte p5 = 34;

const byte p6 = 13;
const byte p7 = 14;
const byte p8 = 25;
const byte p9 = 26;

const byte p10 = 27;
const byte p11 = 0;
const byte p12 = 15;
const byte p13 = 4;

//MUX and SPI control pins
const byte pMISO = 19;
const byte pMOSI = 23;
const byte pCLK = 18;
const byte pCS0 = 2; //also present on MIDI jack
const byte pCS1 = 12;
const byte MUX_PINS[] = {18,19,23};
const  byte pSDA=21;
const  byte pSCL=22;

#endif
