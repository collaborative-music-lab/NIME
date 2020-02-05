
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
byte serBufferIndex = 0;

// define end bytes and escape bytes needed for slip encoding
const byte END_BYTE = 255;
const byte ESC_BYTE = 254;

void SlipOutInt(int val){
  SlipOutByte( (byte) (val >> 8) );//send upper byte 
  SlipOutByte( (byte) val ); //send lower byte 
}

// adds a byte (or escape byte and byte) to the buffer of bytes to be sent
void SlipOutByte(byte val) {
  if ((val == END_BYTE) or (val == ESC_BYTE)) {
    serialBuffer[serBufferIndex] = ESC_BYTE;
    serBufferIndex++;
  }
  serialBuffer[serBufferIndex] = val;
  serBufferIndex++;
}

void SerialOutSlip(){
  for(byte i=0;i<serBufferIndex;i++){
    Serial.write(serialBuffer[i]);
  }
  Serial.write(END_BYTE);
  serBufferIndex = 0;
}



byte SerialSend( byte val[], byte num){
  if( SerialAvailable ){
    for( int i=0; i<num ; i++){
      SlipOutByte( val[i] );
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

