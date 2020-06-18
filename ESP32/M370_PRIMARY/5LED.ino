// https://github.com/FastLED/FastLED/wiki/Basic-usage

#include <FastLED.h>

#define LED_PIN     0
#define NUM_LEDS    64
#define BRIGHTNESS  0
#define LED_TYPE    WS2812
#define COLOR_ORDER GRB
CRGB leds[NUM_LEDS];

#define UPDATES_PER_SECOND 100

CRGBPalette16 currentPalette;
TBlendType    currentBlending;

extern CRGBPalette16 myRedWhiteBluePalette;
extern const TProgmemPalette16 myRedWhiteBluePalette_p PROGMEM;

byte updateLedFlag = 0;

void ledSetup() {
    delay( 3000 ); // power-up safety delay
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
    FastLED.setBrightness(  BRIGHTNESS );
    
    currentPalette = RainbowColors_p;
    currentBlending = LINEARBLEND;
}//ledSetup

void ledLoop(){
  static uint32_t timer = 0;
  int interval = 20;

  ledTest();

  if(millis()-timer>interval){
    timer=millis();
    if(updateLedFlag==1){
      updateLedFlag = 0;
      FastLED.show();
    }
  }
}//ledLoop



void ledTest(){
  static uint32_t timer = 0;
  int interval = 100;
  static int num=0;

  static byte count = 0;
  if(millis()-timer>interval){
    timer=millis();
    // Turn the LED on, then pause
   switch(count){
    case 0: leds[num] = CRGB::Red; break;
    case 1: leds[num] = CRGB::Blue; break;
    case 2: leds[num] = CRGB::Green; break;
    case 3: leds[num] = CRGB::Black; break;
  }
  count++;
  num>=63 ? num=0 : num++;
  
  if(count>3)  count=0;
   FastLED.show();
  }
}//ledTest

void setLed(byte num, byte r, byte g, byte b){
  leds[num].r = r;
  leds[num].g = g;
  leds[num].b = b;

  updateLedFlag = 1;
}
