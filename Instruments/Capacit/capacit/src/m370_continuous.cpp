#include "m370_continuous.h"

///******************************
//Stores values samples in a buffer at a specified sampling rate in Hertz. Returns the buffer and buffer size.
//Typically used to store samples from an ADC (local or via I2C, etc.)
//all values stored as int32_t
//******************************/


/******************CONSTRUCTORS*****************/
m370_continuous::m370_continuous() {}

m370_continuous::m370_continuous(int _frequency) 
{SetFrequency(_frequency);}


m370_continuous::m370_continuous(int _frequency, byte _size) :
size((int)_size+1)
{SetFrequency(_frequency);}

/******************MAIN*****************/
void m370_continuous::begin(){
  //buffer =  new int32_t[size];
}

byte m370_continuous::sample(uint16_t (*samplingFunction)(uint8_t num), uint8_t num){
  if(micros() - timer > interval){
    timer = micros();

    buffer[index] = samplingFunction(num);
    //uint32_t test = samplingFunction(num);
    ++index < size ? index : index=0;
  }
  return index;
}//loop


/******************FUNCTIONS*****************/

void m370_continuous::SetFrequency(uint16_t _frequency){
  if(_frequency==0) _frequency=20000;
  interval= 1000000/_frequency;
}

void m370_continuous::SetSize(byte _size) {size = _size; }

int m370_continuous::available(){ return index; }

uint32_t m370_continuous::getVal(listProcessType process){
  uint32_t outVal = 0;
  if(index>0) outVal = applyListProcess(process,buffer,index);
  index=0;
  return outVal;
} 


