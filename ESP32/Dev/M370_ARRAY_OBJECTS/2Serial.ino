// initialize serial buffer (containing slip-encoded message)
byte serialBuffer[256];
byte serBufferIndex = 0;
byte inBuffer[64];
byte inBufferIndex=0;

// define end bytes and escape bytes needed for slip encoding
const byte END_BYTE = 255;
const byte ESC_BYTE = 254;

/*********************************************
Setup and loop
*********************************************/

void SerialSetup(){
  Serial.begin(115200);
  delay(500);
}

byte SerialAvailable(){
  if( (Serial.available()>0) && SERIAL_ENABLE) return 1;
  return 0;
}

void CheckSerial(){

  while(Serial.available()){
    byte val = Serial.read();

    if(val == ESC_BYTE){
      inBuffer[inBufferIndex]=Serial.read();
      inBufferIndex++;
    } else if (val == END_BYTE){
      ProcessSerialMessage(inBuffer, inBufferIndex);
      inBufferIndex = 0;
    } else {
      inBuffer[inBufferIndex]=val;
      inBufferIndex++;
    }
  }
}

void ProcessSerialMessage(byte message[], byte len){
  if(SERIAL_DEBUG){
    SlipOutByte(1);
    SlipOutByte(message[1]);
    SlipOutByte(message[2]);
    SerialOutSlip();
  }

        
  switch(message[0]){
    case 0: //get new OSC address
    analogSendRate = byteToInt(message[1],message[2]);
    break;

    case 1: //enable analog inputs
    sensors[message[1]].enable = message[2]>0; 
    break;

    case 2: //set analog transmission rate
    sensors[message[1]].interval = message[2];
    break;
  }
}
/*********************************************
SLIP ENCODING
*********************************************/
int byteToInt(byte val1, byte val2){
  int sign = 1;
  int result = (val1 & 127)<<8 + val2;
  if(val1>>7==1) sign =-1;
  result *= sign;

  return result;
}


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
    if(SERIAL_DEBUG) {
      Serial.print (serialBuffer[i]);
      Serial.print(" ");
    }
    else Serial.write(serialBuffer[i]);
  }
  if(SERIAL_DEBUG) {
      Serial.print (END_BYTE);
      Serial.println(" ");
    }
  else Serial.write(END_BYTE);
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
