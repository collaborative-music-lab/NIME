# 370_HELLO_ESP32.py
# based on general_teensy_bridge
# Ian Hattwick and Fred Kelly
# This file created Jan 10 2020

# Receives data from either the UART serial port or WiFi network bus
# - received data is SLIP encoded
# maps incoming messages to osc addresses
#- mapping is stored in 

RAW_INCOMING_SERIAL_MONITOR = 0
PACKET_INCOMING_SERIAL_MONITOR = 0

import serial, serial.tools.list_ports, socket, sys
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio
import struct
import time

data = {
    27:'/analog0',
    33:'/analog1',
    32:'/analog2',
    14:'/analog3',
    4: '/analog4',
    0: '/analog5',
    15:'/analog6',
    13:'/analog7',
    36:'/analog8',
    39:'/analog9',
    34:'/button0',
    35:'/button1'
    }

#messageIDs = new Array(27,33,34,35);

#set up serial port
ports = list(serial.tools.list_ports.comports())
for x in range(len(ports)): 
    print (ports[x])
    if "USB" in ports[x]:
        print("serial")

ser = serial.Serial("/dev/cu.usbserial-14320")
ser.baudrate=115200
ser.read(ser.in_waiting) # if anything in input buffer, discard it

#initialize UDP client
client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
# dispatcher in charge of executing functions in response to RECEIVED OSC messages
dispatcher = Dispatcher()
print("Sending data to port", 5005)

######################
#READ SERIAL MESSAGES
######################


def readNextMessage():


    bytesTotal = bytes()

    # defines reserved bytes signifying end of message and escape character
    endByte = bytes([255])
    escByte = bytes([254])

    
    curByte = ser.read(1)
    #print("newserial packet")
    bytesTotal += curByte
    msgInProgress = 1

    while(msgInProgress):
        curByte = ser.read(1)
        if(RAW_INCOMING_SERIAL_MONITOR):
            print (curByte)

        elif (curByte == endByte):
            #if we reach a true end byte, we've read a full message, return buffer
            msgInProgress = 0
            return bytesTotal
        elif (curByte == escByte):
            # if we reach a true escape byte, set the flag, but don't write the reserved byte to the buffer
            curByte = ser.read()
            bytesTotal += curByte

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

    if(len(message) != 3):
        ser.read(ser.in_waiting)
        #print(len(message))
        return

    address = data[message[0]]
    val = (message[1]<<8) + message[2]

    if( PACKET_INCOMING_SERIAL_MONITOR ):
        print(address,val)

    client.send_message(address, val)


#def getNewAddress(num):

def slipOutByte(val):
    outMessage = bytes();
    endByte = bytes([255])
    escByte = bytes([254])
    if val == endByte:
        outMessage.append(escByte)
        outMessage.append(val)
    else :
        outMessage.append(val)

    outMessage.append(endByte)
    ser.write(outMessage)


######################
#LOOP
######################
async def loop():
    while(1):
        currentMessage = readNextMessage() # can be None if nothing in input buffer
        interpretMessage(currentMessage)
        await asyncio.sleep(0)
        time.sleep(0.001)

async def init_main():
    server = AsyncIOOSCUDPServer(("127.0.0.1", 5006), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    print (ser.timeout)
    ser.read(ser.in_waiting)
    await loop()
    transport.close()

asyncio.run(init_main())
