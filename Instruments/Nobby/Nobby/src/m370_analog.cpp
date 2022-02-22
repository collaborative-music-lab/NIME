#include "m370_analog.h"

///******************************
//OBJECT DEFINITIONS 
//pin: ESPpin number, int, e.g. Sensor[0].pin = 0
//name: string with the intended OSC name of the sensor, e.g. Sensor[0].name = "/joystick/x"
//frequency:  rate at  which readings of the sensor are taken
//******************************/
//

/******************CONSTRUCTORS*****************/
m370_analog::m370_analog(byte _pin) : 
pin  (_pin)
{}
m370_analog::m370_analog(byte _pin, int _frequency) : 
pin  (_pin),
frequency (_frequency)
{}

m370_analog::m370_analog(byte _pin, int _frequency, String _name) : 
pin  (_pin),
frequency (_frequency),
name(_name)
{}

m370_analog::m370_analog(byte _pin, int _frequency, String _name, sensorType _mode) : 
pin  (_pin),
frequency (_frequency),
name(_name),
mode (_mode)
{}

m370_analog::m370_analog(byte _pin, int _frequency, String _name, sensorType _mode, byte _size) : 
pin  (_pin),
frequency (_frequency),
name(_name),
mode (_mode),
bufferSize(_size)
{}

/******************MAIN*****************/
void m370_analog::begin(){
  enable=1;
  pinMode(pin,INPUT_PULLUP);
  analogSampler.begin();
  analogSampler.SetFrequency( frequency );
  analogSampler.SetSize( bufferSize );
}

byte m370_analog::loop(){
  byte _available=0;

  if (enable==1) {

      switch(mode){
        case analog:
        _available = analogSampler.sample(analogRead,pin);
        break;

        case digital:
       _available = analogSampler.sample(digitalRead16form370Analog,pin);
        break;

        case touch:
        //_available= analogSampler.sample(touchRead,pin);
        break;
      }
      
  }//enable
  return _available;
}//loop


/******************FUNCTIONS*****************/
int32_t m370_analog::getVal(){ 
  int32_t out = analogSampler.getVal(MEAN);
  return out; 
}

int32_t m370_analog::getVal(listProcessType _mode){  
  int32_t out = analogSampler.getVal(_mode);
  return out; 
}

byte m370_analog::available(){ return analogSampler.available(); }


uint16_t digitalRead16form370Analog(byte _pin) {
  //returns a digital read value  cast as uint16_t
  // Serial.print("d16: ");
  // Serial.println(digitalRead(_pin));
  return (uint16_t)digitalRead(_pin); 
}
