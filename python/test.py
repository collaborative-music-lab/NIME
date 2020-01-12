import serial, serial.tools.list_ports, socket, sys
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio
import struct

# Header ID's of messages recieved from the Teensy
BUTTON_CH_0 = 0
BUTTON_CH_1 = 1
BUTTON_CH_2 = 2
BUTTON_CH_3 = 3

FADER_CH_0 = 4
FADER_CH_1 = 5
FADER_CH_2 = 6
FADER_CH_3 = 7
FADER_CH_4 = 8
FADER_CH_5 = 9
FADER_CH_6 = 10

IMU_RAW_CH_0 = 11
IMU_RAW_CH_1 = 12
IMU_RAW_CH_2 = 13
IMU_RAW_CH_3 = 14
IMU_RAW_CH_4 = 15

IMU_ANGLES_CH_0 = 16
IMU_ANGLES_CH_1 = 17
IMU_ANGLES_CH_2 = 18
IMU_ANGLES_CH_3 = 19
IMU_ANGLES_CH_4 = 20

# sets grouping of ID's by type
buttonIds = {
    BUTTON_CH_0,
    BUTTON_CH_1,
    BUTTON_CH_2,
    BUTTON_CH_3
}

faderIds = {
    FADER_CH_0,
    FADER_CH_1,
    FADER_CH_2,
    FADER_CH_3,
    FADER_CH_4,
    FADER_CH_5,
    FADER_CH_6
}

imuRawIds = {
    IMU_RAW_CH_0,
    IMU_RAW_CH_1,
    IMU_RAW_CH_2,
    IMU_RAW_CH_3,
    IMU_RAW_CH_4,
}

imuAnglesIds = {
    IMU_ANGLES_CH_0,
    IMU_ANGLES_CH_1,
    IMU_ANGLES_CH_2,
    IMU_ANGLES_CH_3,
    IMU_ANGLES_CH_4,
}

deviceNames = {
    "/dev/tty.Bluetooth-Incoming-Port"
    }

#set up serial port
ports = list(serial.tools.list_ports.comports())
for x in range(len(ports)): 
    print (ports[x])