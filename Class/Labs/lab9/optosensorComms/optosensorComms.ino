 /* Simple test for optical sensor
 * 
 * pinout:
 * LED: connected to 3v and any pin - this sketch uses p0 but it could be p0-p13 (i think)
 * Photosensor: p1
 * 
 */
#include "m370_lbr.h"
#include <Wire.h> 

 byte SERIAL_DEBUG = 0;

// WiFi network name and password:
const char * ssid = "MLE"; //2.4GHz network only (no 5g)
const char * password = "mitmusictech";

////Firmware metadata
String FIRMWARE[] = {
  /*NAME*/ "optosensorTest",
  /*VERSION*/ "0.1",
  /*AUTHOR*/ "Ian Hattwick",
  /*DATE*/ "Mar 21, 2021",
  /*NOTES*/ "initial test"
};


////For wifi, AP mode creates a network and STA mode joins a network
//available comModes are: SERIAL_ONLY, AP_WIFI, STA_WIFI, APandSERIAL, STAandSERIAL;
//set default comMode here:
const comModes comMode = STAandSERIAL;
m370_communication comms(comMode);

/*********************************************
ENCODERS SETUP
*********************************************/
//encoders rely on the  ESP32Encoder library
//Esp32Encoder rotaryEncoder = Esp32Encoder(18,2,4);//A,B,Button
//optional divider argument
//arguments:
// - A and B: digital inputs from encoder
// - Switch; pin for encoder switch, or -1 for no switch
// - divider: many encoders put out multiple pulses per detent
//   The divider helps to make encoder increments match detents

//Esp32Encoder enc(p13,p12,p10,4);//A,B,Switch, Divider


/*********************************************
DIGITAL INPUT SETUP
*********************************************/
const byte NUM_DIGITAL = 4;

m370_digitalInput sw[NUM_DIGITAL] = {
  m370_digitalInput(p6,500),//pin, rate(Hz)
  m370_digitalInput(p7,500),//pin, rate(Hz)
  m370_digitalInput(p8,500),//pin, rate(Hz)
  m370_digitalInput(p9,500)//pin, rate(Hz)
};


void setup() {
 
  comms.baudRate = 115200;
  comms.begin(FIRMWARE);
  
  byte commsBegin = 0;
  while(commsBegin  ==  0){
    if(SERIAL_DEBUG == 2) commsBegin = 1;
    //Serial.println("comms");
    commsBegin = comms.connect()  ; //sends firmware metadata to begin function
    
    }

  delay(100);

  //initialize inputs
  //for( int i=0;i<NUM_DIGITAL;i++) sw[i].begin();
  //enc.begin([]{enc.readEncoder_ISR();});
  //imuSetup();

  //setup phototransistor and LED

  //LED
  pinMode(p0,OUTPUT);
  digitalWrite(p0, LOW);

  //phototransistor
  pinMode(p1, INPUT);

  Serial.println("Setup complete");
}

void loop() {
  readOptosensor();
 
}

void readOptosensor(){
  static uint32_t timer = 0;
  static int interval = 25;
  static int readState = 0;
  static int read1 = 0;
  static int read2 = 0;

  if(millis()-timer > interval){
    timer = millis();
  
    switch(readState){
      case 0: //init read cycle
      digitalWrite(p0, 0);
      readState = 1;
      interval = 1;
      break;
  
      case 1: //read when led on
      read1 = analogRead(p1);
      digitalWrite(p0, 1);
      readState = 2;
      interval = 1;
      break;
  
      case 2: // read with led off
      read2 = analogRead(p1);
      readState = 0;
      interval = 23;

      if(!SERIAL_DEBUG){ 
        comms.outu8(40);
        comms.out16(read1-read2);
        comms.send();
      }
      break;
    }

    if( SERIAL_DEBUG){
      Serial.print("stvalate ");
      Serial.print(read1-read2);
      Serial.print(", state ");
      Serial.print(readState);
      Serial.print(", interval ");
      Serial.println(interval);
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
