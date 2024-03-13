# [370] [s24] Mar 13 notes

# Schedule
1. today: 
     1. Nobby performances
     2. capacit intro
     3. open lab / check-in
2. next wed mar 18: capacit performances
     - if you don't perform, plan on making a video
3. Apr 1: on zoom
4. Apr 3: in class visit with Basel & Ruanne
5. Apr 10: in class visit with Jordan Rudess

# Capacit overview

## i2c
digital communication
SCL clock
SDA data

# Sensor Types

## capacitive: 
senses: changes in capacitance 
outputs: value relative to baseline calculated as average
Theremin
Jeff Snyder Manta: https://youtu.be/O_GLWIITiGo

## optical
senses: some kind of light
outputs: typically optical sensors are resistive, and will be used in a voltage divider
- output value will be relative to baseline determined somehow?
alphasphere: https://youtu.be/EZdgr6sLQ1Q

## hall effect sensor 
senses: magnetic fields
output: direct voltage output
Continuum https://youtu.be/SiAb48qsZHY?t=1077
https://youtu.be/PnBhR8RLJN8

## Piezo
senses: mechanical vibration
outputs: AC signal / sound
Some Instruments The Pipe
Unsounding Objects https://youtu.be/d6lxxCRdF-o

## Ultrasound
senses: distance
outputs: time between signal output and reflection
https://youtu.be/ebxvVJwGWek?t=137

## accelerometer
senses: acceleration (due to gravity or movement)
outputs: value either normalized to -1/1, or in Gs
- roll/tilt/yaw
- raw accel
- 1st derivative velocity (curVal - prevVal)
- 2nd derivative jerk
- see also gyroscope (rotation) and magnetometer (magnetic fields/ due north)
Mimu gloves (Arianna Grande): https://youtu.be/ZcxZAAgvF3c
https://youtu.be/CvyVQqCO8pY

## force-sensitive resistor
senses: force
outputs: typically used in a voltage divider
soundplane: https://youtu.be/bUsrZlKqcW8
linnstrument: https://youtu.be/MDTikW1BFt8?t=39
roli seaboard: https://youtu.be/P14JcRyJCEI

## wind sensors
senses: air pressure?
outputs:?
vindor github https://github.com/ftrias/vindormusic
https://www.nxp.com/part/MP3V5004GP#/
Roland AE-10 https://youtu.be/djUseuUisvM

## environmental
senses: temperature, humidity, noise, light, presence

# Capacit overview

## sensors
four capacitive pads, tuned for maximum sensitivity
- can sense proximity
- also touch will provide much higher capcitance readings
- capacitance is always relative to a baseline, which continually updates

## synthesis
four FM synthesizers, setup in a feedback loop
- FM voice 1-> FM 2-> FM 3-> FM 4-> FM 1
- proximity changes each voice's volume
- touch sends voice to next voice's FM
- pitch is determined by sample-and-hold of an lfo. when a pad goes from active to inactive a new note is chosen




