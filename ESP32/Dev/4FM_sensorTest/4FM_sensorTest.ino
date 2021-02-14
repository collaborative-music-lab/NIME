struct defSensor{
  byte photo[4] = {32,36,39,35};
  byte button[4] = {13,14,25,26};
};

defSensor sensor;

byte mux[] = {12,18,23};
byte latch = 2;
byte muxin = 33;


void setup() {
  Serial.begin(115200);

  for(int i=0;i<4;i++) pinMode(sensor.button[i], INPUT_PULLUP);
  for(int i=0;i<3;i++) pinMode(mux[i], OUTPUT);
  pinMode(muxin,INPUT);
 
  Serial.println("setup");
}

void loop() {
  readAnalog();
  readMux();
  readDigital();
  Serial.println();
  delay(250);
}

void sMon(String cname, int val, byte newline){
  Serial.print(cname);
  Serial.print(" :");
  Serial.print(val);
  if (newline==1) Serial.println();
  else Serial.print("\t");
}

void readAnalog(){
  static uint32_t timer = 0;
  int interval = 200;

  if(millis()-timer>interval){
    timer = millis();
    
    sMon("photo", analogRead(sensor.photo[0]) ,0);
    sMon("", analogRead(sensor.photo[1]) ,0);
    sMon("", analogRead(sensor.photo[2]) ,0);
    sMon("", analogRead(sensor.photo[3]) ,1); 

//    sMon("toggle", analogRead(sensor.toggle[0]),0);
//    sMon("", analogRead(sensor.toggle[1]) ,1);
//    pinMode(sensor.toggle[0], INPUT_PULLUP);
//    pinMode(sensor.toggle[1], INPUT_PULLUP);
  }
}

void readDigital(){
  static uint32_t timer = 0;
  int interval = 200;

  if(millis()-timer>interval){
    timer = millis();
    
    sMon("button", digitalRead(sensor.button[0]) ,0);
    sMon("", digitalRead(sensor.button[1]) ,0);
    sMon("", digitalRead(sensor.button[2]) ,0);
    sMon("", digitalRead(sensor.button[3]) ,1);
  }
}

void readMux(){
  static uint32_t timer = 0;
  int interval = 50;
  static byte address = 0;
  static int vals[8];

  if(millis()-timer>interval){
    timer = millis();
    vals[address] = analogRead(muxin);
      
    for( int k=0;k<3;k++) {
      byte val = (address >> k) & 1;
      //sMon("", mux[k], 0);
      //sMon("", val, 0);
      digitalWrite(mux[k], val);
    }
    
    if(address<3) address++;
    else{ 
      address = 0;
      Serial.print("mux ");

      for(int i=0;i<4;i++) {
        Serial.print(vals[i]);
        Serial.print("\t");
      }
      Serial.println();

    }
  }
}
//
//int optoVals[4];
//
//void readOpto(){
//  for(int i=0;i<4;i++) optoVals
//}
