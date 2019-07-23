#include "Adafruit_NeoTrellis.h"

// OUTPUT message id's
#define ROW_0_STATES_ID 0
#define ROW_1_STATES_ID 1
#define ROW_2_STATES_ID 2
#define ROW_3_STATES_ID 3
#define BUTTON_DOWN_ID 4
#define BUTTON_UP_ID 5

// INPUT message id's
#define UPDATE_LED_ID 0

#define COLOR_ARRAY_LENGTH 16

Adafruit_NeoTrellis trellis;
const byte endByte = 255;
const byte escByte = 254;

byte serialBuffer[64];
const int bufferLength = 64;
int bufferIndex = 0;

byte deslipped[64];
int deslippedIndex = 0;

unsigned short buttonStates = 0;

byte rArray[COLOR_ARRAY_LENGTH];
byte gArray[COLOR_ARRAY_LENGTH];
byte bArray[COLOR_ARRAY_LENGTH];


TrellisCallback blink(keyEvent evt){
  if (evt.bit.EDGE == SEESAW_KEYPAD_EDGE_RISING) {
    buttonStates ^= 1UL << (evt.bit.NUM); // bitwise XOR toggles bit of pressed button

    // sends individual row states
    for (int row = ROW_0_STATES_ID; row <= ROW_3_STATES_ID; row++){
      byte shifted = buttonStates >> (4*row); // shifts relevent buttons to last 4 bits
      byte rowStates = shifted & 0b00001111; // zeroes out everything above bit 3
      slipOutByte(row); // add the row ID (so we know what buttons we're referring to)
      slipOutByte(rowStates); // add the button states themselves
      Serial.write(serialBuffer, bufferIndex); // write the buffer to the serial port
      Serial.write(endByte); // define the end of the message
      bufferIndex = 0; // reset the bufferIndex to start a few buffer
    }



    // Send individual button down event over serial
    slipOutByte(BUTTON_DOWN_ID); // ID the message ("button down")
    slipOutByte(evt.bit.NUM); // the button that was pressed
    Serial.write(serialBuffer, bufferIndex);
    Serial.write(endByte);
    bufferIndex = 0;

    // NOTE: PUREDATA WILL HANDLE HOW TO CHANGE THE LED's BASED ON BUTTON PRESSES
  }
  else if (evt.bit.EDGE == SEESAW_KEYPAD_EDGE_FALLING) {
    // Send individual button up event over serial
    slipOutByte(BUTTON_UP_ID);
    slipOutByte(evt.bit.NUM);
    Serial.write(serialBuffer, bufferIndex);
    Serial.write(endByte);
    bufferIndex = 0;
  }
  return 0;
}

// adds a byte (or escape byte and byte) to the buffer of bytes to be sent
void slipOutByte(byte val) {
  if ((val == endByte) or (val == escByte)){
    serialBuffer[bufferIndex] = escByte;
    bufferIndex++;
  }
  serialBuffer[bufferIndex] = val;
  bufferIndex++;
}

void deSlip() {
  byte curByte;
  bool escFlag = false;
  if (!Serial.available()) {
    return; // if there's nothing in the buffer when the function is called, move on (stop blocking output)
  }

  // otherwise read until end of next LED message
  while (1) {
    if (Serial.available()){
      curByte = Serial.read();
      if (escFlag) {
        deslipped[deslippedIndex] = curByte;
        deslippedIndex++;
        escFlag = false;
      }
      else if (curByte == endByte) { // if we've reached a true end of message (single pixel)
        processMessage();
        deslippedIndex = 0;
        return; // exit function now that the incoming message has been processed (stop blocking output)
      }
      else if (curByte == escByte) {
        escFlag = true;
      }
      else {
        deslipped[deslippedIndex] = curByte;
        deslippedIndex++;
      }
    }
  }
}

void processMessage() {
  switch (deslipped[0]) {
    case UPDATE_LED_ID:
      byte pixel = deslipped[1];
      byte rVal = deslipped[2];
      byte gVal = deslipped[3];
      byte bVal = deslipped[4];
      updateLedArray(pixel, rVal, gVal, bVal);
      setLeds(); // send color information to trellis uC
      break;
  }
}

void updateLedArray(byte i, byte r, byte g, byte b) {
  rArray[i] = r;
  gArray[i] = g;
  bArray[i] = b;
}

void setLeds() {
  for (int i = 0; i < COLOR_ARRAY_LENGTH; i++) {
    uint32_t color = trellis.pixels.Color(rArray[i], gArray[i], bArray[i]);
    trellis.pixels.setPixelColor(i, color);
  }
}

void setup() {
  Serial.begin(57600);
  pinMode(13, OUTPUT);

  if(!trellis.begin()){
    Serial.println("could not start trellis");
    while(1);
  }
  else{
    Serial.println("trellis started");
  }

  //activate all keys and set callbacks
  for(int i=0; i<NEO_TRELLIS_NUM_KEYS; i++){
    trellis.activateKey(i, SEESAW_KEYPAD_EDGE_RISING);
    trellis.activateKey(i, SEESAW_KEYPAD_EDGE_FALLING);
    trellis.registerCallback(i, blink);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  trellis.read(); // Polls state of buttons and triggers necessary callbacks
  deSlip();
  trellis.pixels.show(); // show all pixels
  delay(20); //the trellis has a resolution of around 60hz

}
