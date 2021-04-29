/*
 *  
 *
 */
#include <WiFi.h>
#include <WiFiUdp.h>

// WiFi network name and password:

const char * ssid = "MLE";
const char * password = "mitmusictech";
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

void setup(){
  // Initilize hardware serial:
  Serial.begin(115200);
  
  //Connect to the WiFi network
  connectToWiFi(ssid, password);
}

void loop(){
  if(!serverFound){
    //only send data when connected
    static long timer = 0;
    int interval = 500;
  
    if(millis()-timer > interval){
      timer = millis();
      static byte count = 0;
      if(connected){
        //Send a packet
        udp.beginPacket(castAddress,udpPort);
        udp.printf("Seconds since boot: %lu", count);
        udp.endPacket();
        Serial.println("looking for server");
      }else Serial.println("not connected");
      count++;
    }
  } else {
    //only send data when connected
    static long timer = 0;
    int interval = 500;
  
    if(millis()-timer > interval){
      timer = millis();
      static byte count = 0;

      //Send a packet
      udp.beginPacket(castAddress,udpPort);
      udp.printf("%lu", count);
      udp.endPacket();
      Serial.print("sending to server ");
      Serial.println(count);
      count++;
    }
  } 

 //read from UDP
//  uint8_t incUDP[50];
//  memset(incUDP,0,50);
//  udp.parsePacket();
//  if(udp.read(incUDP, 50) > 0){
//    if(serverFound == false) {
//      Serial.println("server connected");
//      serverFound = true;
//    }
//    serverAddress = udp.remoteIP();
//    serverPort = udp.remotePort();
//    Serial.print("incoming: ");
//    Serial.println((char *)incUDP);
//  }
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
          connected = true;
          break;
      case SYSTEM_EVENT_STA_DISCONNECTED:
          Serial.println("WiFi lost connection");
          connected = false;
          break;
      default: break;
    }
}
