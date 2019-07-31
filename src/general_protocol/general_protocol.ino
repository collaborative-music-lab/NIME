#include "Adafruit_NeoTrellis.h"
Adafruit_NeoTrellis trellis;

//Header ID's for messages sent to Python
const byte BUTTON_CH_0 = 0;
const byte BUTTON_CH_1 = 1;
const byte BUTTON_CH_2 = 2;
const byte BUTTON_CH_3 = 3;

const byte FADER_CH_0 = 4;
const byte FADER_CH_1 = 5;
const byte FADER_CH_2 = 6;
const byte FADER_CH_3 = 7;
const byte FADER_CH_4 = 8;
const byte FADER_CH_5 = 9;
const byte FADER_CH_6 = 10;

const byte IMU_CH_0 = 11;
const byte IMU_CH_1 = 12;
const byte IMU_CH_2 = 13;
const byte IMU_CH_3 = 14;
const byte IMU_CH_4 = 15;

// initialize global serial buffer
byte serialBuffer[64];
const int bufferLength = 64;
int bufferIndex = 0;

// define end bytes and escape bytes needed for slip encoding
const byte endByte = 255;
const byte escByte = 254;

TrellisCallback blink (keyEvent evt) {
  if (evt.bit.EDGE == SEESAW_KEYPAD_EDGE_RISING) {
    sendFaderMessage(0, 0, 0, random(-32768, 32767), 1);
    //sendButtonMessage(0, evt.bit.NUM % 4, evt.bit.NUM / 4, 0, true);
  }
  else if (evt.bit.EDGE == SEESAW_KEYPAD_EDGE_FALLING) {
    //sendButtonMessage(0, evt.bit.NUM % 4, evt.bit.NUM / 4, 0, false);
  }
  return 0;
}

void sendButtonMessage(byte channel, byte x, byte y, byte z, bool state) {
  if (channel < 0) {
    channel = 0;
  }
  else if (channel > 3) {
    channel = 3;
  }
  else {
    slipOutByte(BUTTON_CH_0 + channel);
    slipOutByte(x);
    slipOutByte(y);
    slipOutByte(z);
    slipOutByte(state);
    Serial.write(serialBuffer, bufferIndex);
    Serial.write(endByte);
    bufferIndex = 0;
    // byte order: [id][x][y][z][state]
  }
}

void sendFaderMessage(byte channel, byte x, byte y, long val, bool isSigned) {
  if (isSigned) val += 32768;
  if (channel < 0) {
    channel = 0;
  }
  else if (channel > 6) {
    channel = 6;
  }
  else {
    slipOutByte(FADER_CH_0 + channel);
    slipOutByte(x);
    slipOutByte(y);
    slipOutInt((uint16_t) val);
    slipOutByte(isSigned);
    Serial.write(serialBuffer, bufferIndex);
    Serial.write(endByte);
    bufferIndex = 0;
    // byte order: [id][x][y][highValByte][lowValByte][signed]
  }

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

// writes a two-byte int to the buffer, adding escape bytes if necessary
void slipOutInt(uint16_t val) { //uint16_t
  uint8_t lowValByte = val & 0xff;
  uint8_t highValByte = (val >> 8);
  slipOutByte(highValByte);
  slipOutByte(lowValByte);
}

void setup() {
  Serial.begin(57600);

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
  delay(20); //the trellis has a resolution of around 60hz
}