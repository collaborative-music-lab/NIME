byte touchPin = 4;
long baseline = 0;
int numBaseReadings = 256;
float thresh = 0.9;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  //pinMode(touchPin, INPUT);
  delay(50);
  for(int i=0;i<numBaseReadings;i++) baseline += touchRead(touchPin);
  //baseline = touchRead( touchPin ) * numBaseReadings;
}


void loop() {
//  for(int i=0;i<10;i++){
//  int count = touchRead(i);
//  Serial.print(i);
//  Serial.print(": ");
//  Serial.println(count);
//  delay(25);
//}


  int count = touchRead(touchPin);
  int state = count < baseline / (numBaseReadings + 2);

  switch( state ){
    case 0:
    baseline += count;
    baseline = baseline - (baseline / numBaseReadings);
    break;

    case 1:
    baseline += count / 8;
    baseline = baseline -  (baseline / numBaseReadings) / 8;
    break;
  }
  
  
  //Serial.print("/t ");
  //Serial.print(count);
  //delay(25);
  Serial.print(count);
  Serial.print("\t ");
  Serial.print(baseline / numBaseReadings);
  Serial.print("\t ");
  Serial.println(state);
  delay(100);
}
