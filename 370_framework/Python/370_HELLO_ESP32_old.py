# 370_HELLO_ESP#@.py
# based on general_teensy_bridge
# Ian Hattwick and Fred Kelly
# This file created Jan 10 2020

# Receives data from either the UART serial port or WiFi network bus
# - received data is SLIP encoded
# maps incoming messages to osc addresses
#- mapping is stored in 

RAW_INCOMING_SERIAL_MONITOR = 0
PACKET_INCOMING_SERIAL_MONITOR = 1

import serial, serial.tools.list_ports, socket, sys
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio
import struct
import time

data = {
    34:'/button/0',
    35:'/button/1'
    }

# deviceNames = {
#     "/dev/cu.Bluetooth-Incoming-Port"
#     }

#set up serial port
ports = list(serial.tools.list_ports.comports())
for x in range(len(ports)): 
    print (ports[x])

# for port in ports:
#     if (port.description in deviceNames): #Teensy description is "USB Serial Device"
#         ser = serial.Serial("/dev/cu.Bluetooth-Incoming-Port")
#         ser.baudrate=115200
#         ser.read(ser.in_waiting) # if anything in input buffer, discard it

ser = serial.Serial("/dev/cu.usbserial-1410")
ser.baudrate=115200
ser.read(ser.in_waiting) # if anything in input buffer, discard it


#initialize UDP client
client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
# dispatcher in charge of executing functions in response to RECIEVED OSC messages
dispatcher = Dispatcher()

######################
#READ SERIAL MESSAGES
######################

def readNextMessage():

    bytesInQueue = ser.in_waiting

    if( 0):
        #buffer to decode message into (reading from serial port)
        bytesTotal = bytes()

        # if escape flag is true, next byte is part of message (even if a reserved byte)
        escFlag = False

        curByte = bytes()
        # defines reserved bytes signifying end of message and escape character
        endByte = bytes([255])
        escByte = bytes([254])

        while (bytesInQueue > 0):
                curByte = ser.read()
                bytesInQueue -= 1
                
                if(RAW_INCOMING_SERIAL_MONITOR):
                    print (curByte)

                if (escFlag):
                    bytesTotal += curByte
                    escFlag = False
                elif (curByte == endByte):
                    #if we reach a true end byte, we've read a full message, return buffer
                    return bytesTotal
                elif (curByte == escByte):
                    # if we reach a true escape byte, set the flag, but don't write the reserved byte to the buffer
                    escFlag = True
                else:
                    bytesTotal += curByte

def buttonToPd(ch, num, state):
    address = "/button/ch{}".format(ch)
    client.send_message(address, [num, state])

def faderToPd(ch, num, value):
    address = "/fader/ch{}".format(ch)
    client.send_message(address, [num, value])

def imuRawToPd(ch, a, m, g):
    address = "/imu/raw/ch{}".format(ch)
    imuRawMsg = ["a"] + a + ["m"] + m +["g"] + g
    client.send_message(address, imuRawMsg)
    
def imuAnglesToPd(ch, pitch, roll):
    address = "/imu/angles/ch{}".format(ch)
    imuAnglesMsg = ["pitch", pitch, "roll", roll]
    client.send_message(address, imuAnglesMsg)
   
######################
#INTERPRET MESSAGE
######################    

def interpretMessage(message):
    if message is None:
        return

    address = data[message[0]]
    val = (message[1]<<8) + message[2]

    if( PACKET_INCOMING_SERIAL_MONITOR ):
        print(address,val)

    client.send_message(address, val)

    # if (message[0] in buttonIds):
    #     # based on byte order of msg type, interpret what kind of data we have recieved
    #     channel = message[0] - BUTTON_CH_0
    #     num = message[1]
    #     highStateByte = message[2]
    #     lowStateByte = message[3]
    #     state = (highStateByte << 8) + lowStateByte
    #     buttonToPd(channel, num, state)
    # elif (message[0] in faderIds):
    #     channel = message[0] - FADER_CH_0
    #     num = message[1]
    #     highValByte = message[2]
    #     lowValByte = message[3]
    #     value = (highValByte << 8) + lowValByte
    #     faderToPd(channel, num, value)
    # elif (message[0] in imuRawIds):
    #     channel = message[0] - IMU_RAW_CH_0
    #     allSensorVals = struct.unpack('fffffffff', message[1:])
    #     a = list(allSensorVals[:3])
    #     m = list(allSensorVals[3:6])
    #     g = list(allSensorVals[6:9])
    #     imuRawToPd(channel, a, m, g)
    # elif (message[0] in imuAnglesIds):
    #     channel = message[0] - IMU_ANGLES_CH_0
    #     allSensorVals = struct.unpack('ff', message[1:])
    #     pitch = allSensorVals[0]
    #     roll = allSensorVals[1]
    #     imuAnglesToPd(channel, pitch, roll);

######################
#LOOP
######################
async def loop():
    while(1):
        currentMessage = readNextMessage() # can be None if nothing in input buffer
        interpretMessage(currentMessage)
        #allows dispatcher to take over and check for recieved OSC messages
        await asyncio.sleep(0)
        time.sleep(0.001)

async def init_main():
    server = AsyncIOOSCUDPServer(("127.0.0.1", 5006), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    await loop()
    transport.close()

asyncio.run(init_main())
