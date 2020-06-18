
int localport = 8002;

//Broadcast address for your network
//most likely the same as your routers IP 
//but with the last number set to 255
//e.g. (route) 192.168.0.100 = (broadcast) 192.168.0.255
const IPAddress castAddress(192,168,1,255);
const int udpPort = 1234;

IPAddress serverAddress(192,168,1,100);
int serverPort = 1000;

//Are we currently connected?
boolean connected = false;
boolean serverFound = false;

//The udp library class
WiFiUDP udp;

void WiFiSetup(){
  // Initilize hardware serial:
  //Serial.begin(115200);
  
  //Connect to the WiFi network
  if( WIFI_ENABLE){
    connectToWiFi(ssid, password);
    Serial.println("Wifi enabled, Serial disabled");
  }
}

void WiFiLoop(){
    //check for server IP address
  if(connected){
    while(!serverFound){
      static long timer = 0;
      int interval = 100;
  
      if(millis()-timer > interval){
        timer = millis();
      
        udp.beginPacket(castAddress,udpPort);
        udp.printf("interval: %lu", interval);
        udp.endPacket();
        Serial.println("looking for server");
        if( interval < 10000) interval+=100;
      }

      uint8_t incUDP[50];
      udp.parsePacket();
      if(udp.read(incUDP, 50) > 0){
        WIFI_ENABLE = 1;
        SERIAL_ENABLE = 0;
        serverAddress = udp.remoteIP();
        serverPort = udp.remotePort();
        Serial.print("server connected, IP: ");
        Serial.println(serverAddress);
        Serial.println("Serial disconnected");
        serverFound = true;
        break;
      }
    } 
  } //serverFound

    
  //check for UDP messages  
  if( WIFI_ENABLE ){
    byte udpLen = udp.parsePacket();

    if(udp.available()){
      uint8_t incUDP[512];
      
      udp.read(incUDP, 512);
      if( udpLen > 0){
        if(WIFI_DEBUG)  debug("udpLen",  udpLen);
        ProcessSerialMessage(incUDP, udpLen );
        //Serial.print("incoming: ");
        //Serial.println((char *)incUDP);
      }
    }//available
  }//enable
} // loop

void connectToWiFi(const char * ssid, const char * pwd){
  Serial.println("Connecting to WiFi network: " + String(ssid));

  // delete old config
  WiFi.disconnect(true);
  //register event handler
  WiFi.onEvent(WiFiEvent);
  
  //Initiate connection
  WiFi.begin(ssid, pwd);

  Serial.println("Waiting for WIFI connection...");
}

//wifi event handler
void WiFiEvent(WiFiEvent_t event){
  if( WIFI_ENABLE ){
      switch(event) {
        case SYSTEM_EVENT_STA_GOT_IP:
            //When connected set 
            Serial.print("WiFi connected! IP address: ");
            Serial.println(WiFi.localIP());  
            //initializes the UDP state
            //This initializes the transfer buffer
            udp.begin(WiFi.localIP(),udpPort);
            connected = true;
            break;
        case SYSTEM_EVENT_STA_DISCONNECTED:
            Serial.println("WiFi lost connection");
            connected = false;
            break;
        default: break;
      }
  }
}

void WiFiOutSlip(){
  static byte num = 0;
  
  udp.beginPacket(serverAddress,udpPort);
  udp.write(num);
  num++;
  
    for(byte i=0;i<serBufferIndex;i++){
      if(WIFI_DEBUG) {
        Serial.print (serialBuffer[i]);
        Serial.print(" ");
      }
      else udp.write(serialBuffer[i]);
    }
    if(WIFI_DEBUG) {
        Serial.print (END_BYTE);
        Serial.println(" ");
      }
    else {
      udp.write(END_BYTE);
      serBufferIndex = 0;
   }
  
  udp.endPacket();
}


int testData(){
  static long timer = 0;
  int interval = 500;
  static byte count = 0;

  if(millis()-timer > interval){
    timer = millis();
//    SlipOutByte(byte(count)); //pin, numerical indicator
//    SlipOutInt(count);
//    SendOutSlip();
    udp.beginPacket(serverAddress, udpPort);
    udp.printf("count %lu", count);
    udp.endPacket();
    Serial.print("Sent to ");
    Serial.print(serverAddress);
    Serial.print(" ");
    Serial.print(udpPort);
    Serial.print(": ");
    Serial.println(count);
    count++;
  }
}

int pingMe(){
  static long timer = 0;
  int interval = 500;
  static byte count = 0;

  if(millis()-timer > interval){
    timer = millis();

    Serial.print("Ping ");
    Serial.println(count);
    count++;
  }
}
