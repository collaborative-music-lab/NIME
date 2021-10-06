/* 
Basic use of controlVoltage library to implement a trigger and ramp CV
- trigger duration is 3ms by default
- the ramp CV is updated at the same time as the trigger (100ms interval)
- uses cv(val, rampTime) to smooth the transition between CV values
- basically, a slew limiter

Every controlVoltage object has three functions:
- get() returns the current sample
- loop() generates a new sample once the previous sample is read
- some other function to create a CV event. possibilities include:
  - trigger()
  - gate(int val ) - static gate signal, outputs HIGH if val>0 else LOW
  - timedGate( int length ) - HIGH for length ms, then LOW
  - cv(int val) - static cd
  - cv(int val, int rampTime) slew limited CV
  - AR(int attack, int release) - attack release envelope
  - midi( byte val ) - quantized CV output (1000/octave), with val defined as a midi note
   
Monitor in Arduino's serial plotter
*/
#include "pinDefs.h"

const byte NUM_INPUTS = 3;

void setup(){
  Serial.begin(115200);  // initialize serial interface for print()

  for(int i=0;i<NUM_INPUTS;i++) pinMode(espPin[i], INPUT);
  //Serial.println("controlVoltage trigger example");
}



void loop(){

  //monitor output at signal rate
  static uint32_t signalTimer = 0;
  int signalInterval = 1;
  if(millis()-signalTimer>signalInterval){
    signalTimer = millis();

    for(int i=0;i<NUM_INPUTS-1;i++){
      //Serial.print("cv:");
      Serial.print( analogRead( espPin[i] ) );
      Serial.print(",");
    }
    Serial.print( analogRead( espPin[NUM_INPUTS-1] ) );
    Serial.print(",");
    Serial.println(1500);
  }
}
