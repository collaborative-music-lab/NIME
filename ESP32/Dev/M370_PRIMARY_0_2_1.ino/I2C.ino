/*********************************************
 * functions for attached I2C devices
 * 
 *********************************************/

 /*********************************************
 * MPR121 Capacitive Sensor
 * 
 *********************************************/
 void MPR121setup(){
 Serial.println("Adafruit MPR121 Capacitive Touch sensor test"); 
 byte count = 0;
 // Default address is 0x5A, if tied to 3.3V its 0x5B
 // If tied to SDA its 0x5C and if SCL then 0x5D
 while (!_MPR121.begin(0x5A)) {
  Serial.println("MPR121 not found, check wiring?");
  count++;
  if (count>5) break;
  delay(300);
 }
 Serial.println("MPR121 found!");
 delay(100);

 MPR121chargeCurrent(chargeCurrent); //0-63, def 16
 MPR121chargeTime(chargeTime); //0-7, def 1
 _MPR121.writeRegister(MPR121_NHDF, 0x01);
 _MPR121.writeRegister(MPR121_FDLF, 0xFF);
}

int MPR121_loop(byte num){
 
 int reading = _MPR121.baselineData(num) - _MPR121.filteredData(num);
 //reading *= -1;
 return reading + 4096;
}

void MPR121test(){
 while(1){
   // debugging info, what
  Serial.println("\t\t\t\t\t\t\t\t\t\t\t\t\t"); 
  Serial.println(_MPR121.touched(), HEX);
  Serial.print("Filt: ");
  for (uint8_t i=0; i<NUM_ELECTRODES; i++) {
   Serial.print(_MPR121.filteredData(i)); Serial.print("\t");
  }
  Serial.println();
  Serial.print("Base: ");
  for (uint8_t i=0; i<NUM_ELECTRODES; i++) {
   Serial.print(_MPR121.baselineData(i)); Serial.print("\t");
  }
  Serial.println();
  
  // put a delay so it isn't overwhelming
  delay(100);
 }
}

void MPR121chargeCurrent(byte val){
 byte FFI = 3;
 val = val & 63;
 val = (FFI<<6) + val;
 _MPR121.writeRegister(MPR121_CONFIG1, val);
}

void MPR121chargeTime(byte val){
 byte SFI = 2;
 byte ESI = 0;
 val = val & 7;
 val = (val<<5) + (SFI<<3) + ESI;
 _MPR121.writeRegister(MPR121_CONFIG2, val);
}

 /*********************************************
 * LSM6DS3 Accel/Gyro
 * 
 *********************************************/

 void IMUSetup(){
 IMU.begin();
 }

 void IMULoop(){

  if( ACCEL_ENABLE) for(byte i=0;i < 3; i++) accels[i].loop();
  if( GYRO_ENABLE ) for(byte i=0;i < 3; i++) gyros[i].loop();
  if( TEMP_ENABLE ) for(byte i=0;i < 1; i++) temps.loop();

    
//   static uint32_t timer = 0;
//   int interval = 500;
//   static int count = 0;
//   static int maxVal[9];
//   static int minVal[9];
//  
//   testPeak( &maxVal[0], &minVal[0], IMU.readRawAccelX());
//   testPeak( &maxVal[1], &minVal[1], IMU.readRawGyroX());
//  
//   if(millis()-timer>interval){
//    timer = millis();
//    count++;
//    
//    if(count>1){
//     count = 0;
//     if( ACCEL_ENABLE){
//      Serial.println(maxVal[1]);
//      Serial.println(minVal[1]);
//      //Serial.println(IMU.readRawAccelZ());
//      Serial.println();
//     }
//    
//     if( ACCEL_ENABLE){
//     Serial.println(IMU.readRawGyroX());
//     Serial.println(IMU.readRawGyroY());
//     Serial.println(IMU.readRawGyroZ());
//     Serial.println();
//     }
//     if( ACCEL_ENABLE ){
//     Serial.println(IMU.readTempC());
//     Serial.println();
//     }
//    }
//   }
}
 
int testPeak(int *peak, int *trough, int val){
 if(val>*peak) *peak = val;
 if(val<*trough) *trough = val;
}
