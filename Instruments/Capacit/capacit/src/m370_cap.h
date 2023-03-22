#ifndef _m370_cap_h
#define _m370_cap_h
#include "Arduino.h"
#include "m370_listProcessing.h"


class m370_cap{
  public:

  byte enable = 0;
  String name = "cap";

  m370_cap();
  m370_cap(byte num);
  m370_cap(byte num, int _frequency);
  m370_cap(byte num, int _frequency, String _name);
  m370_cap(byte num, int _frequency, String _name, byte _size);

  void SetFrequency(uint16_t _frequency);
  void SetChargeCurrent(byte _current);
  void SetChargeTime(byte _chargeTime);
  
  int16_t getVal(byte _num);
  int16_t getVal(byte _num, listProcessType _mode);
  
  int16_t getRaw(byte _num);
  //int16_t getVal(byte _num);
  int16_t getProximity();
  byte loop();
  void begin();
  byte available(byte _num);
  byte touchAvailable(byte _num);

  private:
  //list _m370_listProcessing();

  int16_t capData(byte _num);

  
  int32_t *filteredBuffer[12]; 
  int32_t *baselineBuffer[12];
  int32_t curFiltered[12];
  int32_t curBaseline[12];
  int32_t index[12];
  uint32_t prevTouchVal = 0;
  byte isTouched[12];
  
  byte bufferSize = 32;
  byte numCapSensors = 12;
  byte isAvailable[12];
  byte isTouchAvailable[12];

  uint32_t timer;
  uint32_t touchTimer;
  uint32_t interval = 25000;
  uint32_t touchInterval = 10000;
  byte cur=0;
};

#endif
