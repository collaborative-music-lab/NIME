#include "m370_communication.h"

const byte COMM_DEBUG = 0;
WiFiServer server(80);
WiFiUDP udp;

//standard wifi settins
int udpPort = 1234; //where we listen
int serverPort = 1235; //where we send to

//Are we currently connected?
boolean connected2 = false;
boolean serverFound = false;

extern const char * ssid;
extern const char * password;
extern const char * port;

IPAddress espAddress(192,168,1,100);
IPAddress castAddress(192,168,1,255);
IPAddress serverAddress(192,168,1,100);

//must be global so WIFI_EVENT can see iit
  byte m370_wifiConnectionState = 0; //0= no connection, 1= connected to network, 2=handshake completed

//Firmware metadata
// extern const String FIRMWARE_NAME;
// const String _FIRMWARE_NAME = FIRMWARE_NAME;
// extern const String FIRMWARE_VERSION;
// extern const String FIRMWARE_CREATOR;
// extern const String FIRMWARE_DATE;
// extern const String FIRMWARE_NOTES;
/*********************************************
CONSTRUCTOR
*********************************************/

m370_communication::m370_communication(comModes _mode, uint16_t size){
  Init(size);
  mode = _mode;
}

m370_communication::m370_communication(comModes _mode){
  Init(64);
  mode = _mode;
}

m370_communication::m370_communication(){
  Init(64);
}


void m370_communication::Init(uint16_t size){
  bufSize=size;
  rawInBuffer = new uint8_t(bufSize);
  outBuffer = new uint8_t(bufSize);
}

uint8_t m370_communication::begin( String firmwareNotes[5]){
  enable=1;
  inWriteIndex=0;
  inReadIndex=0;
  _firmwareNotes = firmwareNotes;

  Init(bufSize);
  uint8_t returnVal=0;
  Serial.begin(baudRate);

  //set ports
  udpPort = 0; //where we listen

  for (int i = 0; isdigit(port[i]); ++i){
      udpPort += (port[i] - '0') * pow(10,3-i) ;
  }

  // while(1) { 
  //   //Serial.begin(baudRate);
  //   delay(200);
  //   Serial.println("comm mode" + String(mode));
  // }

  if( mode==SERIAL_ONLY || mode==APandSERIAL || mode==STAandSERIAL) returnVal =  serial_setup();
  if( mode==SERIAL_ONLY) {
    ACTIVE_MODE = 1;
    m370_wifiConnectionState = 5;
  }
  //while(1) {Serial.println("opo"); delay(1000);}
  if( mode==APandSERIAL || mode==AP_WIFI){
      WIFI_MODE = 1;
      returnVal += wifi_ap_setup();
  } else if ( mode==STAandSERIAL || mode==STA_WIFI ){//STA mode
    WIFI_MODE = 0;
    returnVal += wifi_sta_setup();
  }
  Serial.println("comm mode " + String(mode));
  return returnVal>0;
}

/*
connect() listens for incoming messages on all specific interfaces
and returns a value based on the first interface it hears from:
1 = serial
2 = wifi
2 = bluetooth (not  implemented)

Typically connect will be called from a while  loop in a setup functtion
This allows the ucontroller to perform specific tasks to indicate connect status
*/
uint8_t m370_communication::connect(){
  //handshaking
  byte numAvailable = available();
  Serial.println("connect ");

  if(m370_wifiConnectionState==0) {
    Serial.print("Waiting for connection ");
    espAddress = WiFi.localIP(); 
    Serial.print(espAddress);
    Serial.println(numAvailable);
    Serial.println("wifi " + String(WIFI_ENABLE));
  } 

  if(m370_wifiConnectionState==5) {
    SERIAL_ENABLE = 1;
    m370_wifiConnectionState = 1;
    Serial.println("force serial");
    return m370_wifiConnectionState;
  }


  if( numAvailable > 0 ){
    // Serial.print('a');
    // Serial.write( _available );
    getInput(inBuffer,&inIndex);
    for(int i=0;i<inIndex;i++) Serial.print(inBuffer[i]);
    send();

    if(inIndex>0){
      if(inBuffer[0]  == 253){
        if (inBuffer[1] == 1 ) WIFI_ENABLE = 0;
        if (inBuffer[1] == 2 ) SERIAL_ENABLE = 0;
        m370_wifiConnectionState = inBuffer[1];      
      }
    }//else
  }//end handshake

  ACTIVE_MODE = m370_wifiConnectionState;
  delay(100);

  //print firmware notes:
  
  // byte numStrings = 0;
  // byte index = 0;
  // while (numStrings<4){
  //   outu8(252+numStrings);
  //   byte outVal = &_firmwareNotes+index;

  //   while(outVal != 0){
  //     outu8(outVal);
  //     index++;
  //   }
  //   send();
  //   index++;
  //   numStrings++;
  // }

  // delay(1000); 
  // while(1){
  //   outu8(213);
  //   send();
  //   delay(500);
  // }
  return m370_wifiConnectionState;
}


