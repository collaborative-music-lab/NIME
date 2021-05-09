/* Simple test for analog and digital inputs, and digital outputs

*/
#include "m370_lbr.h"
#include <Wire.h>

byte SERIAL_DEBUG = 0;

// WiFi network name and password:
const char * ssid = "MLE"; //2.4GHz network only (no 5g)
const char * password = "mitmusictech";

////Firmware metadata
String FIRMWARE[] = {
  /*NAME*/ "modular",
  /*VERSION*/ "0.1",
  /*AUTHOR*/ "Ian Hattwick",
  /*DATE*/ "Apr 29, 2021",
  /*NOTES*/ "init"
};


////For wifi, AP mode creates a network and STA mode joins a network
//available comModes are: SERIAL_ONLY, AP_WIFI, STA_WIFI, APandSERIAL, STAandSERIAL;
//set default comMode here:
const comModes comMode = SERIAL_ONLY;
m370_communication comms(comMode);

/*********************************************
ANALOG SETUP
*********************************************/
const byte NUM_ANALOG = 3;

m370_analog pot[NUM_ANALOG] = {
  m370_analog(33,100), //pin, sampling rate (Hz)
  m370_analog(32,100),  //pin, sampling rate (Hz)
  m370_analog(39,100)
};



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

Esp32Encoder enc1(27, 14, -1, 4); //A,B,Switch, Divider
Esp32Encoder enc2(4, 12, -1, 4); //A,B,Switch, Divider
Esp32Encoder enc3(36, 15, -1, 4); //A,B,Switch, Divider


/*********************************************
  DIGITAL INPUT SETUP
*********************************************/
const byte NUM_DIGITAL = 4;

m370_digitalInput sw[NUM_DIGITAL] = {
  m370_digitalInput(23, 500), //pin, rate(Hz)
  m370_digitalInput(19, 500), //pin, rate(Hz)
  m370_digitalInput(18, 500), //pin, rate(Hz)
  m370_digitalInput(2, 500)
};

/*********************************************
I2C SETUP
*********************************************/

const byte NUM_CAP = 12; //up to 12 sensors

m370_cap cap(NUM_CAP, 500); //number of capsensors, sampling rate (Hz)



void setup() {

  comms.baudRate = 115200;
  comms.begin(FIRMWARE);

  byte commsBegin = 0;
  if (SERIAL_DEBUG ) commsBegin = 1;
  while (commsBegin  ==  0) {
    if (SERIAL_DEBUG == 2) commsBegin = 1;
    //Serial.println("comms");
    commsBegin = comms.connect()  ; //sends firmware metadata to begin function
  }
  //if ( commsBegin == 1 ) Serial.println("Serial connected");
  //else if ( commsBegin == 2) Serial.println("Wifi connected");

  delay(100);

  //initialize inputs
  for ( int i = 0; i < NUM_DIGITAL; i++) sw[i].begin();
  for(byte i=0;i<NUM_ANALOG;i++) pot[i].begin();
  enc1.begin([] {enc1.readEncoder_ISR();});
  enc2.begin([] {enc2.readEncoder_ISR();});
  enc3.begin([] {enc3.readEncoder_ISR();});
  cap.begin();
  
  //imuSetup();

  Serial.println("Setup complete");
}

void loop() {
  readSw();
  readPotentiometers();
  readEncoder();
  readCap();
  //imuLoop();


//  if (comms.available()) {
//    byte inBuffer[64];
//    byte index = 0;
//
//    comms.getInput(inBuffer,  &index);
//  }
}

void readSw() {
  static int count[4];

  for (int i = 0; i < NUM_DIGITAL; i++) {
    sw[i].loop();
    if ( sw[i].available() ) {
      int outVal = sw[i].getState();
      if (outVal == 1) count[i]++;
      if ( SERIAL_DEBUG ) {
        PrintDebug("sw", i, count[i]);
      }
      else {
        comms.outu8(i + 10);
        comms.outu16(outVal);
        comms.send();
      }
    }
  }
}

void readPotentiometers(){
  //increment i once per loop to have a small delay
  //between checking each analog input
  static byte i = 0;

  static int prevPot[] = {0,0,0};

  static uint32_t timer = 0;
  int interval= 10;

  if(millis()-timer>interval){
    timer= millis();  
  
    pot[i].loop();
    if(pot[i].available() ){
      int outVal = (prevPot[i]*3+pot[i].getVal())/4;
      if( abs(outVal-prevPot[i]) > 2 ){
        prevPot[i] = outVal;
        if( SERIAL_DEBUG ) {
          PrintDebug("pot",i,outVal);
        }
        else {
          comms.outu8(i);
          comms.outu16(outVal);
          comms.send();
        }
      }
    }
    i += 1;
    if(i >= NUM_ANALOG) i=0;
  }
}


void readEncoder() {
  static byte curEnc = 0;
  byte curB = 0;
  int val = 0;
  
  if(curEnc == 0 ){
    curB = enc1.button(); //get current button state
    val = enc1.delta(); //get encoder  count
    curEnc = 1;
  } else {
    curB = enc2.button(); //get current button state
    val = enc2.delta(); //get encoder  count
    curEnc = 0;
  }
    //four button states:
    // - 0 for button is being held down
    // - 1 for button transition from not pushed to pushed
    // - 2 for button is not being held down
    // - 3 for button transition from pushed to not pushed
  
  
  if (val != 0) {
    if (SERIAL_DEBUG) {
      Serial.print("count: ");
      Serial.println(val);
    }
    else {
      comms.outu8(30 + curEnc);
      comms.out16( val );
      comms.send();
    }
  }

  switch (curB) {
    case 0: //DOWN
      break;

    case 1: //PUSHED
      if (SERIAL_DEBUG) Serial.println("PUSHED");
      else {
        comms.outu8(32 + curEnc);
        comms.outu16(1);
        comms.send();
      }
      break;

    case 2: //UP

      break;

    case 3: //RELEASED
      if (SERIAL_DEBUG) Serial.println("RELEASED");
      else {
        comms.outu8(32 + curEnc);
        comms.outu16(0);
        comms.send();
      }
      break;
  }//switch
}


void readCap(){
  cap.loop();
  static uint32_t timer = 0;
  static int interval = 20;

  if(millis()-timer>interval){
      timer=millis();

      if(SERIAL_DEBUG){
        
        for(int i=0;i<NUM_CAP;i++){
          if(cap.available(i)){
              int16_t val  =  cap.getVal(i);
              Serial.print(val);
              Serial.print("\t");
           }
         }
        Serial.println();
      }//SERIAL_DEBUG
     
      else{
        for(int i=0;i<NUM_CAP;i++){
          if(cap.available(i)){
              int16_t val  =  cap.getVal(i);
              if( val>10) interval = 20;
              else interval = 40;
              comms.outu8(i+50);
              comms.out16(val);
              comms.send();
              
           }
        }
    }
  }
}

void PrintDebug(String name, int num, int val) {
  Serial.print(name);
  Serial.print(" ");
  Serial.print(num);
  Serial.print(": ");
  Serial.println(val);
}
