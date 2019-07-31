
/*********************************************
Setup and loop
*********************************************/

void SerialSetup(){
  Serial.begin(115200);
}


byte SerialAvailable(){
  if( Serial && serialEnable) return 1;
  return 0;
}

