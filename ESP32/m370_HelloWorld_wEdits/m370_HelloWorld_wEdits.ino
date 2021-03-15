/* m370_HelloWorld_wEdits.ino
 *  Ian Hattwick
 *  Created Mar 7 2021
 *  
 *   Includes modifications to the code from the video:
 *   - onepole lowpass on potentiometers
 *   - only print new vals for pots
 *   - counter on button presses
 *  
 *  This sketch monitors inputs 0-5 on the breakout board
 *  and Serial.prints them to the serial monitor. This patch will
 *  not send data to Python or PD.
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
 *  - Tools->upload speed: set to 460800 or lower
 *  - Serial monitor set to 115200 kbps
 */

 #include <pinDefsv4.h>

//array store previously read values
float prevVal[6];
   
 void setup() {
  Serial.begin(115200);

  //input 0 and 1 are analog for potentiometers
  // analog inputs do not support pullup resistors
  for(int i=0;i<2;i++){
    pinMode(espPin[i], INPUT);
  }

  //inputs 6-9 are for buttons
  //they will have built-in pullup resistors enabled
  //buttons should be connected between the input
  //pin and ground.
  for(int i=6;i<10;i++){
    pinMode(espPin[i], INPUT_PULLUP);
  }

  Serial.println("Hello Arduino!");
  Serial.println("Setup completed");

} //setup

void loop() {

  readPotentiometers();
  readButtons();

}//loop

void readPotentiometers(){
  //we use the variables timer and interval to read the inputs
  //at a fixed interval. This syntax will be extremely common.
  static uint32_t timer = 0; //note the static keyword so timer remembers its value
  int interval = 10; //interval is in milliseconds (ms)

  static float prevVal[2]; //for onepole filter

  if(millis()-timer>interval){
    timer = millis();

    //the first two inputs are for potentiometers
    //we will Serial.print the values every time the function is called
    for(int i=0;i<2;i++){
      //read the analog input
      float val = analogRead(espPin[i]);
      float prev = prevVal[i];

      for(int k=0;k<10;k++){
        val = analogRead(espPin[i]);
        
        //output = x*prev + (1-x)*input
        float factor = 0.95;
        val = factor*prevVal[i] + (1-factor)*val;
        prevVal[i] = val;
      }
      
      if(abs(val-prev)>2){
        //Serial.print to arduino serial monitor
        Serial.print("\tpot ");
        Serial.print(i);
        Serial.print(": ");
        Serial.println(val);
      }
    }
    //Serial.println();
  }
}

void readButtons(){
  //we use the variables timer and interval to read the inputs
  //at a fixed interval. This syntax will be extremely common.
  static uint32_t timer = 0; //note the static keyword so timer remembers its value
  int interval = 4; //interval is in milliseconds (ms)
  
  if(millis()-timer >= interval){
    timer=millis();
    static int count = 0;
    
    //inputs 6-9 are for buttons
    //we will only Serial.print if the value being read changes
    for(int i=6;i<10;i++){

      //read the digital input
      float val = digitalRead(espPin[i]);

      if( val != prevVal[i]){
        //only Serial.print if value changes
        prevVal[i] = val;
        if(val == 0){
          count++;
          Serial.print("button ");
          Serial.print(i);
          Serial.print(": ");
          Serial.print(val);
          Serial.print(": ");
          Serial.println(count);
        }
      }
    }
  }
}
