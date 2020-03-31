# 370_ANALOG_SELECT.py
# Ian Hattwick and Fred Kelly
# This file created Mar 20  2020
#
# This script allows for changing settings for sensor data:
# - enable individual analog inputs
# - set the data rate for analog inputs
#
# Receives data from the UART serial port 
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

#set up serial port
ports = list(serial.tools.list_ports.comports())
for x in range(len(ports)): 
    print (ports[x])
    if "USB" in ports[x]:
        print("serial")

ser = serial.Serial("/dev/cu.usbserial-14340")
ser.baudrate=115200
ser.setDTR(False) # Drop DTR
time.sleep(0.022)    # Read somewhere that 22ms is what the UI does.
ser.setDTR(True)  # UP the DTR back
ser.read(ser.in_waiting) # if anything in input buffer, discard it

#initialize UDP client
client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
# dispatcher in charge of executing functions in response to RECEIVED OSC messages
dispatcher = Dispatcher()
print("Sending data to port", 5005)

#sensor inputs
OSC_ADDRESSES = {
    27:{ 'address':'/analog0', 'enable': 1, 'rate':10 },
    33:{ 'address':'/analog1', 'enable': 1, 'rate':20 },
    32:{ 'address':'/analog2', 'enable': 0, 'rate':50 },
    14:{ 'address':'/analog3', 'enable': 0, 'rate':50 },
    4: { 'address':'/analog4', 'enable': 0, 'rate':50 },
    0: { 'address':'/analog5', 'enable': 1, 'rate':150 },
    15:{ 'address':'/analog6', 'enable': 1, 'rate':150 },
    13:{ 'address':'/analog7', 'enable': 1, 'rate':150 },
    36:{ 'address':'/analog8', 'enable': 0, 'rate':10 },
    39:{ 'address':'/analog9', 'enable': 0, 'rate':10 },
    34:{ 'address':'/button0', 'enable': 0, 'rate':15 },
    35:{ 'address':'/button1', 'enable': 0, 'rate':15 }
}

#OSC_INDEX = {0:27,1:33,2:32,3:14,4:4,5:0,6:15,7:13,8:36,9:39,10:34,11:35}
OSC_INDEX_ARRAY = [27,33,32,14,4,0,15,13,36,39,34,35]

enableMsg = [0,0,0,255]
enableMsg[0] = 1;

def setEnables():
    print('\nsetting enabled inputs <input#><enableStatus>')
    for i in range(len(OSC_INDEX_ARRAY)):
        enableMsg[0] = 1; 
        enableMsg[1]=i;
        enableMsg[2]=OSC_ADDRESSES[OSC_INDEX_ARRAY[i]]['enable']
        ser.write(bytearray(enableMsg)) 
        print('enable', enableMsg[1], enableMsg[2])
        time.sleep(0.05)


    print('\nsetting sensor data rate <input#><dataRateInMS>')
    for i in range(len(OSC_INDEX_ARRAY)):
        enableMsg[0] = 2; 
        enableMsg[1]=i;
        enableMsg[2]=OSC_ADDRESSES[OSC_INDEX_ARRAY[i]]['rate']
        ser.write(bytearray(enableMsg)) 
        print('rate', enableMsg[1], enableMsg[2])
        time.sleep(0.05)


######################
#READ SERIAL MESSAGES
######################

def readNextMessage():
    bytesTotal = bytes()

    # defines reserved bytes signifying end of message and escape character
    endByte = bytes([255])
    escByte = bytes([254])

    
    curByte = ser.read(1)
    bytesTotal += curByte
    msgInProgress = 1

    while(msgInProgress):
        curByte = ser.read(1)
        if(RAW_INCOMING_SERIAL_MONITOR):
            print (int.from_bytes(curByte,byteorder='big'))

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

   
######################
#INTERPRET MESSAGE
######################    

def interpretMessage(message):
    # print('interp')
    if message is None:
        return

    if(0):
        print ('mirror', message)

    if(len(message) < 3):
        ser.read(ser.in_waiting)
        return

    if( message[0]==1):
        print(message[1],message[2])
        return

    if( message[0] in OSC_INDEX_ARRAY):
        address = OSC_ADDRESSES[message[0]]['address']

        val = (message[1]<<8) + message[2]

        if( PACKET_INCOMING_SERIAL_MONITOR ):
            print(address,val)

        client.send_message(address, val)
    

######################
#DISPATCHER
#sends received OSC messages over serial
######################

def slipOutPacket(val = []):
    print ('val', val)
    outMessage = []
    endByte = bytes([255])
    escByte = bytes([254])
    for i in val:
        if i == endByte:
            outMessage.append(escByte)
            outMessage.append(i)
        else :
            outMessage.append(i)
    outMessage += (endByte)
    print(outMessage)
    outMessage = [0,0,34 ,255]
    #ser.write(bytearray(outMessage))

#dispatcher.map("/serialRate", rateHandler)

######################
#LOOP
######################

async def loop():
    debugVal = 0
    time.sleep(0.1)
    ser.flushInput() 
    time.sleep(0.1)  
    setEnables()
    
    while(1):
        currentMessage = readNextMessage() # can be None if nothing in input buffer
        interpretMessage(currentMessage)
        await asyncio.sleep(0)
        time.sleep(0.001)

async def init_main():
    server = AsyncIOOSCUDPServer(("127.0.0.1", 5006), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    #print (ser.timeout)
    ser.read(ser.in_waiting)
    await loop()
    transport.close()

asyncio.run(init_main())
