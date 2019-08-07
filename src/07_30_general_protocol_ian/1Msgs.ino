// initialize global serial buffer
byte serialBuffer[64];
const int bufferLength = 64;
int bufferIndex = 0;

// define end bytes and escape bytes needed for slip encoding
const byte endByte = 255;
const byte escByte = 254;


/*********************************************
Setup and loop
*********************************************/
void MsgsSetup(){
  
}

void sendButtonMessage(byte channel, byte x, byte y, byte z, bool state) {
  if (channel < 0) {
    channel = 0;
  }
  else if (channel > 3) {
    channel = 3;
  }
  else {
   /* slipOutByte(BUTTON_CH_0 + channel);
    slipOutByte(x);
    slipOutByte(y);
    slipOutByte(z);
    slipOutByte(state);*/
    Serial.write(serialBuffer, bufferIndex);
    Serial.write(endByte);
    bufferIndex = 0;
    // byte order: [id][x][y][z][state]
  }
}

void sendFaderMessage(byte channel, byte x, byte y, long val, bool isSigned) {
  if (isSigned) val += 32768;
  if (channel < 0) {
    channel = 0;
  }
  else if (channel > 6) {
    channel = 6;
  }
  else {
    //convert all values to a byte array
    byte testVal[4];
    testVa[0] = channel;
    testVal[1] = num;
    
    testVal[2] =getHighByte( val );
    testVal[3] =getLowByte( val );
    
    byte state = WifiSend( testVal, 4 );
    byte serialSstate = SerialSend( testVal, 4 );

  }

}

// adds a byte (or escape byte and byte) to the buffer of bytes to be sent
void slipOutByte(byte val) {
  if ((val == endByte) or (val == escByte)) {
    serialBuffer[bufferIndex] = escByte;
    bufferIndex++;
  }
  serialBuffer[bufferIndex] = val;
  bufferIndex++;
}

// writes a two-byte int to the buffer, adding escape bytes if necessary
void slipOutInt(uint16_t val) { //uint16_t
  uint8_t lowValByte = val & 0xff;
  uint8_t highValByte = (val >> 8);
  slipOutByte(highValByte);
  slipOutByte(lowValByte);
}
