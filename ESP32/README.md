# ESP32 firmware for 21M.370

This firmware was developed using the Arduino IDE and the toolchain provided by Espressif. 

## Installing

1. Download a recent version of Arduino (You will need to use the downloadable version rather than the web-based IDE).

2. Install hardware support for the ESP32:
	Follow the instructions for 'Installing using Boards Manager' from [this link to install the drivers](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html).

Any additional downloads will be updated on an as-needed basis.

You will also likely need to download drivers for the [CP2104 USB drivers](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers)


## Hardware settings

Once the ESP32 hardware support is installed:

1. Select the "TTGO T1" hardware definition from the Tools->Board menu. There will be a bunch of boards listed - scroll down and select the "TTGO T1" board.
2. Change the Upload Speed (Tools->Upload Speed) to 460800. If you experience problems uploading the the board you may try a lower speed. The default 921600 will likely fail to upload.
3. Go to Tools->Port and look for something that looks like 'usbserial' or something like that. If you don't see it you can try restarting Arduino with the board plugged in. Or verify that the board is plugged in correctly and powered on.

## FAQ/good to know

1. If GPIO 4 on the ESP32 board is pulled low it will cause a boot failure for the ESP32. Better to not use this pin for now?
2. GPIO 7 was incorrectly assigned to pin 14 in 370.h. It should be pin 13.
3. ESP32 pin to m370 pin mapping for board v2.06:
```
m370 	ESP32	Notes
pin	GPIO 
-----------------------------
0	27
1	33
2	32
3	14
4	4	strapping pin
5	0	strapping pin
6	15	strapping pin / must be  high on boot
7	13
8	36	input only
9	39	input only
cs0	2	strapping pin
cs1	12	strapping pin/ must be low on boot
MISO	19	
MOSI	23
SCK	18
SCL	22
SDA	21
MIDI	5	strapping pin / must be  high on boot
dac1	25
dac2	26
```

