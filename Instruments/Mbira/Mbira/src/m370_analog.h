#ifndef _M370_ANALOG_h
#define _M370_ANALOG_h
#include "Arduino.h"
#include "m370_continuous.h"
#include "m370_listProcessing.h"

enum sensorType { analog, digital, touch };


  uint16_t digitalRead16form370Analog(byte _pin); //returns a digitalRead cast as uint16_t

class m370_analog{
  public:
  

  byte enable = 0;
  String name = "none";

  m370_continuous analogSampler = m370_continuous(frequency,bufferSize);

  m370_analog(byte _pin);
  m370_analog(byte _pin, int _frequency);
  m370_analog(byte _pin, int _frequency, String _name);
  m370_analog(byte _pin, int _frequency, String _name, sensorType _mode);
  m370_analog(byte _pin, int _frequency, String _name, sensorType _mode, byte _size);
  int32_t getVal();
  int32_t getVal(listProcessType _mode);
  byte loop();
  void begin();
  byte available();
  uint16_t frequency = 100;
  sensorType mode = analog;

  // uint16_t digitalRead16(byte _pin);

  private:
  int32_t *val; 
  byte pin;
  byte bufferSize = 32;
};

#endif
