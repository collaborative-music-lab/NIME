/*  370_HELLO_WORLD::M370.h
 * 
 * Header file for 21M.370 ESP32 firmware
 * 
 * Sections:
 * - pin mappings
 * - global variables
 * - function prototypes if necessary
 * - object definitions
 * 
 * NOTE:
 * ESP32 pins 21 and 22 used for I2C
 * - pin 22 is also built in LED on ESP32
 */

 //array of analog pins 
 // converts arbitrary pin numbers on the ESP32 to 0-9
const byte espPin[] = {27,33,32,14,4,0,15,13,36,39};
//addresses for _MPR121
const byte capPins[] = {64,65,66,67,68,69,70,71,72,73,74,75};

//main row of input pins
const byte p0 = 27;
const byte p1 = 33;
const byte p2 = 32;
const byte p3 = 14;
const byte p4 = 4;
const byte p5 = 0;
const byte p6 = 15;
const byte p7 = 13;

//special analog pins with (possibly) lower noise?
const byte p8 = 36;
const byte p9 = 39;
//alternate names
const byte AN0 = 36;
const byte AN1 = 39;

//MUX and SPI control pins
const byte pMISO = 19;
const byte pMOSI = 23;
const byte pCLK = 18;
const byte pSS = 2; //also present on MIDI jack
const byte pSS2 = 12;
const byte MUX_PINS[] = {18,19,23};

//LED and buttons on PCB
const byte LED = 13;
const byte BUTTON_0 = 34;
const byte BUTTON_1 = 35;

//3.5mm jacks
const byte euroGate = 0;
const byte euroClock= 2;
const byte dac1 = 25; //tip
const byte dac2 = 26; //ring
const byte dac1in = 36;
const byte dac2in = 39;
const byte MIDI = 5; //tip
const byte MIDI_5v = 2; //must be set high for MIDI use
//note this jack puts out 5v due to level translator


/******************************
GLOBAL VARIABLES
******************************/
uint32_t curMillis = 0;

//for ultrasonic sensor
byte trigPin = 27;

enum PROCESS_MODE{
  MEAN, MEDIAN, MIN, MAX, PEAK_DEVIATION, CAP_SENSE,
  TRIG, ECHO
};

enum dataType{
  BYTE, INT, UINT, FLOAT
};


int touchedSensors = 0;
uint16_t totalCapacitance = 0;

/******************************
FUNCTION DELCARATIONS
******************************/

void debug(String type, int val);
void SlipOutInt(int val);
void SlipOutByte(byte val);
void SerialOutSlip();
int oversample(int adcPin, int numSamples);
int Mean(int vals[], byte num);
int Median(int vals[], byte num);
int Peak(int vals[], byte num);
int Trough(int vals[], byte num);
int PeakDeviation(int vals[], byte num, int prev);
int MPR121_loop(byte num);
int getPing(byte _pin);


/******************************
OBJECT DEFINITIONS 
pin: ESPpin number, int, e.g. Sensor[0].pin = 0
name: string with the intended OSC name of the sensor, e.g. Sensor[0].name = "/joystick/x"
interval: milliseconds between readings of the sensor
smoothingtype: type of smoothing to apply to the sensor reading
type: type of data returned by the sensor
smoothing: a variable to be passed to a smoothing function
val: pointer to an array to store sensor readings
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
          SerialOutSlip();
  
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

/******************************
_MPR121 OBJECT  
******************************/

class Cap{
  public: 
  uint16_t interval = 100;
  byte state = 1;
  int val[32];
  byte overSample=16;
  int outVal=0;
  PROCESS_MODE sampleProcessMode = MEDIAN;

  //constructors
  Cap() {}

  Cap( int _interval) : 
  interval(_interval),
  samplePeriod(interval/overSample)
  {}

  void setup(){}

  void loop(byte num){
    //take sample of current value
    if(curMillis - samplePeriod > sampleMillis){
        sampleMillis = curMillis;
        if(sampleIndex<32){
          val[sampleIndex] = MPR121_loop(num);
          sampleIndex++;
        }
    }

    //process samples and output
    if(curMillis - interval > prevMillis){
      prevMillis = curMillis;

      if(sampleIndex > 0){
        outVal = Mean(val, sampleIndex);
        //outVal -= 4096;
        int curVal = outVal-4096;
        //Serial.println(outVal);
        //delay(100);

//        SlipOutByte(capPins[num]);
//        SlipOutInt(outVal);
//        SerialOutSlip();
//        Serial.print(num);
//        Serial.print(" ");
//        Serial.print(curVal);
//        Serial.println(", ");
        prevVal = outVal;
        sampleIndex=0;

        //calculate touch state
        if(curVal > maxVal) maxVal = curVal;
        if(curVal < minVal) minVal = curVal;
        
        if( (curVal > ((maxVal*2)/3))){
          state = 1;
          touchedSensors = touchedSensors | (1<<num);
        } else if ( (curVal < ((maxVal*2)/4))){
          state = 0;
          touchedSensors = touchedSensors & ~(1<<num);
        }
        if(state != prevState){
          prevState = state;
          SlipOutByte(num+110); //pin, numerical indicator
          SlipOutInt(state);
          SerialOutSlip();
        }
      } 
    }
  }//loop

  void SetInterval(int val){
    interval = val;
    samplePeriod = interval/overSample;
  }

  private:
  byte pin;
  uint32_t prevMillis=0;
  int samplePeriod=interval;
  uint32_t sampleMillis=0;
  int sampleIndex=0;
  int prevVal=0;
  int maxVal = 5;
  int minVal = 0;
  byte prevState = 0;
};//sensor class
