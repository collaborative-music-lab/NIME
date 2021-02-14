#include <m370_lbr.h>

// WiFi network name and password:
const char * ssid = "MLE"; //2.4GHz network only (no 5g)
const char * password = "mitmusictech";

////Firmware metadata
const String FIRMWARE[] = {
  /*NAME*/ "FMbox",
  /*VERSION*/ "0.1",
  /*AUTHOR*/ "Ian Hattwick",
  /*DATE*/ "Feb 11, 2020",
  /*NOTES*/ "initial test"
};


////For wifi, AP mode creates a network and STA mode joins a network
//available comModes are: SERIAL_ONLY, AP_WIFI, STA_WIFI, APandSERIAL, STAandSERIAL;
//set default comMode here:
const comModes comMode = STAandSERIAL;

m370_communication comms(comMode);

const byte NUM_OPTO = 4;
int optoInterval = 50;

m370_analog opto[NUM_OPTO] = {
  m370_analog(32, optoInterval, "opto0"), //sensorpin,ledpin,frequency(Hz)
  m370_analog(36,  optoInterval, "opto1"), //sensorpin,ledpin,frequency(Hz)
  m370_analog(39,  optoInterval, "opto2"), //sensorpin,ledpin,frequency(Hz)
  m370_analog(35, optoInterval, "opto3"), //sensorpin,ledpin,frequency(Hz)
};

const byte NUM_DIGITAL = 4;
m370_digitalInput  buttons[NUM_DIGITAL] = {
  m370_digitalInput(13,500),
  m370_digitalInput(14,500),
  m370_digitalInput(25,500),
  m370_digitalInput(26,500)
};

//const byte NUM_ANALOG = 4;
//m370_analogInput  pots[NUM_DIGITAL] = {
//  m370_analogInput(13,500),
//  m370_analogInput(14,500),
//  m370_analogInput(25,500),
//  m370_analogInput(26,500)
//};

byte mux[] = {12,18,23};
byte latch = 2;
byte muxin = 33;


void setup() {
  Serial.begin(115200);

  comms.baudRate = 115200;

  byte commsBegin = 0;
  while(commsBegin  ==  0){
    commsBegin = comms.begin(FIRMWARE); //sends firmware metadata to begin function
  }

  for(byte i=0;i<NUM_OPTO;i++) opto[i].begin();
  for(byte i=0;i<NUM_DIGITAL;i++) buttons[i].begin();
  //pinMode(33,INPUT);
  //pinMode(4,OUTPUT);

  for(int i=0;i<3;i++) pinMode(mux[i], OUTPUT);
  pinMode(muxin,INPUT);

  pinMode(2,OUTPUT);
  digitalWrite(2,LOW);

  pinMode(13, INPUT_PULLUP);
  pinMode(14, INPUT_PULLUP);
  pinMode(25, INPUT_PULLUP);
  pinMode(26, INPUT_PULLUP);
 
  Serial.println("setup");
}

void loop() {
  for(int i=0;i<NUM_OPTO;i++) opto[i].loop(); 
  for(int i=0;i<NUM_DIGITAL;i++) buttons[i].loop(); 
  readMux();

 static uint32_t timer=0;
 int interval = 25;
 static byte state= 0;
  if(millis()-timer>interval){
    timer=millis();

    //optosensors send
    for(byte i=0;i<NUM_OPTO;i++){
      if(opto[i].available()){ 
          int outVal = opto[i].getVal();
          //Serial.println(outVal);
          comms.outu8(99+i);
          comms.out16(outVal);
          comms.send();
      }
    }
  }
  
  //buttons send
  for(byte i=0;i<NUM_DIGITAL;i++){
      if(buttons[i].available()){ 
//           Serial.print(i);
//        Serial.print("\t");
          int outVal = buttons[i].getState();
//          Serial.print(outVal);
//        Serial.println("\t");
          //Serial.println(outVal);
          comms.outu8(50 + i);
          comms.out16(outVal);
          comms.send();
      }
    }

  if (comms.available()){
    byte inBuffer[64];
    byte index=0;

    comms.getInput(inBuffer,  &index);
    //comms.outu8(index);
    //comms.send();
    int val =0;
    while(val<index){
      //comms.outu8(val);
      //comms.outu8(inBuffer[val]);
      val++;
    }
    //comms.send();

//    digitalWrite(ledPin,HIGH);
//  delay(50);
//  digitalWrite(ledPin,LOW);
//    
  }

}

void sMon(String cname, int val, byte newline){
  Serial.print(cname);
  Serial.print(" :");
  Serial.print(val);
  if (newline==1) Serial.println();
  else Serial.print("\t");
}

void readMux(){
  static uint32_t timer = 0;
  int interval = 50;
  static byte address = 0;
  static int vals[8];

  if(millis()-timer>interval){
    timer = millis();
    vals[address] = analogRead(muxin);
      
    for( int k=0;k<3;k++) {
      byte val = (address >> k) & 1;
      //sMon("", mux[k], 0);
      //sMon("", val, 0);
      digitalWrite(mux[k], val);
    }
    
    if(address<3) address++;
    else{ 
      address = 0;
      //Serial.print("mux ");
      comms.outu8(31);
      for(int i=0;i<8;i++) {
        comms.outu16(vals[i]);
      }
      comms.send();
    }
    
  }
}
//
//int optoVals[4];
//
//void readOpto(){
//  for(int i=0;i<4;i++) optoVals
//}
