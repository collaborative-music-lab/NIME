

// WiFi network name and password:
const char * networkName = "Beer";
const char * networkPswd = "Fak2@1959";

//IP address to send UDP data to:
// either use the ip address of the server or 
// a network broadcast address
const char * udpAddress = "192.168.1.202";
const int udpPort = 804;

//Are we currently connected?
boolean wifiConnected = false;

//The udp library class
WiFiUDP udp;


/*********************************************
Setup and loop
*********************************************/

void WiFiSetup(){
  connectToWiFi(networkName, networkPswd);
}

void WiFiLoop(){
  static byte testVal = 0;
  
  if( WifiAvailable() ){
    udp.beginPacket(udpAddress,udpPort);
    udp.print(testVal);
    udp.endPacket();
    testVal++;
  }
}

/*********************************************
  WIFI HELPER FUNCTIONS
*********************************************/

byte WifiSend(byte val[], byte num){
  if( WifiAvailable() ){
    udp.beginPacket(udpAddress,udpPort);
    for( byte i=0; i< num; i++) udp.print(val[i]);
    udp.endPacket();
  }
}

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
    switch(event) {
      case SYSTEM_EVENT_STA_GOT_IP:
          //When connected set 
          Serial.print("WiFi connected! IP address: ");
          Serial.println(WiFi.localIP());  
          //initializes the UDP state
          //This initializes the transfer buffer
          udp.begin(WiFi.localIP(),udpPort);
          wifiConnected = true;

          for(int i=0;i<5;i++){
          digitalWrite(LED_PIN, 1);
          delay(100);
          digitalWrite(LED_PIN, 0);
          delay(100);
          }
          Serial.println("still on");
          break;
          
      case SYSTEM_EVENT_STA_DISCONNECTED:
          Serial.println("WiFi lost connection");
          wifiConnected = false;
          break;
    }
}

byte WifiAvailable(){
  if( wifiConnected == 1 && wifiEnable == 1) return 1;
  return 0;
}
