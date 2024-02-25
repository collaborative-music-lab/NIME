/* m370_scanInputs.ino
 *  Ian Hattwick
 *  Created Mar 1 2023
 *  
 *  This sketch monitors all analog and digital inputs, and prints changes to them to the Serial
 *  monitor. 
 *  This patch will not send data to Python or PD.
 *  
 *  Before being able to compile for the ESP32 do the following
 *  - paste the following link into Arduino->preferences->Additional board managers URLS:
 *    https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
 *    - then go to tools->boards->board manager
 *    - enter esp32 in the search box
 *     - select the esp32 definitions by espressif and install
 *     - then you should see the options below
 *  
 *  You should always use the following settings:
 *  - Tools->Board: TTGO T1
 *  - Tools->Port: select the serial port for your ESP32
 *  - Tools->upload speed: set to 460800 or lower (higher may or may not work)
 *  - Serial monitor set to 115200 kbps
 */

 #include "pinDefs.h"

//set the number of pins to monitor
//6 analog pins are available on pins 0-5
//8 digital pins are available on pins 6-13
const byte NUMBER_ANALOG_PINS = 6;
const byte NUMBER_DIGITAL_PINS = 8;

int buttonState[8]; //remember the state of our buttons

void setup() {
  Serial.begin(115200);

  //input 0 to 6 are analog
  // analog inputs do not support pullup resistors
  for(int i=0;i<NUMBER_ANALOG_PINS;i++){
    pinMode(espPin[i], INPUT);
  }

  //inputs 6-13 are for buttons
  //they will have built-in pullup resistors enabled
  //buttons should be connected between the input
  //pin and ground.
  for(int i=6;i<(6 + NUMBER_DIGITAL_PINS) ;i++){
    pinMode(espPin[i], INPUT_PULLUP);
  }

  for(byte i=0;i<14;i++) Serial.print( String(espPin[i]) + "\t");
  Serial.println(); 
  Serial.println("Hello Arduino!");
  Serial.println("Setup completed");

  //uncomment below to continuously stream the raw data
  //monitorRawAnalogInput();
  //monitorRawDigitalInput();
} //setup

void loop() {

  //these two functions read the pots and buttons individually
  readPotentiometers();
  readButtons();

  //you can also uncomment these to see just the raw input data
  // monitorRawAnalogInput();
  //monitorRawDigitalInput();
}//loop

void readPotentiometers(){
  //we use the variables timer and interval to read the inputs
  //at a fixed interval. This syntax will be extremely common.
  static uint32_t timer = 0; //note the static keyword so timer remembers its value
  int interval = 50; //interval is in milliseconds (ms)

  if(millis()-timer>interval){
    timer = millis();
    byte button_is_pushed = 0;

    //only print analog pins if no button is pushed
    for(int i=0;i<NUMBER_DIGITAL_PINS;i++){
      if( buttonState[i] == 0 ) button_is_pushed = 1;
    }

    //the first six inputs are for potentiometers
    //we will Serial.print the values every time the function is called
    if( button_is_pushed != 1) {
      Serial.print("analog in: ");
      for(int i=0; i<NUMBER_ANALOG_PINS;i++){
        //read the analog input
        float val = analogRead(espPin[i]);

        //Serial.print to arduino serial monitor
        Serial.print(val);
        Serial.print("\t");    
      }
      Serial.println();
    }
  }
}

void readButtons(){
  static byte prevVal[NUMBER_DIGITAL_PINS];
  static byte count;
 
  //inputs 6-9 are for buttons
  //we will only Serial.print if the value being read changes
  for(int i=0;i <  NUMBER_DIGITAL_PINS;i++){

    //read the digital input
    int val = digitalRead( espPin[ i+6 ] ); //digital pins begin on espPin[6]
    buttonState[i] = val;

    if( val != prevVal[i]){
      //only Serial.print if value changes
      prevVal[i] = val;
      if(val == 0){
        count++;
        Serial.print("button\t");
        Serial.print(i);
        Serial.print(": ");
        Serial.print(val);
        Serial.print(": ");
        Serial.println(count);
      }
    }
  }
}

void monitorRawAnalogInput(){
  while(1){
    static uint32_t timer = 0;
    if(millis()-timer > 100){
      for(byte i=0;i<NUMBER_ANALOG_PINS;i++) Serial.print( String(analogRead(espPin[i])) + "\t");
      Serial.println();
    }
  }
}

void monitorRawDigitalInput(){
  while(1){
    static uint32_t timer = 0;
    if(millis()-timer > 100){
      for(byte i=0;i<NUMBER_DIGITAL_PINS;i++) Serial.print( String(digitalRead(espPin[i+6])) + "\t");
      Serial.println();
    }
  }
}