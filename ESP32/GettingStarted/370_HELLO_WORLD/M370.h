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
 */

 //array of analog pins 
 // converts arbitrary pin numbers on the ESP32 to 0-9
const byte espPin[] = {27,33,32,14,4,0,15,14,36,39};

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

enum smoothType{
  NONE, AVERAGE, MEDIAN, MINIMUM, MAXIMUM
};

enum dataType{
  BYTE, INT, UINT, FLOAT
};


/******************************
GLOBAL VARIABLES
******************************/

void debug(String type, int val);

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

  Sensor(byte _pin, String _address) : pin(_pin), address(_address) 
  {}

  void setup(){}

  void loop(){
      if(curMillis - interval > prevMillis){
        prevMillis = curMillis;
        debug(address, analogRead( pin ));
      }
    }

  private:
  byte pin;
  uint32_t prevMillis=0;
  String address = "none";  
};//sensor class

