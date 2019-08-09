// initialize message ID's
const byte BUTTON_CH_0 = 0;
const byte BUTTON_CH_1 = 1;
const byte BUTTON_CH_2 = 2;
const byte BUTTON_CH_3 = 3;

const byte FADER_CH_0 = 4;
const byte FADER_CH_1 = 5;
const byte FADER_CH_2 = 6;
const byte FADER_CH_3 = 7;
const byte FADER_CH_4 = 8;
const byte FADER_CH_5 = 9;
const byte FADER_CH_6 = 10;

const byte IMU_CH_0 = 11;
const byte IMU_CH_1 = 12;
const byte IMU_CH_2 = 13;
const byte IMU_CH_3 = 14;
const byte IMU_CH_4 = 15;

// initialize global message buffer
byte messageBuffer[64];

// initialize serial buffer (containing slip-encoded message)
byte serialBuffer[64];
int serBufferIndex = 0;

// define end bytes and escape bytes needed for slip encoding
const byte endByte = 255;
const byte escByte = 254;


/*********************************************
Setup and loop
*********************************************/
void MsgsSetup(){
  
}

void sendButtonMessage(byte channel, byte num, int state) {
  if (channel < 0) {
    channel = 0;
  }
  else if (channel > 3) {
    channel = 3;
  }
  else {
    uint8_t id = BUTTON_CH_0 + channel;
    uint8_t highValByte = (state >> 8);
    uint8_t lowValByte = state & 0xff;
    messageBuffer[0] = id;
    messageBuffer[1] = num;
    messageBuffer[2] = highValByte;
    messageBuffer[3] = lowValByte;
    SerialSend(messageBuffer, 4);
    WifiSend(messageBuffer, 4);
    // byte order: [id][num][highValByte][lowValByte]
    // total message length: 4 bytes
  }
}

void sendFaderMessage(byte channel, byte num, int val) {
  if (channel < 0) {
    channel = 0;
  }
  else if (channel > 6) {
    channel = 6;
  }
  else {
    uint8_t id = FADER_CH_0 + channel;
    uint8_t highValByte = (val >> 8);
    uint8_t lowValByte = val & 0xff;
    messageBuffer[0] = id;
    messageBuffer[1] = num;
    messageBuffer[2] = highValByte;
    messageBuffer[3] = lowValByte;
    SerialSend(messageBuffer, 4);
    WifiSend(messageBuffer, 4);
    // byte order: [id][num][highValByte][lowValByte]
    // total message length: 4 bytes
  }

}
// TODO: WRITE SLIP OUT FUNCTION THAT HAS NARROWER SCOPED OUTPUT BUFFER (takes in full message and length as argument)


// adds a byte (or escape byte and byte) to the buffer of bytes to be sent
void slipOutByte(byte val) {
  if ((val == endByte) or (val == escByte)) {
    serialBuffer[serBufferIndex] = escByte;
    serBufferIndex++;
  }
  serialBuffer[serBufferIndex] = val;
  serBufferIndex++;
}
