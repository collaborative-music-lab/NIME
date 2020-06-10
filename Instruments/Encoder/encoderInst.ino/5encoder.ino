void EncoderLoop(){
  static uint32_t timer = 0;
  int interval = 10;

  if(millis()-timer>interval){
    timer=millis();

    for(byte i=0;i<NUM_ENCODERS;i++){
      int val = enc[i].delta();
      if(val!=0){
        Serial.print(i);
        debug(" enc: ", val);
      }
    }
  }
}

void EncoderSetup(){
 // for(byte i=0;i<NUM_ENCODERS;i++) 
  enc[0].begin([]{enc[0].readEncoder_ISR();});
  enc[1].begin([]{enc[1].readEncoder_ISR();});
}

