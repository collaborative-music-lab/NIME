

 // array of ESPpins
 //you can just use the first 6 for our analog inputs for now
 //and 14 for both analog and digital inputs
const byte espPin[] = {32,36,39,35,33,34, //analog inputs
  13,14,25,26,27,15,0,4, //digital inputs
  19,23,18,2,12, //SPI
  21,22, //I2C
  16,17, //UART 2
  5 //MIDI
  };
  
  void setup() {
  Serial.begin(115200);

  for(int i=0;i<  14;i++) pinMode(espPin[i], INPUT);
  
  Serial.println("setup complete");

}


void loop() {
  byte myPins[] = {0,1,6,7,8,9,10,11,12,13};
  for( int i=0;i<6;i++){
  Serial.print( analogRead( espPin[i]) );
   Serial.print("\t");
  }
  Serial.println();
  delay(500);
}
