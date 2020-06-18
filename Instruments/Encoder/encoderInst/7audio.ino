volatile byte dacFlag;
int totalInterruptCounter;
 
hw_timer_t * timer = NULL;
portMUX_TYPE timerMux = portMUX_INITIALIZER_UNLOCKED;

//audio interrupt function
void IRAM_ATTR audioInterrupt() {
  portENTER_CRITICAL_ISR(&timerMux);
  dacFlag=1;
  portEXIT_CRITICAL_ISR(&timerMux);
 
}

void AudioSetup(){
  //for  2  DAC  channels max SR seems to be ~980Hz
  //pre=80, scalar=1200
  //for SR of 833 base freq of 80MHz, prescalar of 80 = 1MHz
  timer = timerBegin(0, 80, true);//timer(0-3), prescalar, (up==true, down==false)
  timerAttachInterrupt(timer, &audioInterrupt, true);
  timerAlarmWrite(timer, 1200, true);//timerName, scalar
  timerAlarmEnable(timer);
  Serial.println();
  Serial.println("___________________________________________________");
  for(int i=0;i<256;i++){
    i < 128 ? ddsWT[i] = i*32  : ddsWT[i]  = (4095- (i-128)*32);
    Serial.print(ddsWT[i]);
    Serial.print("  ");
    i % 16 ==  0 ?  Serial.println() : 0;
  }
  Serial.println();
  Serial.println("___________________________________________________");
}

void AudioLoop(){
  if(dacFlag){
    dacFlag = 0;
    for(byte  i=0;i<NUM_DACS;i++){
      dacOut(i,dds[i].buf[dds[i].read]);
      dds[i].read++;
      dds[i].read &= (dds[i].bufSize-1);
//      debug("read ", dds[i].read);
    }
    totalInterruptCounter++;
  }

  static long timer=0;

  if(millis()-timer>1000){
    timer=millis();
    Serial.print("________________________________iyerrrupts: ");
    Serial.println(totalInterruptCounter);
    totalInterruptCounter=0;
    for(byte  i=0;i<NUM_DACS;i++){
      //dds[i].inc = 81;
     // if(dds[i].inc>64)dds[i].inc=1;
    }
  }

  for(byte  i=0;i<NUM_DACS;i++){
    while((dds[i].read + dds[i].bufSize - dds[i].write) % dds[i].bufSize > 1){

      uint16_t temp;
      int diff;
      uint16_t prog;
      switch(1){
        case 0: //linear interpolation
         temp = ddsWT[dds[i].sample>>8];        //base WT value
        
         diff = ddsWT[((dds[i].sample>>8)+1)&255] - temp; ////diff  between  current WT value and next WT value
         prog = dds[i].sample & 255;        //fraction
    
        temp = temp + ((diff*prog)>>8); //base + fraction
    
        //write to buffer
        dds[i].buf[dds[i].write] = temp;
        dds[i].write++;
        dds[i].write &= (dds[i].bufSize-1);
        
        dds[i].sample += dds[i].inc;  //increment sample
        break; //case 0

        case 1://lerp sensor data
        dds[i].cur = unsignedInterpolate(dds[i].sensor,dds[i].cur,dds[i].smooth);
//        debug("enc", i);
//        debug("sensor", dds[i].sensor);
//        debug("cur", dds[i].cur);
//        debug("smooth", dds[i].smooth);
        //write to buffer
        dds[i].buf[dds[i].write] = dds[i].cur;
        //Serial.println();
        dds[i].write >= 7 ? dds[i].write=0: dds[i].write++;
//        debug("write ", dds[i].write);
        break;
      }

    }
  }
 
}//audio loop
