/*
m370_communication

1. check whether communicating via Serial, WIFI_AP, or WIFI_STA
2. Setup appropriate channel
3. buffer and send data
4. check for and store incoming data
 * 
 */


#ifndef M370COMMUNICATION_h
#define M370COMMUNICATION_h
#include "Arduino.h"
#include <WiFi.h>
#include <WiFiUdp.h>

//#include "src/SparkFunLSM6DS3.h"
//#include "src/Adafruit_MPR121.h"
//#include "src/NewPing.h"
//#include "src/Adafruit_MCP4728.h"
//#include <slip.h>

// void  debug(String name, int val);
// void  debug2(String name, int val1, int  val2);
// void  debug3(String name, int val1, int val2,  int val3);

/************************
**Communication setup
************************/
//for AP mode: https://randomnerdtutorials.com/esp32-access-point-ap-web-server/



//For wifi, AP mode creates a network and STA mode joins a network
enum comModes{SERIAL_ONLY, AP_WIFI, STA_WIFI, APandSERIAL, STAandSERIAL};
void WiFiEvent(WiFiEvent_t event);

/************************
**Communication class
************************/


class m370_communication{
	public:
	m370_communication();
	m370_communication(comModes _mode); //communication mode as enum : {SERIAL, AP_WIFI, STA_WIFI, APandSERIAL, STAandSERIAL};
	m370_communication(comModes _mode, uint16_t size); //buffer sizes in bytes, def:64

	uint8_t begin( String firmwareNotes[5]); //returns success or failure
	uint8_t connect(); //returns 1=serial, 2=wifi, 3=bluetooth
	void setIP(byte base[]);

	//uint16_t checkInput();
	uint16_t available();
	uint16_t getInput(uint8_t *inBuf, uint8_t *inInd);

	void outu8(uint8_t val);
	void out8(int8_t val);
	void outu16(uint16_t val);
	void out16(int16_t val);
	void outu32(uint32_t val);
	void out32(int32_t val);
	void outString(String val);

	uint16_t send();

	byte enable = 1;
	byte asciiDebug = 0;
	int baudRate = 460800;
	comModes mode = SERIAL_ONLY;

	  //below all auto configured based  on comMode
	byte SERIAL_ENABLE = 0; //enables communication over USB
	byte WIFI_MODE = 0; //0=STA, 1=AP
	byte WIFI_ENABLE = 0; //enables communication over WIFI
	byte ACTIVE_MODE = 0; //1=serial,2=wifi, 3=blutooth
	byte BLUETOOTH_ENABLE = 0;

	//standard wifi settins
	int localport = 8002;
	int udpPort2 = 1238;
	int serverPort = 1235;
	

	byte handshakeAck = 0;
	byte serverFound=0;

	// IPAddress serverAddress(192,168,1,100);
	  
	private:
	void Init(uint16_t size);
	void pack(byte val);
	void slipOut(byte val);
	String* _firmwareNotes;

	uint16_t bufSize;
	
	//slip decoded buffer
	byte inBuffer[64];
	uint8_t inIndex = 0;
	//raw input
	byte *rawInBuffer;
	uint8_t inWriteIndex = 0;
	uint8_t inReadIndex = 0;

	byte *outBuffer;
	uint8_t outIndex = 0;

	uint16_t _available = 0;

	uint8_t wifi_ap_setup();
	uint8_t wifi_sta_setup();
	uint8_t serial_setup();

  
  	// define end bytes and escape bytes needed for slip encoding
	const byte END_BYTE = 255;
	const byte ESC_BYTE = 254;
};

#endif
