#include "Esp32Encoder.h"
/*
Rotary encoder  library example

Three wo methods available to call:
- encoder.count() returns a 32-bit int counting pulses
  count has an optional inbuilt divider which only increments count after N pulses
  this is useful for detented encoders which have multiple pulses between detents
- delta() returns the raw number of pulses between calls
- button() returns state of encoder button
*/

//Esp32Encoder rotaryEncoder = Esp32Encoder(18,2,4);//A,B,Button
//optional divider argument:
Esp32Encoder rotaryEncoder = Esp32Encoder(18,2,4,4);//A,B,Button, Divider

//example of ESP32Encoder methods
void rotary_loop() {
  byte curB = rotaryEncoder.button(); //get current button state

  static int val  = 0;
  int prevVal = val;

  switch(curB){
    case 0: //DOWN
      val  = rotaryEncoder.count(); //get encoder  count
      if(val!= prevVal){
        Serial.print("count: ");
        Serial.println(val);
      }
    break;

    case 1: //PUSHED
    Serial.println("PUSHED");
    break;

    case 2: //UP
    val  = rotaryEncoder.delta(); //get encoder pulses
      if(val!= 0){
        Serial.print("delta: ");
        Serial.println(val);
      }
    break;

    case 3: //RELEASED
    Serial.println("RELEASED");
    break;
  }//switch
  ledcWrite(0, (val%32) *  8);
}//loop

void setup() {
	Serial.begin(115200);
  ledcAttachPin(0, 0);
  // Initialize channels
  // channels 0-15, resolution 1-16 bits, freq limits depend on resolution
  // ledcSetup(uint8_t channel, uint32_t freq, uint8_t resolution_bits);
  ledcSetup(0, 4000, 8); // 12 kHz PWM, 8-bit resolution
  
	rotaryEncoder.begin([]{rotaryEncoder.readEncoder_ISR();});
}

void loop() {
  //custom function calling encoder methods
  rotary_loop();
	
	delay(5);															 
}
