// array of ESPpins
 //you can just use the first 6 for our analog inputs for now
 //and 14 for both analog and digital inputs
const byte espPin[] = 
  {32,36,39,35,33,34, //analog inputs 0-5
  13,14,25,26,27,15,0,4, //digital inputs 6-13
  19,23,18,2,12, //SPI
  21,22, //I2C
  16,17, //UART 2
  5 //MIDI
  };
  
  void setup() {
  Serial.begin(115200);

  //set first 6 pins to be inputs
  //this is the analog pins on the PCB
  for(int i=0;i< 6; i++) pinMode(espPin[i], INPUT);

  //set pins 6-13 to be inputs
  //these are the digital pins on the PCB
  //they are pulled up on the PCB so the buttons can just be connected
  //to ground
  for(int i=6;i< 23; i++) pinMode(espPin[i], INPUT_PULLUP);
  
  Serial.println("setup complete");

}


void loop() {
  //this is a placeholder for just those pins we are actually using
  byte myPins[] = {0,1,6,7,8,9,10,11,12,13};
  
  for( int i=0;i<6;i++){
  Serial.print( analogRead( espPin[i]) );
   Serial.print("\t");
  }
  Serial.println();
  for( int i=6;i<23;i++){
  Serial.print( digitalRead( espPin[i]) );
   Serial.print("\t");
  }
  Serial.println();
  Serial.println();
  
  delay(500);
  
}
