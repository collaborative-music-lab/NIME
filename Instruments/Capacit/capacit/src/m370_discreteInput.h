// #ifndef _DISCRETE_INPUT_H
// #define _DISCRETE_INPUT_H
// #include "Arduino.h"

// /******************************
// Class for digital inputs
// ******************************/

// class m370_discreteInput{
//   public: 
//   String name = "none"; 
//   byte enable = 1;
//   byte invert=1;

//   //constructors
//   m370_discreteInput();
//   m370_discreteInput(int _interval);
//   m370_discreteInput(int _interval, uint32_t _resolution);

//   void begin();
//   uint8_t loop();
//   void SetInterval(uint16_t val);
//   uint8_t available();
//   uint8_t getState();

//   private:
//   void pushed();
//   void  released();
//   byte _available=0;

//   uint32_t timer=0;
//   uint32_t interval = 1000;

//   byte resolution = 16;
//   uint32_t button_history = 0;
//   uint32_t onPattern;
//   uint32_t offPattern;
//   uint32_t resolutionMask;

//   enum availStates{UP,DOWN,PUSHED,RELEASED};
//   availStates curState;
// };//DigitalIn class

// #endif