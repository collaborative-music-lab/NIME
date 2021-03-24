
LSM6 imu;

void imuSetup(){
  Wire.begin(21,22);

  if (!imu.init())
  {
    Serial.println("Failed to detect and initialize IMU!");
    //while (1);
  }
  imu.enableDefault();
  imu.setTimeout(100);
   Serial.println("imu setup");
}

void imuLoop(){
  static uint32_t timer = 0;
  int interval = 50;

  if(millis()-timer>interval){
    timer=millis();
    
    imu.read();

    if(SERIAL_DEBUG){
      Serial.print("imu ");
      Serial.print(imu.a.x);
      Serial.print(" ");
      Serial.print(imu.a.y);
      Serial.print(" ");
      Serial.print(imu.a.z);
      Serial.print(" ");
  
      Serial.print(imu.g.x);
      Serial.print(" ");
      Serial.print(imu.g.y);
      Serial.print(" ");
      Serial.print(imu.g.z);
      Serial.println(" ");
    }
    else{
      comms.outu8(71);
      comms.out16(imu.a.x);
      comms.out16(imu.a.y);
      comms.out16(imu.a.z);
      comms.send();
//        Serial.println("uimu");
//
      comms.outu8(72);
      comms.out16(imu.g.x);
      comms.out16(imu.g.y);
      comms.out16(imu.g.z);
      comms.send();
    }
  }
}
