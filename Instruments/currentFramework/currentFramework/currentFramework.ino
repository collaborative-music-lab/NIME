/* 

Main sketch to show how to use the framework

There are four main sections:
1) communication setup
   - here we will define how we expect to communicate with the ESP32. Options are:
   - SERIAL_ONLY: use the USB  port
   - AP_WIFI: create a new wifi network
   - STA_WIFI: join an existing wifi network
   - BLUETOOTH: function as a bluetooth device (not implemented)
   - you can also be prepared to look for python using multiple types of connection
   - e.g. STAandSERIAL

   you will also need to define the wifi network name (SSID) and the password. 
   - it is okay to leave password blank if there isn't one, e.g. password = "";

2) sensor declarations
   - set how many of each sensor type, and other basic parameters
   - you don't need to comment out the declaration if not using a particular sensor type

3) setup()
   - begin each sensor
   - if you are not using a sensor type, you should comment it out here

4) loop() and read functions
  - a different read function is provided to read each sensor's data
  - read functions will also send data to python
  - you should comment out the read function in the main loop if not using the sensor
  - e.g. 
  loop(){
    //readAnalog(); //don't read the analog sensors
    readDigital(); //do read the digital sensors
  }

*/

#include "m370_lbr.h"
#include <Wire.h>

byte SERIAL_DEBUG = 0;

// WiFi network name and password:
//const char * ssid = "esp32"; //2.4GHz network only (no 5g)
//const char * password = "mitmusictech";

const char * ssid = "MLE2"; //2.4GHz network only (no 5g)
const char * password = "mitmusictech";

////Firmware metadata
String FIRMWARE[] = {
  /*NAME*/ "curentFramework",
  /*VERSION*/ "0.1",
  /*AUTHOR*/ "Ian Hattwick",
  /*DATE*/ "May 9, 2021",
  /*NOTES*/ "added wifiAP"
};


//For wifi, AP mode creates a network and STA mode joins a network
//available comModes are: SERIAL_ONLY, AP_WIFI, STA_WIFI, APandSERIAL, STAandSERIAL;
//set default comMode here:
const comModes comMode = AP_WIFI;
//const comModes comMode = STAandSERIAL;
m370_communication comms(comMode);
 
/*********************************************
ANALOG SETUP
*********************************************/
const byte NUM_ANALOG = 5;
//threshold to decide whether to send new analog data
//if abs(newValue-oldValue) >= threshold then send data
//if threshold <= 0, always send value

const byte ANALOG_SEND_THRESHOLD = 0; //0= always send data

m370_analog ana[NUM_ANALOG] = {
  m370_analog(33,20), //pin, sampling rate (Hz)
  m370_analog(34,20),  //pin, sampling rate (Hz)
  m370_analog(35,20), //pin, sampling rate (Hz)
  m370_analog(39,20),  //pin, sampling rate (Hz)
  m370_analog(36,20)  //pin, sampling rate (Hz)
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

Esp32Encoder enc1(23, 5, 17, 4); //A,B,Switch, Divider
Esp32Encoder enc2(19, 18, 16, 4); //A,B,Switch, Divider


/*********************************************
  DIGITAL INPUT SETUP
*********************************************/
const byte NUM_DIGITAL = 5;

m370_digitalInput digi[NUM_DIGITAL] = {
  m370_digitalInput(25, 500), //pin, rate(Hz)
  m370_digitalInput(26, 500), //pin, rate(Hz)
  m370_digitalInput(32, 500), //pin, rate(Hz)
  m370_digitalInput(27, 500), //pin, rate(Hz)
  m370_digitalInput(14, 500) //pin, rate(Hz)
};

/*********************************************
CAPACITIVE SETUP
*********************************************/
const byte NUM_CAP = 4; //up to 12 sensors
m370_cap cap(NUM_CAP, 500); //number of capsensors, sampling rate (Hz)

/*********************************************
IMU SETUP
*********************************************/
//note imu setup and loop are in a separate file called imu.ino, which 
//should appead as a tab inside Arduino
LSM6 imu; //declare an LSM6 object

/*********************************************
PRIMARY SETUP FUNCTION
*********************************************/
void setup() {

  comms.baudRate = 115200;
  comms.begin(FIRMWARE);
  Serial.println("comms.begin completed");
  
  byte commsConnect = 0;
  while (commsConnect  ==  0) {
    if (SERIAL_DEBUG == 2) break;
    //Serial.println("comms");
    commsConnect = comms.connect()  ; //sends firmware metadata to begin function

  }
  if ( commsConnect == 1 ) Serial.println("Serial connected");
  else if ( commsConnect == 2) Serial.println("Wifi connected");

  delay(100);

  //INITIALIZE INPUTS
  //uncomment out the setup for the sensor types you want to use
  
  for ( int i = 0; i < NUM_ANALOG; i++) ana[i].begin();
  //for ( int i = 0; i < NUM_DIGITAL; i++) digi[i].begin();
  //enc1.begin([] {enc1.readEncoder_ISR();});
  //enc2.begin([] {enc2.readEncoder_ISR();});
  //beginIMU(); //funtion defined in IMU tab
  //cap.begin();

  Serial.println("Setup complete");
}

/*********************************************
PRIMARY LOOP FUNCTION
*********************************************/
void loop() {
  //uncomment read function for the sensor types you want to use
  
  readAnalog();
  //readDigital();
  //readCapacitive();
  //readEncoder();
  //readIMU();

  //read from python
  //leave uncommented
  if (comms.available()) {
    byte inBuffer[64];
    byte index = 0;

    comms.getInput(inBuffer,  &index);
  }
}

/*********************************************
READ FUNCTIONS
*********************************************/

void readAnalog(){
  static uint32_t timer = 0;
  int interval = 10; //ms interval to send to python
  static int prevVal[NUM_ANALOG];

  for (int i=0;i<NUM_ANALOG;i++){ 
    ana[i].loop();
  
    if( millis() - timer > interval ){
        timer = millis();
    
        if(ana[i].available() ){
          int outVal = ana[i].getVal();
          if( abs(outVal-prevVal[i]) > ANALOG_SEND_THRESHOLD  ){
            prevVal[i] = outVal;
            if( SERIAL_DEBUG ) {
              PrintDebug("ana",i,outVal);
            }
            else {
              comms.outu8(i);
              comms.outu16(outVal);
              comms.send();
            }
          }
        
      }
    }
  }
}


void readDigital() {
  for (int i = 0; i < NUM_DIGITAL; i++) {
    digi[i].loop();
    if ( digi[i].available() ) {
      int outVal = digi[i].getState();

      if ( SERIAL_DEBUG ) {
        PrintDebug("digi", i, outVal);
      }
      else {
        comms.outu8(i + 10);
        comms.outu16(outVal);
        comms.send();
      }
    }
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


void readCapacitive(){
  cap.loop();
  static uint32_t timer = 0;
  int interval = 20;

  if(millis()-timer>interval){
      timer=millis();

      if(SERIAL_DEBUG){
        Serial.print("cap: ");
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
