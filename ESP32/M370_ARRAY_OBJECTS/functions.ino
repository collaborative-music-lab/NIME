//read analog input multiple times to reduce noise
int oversample(int adcPin, int numSamples) {
  int total = 0;
  for (int i = 0; i < numSamples; i++) {
    total += analogRead(adcPin);
  }
  return total / numSamples;
}

/*************************
 * SENSOR SIGNAL PROCESSING
 * 
 *************************/
 
int Mean(int vals[], byte num){
  uint32_t sum=0;
  for(byte i=0;i<num;i++){
    sum+=vals[i];
  }
  return sum/num;
}//mean

int Median(int vals[], byte num){
  combSort11(vals, num);
  return vals[num/2+1];
}//median

int Peak(int vals[], byte num){
  combSort11(vals, num);
  return vals[num-1];
}//median

int Trough(int vals[], byte num){
  combSort11(vals, num);
  return vals[0];
}//median

int PeakDeviation(int vals[], byte num, int prev){
  int out = 0;
  int deviation = 0;
  for(int i=0;i<num;i++){
    if(abs(prev-vals[i]) > deviation) {
      out = vals[i];
      deviation = abs(prev-vals[i]);
    }
  }
  return out;
}//peakDeviation


//SORTING ALGORITHM
//https://forum.arduino.cc/index.php?topic=280486.0
void combSort11(int *ar, uint8_t n)
{
  int i, j, gap, swapped = 1;
  int temp;

  gap = n;
  while (gap > 1 || swapped == 1)
  {
    gap = gap * 10 / 13;
    if (gap == 9 || gap == 10) gap = 11;
    if (gap < 1) gap = 1;
    swapped = 0;
    for (i = 0, j = gap; j < n; i++, j++)
    {
      if (ar[i] > ar[j])
      {
        temp = ar[i];
        ar[i] = ar[j];
        ar[j] = temp;
        swapped = 1;
      }
    }
  }
}

