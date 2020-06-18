// based on https://github.com/igorantolic/ai-esp32-rotary-encoder
// which was itself based on https://github.com/marcmerlin/IoTuz code - extracted and modified Encoder code
// 
// 

#include "Esp32Encoder.h"

void IRAM_ATTR Esp32Encoder::readEncoder_ISR()
{	
	portENTER_CRITICAL_ISR(&(this->mux));

	this->old_AB <<= 2;                   //remember previous state
 this->old_AB;
	int8_t ENC_PORT = (
	  (digitalRead(this->encoderBPin)) ? (1 << 1) : 0) + 
	  ((digitalRead(this->encoderAPin)) ? (1 << 0) : 0
	  );
	this->old_AB |= ( ENC_PORT & 0x03 );  //add current state
	this->encoder0Pos += ( this->enc_states[( this->old_AB & 0x0f )]);		
	portEXIT_CRITICAL_ISR(&(this->mux));
}//readEncoder_ISR

Esp32Encoder::Esp32Encoder(uint8_t _APin, uint8_t _BPin, uint8_t _ButtonPin, uint8_t _divider)
{
	this->old_AB = 0;
	
	this->encoderAPin = _APin;
	this->encoderBPin = _BPin;
	this->encoderButtonPin = _ButtonPin;
  this->divider = _divider;
	pinMode(this->encoderAPin, INPUT);
	pinMode(this->encoderBPin, INPUT);

}//Esp32Encoder

//Esp32Encoder::Esp32Encoder(uint8_t _APin, uint8_t _BPin, uint8_t _ButtonPin, uint8_t _divider)
//{
//  this->old_AB = 0;
//  
//  this->encoderAPin = _APin;
//  this->encoderBPin = _BPin;
//  this->encoderButtonPin = _ButtonPin;
//  this->divider =_divider;
//  pinMode(this->encoderAPin, INPUT);
//  pinMode(this->encoderBPin, INPUT);
//
//}//Esp32Encoder


int16_t Esp32Encoder::readEncoder()
{
  int  out =  this->encoder0Pos;
  this->encoder0Pos = 0;
	return (out);
}

int16_t Esp32Encoder::delta() {   return (readEncoder()); }

int32_t Esp32Encoder::count()
{
  int encoderDelta = readEncoder();
  if (encoderDelta == 0) return _count ;
  int prevRaw = _raw;
  _raw+=encoderDelta;
  if(  abs(_raw) > this->divider-1 || (abs(_raw)-abs(prevRaw)<0)){
    _raw=0;
    encoderDelta > 0 ? this->_count++ : this->_count--;
  }
  return (this->_count);
}

int16_t Esp32Encoder::encoderChanged() 
{
	int16_t _encoder0Pos = readEncoder();
	
	int16_t encoder0Diff = _encoder0Pos - this->lastReadEncoder0Pos;

	this->lastReadEncoder0Pos = _encoder0Pos;
	return encoder0Diff;
}//readEncoder

void Esp32Encoder::begin(void (*ISR_callback)(void))
{
	this->previous_butt_state = 0;
	pinMode(this->encoderButtonPin, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(encoderAPin), ISR_callback, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoderBPin), ISR_callback, CHANGE);
}//begin

ButtonState Esp32Encoder::button()
{
	uint8_t butt_state = !digitalRead(this->encoderButtonPin);

  if( butt_state != this->previous_butt_state ){
     this->previous_butt_state = butt_state;
     switch(butt_state){
      case 1: return  BUT_PUSHED;
      case 0: return BUT_RELEASED;
     }
  }else {
    switch(butt_state){
      case 0: return  BUT_DOWN;
      case 1: return BUT_UP;
     }
  }
}//button
