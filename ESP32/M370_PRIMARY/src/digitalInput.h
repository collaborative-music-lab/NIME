/******************************
Class for digital inputs
******************************/

class DigitalIn{
  public: 
  uint16_t interval = 500;
  byte enable = 1;
  byte state = 1;
  uint32_t button_history = 0;
  byte button_state = 0;
  byte overSample=1;
  byte pin = 22;



  //constructors
  DigitalIn(byte _pin, String _address) : 
    pin(_pin), 
    address(_address) 
  {}

  DigitalIn(byte _pin, String _address, int _interval) : 
    pin(_pin), 
    address(_address), 
    interval(_interval) 
  {}

  DigitalIn(byte _pin, String _address, int _interval, uint32_t _resolution) : 
    pin(_pin), 
    address(_address), 
    interval(_interval), 
    resolution((byte)_resolution)
  {    
    byteMask = ~(byte)(pow(2,_resolution/3)-1)<<(_resolution/4); 
  }

  void setup(){

    resolutionMask = (1<<resolution)-1;
    onPattern = (1<<(resolution-1))-1;
    offPattern = 1 << (resolution-1);

    Serial.print("button ");
    Serial.println(pin);
    Serial.print("resolution ");
    Serial.println(resolution);
    Serial.print("resolutionMask ");
    Serial.println(resolutionMask, BIN);
    Serial.print("onPattern ");
    Serial.println(onPattern, BIN);
    Serial.print("offPattern ");
    Serial.println(offPattern, BIN);
    Serial.println();

    pinMode(pin, INPUT);
  }

  void loop(){
    if (enable==1) {
 
      if(millis() - interval > prevMillis){
        prevMillis = millis();

        // Serial.print("button ");
        // Serial.print(pin);
        // Serial.print("\t");
        // Serial.print(digitalRead(pin));
        // Serial.println("\t");


        button_history = (button_history<<1)+digitalRead(pin);
        button_history  &= resolutionMask;
        if(button_history == onPattern ) released();
        else if (button_history == offPattern ) pushed();
        // else if(button_history ==0){}
        // else if (button_history == (1<<resolution)-1) {}
        //   else (Serial.println(button_history, BIN));

      }
    }
  }//loop

  void pushed(){
    Serial.print(pin);
    Serial.println(" pushed");
  }

  void  released(){
    Serial.print(pin);
    Serial.println(" released");
  }

  void SetInterval(int val){
    interval = val;
    samplePeriod = interval/overSample;
  }

  private:
  byte resolution = 32;
  uint32_t prevMillis=0;
  int samplePeriod=interval;
  uint32_t sampleMillis=0;
  int sampleIndex=0;
  String address = "none";  
  int prevVal=0;
  uint32_t byteMask = 15<<8; //0b1111 shiftd 8bits
  uint32_t onPattern = (1<<15)-1;
  uint32_t offPattern = 1<<15;
  uint32_t resolutionMask = (1<<16)-1;
};//DigitalIn class