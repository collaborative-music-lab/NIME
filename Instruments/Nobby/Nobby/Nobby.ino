/* Nobby.ino
 *  Ian Hattwick
 *  created Jan 15 2022
 *  
 *  21M.370 example instrument
 *  
 *  Simple controller with 4 analog and 4 digital inputs:
 *  p0: potentiometer
 *  p1: potentiometer
 *  p2: potentiometer
 *  p3: potentiometer
 *  p6: button
 *  p7: button
 *  p8: button
 *  p9: button
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
  /*NAME*/ "Nobby",
  /*VERSION*/ "0.1",
  /*AUTHOR*/ "Ian Hattwick",
  /*DATE*/ "Jan 15, 2022",
  /*NOTES*/ "initial test"
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
const byte NUM_ANALOG = 4;

m370_analog ana[NUM_ANALOG] = {
  m370_analog(p0,20), //pin, sampling rate (Hz) F = 1/T, T = 1/F
  m370_analog(p1,20),  //pin, sampling rate (Hz)
  m370_analog(p2,20), //pin, sampling rate (Hz)
  m370_analog(p3,20)  //pin, sampling rate (Hz)
};
/*********************************************
DIGITAL INPUT SETUP
*********************************************/
const byte NUM_DIGITAL = 4;

m370_digitalInput sw[NUM_DIGITAL] = {
  m370_digitalInput(p6),//pin
  m370_digitalInput(p7),//pin
  m370_digitalInput(p8),//pin
  m370_digitalInput(p13)//pin
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
  readPotentiometers();
  readButtons();

  if (comms.available()){
    byte inBuffer[64];
    byte index=0;

    comms.getInput(inBuffer,  &index);
  }
}

void readButtons(){
  static int count[4];
  
  for(int i=0;i<NUM_DIGITAL;i++){
    sw[i].loop();
    if( sw[i].available() ){
      int outVal = sw[i].getState();
      if(outVal==1) count[i]++;
      if( SERIAL_DEBUG ) {
        PrintDebug("sw",i,count[i]);
      }
      else {
        comms.outu8(i+10); 
        comms.outu16(outVal);
        comms.send();
      }
    }
  }
}

void readPotentiometers(){
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
