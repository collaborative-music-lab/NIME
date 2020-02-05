
/*********************************************
Setup and loop
*********************************************/

void SerialSetup(){
  Serial.begin(115200);
  delay(500);
}

byte SerialAvailable(){
  if( Serial && SERIAL_ENABLE) return 1;
  return 0;
}

/*********************************************
SLIP ENCODING
*********************************************/

// initialize serial buffer (containing slip-encoded message)
byte serialBuffer[256];
int serBufferIndex = 0;

// define end bytes and escape bytes needed for slip encoding
const byte END_BYTE = 255;
const byte ESC_BYTE = 254;

// adds a byte (or escape byte and byte) to the buffer of bytes to be sent
void slipOutByte(byte val) {
  if ((val == END_BYTE) or (val == ESC_BYTE)) {
    serialBuffer[serBufferIndex] = ESC_BYTE;
    serBufferIndex++;
  }
  serialBuffer[serBufferIndex] = val;
  serBufferIndex++;
}



byte SerialSend( byte val[], byte num){
  if( SerialAvailable ){
    for( int i=0; i<num ; i++){
      slipOutByte( val[i] );
    }
  Serial.write(serialBuffer, serBufferIndex);
  Serial.write(END_BYTE);
  serBufferIndex = 0;
  }
}

void debug(String type, int val){
  Serial.print(type);
  Serial.print("\t");
  Serial.println(val);
}