/*********************************************
SETUP FUNCTIONS
*********************************************/

uint8_t m370_communication::wifi_ap_setup(){
  Serial.println("Initializing Access Point: " + String(ssid));
  WiFi.softAP(ssid, password);
  WiFi.onEvent(WiFiEvent);
  server.begin();
  espAddress = WiFi.softAPIP();
  Serial.print("ESP IP address: ");
  Serial.print(espAddress);
  Serial.print(" ");
  Serial.println(udpPort);
  castAddress = espAddress;
  castAddress[3]=255;
  Serial.print("Broadcast IP address: ");
  Serial.println(castAddress);
  udp.begin(WiFi.localIP(),udpPort);
  WIFI_ENABLE = 1;
  return 1;
}

uint8_t m370_communication::wifi_sta_setup(){
  Serial.println("Connecting to WiFi network: " + String(ssid));

  // delete old config
  WiFi.disconnect(true);
  //register event handler
  WiFi.onEvent(WiFiEvent);
  
  //Initiate connection
  WiFi.begin(ssid, password);
  Serial.print("WIFI STA setup, ");
  Serial.println("Waiting for WIFI connection...");
  WIFI_ENABLE = 1;
  return 1;
}

uint8_t m370_communication::serial_setup(){
  //Serial.begin(baudRate);
  delay(200);
  if( COMM_DEBUG ) Serial.println("Serial initialized");
  //m370_wifiConnectionState=1;
  SERIAL_ENABLE = 1;
  return 1;
}

void m370_communication::setIP(byte base[]){
  for(int i=0;i<4;i++)Serial.println(base[i]);
   // castAddress(base[0],base[1],base[2],255);
}
/*********************************************
INPUT
*********************************************/

//Stores raw slip encoded data in input buffer, and returns
//number of available bytes
uint16_t m370_communication::available(){
  if(SERIAL_ENABLE){
    while(Serial.available()) {
      ACTIVE_MODE = 1;
      inWriteIndex<bufSize-1 ? inWriteIndex++ : inWriteIndex=0 ;
      rawInBuffer[inWriteIndex] = Serial.read();
      if(COMM_DEBUG){
        Serial.print('w');
        Serial.write( inWriteIndex );
      }
    }
  }
  if(WIFI_ENABLE){
    //read from UDP
    int size = udp.parsePacket();
    //Serial.println("udp available " + String(size));
    if(size > 0){
      serverAddress = udp.remoteIP();
      //serverPort = udp.remotePort();
      
      for(int i=0; i<size; i++){
        inWriteIndex<bufSize-1 ? inWriteIndex++ : inWriteIndex=0 ;
        rawInBuffer[inWriteIndex] = udp.read();
        if(COMM_DEBUG) Serial.print("wifi ");
        if(COMM_DEBUG){
          Serial.print(rawInBuffer[inWriteIndex]);
          Serial.print(" ");
        }
        if(COMM_DEBUG) Serial.println();
      }
    }
  }
  
  _available = (inWriteIndex + bufSize - inReadIndex) % bufSize;
  // if(_available > 0){
  //   Serial.print("check available ");
  //   Serial.println(_available);
  //   Serial.print("write indx ");
  //   Serial.println(inWriteIndex);
  //   Serial.print("read index ");
  //   Serial.println(inReadIndex);
  //   for(int i=inReadIndex;i<inReadIndex+_available;i++){
  //     Serial.print(rawInBuffer[i]);
  //     Serial.print(" ");
  //   }
  //   Serial.println();
  // }
  return _available;
}

// uint16_t m370_communication::slipDecode(byte val){

// }

//uint16_t m370_communication::available(){ return _available;}

