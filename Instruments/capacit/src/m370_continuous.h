#ifndef _M370_CONTINUOUS_h
#define _M370_CONTINUOUS_h
#include "Arduino.h"
#include "m370_listProcessing.h"
 
///******************************
//Stores incoming values in a buffer at a specified sampling rate in Hertz. Returns the buffer and buffer size.
////Typically used to store samples from an ADC (local or via I2C, etc.)
//all values stored as int32_t
//max buffer size of 256

//previously allowed the buffer size to be dynamically set. Due to conflicts  between this and
//the I2C communication  from the MPR121  library the buffer size was set at 256 (although the 
//eeffective buffer size is still variable) 
//******************************/

class m370_continuous{
  public:

  m370_continuous();
  m370_continuous(int _frequency);
  m370_continuous(int _frequency, byte _size);

  byte sample(uint16_t (*samplingFunction)(uint8_t num), uint8_t num);
  void begin();
  void SetFrequency(uint16_t interval);
  int available();
  void SetSize(byte  _size);
  //byte m370_continuous::getBuffer(uint32_t bufToWrite[])
  uint32_t getVal();
  uint32_t getVal(listProcessType _process);

  private:
  int32_t buffer[256]; 
  byte size = 16;
  uint32_t timer = 0;
  uint32_t interval=20000;
  byte index;
};

#endif
