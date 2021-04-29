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
  /*NAME*/ "chesterv2",
  /*VERSION*/ "0.1",
  /*AUTHOR*/ "Ian Hattwick",
  /*DATE*/ "Apr 26, 2021",
  /*NOTES*/ "checking sensors"
};


////For wifi, AP mode creates a network and STA mode joins a network
//available comModes are: SERIAL_ONLY, AP_WIFI, STA_WIFI, APandSERIAL, STAandSERIAL;
//set default comMode here:
const comModes comMode = STAandSERIAL;
m370_communication comms(comMode);

/*********************************************
ANALOG SETUP
*********************************************/
const byte NUM_ANALOG = 5;

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

m370_digitalInput sw[NUM_DIGITAL] = {
  m370_digitalInput(25, 500), //pin, rate(Hz)
  m370_digitalInput(26, 500), //pin, rate(Hz)
  m370_digitalInput(32, 500), //pin, rate(Hz)
  m370_digitalInput(27, 500), //pin, rate(Hz)
  m370_digitalInput(14, 500) //pin, rate(Hz)
};


void setup() {

  comms.baudRate = 115200;
  comms.begin(FIRMWARE);

  byte commsBegin = 0;
  while (commsBegin  ==  0) {
    if (SERIAL_DEBUG == 2) commsBegin = 1;
    //Serial.println("comms");
    commsBegin = comms.connect()  ; //sends firmware metadata to begin function

  }
  if ( commsBegin == 1 ) Serial.println("Serial connected");
  else if ( commsBegin == 2) Serial.println("Wifi connected");

  delay(100);

  //initialize inputs
  for ( int i = 0; i < NUM_DIGITAL; i++) sw[i].begin();
  enc1.begin([] {enc1.readEncoder_ISR();});
  enc2.begin([] {enc2.readEncoder_ISR();});
  imuSetup();

  Serial.println("Setup complete");
}

void loop() {
  readSw();
  readEncoder();
  imuLoop();


  if (comms.available()) {
    byte inBuffer[64];
    byte index = 0;

    comms.getInput(inBuffer,  &index);
  }
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

void PrintDebug(String name, int num, int val) {
  Serial.print(name);
  Serial.print(" ");
  Serial.print(num);
  Serial.print(": ");
  Serial.println(val);
}
