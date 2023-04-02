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
const byte NUM_ANALOG = 1;

m370_analog ana[NUM_ANALOG] = {
  m370_analog(p0,20) //pin, sampling rate (Hz) F = 1/T, T = 1/F
};
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
  for(int i=0;i<NUM_ANALOG;i++){
    ana[i].loop();
    if(ana[i].available() ){
      int outVal = ana[i].getVal();
      if( SERIAL_DEBUG ) {
        PrintDebug("analog",i,outVal);
      }
      else {
        comms.outu8(i);
        comms.outu16(outVal);
        comms.send();
      }
    }
  }
}



void PrintDebug(String name, int num, int val){
  Serial.print(name);
  Serial.print(" ");
  Serial.print(num);
  Serial.print(": ");
  Serial.println(val);
}
