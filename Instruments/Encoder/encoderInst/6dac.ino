void DacLoop(){
  static uint32_t timer = 0;
  int interval = 10;

  if(millis()-timer>interval){
    timer=millis();

    static int dacval = 0;
    dacval += 10;
    if(dacval > 4095) dacval = 0;
    //debug("dac value: ", dacval);

    for(byte i=0;i<NUM_DACS;i++){
      
      switch(i){
        case 0:
        dac.setChannelValue(MCP4728_CHANNEL_A, dacval);
        break;

        case 1:
        dac.setChannelValue(MCP4728_CHANNEL_C, dacval);
        break;

        case 2:
        dacWrite(25,dacval/255);
        break;

        case 3:
        dac.setChannelValue(MCP4728_CHANNEL_A, dacval);
        break;
      }
    }
  }
}

void DacSetup(){
     Serial.println("Adafruit MCP4728 test!");

  // Try to initialize!
  while (!dac.begin()) {
    Serial.println("Failed to find MCP4728 chip");
    delay(1000);
  }
  int dacval = 0;

  dac.setChannelValue(MCP4728_CHANNEL_A, dacval);
  dac.setChannelValue(MCP4728_CHANNEL_B, dacval*2);
  dac.setChannelValue(MCP4728_CHANNEL_C, dacval*3);
  dac.setChannelValue(MCP4728_CHANNEL_D, dacval*4);
}

void dacOut(byte num, int val){
  
  switch(num){
        case 0:
        val/=2;
        val>4095 ? val=4095 : val<0 ? val=0 : val;
        dac.setChannelValue(MCP4728_CHANNEL_A, val);
        break;

        case 1:
        val>4095 ? val=4095 : val<0 ? val=0 : val;
        dac.setChannelValue(MCP4728_CHANNEL_C, val);
        break;

        case 2:
        val>4095 ? val=4095 : val<0 ? val=0 : val;
        dacWrite(25,val/255);
        break;

        case 3:
        dac.setChannelValue(MCP4728_CHANNEL_A, val);
        break;
      }
}