uint16_t m370_communication::getInput(uint8_t inBuf[], uint8_t *inInd){
  byte val;
  int inBufSize = *inInd;
  *inInd=0;

  while( ((inWriteIndex+bufSize-inReadIndex)%bufSize) > 0) {
    val = rawInBuffer[inReadIndex];
    inReadIndex<bufSize-1 ? inReadIndex++ : inReadIndex=0 ;
    //slip decode
    if(val==ESC_BYTE){
      if(1){ //*inInd < inBufSize) {
        inBuf[*inInd]  = val;
        inReadIndex<bufSize-1 ? inReadIndex++ : inReadIndex=0 ;
        *inInd+=1;
      }
    } else if(val==END_BYTE){
      _available = (inWriteIndex + bufSize - inReadIndex) % bufSize;
      if(COMM_DEBUG){
        Serial.print('a');
        Serial.print(_available);
        Serial.print('g');
        Serial.print(*inInd);
        for(int i=0;i<*inInd;i++)Serial.print(inBuf[i]);
        Serial.println('g');
      }
      return _available;
    } else {
      if(1){ //*inInd < inBufSize) {
        inBuf[*inInd]  = val;
        *inInd+=1;
      }
    }//slip

  }//while
  if(COMM_DEBUG){
    Serial.print('h');
        for(int i=0;i<*inInd;i++)Serial.print(inBuf[i]);
          Serial.print('h');
    }
  _available = (inWriteIndex + bufSize - inReadIndex) % bufSize;
  return _available;
}


/*********************************************
OUTPUT
*********************************************/

void m370_communication::outu8(uint8_t val){
  slipOut(val);
}

void m370_communication::out8(int8_t val){
  uint8_t val2 = (int)val+128;
  slipOut(val2);
}

void m370_communication::outu16(uint16_t val){
  slipOut(val>>8);
  slipOut( val );
}

void m370_communication::out16(int16_t val){
  uint16_t val2 = (int32_t)val + (1<<15);
  slipOut(val2>>8);
  slipOut(val2);
}

void m370_communication::outu32(uint32_t val){
  slipOut(val>>24);
  slipOut(val>>16);
  slipOut(val>>8);
  slipOut(val);
}
void m370_communication::out32(int32_t val){
  uint32_t val2 = abs(val);
  val < 0 ? val2 = (1<<15) - val2  : val2 += (1<<31);
  slipOut(val2>>24);
  slipOut(val2>>16);
  slipOut(val2>>8);
  slipOut(val2);
}

void m370_communication::outString(String val){
  byte toSend[255];
  val.getBytes(toSend,255);
  for(int i=0;i<val.length();i++) slipOut(toSend[i]);
}

uint16_t m370_communication::send(){
  if(outIndex<1) return 0;
  pack(255);
  //addEndByte();
  // Serial.print("Sent: ")
  // Serial.print(outIndex);

  if(enable){
    if(asciiDebug) {
      for(byte i=0;i<outIndex;i++){
        Serial.print (outBuffer[i]);
        Serial.print(" ");
        }
      }
    //serial
    else if(ACTIVE_MODE==1){ //else if(SERIAL_ENABLE){
      for(byte i=0;i<outIndex;i++){
        Serial.write(outBuffer[i]);
      }
    }
    //wifi
    else if(ACTIVE_MODE==2){ //else if(WIFI_ENABLE){
      // Serial.print("Sending " + String(outBuffer[0]) + "to ");
      // Serial.print(serverAddress);
      // Serial.print(", ");
      // Serial.println(serverPort);
      udp.beginPacket(serverAddress,serverPort);
      for(byte i=0;i<outIndex;i++){
        udp.write(outBuffer[i]);
      }
      udp.endPacket();
    }
    uint16_t  returnValue =   outIndex;
    outIndex = 0;
    return  returnValue;
  }
}//send

void m370_communication::slipOut(byte val){
  if(val == END_BYTE || val == ESC_BYTE){
    pack(ESC_BYTE);
    pack(val);
  } else pack(val);
}

void m370_communication::pack(byte val){
  outBuffer[outIndex++] = val;
}

//int byteToInt(byte val1, byte val2){
//  int sign = 1;
//  int result = (val1 & 127)<<8 + val2;
//  if(val1>>7==1) sign =-1;
//  result *= sign;
//
//  return result;
//}


//wifi event handler
//called as interrupt on changes to wifi connection status
void WiFiEvent(WiFiEvent_t event){

  switch(event) {
    case SYSTEM_EVENT_STA_GOT_IP:
        //When connected set 
        Serial.print("WiFi connected! IP address: ");
        espAddress = WiFi.localIP(); 
        Serial.println(espAddress); 
        //initializes the UDP state
        //This initializes the transfer buffer
        //m370_wifiConnectionState = 1;
        udp.begin(WiFi.localIP(),udpPort);
        serverFound=1;
        break;
    case SYSTEM_EVENT_STA_DISCONNECTED:
        //Serial.println("WiFi lost connection");
        serverFound = 0;
        //m370_wifiConnectionState = 1;
        break;
    case SYSTEM_EVENT_AP_STACONNECTED:
        Serial.print("New device connected "  );
        serverFound = 1;
        //m370_wifiConnectionState = 1;
        break;
    default: break;
  }
}

