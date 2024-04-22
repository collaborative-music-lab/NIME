/*
 * utiliy functions for proccessing arrays of data:
 * - Mean
 * -Median
 * -Peak
 * -Trough
 * -SortList: based on combSort11
 * 
 */


#ifndef M370LIST_PROCESSING_h
#define M370LIST_PROCESSING_h
#include "Arduino.h"

enum listProcessType {MEAN, MEDIAN, PEAK, TROUGH, LAST, PEAK_DEVIATION};

/*************************
 * SENSOR SIGNAL PROCESSING
 * 
 *************************/

//declarations
int32_t applyListProcess(listProcessType process, int32_t vals[], byte num);
int32_t LPMean(int32_t vals[], byte num);
int32_t LPMedian(int32_t vals[], byte num);
int32_t LPPeak(int32_t vals[], byte num);
int32_t LPTrough(int32_t vals[], byte num);

int32_t LPLast(int32_t vals[], byte num);
int32_t LPPeakDeviation(int32_t vals[], byte num);

void LPSortList(int32_t *ar, uint8_t n);

#endif
