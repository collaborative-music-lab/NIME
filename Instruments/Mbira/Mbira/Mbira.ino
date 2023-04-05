/* Blank.ino
 *  Ian Hattwick
 *  
 *  21M.370 blank template
 *  

 * 
 */
#include "m370_lbr.h" 

const byte SERIAL_DEBUG = 0;

// WiFi network name and password:
// ignore this for now
const char * ssid = "ssid"; //2.4GHz network only (no 5g)
const char * password = "pw";

////Firmware metadata
String FIRMWARE[] = {
  /*NAME*/ "Blank",
  /*VERSION*/ "0.1",
  /*AUTHOR*/ "Ian Hattwick",
  /*DATE*/ "Mar 1, 2023",
  /*NOTES*/ "initial"
};


//comms handles communication with Python
//!!setting comMode to SERIAL_ONLY will force the ESP32 to 
//begin sending serial data immediately, rather than waiting
//for python to connect
const comModes comMode = SERIAL_ONLY;

m370_communication comms(comMode);

/*********************************************
ANALOG SETUP
*********************************************/
const byte NUM_ANALOG = 6;

byte analog_polling_rate = 1000;

m370_analog ana[NUM_ANALOG] = {
  m370_analog(p0,analog_polling_rate), //pin, sampling rate (Hz) F = 1/T, T = 1/F
  m370_analog(p1,analog_polling_rate),
  m370_analog(p2,analog_polling_rate),
  m370_analog(p3,analog_polling_rate),
  m370_analog(p4,analog_polling_rate),
  m370_analog(p5,analog_polling_rate)
};

uint32_t analogSum[NUM_ANALOG];
uint32_t analogCount[NUM_ANALOG];
/*********************************************
DIGITAL INPUT SETUP
*********************************************/
const byte NUM_DIGITAL = 1;

m370_digitalInput sw[NUM_DIGITAL] = {
  m370_digitalInput(p6)//pin
};


void setup() {
 
  for(byte i=0;i<NUM_DIGITAL;i++) sw[i].begin();
  for(byte i=0;i<NUM_ANALOG;i++) ana[i].begin();

  comms.baudRate = 115200;
  comms.begin(FIRMWARE);
  
  byte commsBegin = 0;
  while(commsBegin  ==  0){
    if(SERIAL_DEBUG == 1) break;
    //Serial.println("comms");
    commsBegin = comms.connect()  ; //sends firmware metadata to begin function
  }
  delay(100);
 Serial.println("comm mode " + String(commsBegin));
 Serial.println("setup completed"); 
}// setup

void loop() {
  readAnalog();
  readDigital();

  if (comms.available()){
    byte inBuffer[64];
    byte index=0;

    comms.getInput(inBuffer,  &index);
  }
}

void readDigital(){
  for(int i=0;i<NUM_DIGITAL;i++){
    sw[i].loop();
    if( sw[i].available() ){
      int outVal = sw[i].getState();
      if( SERIAL_DEBUG ) {
        Serial.println("digital " + String(i) + " " + String(outVal));
      }
      else {
        comms.outu8(i+10); 
        comms.outu16(outVal);
        comms.send();
      }
    }
  }
}

void readAnalog(){
  static uint32_t timer = 0;
  int printInterval = 10;

  for(int i=0;i<NUM_ANALOG;i++){
    ana[i].loop();
    if(ana[i].available() ){
      int outVal = ana[i].getVal();
      analogSum[i] += outVal;
      analogCount[i]++;
    }
  }
  if(millis()-timer > printInterval){
      timer = millis();
      for(int i=0;i<NUM_ANALOG;i++){
        if( SERIAL_DEBUG ) {
          //PrintDebug("analog",i,outVal);
          Serial.print(analogSum[i]/analogCount[i]);
          Serial.print("\t");
        }
        else {
        comms.outu8(i);
        comms.outu16(analogSum[i]/analogCount[i]);
        comms.send();
      }
      analogSum[i] = 0;
      analogCount[i] = 0;
    }
    if(SERIAL_DEBUG) Serial.println();
  }
}



void PrintDebug(String name, int num, int val){
  Serial.print(name);
  Serial.print(" ");
  Serial.print(num);
  Serial.print(": ");
  Serial.println(val);
}
