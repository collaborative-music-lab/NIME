# 370_CAPSENSE.py
# Ian Hattwick and Fred Kelly
# This file created Apr 1  2020
#
# Adds support for reading capacitive sensor data from the MPR121

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

ser = serial.Serial("/dev/cu.usbserial-1440")
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

######################
#INITIALIZE ANALOG INPUTS
######################
OSC_ADDRESSES = {
    27:{ 'address':'/analog0', 'enable': 1, 'rate':100, 'mode':'MEAN' },
    33:{ 'address':'/analog1', 'enable': 1, 'rate':100, 'mode':'MEAN' },
    32:{ 'address':'/analog2', 'enable': 1, 'rate':100, 'mode':'MEAN' },
    14:{ 'address':'/analog3', 'enable': 0, 'rate':50, 'mode':'MEAN' },
    4: { 'address':'/analog4', 'enable': 0, 'rate':50, 'mode':'MEAN' },
    0: { 'address':'/analog5', 'enable': 0, 'rate':150, 'mode':'MEAN' },
    15:{ 'address':'/analog6', 'enable': 0, 'rate':150, 'mode':'MEAN' },
    13:{ 'address':'/analog7', 'enable': 0, 'rate':150, 'mode':'MEAN' },
    36:{ 'address':'/analog8', 'enable': 0, 'rate':10, 'mode':'MEAN' },
    39:{ 'address':'/analog9', 'enable': 0, 'rate':10, 'mode':'MEAN' },
    34:{ 'address':'/button0', 'enable': 0, 'rate':15, 'mode':'MEAN' },
    35:{ 'address':'/button1', 'enable': 0, 'rate':25, 'mode':'MEAN' }
}

OSC_INDEX_ARRAY = [27,33,32,14,4,0,15,13,36,39,34,35]
ANALOG_MODES = {
    'MEAN':0,
    'MEDIAN':1,
    'MIN':2,
    'MAX':3,
    'PEAK_DEVIATION': 4,
    'CAP_SENSE':5
}

#Load enable and rate status for all analog pins
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

    print('\nsetting sensor data mode <input#><mode>')
    for i in range(len(OSC_INDEX_ARRAY)):
        enableMsg[0] = 3; 
        enableMsg[1]=i;
        _mode = OSC_ADDRESSES[OSC_INDEX_ARRAY[i]]['mode']
        enableMsg[2]=ANALOG_MODES[_mode]
        ser.write(bytearray(enableMsg)) 
        print('mode', enableMsg[1], enableMsg[2])
        time.sleep(0.05)



######################
#INITIALIZE CAPACITIVE INPUTS
######################
NUM_ELECTRODES = 12;
chargeCurrent = 63; #0-63
capInterval = 100;

def setCapSense():
    capMessage = [10,NUM_ELECTRODES, 255]
    ser.write(bytearray(capMessage))
    capMessage = [12,chargeCurrent, 255]
    ser.write(bytearray(capMessage))
    capMessage = [11,0,capInterval, 255]
    for i in range(NUM_ELECTRODES):
        capMessage[1] = i
        ser.write(bytearray(capMessage))


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

    #analog inputs
    if( message[0] in OSC_INDEX_ARRAY):
        address = OSC_ADDRESSES[message[0]]['address']

        val = (message[1]<<8) + message[2]

        if( PACKET_INCOMING_SERIAL_MONITOR ):
            print(address,val)

        client.send_message(address, val)
    #capacitive inputs
    elif(message[0] >= 64 and message[0]<76):
        address = '/capsense' + str(message[0]-64);

        val = (message[1]<<8) + message[2] - 4096

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
    setCapSense()
    
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
