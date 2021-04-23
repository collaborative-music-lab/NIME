#include "m370_listProcessing.h"

//definitions
int32_t applyListProcess(listProcessType process, int32_t vals[], byte num){
  switch(process){
    case MEAN: return LPMean(vals,num); break;
    case MEDIAN: return LPMedian(vals,num); break;
    case TROUGH: return LPTrough(vals,num); break;
    case PEAK: return LPPeak(vals,num); break;
    case LAST: return LPLast(vals,num); break;
    case PEAK_DEVIATION: return LPPeakDeviation(vals,num); break;
    default : 
    return LPMean(vals,num); break;
  }
}


 
int32_t LPMean(int32_t vals[], byte num){
  uint32_t sum=0;
  for(byte i=0;i<num;i++){
    sum+=vals[i];
  }
  return sum/num;
}//mean

int32_t LPMedian(int32_t vals[], byte num){
  LPSortList(vals, num);
  return vals[num/2+1];
}//median

int32_t LPPeak(int32_t vals[], byte num){
  LPSortList(vals, num);
  return vals[num-1];
}//median

int32_t LPTrough(int32_t vals[], byte num){
  LPSortList(vals, num);
  return vals[0];
}//median

int32_t LPPeakDeviation(int32_t vals[], byte num){
  int32_t base  = LPMean(vals,num);
  int32_t out = 0;
  int32_t deviation = 0;
  for(int i=0;i<num;i++){
    if(abs(base-vals[i]) > deviation) {
      out = vals[i];
      deviation = abs(base-vals[i]);
    }
  }
  return out;
}//peakDeviation

int32_t LPLast(int32_t vals[], byte num){
  return vals[num-1];
}


//SORTING ALGORITHM
//https://forum.arduino.cc/index.php?topic=280486.0
void LPSortList(int32_t *ar, uint8_t n)
{
  int32_t i, j, gap, swapped = 1;
  int32_t temp;

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