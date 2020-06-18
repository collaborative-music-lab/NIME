int  gateLength = 5;
int clockInterval = 10;

void ClockLoop(){
  static uint32_t timer = 0;
  static byte  count =  0;
  
  static byte clockState = 0;
  static long onset =  0;
//  if(millis()-timer>clockInterval &&  digitalRead(p0)==1){
//    //pinMode(MIDI,OUTPUT);
//    timer=millis();
//    onset=millis();
//    clockState =  1;
//    digitalWrite(MIDI,1);
//
//    //gen MIDI notes
//    byte notes[]={0,3,5,7,10,12,15,17};
//    //dds[0].sensor = m2v[notes[count++]];
//    count &=7;
//  }
  if(clockState == 1){
    if(millis()>onset+gateLength){
      digitalWrite(MIDI,0);
      clockState  = 0;
    }
  }
}

void EncoderLoop(){
  static uint32_t timer = 0;
  int interval = 10;
  static  long encoder_counter[NUM_ENCODERS];

  if(millis()-timer>interval){
    timer=millis();
    
    
    for(byte i=0;i<NUM_ENCODERS;i++){
      int  val  =  enc[i].delta();
      if(val!=0){
       encoder_counter[i]+=val;
       Serial.print("enc ");
       Serial.print(i);
       Serial.print(" val: ");
       Serial.println(encoder_counter[i]);
      }
    }//for i
  }//millis
}//encoder Loop


int checkData(int newVal, int oldVal, int mode){

  switch(mode){
    case -1: //encoder or button
    return newVal!=0;
    break;

    default:
    if(abs(newVal-oldVal)>mode) return 1;
    else return 0;
  }
}//checkData

void EncoderSetup(){
  //for(byte i=0;i<NUM_ENCODERS;i++) {
  enc[0].begin([]{enc[0].readEncoder_ISR();});
  enc[1].begin([]{enc[1].readEncoder_ISR();});
  enc[2].begin([]{enc[2].readEncoder_ISR();});
 // }
  Serial.println("v/octave");
 for(byte i=0;i<64;i++){
  m2v[i]  = int((float)i*(3.3/39.6)*4095);
  Serial.println(m2v[i]);
 }
 Serial.println("___");
}


int leak(int oldData, int newData, float attack, float decay, float min, float max, float expo, int scale){
  float output = (float)oldData*decay;
  output += pow((float)abs(newData)*scale,expo)*(1-attack);
  output > 4095 ? output = 4095 : 0;
  output *= (max-min);
  output += min*4095;
  return (int) output;
}
