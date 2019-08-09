
/*********************************************
Setup and loop
*********************************************/
static byte serialBuffer[64] ;

void SerialSetup(){
  Serial.begin(115200);
}


byte SerialAvailable(){
  if( Serial && serialEnable) return 1;
  return 0;
}

byte SerialSend( byte val[], byte num){
  
  if( SerialAvailable ){
    for( int i=0; i<num ; i++){
      slipOutByte( val[i] );
    }
  
    Serial.write(serialBuffer, bufferIndex);
    Serial.write(endByte);
    bufferIndex = 0;
  }
}

