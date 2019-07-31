const byte LED_PIN = 22;
byte led_val = 0;

/*
 *  This sketch sends random data over UDP on a ESP32 device
 *
 */
#include <WiFi.h>
#include <WiFiUdp.h>

// WiFi network name and password:
const char * networkName = "Studio_MoMe'";
const char * networkPswd = "Downtown";

//IP address to send UDP data to:
// either use the ip address of the server or 
// a network broadcast address
const char * udpAddress = "192.168.1.202";
const int udpPort = 804;

//Are we currently connected?
boolean connected = false;

//The udp library class
WiFiUDP udp;

void setup() {
  Serial.begin(115200);
  
  pinMode( LED_PIN, OUTPUT);

  connectToWiFi(networkName, networkPswd);

}

void loop() {
  //only send data when connected
  if(connected){
    //Send a packet
    udp.beginPacket(udpAddress,udpPort);
    udp.printf("Seconds since boot: %u", millis()/1000);
    udp.endPacket();
  }
  
  led_val = !led_val;
  digitalWrite(LED_PIN, led_val);
  delay( 200 ); 
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
    }
}
