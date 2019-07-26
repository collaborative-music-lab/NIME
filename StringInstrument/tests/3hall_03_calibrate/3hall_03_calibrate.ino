const byte SERIAL_DEBUG = 1;

const byte NUM_SENSORS = 2;
uint32_t base[NUM_SENSORS];
byte pin[8];

void setup() {
  analogReadResolution(12);
  for(int i=0;i<NUM_SENSORS;i++) pin[i] = 23-1;
  for(int i=0;i<NUM_SENSORS;i++) pinMode(pin[i],INPUT);
  pin[0] = A9;
  pin[1] = A8;
  Serial.begin(115200);
  //setTouchReadSensitivity(9,5,2);
  for(int i=0;i<NUM_SENSORS;i++) base[i] = analogRead(pin[i]);
}


void loop() {
  static long counter = 0;
  static long accum[NUM_SENSORS];
  long readVal[NUM_SENSORS];
  for(int i=0;i<NUM_SENSORS;i++) {
    readVal[i] = analogRead(pin[i]);
    accum[i]+= readVal[i];
  }
  counter++;
  //long touchAccum = touchCount(0);
  
  static long timer = 0;
  int interval = 100;
  
  if(millis() - timer > interval){
    timer = millis();
    uint32_t val[NUM_SENSORS];
    for(int i=0;i<NUM_SENSORS;i++) {
      val[i] = (accum[i]/counter) - base[i];
      base[i] = base[i] * 0.95 + (accum[i]/counter) * 0.05;
      //accum[i] = 0;
    }
    
    //Serial.print(touchCount(0)/100);
    //Serial.print("\t");
    if( SERIAL_DEBUG == 0) Serial.write(255);
    else Serial.println();
    clipWrite(accum[0]/counter);
    clipWrite(accum[1]/counter);
    clipWrite(val[0]-val[1]);
     accum[0] = 0;
     accum[1] = 0;
    counter = 0;
    //touchCount(1);
  }
  //delay(1);
  static long timer2 = 0;
  if(millis()>timer2){
    timer2=millis();
    if( SERIAL_DEBUG == 0) clipWrite(readVal[0]-base[0]);
  }
}

long touchCount(byte zero){
  static long timer = 0;
  static long count = 0;
  int interval = 10;
  if(millis() - timer > interval){
    timer = millis();
    count += touchRead(A8);
  }
  if( zero == 1) count = 0;
  return count;
}

void clipWrite(int val){
  if( SERIAL_DEBUG == 0 ) val = constrain(val+127, 0, 254);
  //else val = constrain(val, 0, 254);
  if( SERIAL_DEBUG == 0) Serial.write(val);
  else {
    Serial.print(val);
    Serial.print("\t");
  }
}
