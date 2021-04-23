 /* blueprint for creating a minimal viable instrument
 * 
 * 
 */
#include "m370_lbr.h"

 byte SERIAL_DEBUG = 0;

// WiFi network name and password:
const char * ssid = "MLE"; //2.4GHz network only (no 5g)
const char * password = "mitmusictech";

////Firmware metadata
String FIRMWARE[] = {
  /*NAME*/ "minimal viable instrument",
  /*VERSION*/ "0.1",
  /*AUTHOR*/ "Ian Hattwick",
  /*DATE*/ "Apr 21, 2021",
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
ANALOG SETUP
*********************************************/
const byte NUM_ANALOG = 4;

m370_analog ana[NUM_ANALOG] = {
  m370_analog(p2, 200), //pin, sampling rate (Hz)
  m370_analog(p3, 200),  //pin, sampling rate (Hz)
  m370_analog(p4, 200), //pin, sampling rate (Hz)
  m370_analog(p5, 200)  //pin, sampling rate (Hz)
};

/*********************************************
DIGITAL INPUT SETUP
*********************************************/
const byte NUM_DIGITAL = 4;

m370_digitalInput digi[NUM_DIGITAL] = {
  m370_digitalInput(p6,500),//pin, rate(Hz)
  m370_digitalInput(p7,500),//pin, rate(Hz)
  m370_digitalInput(p8,500),//pin, rate(Hz)
  m370_digitalInput(p9,500)//pin, rate(Hz)
};


void setup() {

 //setup serial communication
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
  
  for( int i=0;i<NUM_DIGITAL;i++) digi[i].begin();
  for( int i=0;i<NUM_ANALOG;i++) ana[i].begin();
  //enc.begin([]{enc.readEncoder_ISR();});
  //imuSetup();

  //optosensor setup
  //LED
  pinMode(p0,OUTPUT);
  digitalWrite(p0, LOW);
  //phototransistor
  pinMode(p1, INPUT);

  Serial.println("Setup complete");
}

void loop() {
  readAnalog();
  readDigital();
  readEncoder();
  readOptosensor();
}

void readAnalog(){
  static uint32_t timer = 0;
  int interval = 20; //in milliseconds
 
  for(int i=0;i<NUM_ANALOG;i++){
    ana[i].loop();

    if( millis() - timer  > interval){
      timer = millis();
      if(ana[i].available() ){
        int outVal = ana[i].getVal();
        if( SERIAL_DEBUG ) {
          PrintDebug("analog",i,outVal);
        }
        else {
          comms.outu8(i); //number represents number
          comms.outu16(outVal); //out16 signed, outu16 
          comms.send();
        }
      }
    }
  }
}

void readDigital(){
  for(int i=0;i<NUM_DIGITAL;i++){
    digi[i].loop();
    if( digi[i].available() ){
      int outVal = digi[i].getState();
      if( SERIAL_DEBUG ) {
        PrintDebug("digital",i,outVal);
      }
      else {
        comms.outu8(i+10); //sensor 
        comms.outu16(outVal);
        comms.send();
      }
    }
  }
}//readDigital

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
        comms.outu8(40); //sensor number
        comms.out16(read1-read2); //value out16 outu16
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
  }//timer
}//readOptosensor

void readEncoder(){
//  byte curB = enc.button(); //get current button state
//  //four button states:
//  // - 0 for button is being held down
//  // - 1 for button transition from not pushed to pushed
//  // - 2 for button is not being held down
//  // - 3 for button transition from pushed to not pushed
//
//  int val = enc.delta(); //get encoder  count
//  if(val!= 0){
//    if(SERIAL_DEBUG){
//      Serial.print("count: ");
//      Serial.println(val);
//    }
//    else{
//      comms.outu8(30);
//      comms.out16( val );
//      comms.send();
//    }
//  }
//
//  switch(curB){
//    case 0: //DOWN
//    break;
//
//    case 1: //PUSHED
//    if(SERIAL_DEBUG) Serial.println("PUSHED");
//    else{
//      comms.outu8(31);
//      comms.outu16(1);
//      comms.send();
//    }
//    break;
//
//    case 2: //UP
//   
//    break;
//
//    case 3: //RELEASED
//    if(SERIAL_DEBUG) Serial.println("RELEASED");
//    else{
//      comms.outu8(31);
//      comms.outu16(0);
//      comms.send();
//    }
//    break;
//  }//switch
}


void PrintDebug(String name, int num, int val){
  Serial.print(name);
  Serial.print(" ");
  Serial.print(num);
  Serial.print(": ");
  Serial.println(val);
}
