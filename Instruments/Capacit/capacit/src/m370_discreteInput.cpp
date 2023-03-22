
// /******************************
// Class for digital inputs
// ******************************/

// #include "m370_discreteInput.h"

// //constructors
// m370_discreteInput::m370_discreteInput(byte _pin) : 
//   pin(_pin)
// {}

// m370_discreteInput::m370_discreteInput(byte _pin, int _interval) : 
//   pin(_pin)
// {SetInterval(_interval);}

// m370_discreteInput::m370_discreteInput(byte _pin, int _interval, String _name) : 
//   pin(_pin), 
//   name(_name)
// {SetInterval(_interval);}

// m370_discreteInput::m370_discreteInput(byte _pin, int _interval, String _name, uint32_t _resolution) : 
//   pin(_pin), 
//   name(_name),
//   resolution (_resolution>31 ? 31  : _resolution<3 ? 3 : _resolution)
// {SetInterval(_interval);}

// void m370_discreteInput::begin(){

//   resolutionMask = (1<<resolution)-1;
//   onPattern = (1<<(resolution-1))-1;
//   offPattern = 1 << (resolution-1);
//   // Serial.println(resolutionMask,BIN);
//   // Serial.println(onPattern,BIN);
//   // Serial.println(offPattern,BIN);

//   pinMode(pin, INPUT);
//   digitalRead(pin)==1 ? curState=DOWN : curState=UP;
//   curState==DOWN ? button_history=onPattern : button_history=offPattern;
// }

// uint8_t m370_discreteInput::loop(){
//   if (enable==1) {
//     //check whether to check input in this loop
//     byte run=0;
//     if(interval==0) run=1;
//     else if(micros() - interval > timer){
//       timer = micros();
//       run=1;
//     }

//     if(run){
//       byte curReading = digitalRead(pin);
//       invert ?  curReading=!curReading : curReading;
//       button_history = (button_history<<1) + curReading;
//       button_history  &= resolutionMask;
//       if(button_history == onPattern ) released();
//       else if (button_history == offPattern ) pushed();
//     }//run

//   }//enable
//   return _available;
// }//loop

// void m370_discreteInput::pushed(){
//   curState = PUSHED;
//   _available=1;
//   //Serial.println("pusj");
// }

// void  m370_discreteInput::released(){
//   curState=RELEASED;

//   //Serial.println("release");
//   _available=1;
// }

// uint8_t m370_discreteInput::available(){  return _available; }

// uint8_t m370_discreteInput::getState(){ 
//   _available=0;
//   //Serial.print(curState);
//   curState==RELEASED ? curState=UP : curState==PUSHED ? curState=DOWN : 0;
//   //Serial.println(curState);
//   if( curState==DOWN ) return 0;
//   else return 1;
// }

// void m370_discreteInput::SetInterval(uint16_t val){
//   val==0 ? interval = 0 : interval = 1000000/val; //in hertz
// }
