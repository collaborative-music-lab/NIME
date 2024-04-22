# [370] [s24] Apr 22 notes

# Overview

1. Calendar
	* Mon Apr 22: Performer Presentations, IMU Workshop
	* Wed Apr 24: Performer Presentations, Wekinator workshop
	* Mon Apr 29: (on zoom) Grad presentations, final project check-in
	* Wed May 1: in Room 4-158, guest presentation
2. Final Project schedule
	* May 6 & 8: individual presentations
	* Mar 13: in-class performances
3. Moldover presentation
4. Pamela Z presentation
5. IMU & sensor processing
	* Wifi setup
	* monitoring IMU data

6. IMU workshop

# Moldover presentation

# Pamela Z presentation

# IMU sensor processing
*TLDR formulas:*
* onepole lowpass: `outVal = (new * (1-coefficient) + old * coefficient)`
* leaky integrator: `outVal = (bucket + newVal) * leakSize`
* accel jerk (derivative): `outVal = curVal - prevVal`
* gyro angle (integration): `outVal = (curVal + prevVal) * leak`
* accel magnitude: `magnitude = sqrt(x^2 + y^2 + z^2)`
* accel tilt: `angle = arctan(sqrt(x^2 + y^2)/z)`
 
## Wifi Setup
The ESP32 can either join an existing WiFi network, or create its own network (e.g. act as a router). We will give an example of joining a network here. 

1. In Arduino sketch:
   1. set SSID and password to a local WiFi network
      1. note: probably won’t work with institutional networks
   2. Check the port number - it should match in Arduino and Python
   3. Set comModes variable to STAandSERIAL
      1. lets the ESP32 communicate over either USB or WiFi
      2. ‘STA’ means join a network, ‘AP’ means create a network
   4. In Python, comment out the line defining serial: communicaton: `comms = m370_communication.communication(“serial” . . .`
   5. and uncomment the line defining wifi: `comms = m370_communication.communication("wifi", `
      1. make sure the port that is defined matches the port in the arduino sketch
   6. You can switch back and forth between USB and WIFI just by uncommenting those two `comms` lines.

That should work - when you run the python script you’ll see it searching for the ESP32 over:
``` 
send to  192.168.4.1   1236   [253, 2, 1, 255]
broadcast to  192.168.4.255   1236   [253, 2, 1, 255]
received b'GW\x90\x86SP\xcf\xff' ('192.168.1.11', 1236)
received message: b'GW\x90\x86SP\xcf\xff' address ('192.168.1.11', 1236) length 8 
```

Note: When stopping and starting the python script, sometimes you may have to go through starting/stopping several times before it makes a valid wifi connection. . . .

## Monitoring IMU data
Just like with Capacit, it can be helpful to visually monitor IMU data. To do that:
1. In IMU_Lab_ctrl.pd, click the `IMUmonitor` object in the MONITOR section.
2. Click the `enable monitor`toggle to start monitoring
3. Note the `route ` object determines which OSC messages are displayed. 
4. You can change the which data is displayed by editing the `route` object, or by editing the OSC messages sent in the oscMappings.py script.
   1. e.g. searching for ‘/tiltX’ will show you that there are several kinds of tilt we can monitor, and only one should be uncommented at a time.

## Smoothing sensor data
Raw sensor data: sensor’s base output
Cooked sensor data: processed to reveal features of interest

Often, smoothing data will require the ability to store old values. The `state` structure in IMU_Lab -> oscMappings.py, line 33 keeps track of all raw and cooked sensor data.

Note:
* smoothing data will make the impact of sudden changes appear in the output more slowly. 
* it is often better to do smoothing on a microcontroller, e.g. sample a signal really quickly (1000Hz or more), smooth it, and then send to python more slowly (100Hz or so)
* sometimes it is helpful to keep track of the unsmoothed data as well, if you are looking for sudden changes like strikes or plucks
* also keep in mind you can process ascending and descending values differently. . . .

1. Onepole lowpass filter:
   1. `outVal= (new * (1-coefficient) + old * coefficient)`
   2. equivalent to:
      1. `outVal= old + coefficient * (new - old )`
   3. oscMappings.py, line 322
   4. Variations:
      1. have the coefficient be different depending on whether (old>new) or (old<new)
2. Leaky integrator
   1. add new values to a bucket
   2. shrink the bucket either by scaling it or use a constant leak
   3. oscMappings.py, line 336
3. Mean, Median, Peak, Trough
   1. uses:
      1. Mean (average): smooth out fluctations in data
      2. Median: remove occasionally outliers
      3. Peak: focus on high values
      4. Trough: focus on low values   
   2. All require keeping track of values over time
   3. Typically store values in a ‘circular buffer’
   4. Useful in Arduino
      1. Read sensor data really quickly so we don’t miss quick changes
      2. store samples in a buffer
      3. at a slower rate, send average of buffer to python

## Calculating a baseline
We often want to look for sensor data relative to a baseline, e.g. how much it changes from its ‘normal’ value. To do this, we need to keep track of the ‘normal’ value, or the baseline. Since this ‘normal’ value may change over time, it is helpful to have the baseline update very slowly over time:
1. capture the ‘normal’ value of the sensor when the microcontroller starts up
2. for each sensor reading, let a very small part of the input signal affect the baseline, e.g. a onepole filter with coefficient of  0.999
3. when the signal deviates from the baseline by a significant amount, maybe consider ignoring that data rather than using it to update the baseline
   1. functionally, we are trying to account for sensor or mechanical drift, but ignore when we are actively engaging with the sensor

## Tracking change of data over time
The derivative, or delta, can be useful to detect sudden changes, e.g. plucks or strikes. There are several different kinds of derivatives we can take.
1. Given a single sensor data for the position of a sensor (for example an Mbira tine)
2. Velocity, first derivative: curPosition - prevPosition
3. Acceleration, second derivative: curVelocity - prevVelocity
4. Jerk, third derivative: curAccel - prevAccel
5. Snap, fourth derivative: curJerk - prevJerk

Raw accelerometer data is by definition acceleration. . . 

Note: you can also integrate successive values in order to go from acceleration to velocity, for example. But this is often tricky as small errors will accumulate. . . 

## Tracking the power of a signal
The ‘power’ of a signal is related to how much it has deviated from its base value. So we assume the base value is near 0.
* We can calculate the power of a signal over time by:
  1. capture a group of samples
  2. square all of the individual samples
  3. add them together
  4. take the root of the sum
  5. Also called the ‘root-mean-sum’ (RMS)

### Accelerometer magnitude
Power is a good way to describe the magnitude of an accelerometer:
1. square each axis of acceleration
2. add them together
3. take the square root
4. magnitude = sqrt(ax^2 + ay^2 + az^2)
5. chester-simple.py -> oscMappings.py, line 193

## Accelerometer tilt
Tilt is the most common usage of accelerometer data.
* It is easy to make sense of, physically
* It provides a static value which is easy to map
* but is not the same as the raw accel data: raw axes are interdependent

The best way to calculate tilt is:
* angle = arctan(sqrt(ax^2 + ay^2)/az)
* oscMappings.py, line 138

If you also have a gyroscope, you can use a ‘complementary filter’ to add the gyro data to the accelerometer tilt. See oscMappings.py, line 177




