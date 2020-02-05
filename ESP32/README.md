# ESP32 firmware for 21M.370

This firmware was developed using the Arduino IDE and the toolchain provided by Espressif. 

## Installing

1. Download a recent version of Arduino (I recommed downloading rather than trying to use the web-based IDE).

2. Install hardware support for the ESP32:
	Follow the instructions from this link to install the drivers for the ESP32, but instead of pasting in the sparkfun github link paste in the following link:
	`https://dl.espressif.com/dl/package_esp32_index.json`
	(note that the sparkfun libraries are super useful and we may use them in the future, so it doesn’t hurt to download those as well).

Any additional downloads will be updated on an as-needed basis

## Hardware settings

Once the ESP32 hardware support is installed:

1. Select the "TTGO T1" hardware definition from the Tools->Board menu. There will be a bunch of boards listed - scroll down and select the "TTGO T1" board.
2. Change the Upload Speed (Tools->Upload Speed) to 460800. If you experience problems uploading the the board you may try a lower speed. The default 921600 will likely fail to upload.
3. Go to Tools->Port and look for something that looks like 'usbserial' or something like that. If you don't see it you can try restarting Arduino with the board plugged in. Or verify that the board is plugged in correctly and powered on.
