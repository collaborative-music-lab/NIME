int  gateLength = 5;
int clockInterval = 10;

void ClockLoop(){
  static uint32_t timer = 0;
  static byte  count =  0;
  
  static byte clockState = 0;
  static long onset =  0;
  if(millis()-timer>clockInterval &&  digitalRead(p0)==1){
    //pinMode(MIDI,OUTPUT);
    timer=millis();
    onset=millis();
    clockState =  1;
    digitalWrite(MIDI,1);

    //gen MIDI notes
    byte notes[]={0,3,5,7,10,12,15,17};
    dds[0].sensor = m2v[notes[count++]];
    count &=7;
  }
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

  if(millis()-timer>interval){
    timer=millis();
    
    
   int inVal[6];
   static int prevVal[6];

   String input[] = {"pot ", "joyX ", "joyY ", "enc0 ", "enc1 ",  "but "};

   //read sensor data
   inVal[0] = 4095-sensors[1].outVal; //pot
   inVal[1] = sensors[3].outVal; //joyX
   inVal[2] = sensors[2].outVal; //joyY
   inVal[3] = enc[0].delta(); //enc0
   inVal[4] = enc[1].delta(); //enc1
   inVal[5] = sensors[0].outVal; //button
   
    //calc leaky iintegrator
    static float attack[] = {0.,0.};
    static  float decay[] = {0.1,0.1};
    static float range[]={0,0,1,1};
    static int encOut[2];

    float expo[] = {0.5,0.3,1,0.8};
    int dacScale = 2000;//applied to delta input, then input is expo[3]
    
//    for(int k=0;k<2;k++){
//      attack[k] = pow(attack[k],0.5);
//      decay[k] = pow(decay[k],0.3);
//      range[k+2] = pow(range[k+2],2)*20;
//    }

    encOut[0] = leak(encOut[0], inVal[3],attack[0],decay[0]*0.1+0.9, range[0], range[2], expo[3], dacScale);
    //dacOut(0,encOut[0]);
//    debug("enc0: ", encOut[0]);
   // dds[0].sensor = encOut[0];

    encOut[1] = leak(encOut[1], inVal[4],attack[1],decay[1]*0.1+0.9, range[1], range[3], expo[3], dacScale);
   // dacOut(1,encOut[1]);
//   debug("inVal: ", inVal[4]);
//   debugF("min: ", range[1]);
//   debugF("max: ", range[3]);
//   debug("enc1: ", encOut[1]);
   dds[1].sensor = encOut[1];

//    debugF("attack", attack[0]);
//   debugF("decay", decay[0]);
//   debug("inVal", inVal[3]);
//   Serial.print(encOut[0]);
//   Serial.print("\n");
//   Serial.println(encOut[1]);
  //  debugF("min", range[0]);
 //  debugF("max", range[2]);
 //  Serial.println("______________");

    int8_t sensorMode[] = {2,2,2,-1,-1,-1};
    for(byte i=0;i<6;i++){
      if(checkData(inVal[i],prevVal[i],sensorMode[i])){
        prevVal[i]=inVal[i];
        //Serial.print(input[i]);
        //debug(input[i], inVal[i]);

        byte k = 0;//for  loop iter

        switch(i){
          case 0: //pot
          for(k=0;k<NUM_DACS;k++) {
            dds[k].inc = inVal[i];
            dds[k].smooth = 200;//inVal[i]>>4;
          }
   
          for(k=0;k<2;k++){
          if(inVal[i]<2048) {
            attack[k]=0;
            decay[k]=pow( (float)inVal[i]/2048, expo[1]);
          }
          else {
            attack[k]=pow( ((float)inVal[i]-2048)/2048, expo[0]);
            decay[k]= pow( 2. - ((float)inVal[i]/2048.), expo[1]);
          }
          }
          break;

          case 1: //joyX
          clockInterval = pow((float)inVal[i]/4096,2)*1000 + 10;
//          if(inVal[i]<2048){
//            range[0]=0;
//            range[2]=pow((float)(inVal[i])/2048,expo[2]);
//          }
//          else{
//            range[0]=pow((float)(inVal[1]-2048)/2048,expo[2]);
//            range[2]=1;
//          }
            break;

            case 2: //joyY
            gateLength = ((uint32_t)clockInterval * (inVal[i]>>4))>>8;
            debug("interval ", clockInterval);
            debug("gatte ", gateLength);
//            if(inVal[i]<2048){
//            range[1]=0;
//            range[3]=pow((float)(inVal[i])/2048,expo[2]);
//          }
//          else{
//            range[1]=pow((float)(inVal[i]-2048)/2048,expo[2]);
//            range[3]=1;
//          }
            break;

            case 3://enc0
//            encOut[0] = leak(encOut[0], -inVal[i],attack[0],decay[0], range[2]);
//            dacOut(0,encOut[0]);
            break;

            case 4://enc0
//            encOut[1] = leak(encOut[1], -inVal[i],attack[1],decay[1], range[3]);
//            dacOut(1,encOut[1]);
            break;

            case 5:
            dacOut(2,4095);
            delay(2);
            dacOut(2,0);
            break;
          }//switch
          
        }//checkData
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
