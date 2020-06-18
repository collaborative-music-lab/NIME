/******************************
Class for digital inputs
******************************/

class Sensor{
  public: 
  uint16_t interval = 500;
  byte enable = 1;
  byte state = 1;
  int val[32];
  byte overSample=1;
  byte pin = 22;
  PROCESS_MODE sampleProcessMode = MEDIAN;

  //constructors
  Sensor(byte _pin, String _address) : 
    pin(_pin), 
    address(_address) 
  {}

  Sensor(byte _pin, String _address, int _interval) : 
    pin(_pin), 
    address(_address), 
    interval(_interval) 
  {}

  Sensor(byte _pin, String _address, int _interval, byte _overSample) : 
    pin(_pin), 
    address(_address), 
    interval(_interval), 
    samplePeriod(interval/_overSample),
    overSample(_overSample)
  {}

  Sensor(byte _pin, String _address, int _interval, byte _overSample, PROCESS_MODE _processMode) : 
    pin(_pin), 
    address(_address), 
    interval(_interval), 
    samplePeriod(interval/_overSample),
    overSample(_overSample),
    sampleProcessMode(_processMode)
  {
    if(sampleProcessMode == TRIG) pinMode(pin,OUTPUT);
    else pinMode(pin,INPUT);
  }

  void setup(){}

  void loop(){
    if (enable==1) {
      if(curMillis - samplePeriod > sampleMillis){
          sampleMillis = curMillis;
          if(sampleIndex<32){
            val[sampleIndex] = oversample(pin,overSample);
            sampleIndex++;
          }
      }
  
      if(curMillis - interval > prevMillis){
        prevMillis = curMillis;
  
        //debug(address, analogRead( pin ));
        if(sampleIndex > 0){
           int outVal=0;
   
          switch(sampleProcessMode){
            case MEAN:
            outVal = Mean(val, sampleIndex);
            break;
  
            case MEDIAN:
            outVal = Median(val, sampleIndex);
            break;
  
            case MIN:
            outVal = Trough(val, sampleIndex);
            break;
  
            case MAX:
            outVal = Peak(val, sampleIndex);
            break;
  
            case PEAK_DEVIATION:
            outVal = PeakDeviation(val, sampleIndex, prevVal);
            break;
  
            case CAP_SENSE:
            //val[sampleIndex-1] = touchRead(pin);
            //outVal = Mean(val, sampleIndex);
            outVal = touchRead(pin);
            break;

            case TRIG:
            return;
            break;

            case ECHO:
            outVal = getPing(pin);
          }
          //Serial.println(outVal);
          //delay(100);
          SlipOutByte(pin);
          SlipOutInt(outVal);
          SendOutSlip();
          if(ANALOG_DEBUG) {
            Serial.print(pin);
            Serial.print(": ");
            Serial.println(outVal);
          }
          
          prevVal = outVal;
          sampleIndex=0;
        } 
      }
    }
  }//loop

  void SetInterval(int val){
    interval = val;
    samplePeriod = interval/overSample;
  }

  private:
  uint32_t prevMillis=0;
  int samplePeriod=interval;
  uint32_t sampleMillis=0;
  int sampleIndex=0;
  String address = "none";  
  int prevVal=0;
};//sensor class