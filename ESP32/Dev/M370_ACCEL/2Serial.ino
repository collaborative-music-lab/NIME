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
  if( SERIAL_ENABLE || ANALOG_DEBUG){
    Serial.begin(115200);
    delay(100);
    if(ANALOG_DEBUG) Serial.println("Serial enabled");
  }
}

byte SerialAvailable(){
  if( (Serial.available()>0) && SERIAL_ENABLE) return 1;
  return 0;
}

void CheckSerial(){
  if( SERIAL_ENABLE){
    while(Serial.available()){
      byte val = Serial.read();
      //Serial.write(val);
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
}//checkSerial

void ProcessSerialMessage(byte message[], byte len){
  if(SERIAL_DEBUG){
    SlipOutByte(1);
    SlipOutByte(message[1]);
    SlipOutByte(message[2]);
    SerialOutSlip();
  }
  if(WIFI_DEBUG){
    for(byte i=0;i<len;i++){
      Serial.print(message[i]);
      Serial.print(" ");
    }
    Serial.println();
  }

        
  switch(message[0]){
    case 0: //get new OSC address
    analogSendRate = byteToInt(message[1],message[2]);
    break;

    case 1: //enable analog inputs
    if(message[1]<12) sensors[message[1]].enable = message[2]>0; 
    else if( message[1]<15) accels[message[1]-12].enable = message[2]>0; 
    else if( message[1]<18) gyros[message[1]-15].enable = message[2]>0; 
    else if( message[1]<19) temps.enable = message[2]>0; 
    break;

    case 2: //set analog transmission rate
    if(message[1]<12)  sensors[message[1]].SetInterval(message[2]);
    else if( message[1]<15) accels[message[1]-12].SetInterval( message[2]); 
    else if( message[1]<18) gyros[message[1]-15].SetInterval( message[2]); 
    else if( message[1]<19) temps.SetInterval(message[2]);
    break;

    case 3: //set analog mode
 //   PROCESS_MODE type = MEAN;
    if(message[1]<12) {
      switch(message[2]){
        case 0: sensors[message[1]].sampleProcessMode = MEAN; break;
        case 1: sensors[message[1]].sampleProcessMode = MEDIAN; break;
        case 2: sensors[message[1]].sampleProcessMode = MIN; break;
        case 3: sensors[message[1]].sampleProcessMode = MAX; break;
        case 4: sensors[message[1]].sampleProcessMode = PEAK_DEVIATION; break;
        case 5: sensors[message[1]].sampleProcessMode = CAP_SENSE; break;
        
        case 10: 
        sensors[message[1]].sampleProcessMode = TRIG;
        trigPin =  sensors[message[1]].pin;
        pinMode(trigPin, OUTPUT);
        break;
        case 11: sensors[message[1]].sampleProcessMode = ECHO; break; 
      }
    }
    break;

    case 10: //set number of _MPR121 electrodes
    NUM_ELECTRODES = message[1];
    break;

    case 11: //set cap timing
    capSense[message[1]].SetInterval(message[2]);
    break;
    
    case 12: //set charge current
    chargeCurrent = message[1];
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
    if(0) {
      Serial.print (serialBuffer[i]);
      Serial.print(" ");
    }
    else Serial.write(serialBuffer[i]);
  }
  if(0) {
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
