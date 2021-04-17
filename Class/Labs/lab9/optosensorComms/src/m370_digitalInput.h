#ifndef _DIGITAL_INPUT_
#define _DIGITAL_INPUT_
#include "Arduino.h"
//#include "m370_discreteInput.h"

/******************************
Class for digital inputs
******************************/

class m370_digitalInput{
  public: 
  String name = "none"; 
  byte enable = 0;
  byte invert=1;

  //m370_discreteInput sampler  = m370_discreteInput();
  //constructors
  m370_digitalInput(byte _pin);
  m370_digitalInput(byte _pin, int _interval);
  m370_digitalInput(byte _pin, int _interval,  String _address );
  m370_digitalInput(byte _pin, int _interval,  String _address, uint32_t _resolution);

  void begin();
  uint8_t loop();
  void SetInterval(uint16_t val);
  uint8_t available();
  uint8_t getState();

  private:
  void pushed();
  void  released();
  byte _available=0;

  byte pin = 22;
  uint32_t timer=0;
  uint32_t interval = 1000;

  byte resolution = 16;
  uint32_t button_history = 0;
  uint32_t onPattern;
  uint32_t offPattern;
  uint32_t resolutionMask;

  enum availStates{UP,DOWN,PUSHED,RELEASED};
  availStates curState;
};//DigitalIn class

#endif