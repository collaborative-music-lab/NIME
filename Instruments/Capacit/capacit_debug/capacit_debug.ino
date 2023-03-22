  /* capacit.ino
 *  Ian Hattwick
 *  created Mar 12 2021
 *  
 *  21M.370 debug file
    - testing problems with MPR121 library
 */ 
#include "m370_lbr.h" 

const byte SERIAL_DEBUG = 1;

// WiFi network name and password:
// ignore this for now
const char * ssid = "ssid"; //2.4GHz network only (no 5g)
const char * password = "pw";

////Firmware metadata
String FIRMWARE[] = {
  /*NAME*/ "capacit",
  /*VERSION*/ "0.11",
  /*AUTHOR*/ "Ian Hattwick",
  /*DATE*/ "Mar 12, 2023",
  /*NOTES*/ "debug"
};


//comms handles communication with Python
const comModes comMode = SERIAL_ONLY;
m370_communication comms(comMode);


/*********************************************
I2C SETUP
*********************************************/

const byte NUM_CAP = 4; //up to 12 sensors

MPR121 cap(21,22); //number of capsensors, sampling rate (Hz)


/*********************************************
MAIN SETUP AND LOOP
*********************************************/
void setup() {

  cap.begin();

  cap.chargeCurrent(63); //0-63, def 16
  cap.chargeTime(1); //1-7, def 1
  cap.setThresholds(200, 100);
  cap.proxChargeCurrent(63); //0-63, def 16
  cap.proxChargeTime(3); //1-7, def 1

  comms.baudRate = 115200;
  comms.begin(FIRMWARE);
  
  byte commsBegin = 0;
  while(commsBegin  ==  0){
    if(SERIAL_DEBUG == 1) break;
    //Serial.println("comms");
    commsBegin = comms.connect()  ; //sends firmware metadata to begin function
  }

 Serial.println("setup completed");
}// setup

void loop() {
  
  readCap();

  //read serial input
  if (comms.available()){
    byte inBuffer[64];
    byte index=0;

    comms.getInput(inBuffer,  &index);
    if(index > 1){
      switch(inBuffer[0]){
        // case 50: cap.SetChargeCurrent(inBuffer[1]); break;
        // case 51: cap.SetChargeTime(inBuffer[1]); break;
        break;
      }
    }
  }
}//loop

/*********************************************
SUB FUNCTIONS
*********************************************/

void readCap(){
  static uint32_t timer = 0;
  int interval = 25;
  int cap_val[NUM_CAP];

  if(millis() - timer > interval){
    timer = micros();

    for(int i=0;i<NUM_CAP;i++) {
      cap_val[i]  = -(cap.filteredData(i)  - cap.baselineData(i));

      if(SERIAL_DEBUG){
        Serial.print(cap_val[i]);
        Serial.print("\t");
      }
      else{
        comms.outu8(i+50);
        comms.out16(cap_val[i]);
        comms.send();
      }
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
