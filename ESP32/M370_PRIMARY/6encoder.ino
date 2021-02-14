/*
 * for  some reason the input pins are notalways initializedcorrectly
 * 
 * akludge is to continuously reinit the encoders  until the encoder  counter
 * exceeds  a small  value
 */
void EncoderLoop(){
  static uint32_t timer = 0;
  int interval = 10;
  static  long encoder_counter[NUM_ENCODERS];
  static byte reinitEncoder[] =  {1,1,1};

  if(millis()-timer>interval){
    timer=millis();

    for(byte i=0;i<NUM_ENCODERS;i++){
      int  val  =  enc[i].delta();
      if(val!=0){
       encoder_counter[i]+=val;
//       Serial.print("enc ");
//       Serial.print(i);
//       Serial.print(" val: ");
//       Serial.println(encoder_counter[i]);
        SlipOutByte(i+89); //pin, numerical indicator
        SlipOutInt(encoder_counter[i]+4096);
        SendOutSlip();

        for(byte k=0;k<8;k++){
          byte ledVal = abs(encoder_counter[i])&31;
          setLed((7-i)+k*8,0,0,(ledVal>(k*4))*100);
//            Serial.print((7-i)+k*8);
//            Serial.print(" ");
//            Serial.print(abs(encoder_counter[i])&31);    
//            Serial.print(" ");
//            Serial.println();
        }
        if( abs(encoder_counter[i])>NUM_ENCODERS ) reinitEncoder[i]=0;
//        if(reinitEncoder[i]) {
//          delay(500);
//          if( i== 0 )  enc[0].begin([]{enc[0].readEncoder_ISR();});
//          if( i== 1 )  enc[1].begin([]{enc[1].readEncoder_ISR();});
//          if( i== 2 )  enc[2].begin([]{enc[2].readEncoder_ISR();});
//          delay(500);
//        }
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
  for(byte i=0;i<NUM_ENCODERS;i++) setLed(32+i,0,0,100);
  enc[0].begin([]{enc[0].readEncoder_ISR();});
  enc[1].begin([]{enc[1].readEncoder_ISR();});
  enc[2].begin([]{enc[2].readEncoder_ISR();});
 // }
//  Serial.println("v/octave");
// for(byte i=0;i<64;i++){
//  m2v[i]  = int((float)i*(3.3/39.6)*4095);
//  Serial.println(m2v[i]);
// }
// Serial.println("___");
}


int leak(int oldData, int newData, float attack, float decay, float min, float max, float expo, int scale){
  float output = (float)oldData*decay;
  output += pow((float)abs(newData)*scale,expo)*(1-attack);
  output > 4095 ? output = 4095 : 0;
  output *= (max-min);
  output += min*4095;
  return (int) output;
}