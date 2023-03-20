#include "m370_cap.h"
#include "m370_MPR121.h"
#include "m370_listProcessing.h"

 m370_MPR121 mpr121(21,22); //SDA,SCL

///******************************
//OBJECT DEFINITIONS 
//pin: ESPpin number, int, e.g. Sensor[0].pin = 0
//name: string with the intended OSC name of the sensor, e.g. Sensor[0].name = "/joystick/x"
//frequency:  rate at  which readings of the sensor are taken
//******************************/
//

/******************CONSTRUCTORS*****************/
m370_cap::m370_cap()
{}

m370_cap::m370_cap(byte num) : 
numCapSensors  (num)
{}

m370_cap::m370_cap(byte num, int _frequency) : 
numCapSensors  (num)
{SetFrequency(_frequency);}

m370_cap::m370_cap(byte num, int _frequency, String _name) : 
numCapSensors  (num),
name(_name)
{SetFrequency(_frequency);}

m370_cap::m370_cap(byte num, int _frequency, String _name, byte _size) : 
numCapSensors  (num),
name(_name),
bufferSize(_size)
{SetFrequency(_frequency);}

/******************MAIN*****************/
void m370_cap::begin(){
  enable=1;
  mpr121.begin();

  mpr121.chargeCurrent(63); //0-63, def 16
  mpr121.chargeTime(1); //1-7, def 1
  mpr121.setThresholds(200, 100);
  mpr121.proxChargeCurrent(63); //0-63, def 16
  mpr121.proxChargeTime(3); //1-7, def 1
  
  for(byte i=0;i<numCapSensors;i++){
    filteredBuffer[i] = new int32_t[bufferSize];
    baselineBuffer[i] = new int32_t[bufferSize];
  }
}

byte m370_cap::loop(){

  if (enable==1) {
    //get continuous proximity data
    if(micros() - timer > interval){
      timer = micros();

       filteredBuffer[cur][index[cur]] = mpr121.filteredData(cur);
       baselineBuffer[cur][index[cur]] = mpr121.baselineData(cur);
       ++index[cur] < bufferSize ? index[cur] : index[cur]=0;
       isAvailable[cur]=1;

       cur++;
       cur<numCapSensors ? cur: cur=0;
    }//proximity

    //get touch status
    if(micros() - touchTimer > touchInterval){
      touchTimer = micros();
      
       uint32_t touchVal = mpr121.touched();
       if(touchVal != prevTouchVal){
        for(byte i=0;i<numCapSensors;i++){
          if((touchVal>>i & 1) != (prevTouchVal>>i & 1)) {
            isTouchAvailable[i]=1;
            isTouched[i]=touchVal>>i & 1;
            //update prox for this sensor
            // filteredBuffer[i][index[i]] = mpr121.filteredData(i);
            // baselineBuffer[i][index[i]] = mpr121.baselineData(i);
          }
        }
         prevTouchVal=touchVal;
       }
    }//touch
  }//enable
  return isAvailable[0];
}//loop


/******************FUNCTIONS*****************/

int16_t m370_cap::getVal(byte _num){  
  isAvailable[_num] = 0;
  if(index[_num]>0){
    curFiltered[_num] = LPMean(filteredBuffer[_num],index[_num]);
    curBaseline[_num] = LPMean(baselineBuffer[_num],index[_num]);
    index[_num] = 0;
  }
  return capData(_num);
}

int16_t m370_cap::getVal(byte _num, listProcessType _mode){  
  isAvailable[_num] = 0;
  //isTouchAvailable[_num] = 0;
  if(index[_num]>0){
    curFiltered[_num] = applyListProcess(_mode,filteredBuffer[_num],index[_num]);
    curBaseline[_num] = LPMean(baselineBuffer[_num],index[_num]);
    index[_num] = 0;
  }
  return capData(_num);
}

int16_t m370_cap::getRaw(byte _num){  
  isAvailable[_num] = 0;
  if(index[_num]>0){
    curFiltered[_num] = LPPeak(filteredBuffer[_num],index[_num]);
    curBaseline[_num] = LPTrough(baselineBuffer[_num],index[_num]);
    index[_num] = 0;
  }
  return curFiltered[_num];
}



int16_t m370_cap::getProximity(){  

  return mpr121.proximityData();
}

int16_t m370_cap::capData(byte _num){
  int16_t outVal  = -(curFiltered[_num]  - curBaseline[_num]);
  //outVal > 10 ? outVal -= 10 : outVal=0;
  //outVal  = curFiltered[_num] ;
  outVal<<= 1;
  outVal +=  isTouched[_num];
  return outVal;
}

byte m370_cap::available(byte _num){ return isAvailable[_num]; }

byte m370_cap::touchAvailable(byte _num){ return isTouchAvailable[_num]; }

void m370_cap::SetFrequency(uint16_t _frequency){
  if(_frequency==0) _frequency=20000;
  interval = 1000000/_frequency;
  touchInterval = interval/8;
  interval /= numCapSensors;
}

void m370_cap::SetChargeCurrent(byte _current){
  if (_current>63) _current=63;
  mpr121.chargeCurrent(_current); //0-63, def 16

}

void m370_cap::SetChargeTime(byte _chargeTime){
  if(_chargeTime > 7) _chargeTime = 7;
  else if (_chargeTime < 1) _chargeTime = 1;
    mpr121.chargeTime(_chargeTime); //1-7, def 1
}
