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

const byte IMU_RAW_CH_0 = 11;
const byte IMU_RAW_CH_1 = 12;
const byte IMU_RAW_CH_2 = 13;
const byte IMU_RAW_CH_3 = 14;
const byte IMU_RAW_CH_4 = 15;

const byte IMU_FUSION_CH_0 = 16;
const byte IMU_FUSION_CH_1 = 17;
const byte IMU_FUSION_CH_2 = 18;
const byte IMU_FUSION_CH_3 = 19;
const byte IMU_FUSION_CH_4 = 20;

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

void sendButtonMessage(byte channel, byte num, int state, int interval, int * lastTime) {
  if (curTime - *lastTime < interval) {
    return;
  }
  else {
    *lastTime = curTime;
  }
  
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

void sendFaderMessage(byte channel, byte num, int val, int interval, int * lastTime) {
  if (curTime - *lastTime < interval) {
    return;
  }
  else {
    *lastTime = curTime; // update the contents of that memory address to curTime
  }
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

void sendImuRaw(byte channel, sensors_event_t a, sensors_event_t m, sensors_event_t g, int interval, int* lastTime) {
  if (curTime - *lastTime < interval) {
    return;
  }
  else {
    *lastTime = curTime; // update the contents of that memory address to curTime
  }
  
  union {
    float axFloat;
    byte axBytes[4];
  } axUnion;

  union {
    float ayFloat;
    byte ayBytes[4];
  } ayUnion;

  union {
    float azFloat;
    byte azBytes[4];
  } azUnion;

  union {
    float mxFloat;
    byte mxBytes[4];
  } mxUnion;

  union {
    float myFloat;
    byte myBytes[4];
  } myUnion;

  union {
    float mzFloat;
    byte mzBytes[4];
  } mzUnion;

  union {
    float gxFloat;
    byte gxBytes[4];
  } gxUnion;

  union {
    float gyFloat;
    byte gyBytes[4];
  } gyUnion;

  union {
    float gzFloat;
    byte gzBytes[4];
  } gzUnion;

  axUnion.axFloat = a.acceleration.x;
  ayUnion.ayFloat = a.acceleration.y;
  azUnion.azFloat = a.acceleration.z;
  mxUnion.mxFloat = m.magnetic.x;
  myUnion.myFloat = m.magnetic.y;
  mzUnion.mzFloat = m.magnetic.z;
  gxUnion.gxFloat = g.gyro.x;
  gyUnion.gyFloat = g.gyro.y;
  gzUnion.gzFloat = g.gyro.z;

  messageBuffer[0] = IMU_RAW_CH_0 + channel;
  for (int i = 0; i < 4; i++) {
    messageBuffer[i + 1] = axUnion.axBytes[i];
    messageBuffer[i + 5] = ayUnion.ayBytes[i];
    messageBuffer[i + 9] = azUnion.azBytes[i];
    messageBuffer[i + 13] = mxUnion.mxBytes[i];
    messageBuffer[i + 17] = myUnion.myBytes[i];
    messageBuffer[i + 21] = mzUnion.mzBytes[i];
    messageBuffer[i + 25] = mxUnion.mxBytes[i];
    messageBuffer[i + 29] = myUnion.myBytes[i];
    messageBuffer[i + 33] = mzUnion.mzBytes[i];
  }
  SerialSend(messageBuffer, 37);
  WifiSend(messageBuffer, 37);
  // byte order: [id]
  //             [accelX float][-][-][-][accelY float][-][-][-][accelZ float][-][-][-]
  //             [magX float][-][-][-][magY float][-][-][-][magZ float][-][-][-]
  //             [gyroX float][-][-][-][gyroY float][-][-][-][gyroZ float][-][-][-]
  // total message length: 37 bytes (each float takes 4 bytes, there are 3 floats per degree-of-freedom)
}

// adds a byte (or escape byte and byte) to the buffer of bytes to be sent
void slipOutByte(byte val) {
  if ((val == endByte) or (val == escByte)) {
    serialBuffer[serBufferIndex] = escByte;
    serBufferIndex++;
  }
  serialBuffer[serBufferIndex] = val;
  serBufferIndex++;
}
