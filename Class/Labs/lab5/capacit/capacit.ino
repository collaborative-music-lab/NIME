/* capacit.ino
 *  Ian Hattwick
 *  created Mar 12 2021
 *  
 *  21M.370 example instrument
 *  
 *  uses MPR121 I2C capacitive sensor
 *  with: 
 *  - up to 6 analog on p0-p5
 *  - up to 8 digital inputs on p6-p13
 *  - up to 12 capacitive touch and proximity inputs
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
  /*NAME*/ "capacit",
  /*VERSION*/ "0.1",
  /*AUTHOR*/ "Ian Hattwick",
  /*DATE*/ "Mar 12, 2021",
  /*NOTES*/ "initial"
};


//comms handles communication with Python
const comModes comMode = STAandSERIAL;

m370_communication comms(comMode);

/*********************************************
ANALOG SETUP
*********************************************/
const byte NUM_ANALOG = 2;
const int analogSamplingRate = 20; //in Hz

m370_analog pot[6] = {
  m370_analog(p0,analogSamplingRate), //pin, sampling rate (Hz)
  m370_analog(p1,analogSamplingRate),  //pin, sampling rate (Hz)
  m370_analog(p2,analogSamplingRate),  //pin, sampling rate (Hz)
  m370_analog(p3,analogSamplingRate),  //pin, sampling rate (Hz)
  m370_analog(p4,analogSamplingRate),  //pin, sampling rate (Hz)
  m370_analog(p5,analogSamplingRate),  //pin, sampling rate (Hz)
};
/*********************************************
DIGITAL INPUT SETUP
*********************************************/
const byte NUM_DIGITAL = 4;

m370_digitalInput sw[8] = {
  m370_digitalInput(p6),//pin
  m370_digitalInput(p7),//pin
  m370_digitalInput(p8),//pin
  m370_digitalInput(p9),
  m370_digitalInput(p10),
  m370_digitalInput(p11),
  m370_digitalInput(p12),
  m370_digitalInput(p13)
};
/*********************************************
I2C SETUP
*********************************************/

const byte NUM_CAP = 12;

m370_cap cap(NUM_CAP, 100); //number of capsensors, sampling rate (Hz)


/*********************************************
MAIN SETUP AND LOOP
*********************************************/
void setup() {
 
  for(byte i=0;i<NUM_DIGITAL;i++) sw[i].begin();
  for(byte i=0;i<NUM_ANALOG;i++) pot[i].begin();
  cap.begin();

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
  
  //if(1){              //uncomment this line to serial debug pots and buttons as well as capsense
  if( !SERIAL_DEBUG){   //uncomment this line to only serial debug capsense
    readPotentiometers();
    readButtons();
  }
  readCap();

  //read serial input
  if (comms.available()){
    byte inBuffer[64];
    byte index=0;

    comms.getInput(inBuffer,  &index);
  }
}//loop

/*********************************************
SUB FUNCTIONS
*********************************************/

void readButtons(){
  static int count[NUM_DIGITAL];
  
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
  //increment i once per loop to have a small delay
  //between checking each analog input
  static byte i = 0;
  
  pot[i].loop();
  if(pot[i].available() ){
    int outVal = pot[i].getVal();
    if( SERIAL_DEBUG ) {
      PrintDebug("pot",i,outVal);
    }
    else {
      comms.outu8(i);
      comms.outu16(outVal);
      comms.send();
    }
  }
  i += 1;
  if(i >= NUM_ANALOG) i=0;
}


void readCap(){
  cap.loop();

  if(SERIAL_DEBUG){
    static uint32_t timer = 0;
    int interval = 50;
    
    if(millis()-timer>interval){
      timer=millis();
  
      for(int i=0;i<NUM_CAP;i++){
        if(cap.available(i)){
            int16_t val  =  cap.getVal(i,TROUGH);
            Serial.print(val);
            Serial.print("\t");
         }
       }
      Serial.println();
    }
  } 
  else{
    for(int i=0;i<NUM_CAP;i++){
      if(cap.available(i)){
          int16_t val  =  cap.getVal(i,TROUGH);
          comms.outu8(i+50);
          comms.out16(val);
          comms.send();
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
