# 370_PRIMARY.py
# Ian Hattwick with Fred Kelly
# This file created July 8  2020
# adds support for new ESP32  firmware
#
# Primary script for interfacing with the ESP32
# Setup for serial communication, change communication mode below to try wifi with ESP32
# For wifi:
# 1. set mode below
# 2. set WIFI network and password in arduino, 
# 3. set arduino mode to wifi
# 4. reset ESP32 using side button (or power cycling) before running python script

RAW_INCOMING_SERIAL_MONITOR = 0
PACKET_INCOMING_SERIAL_MONITOR = 0   

CUR_PYTHON_SCRIPT = "370_commTest"
    
import serial, serial.tools.list_ports, socket, sys
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio
import struct
import time

######################
# SET COMMUNICATION MODE
######################
# don't forget to set the ESP32 firmware to match!
SERIAL_ENABLE = 0
WIFI_ENABLE = 1 #!!!! READ FOLLOWING COMMENT
# !!!! WIFI MAY require that you reset ESP32 before running python script
# !!!! and DOES require that you run the python script AFTER resetting the ESP32

######################
#SETUP SERIAL PORT
######################
import scripts.SerialSetup2 as SerialMain
ser  = SerialMain.run(SERIAL_ENABLE, "/dev/cu.usbserial-1430", 115200)

serialOutputBuffer= [[0],[0]]

def addToSerialBuffer(vals):
    serialOutputBuffer.append(vals)

def sendSerialBuffer():
    if len(serialOutputBuffer)  <  2: return 0
    #print("buffer",(serialOutputBuffer[1]))
    #print("len  of serial  buffer", len(serialOutputBuffer))
    slipOutPacket(serialOutputBuffer[1])
    time.sleep(0.002)
    del(serialOutputBuffer[1])

def slipOutPacket(val = []):
    """Send SLIP encoded values to serial or wifi."""
    #print ('val', val)
    outMessage = []
    endByte = bytes([255])
    escByte = bytes([254])
    for i in val:
        if i == endByte:
            outMessage.append(escByte)
            outMessage.append(i)
        elif i == escByte:
            outMessage.append(escByte)
            outMessage.append(i)
        else :
            outMessage.append(i)
    outMessage += (endByte)
    #print("slip", outMessage)
    #outMessage = [0,0,34 ,255]
    if(SERIAL_ENABLE): ser.write(bytearray(outMessage))
    if(WIFI_ENABLE): 
        print("sending to ", espAddress)
        s.sendto(bytearray(outMessage),espAddress)


######################
#SETUP WIFI
######################
import scripts.WifiSetup as wf
clientAddress = ('192.168.1.8', 1234)
s,espAddress = wf.run(WIFI_ENABLE, clientAddress)
#espAddress = ("192.168.0.1",1234)

######################
#SETUP OSC
######################
#initialize UDP client
client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
# dispatcher in charge of executing functions in response to RECEIVED OSC messages
dispatcher = Dispatcher()
print("Sending OSC to port", 5005, "on localhost")
client.send_message("/scriptName", CUR_PYTHON_SCRIPT)


######################
#INTERPRET MESSAGE
######################  

analogBaseAddress = 10
digitalBaseAddress = 50
encoderBaseAddress = 100
capsenseBaseAddress = 150
imuBaseAddress = 200

import scripts.processSerial as ps

def interpretMessage(message):
    # print('interp')
    if message is None:
        return

    if(0):
        for i in range(len(message)):
            print ('mirror', message[i])

    if( message[0]==1):
        print(message[1],message[2])
        return

    address="/default"
    val=0

    # #analog inputs
    if( analogBaseAddress <= message[0] < digitalBaseAddress):
        address = "/analog/" + str(message[0]-analogBaseAddress)
        val = ps.from_uint16(message[1],message[2])
        cMap.input("dial", message[0]-analogBaseAddress, val)

    if( PACKET_INCOMING_SERIAL_MONITOR ):
        print(address,val)
    #client.send_message(address, val)

######################
#COMMUNICATION INPUT
######################

def readNextMessage():
    """Reads new messages over Serial or wifi."""
    if SERIAL_ENABLE:
        if ser.in_waiting:
            return checkSerial()

    elif WIFI_ENABLE:
        return checkWiFi()

#dispatcher.map("/serialRate", rateHandler)

def checkSerial():
    """Checks Serial port for incoming slip-encoded messages and returns decoded array."""
    msgBuffer = bytes()

    # defines reserved bytes signifying end of message and escape character
    endByte = bytes([255])
    escByte = bytes([254])

    msgInProgress = 1

    while(msgInProgress):
        curByte = ser.read(1)
        if(RAW_INCOMING_SERIAL_MONITOR):
            #print ("raw serial: ", int.from_bytes(curByte,byteorder='big'))
            print(int.from_bytes(curByte,byteorder='big'))

        if (curByte == endByte):
            #if we reach a true end byte, we've read a full message, return buffer
            msgInProgress = 0
            return msgBuffer
        elif (curByte == escByte):
            # if we reach a true escape byte, set the flag, but don't write the reserved byte to the buffer
            curByte = ser.read()
            msgBuffer += curByte

        else:
            msgBuffer += curByte

prevUdpMsgNum = 0

def checkWiFi():
    """Checks WiFi UDP for incoming messages."""
    global prevUdpMsgNum
    index = 1;

    bytesTotal = bytes()

    try:
        data, clientAddress = wf.recv()
        if( data[0] == prevUdpMsgNum): return
    except:
        return
    #print ("received message:", data, "address", clientAddress)
    #s.sendto(data, (clientAddress) ) 

    # defines reserved bytes signifying end of message and escape character
    endByte = (255).to_bytes(1, byteorder="little")
    escByte = (254).to_bytes(1, byteorder="little")

    
    #bytesTotal = len(data)
    msgInProgress = 1
    #print("newMsg ", "length", len(data), bytesTotal)

    if( index < len(data) ):
        while(msgInProgress and index<len(data)):
            curByte = (data[index]).to_bytes(1, byteorder="little")
            #print("cur",  curByte, curByte == (35).to_bytes(1, byteorder="little"), endByte)
            if(RAW_INCOMING_SERIAL_MONITOR):
                #print (int.from_bytes(curByte,byteorder='big'))
                print("raw wifi: ", bytesTotal)
                index+=1

            elif (curByte == endByte):
                #if we reach a true end byte, we've read a full message, return buffer
                msgInProgress = 0
                #print ("end", bytesTotal)
                return bytesTotal
            elif (curByte == escByte):
                # if we reach a true escape byte, set the flag, but don't write the reserved byte to the buffer
                bytesTotal += curByte
                index+=1

            else:
                bytesTotal += curByte
                index+=1

######################
#COMMUNICATION  OUTPUT
######################

def setLeds(add,num,r,g,b):
    ledMsg = [50,int(num),int(r), int(g),int(b) ]
    #print("setLed", ledMsg)
    SerialMain.addToSerialBuffer(bytearray(ledMsg))


def seqLed(add,num,val):
    """Receive sequencer index, send values via OSC, and update  LED."""
    #send values disabled due to timing issues
    # for i in range(3):
    #     address = "/seq/" + str(i)
    #     val = seq[i].getStep(num)
    #     client.send_message(address, val)

    #update LED
    cur = val if val < len(seq[0].led) else len(seq[i].led)-1
    curLed = seq[num].led[cur]

    panel.led[curLed].set(0,200,200,200)
    bufferLeds(curLed)
    prev = cur-1 if  cur>0 else 7
    prevLed = seq[num].led[prev]
    panel.led[prevLed].set(0,0,0,0)
    bufferLeds(prevLed)
    #print("seqLed", num, ledMap[num],prev, ledMap[prev] )
    writeLed()



######################
#LOOP
######################

async def loop():
    debugVal = 0
    time.sleep(0.1)
    if SERIAL_ENABLE: 
        print("Resetting  ESP32")
        ser.flushInput()
    # if WIFI_ENABLE:

    time.sleep(0.1)
    handshakeStatus = 1
    while(1):
        slipOutPacket([handshakeStatus,0])
        currentMessage = readNextMessage()
        if currentMessage is None:
            print("waiting")
        #else: print(currentMessage)
        elif currentMessage[0] == 1:
            print("ESP32  found")
            handshakeStatus=2
        elif currentMessage[0] == 2:
            print("Firmware name", currentMessage[1:].decode("utf-8"))
            client.send_message("/firmwareName", currentMessage[1:].decode("utf-8"))
            handshakeStatus=3
        elif currentMessage[0] == 3:
            print("Firmware version", currentMessage[1:].decode("utf-8"))
            client.send_message("/firmwareVersion", currentMessage[1:].decode("utf-8"))
            handshakeStatus=4
        elif currentMessage[0] == 4:
            print("Firmware author", currentMessage[1:].decode("utf-8"))
            client.send_message("/firmwareVersion", currentMessage[1:].decode("utf-8"))
            handshakeStatus=5
        elif currentMessage[0] == 5:
            print("Firmware date", currentMessage[1:].decode("utf-8"))
            client.send_message("/firmwareVersion", currentMessage[1:].decode("utf-8"))
            handshakeStatus=6
        elif currentMessage[0] == 6:
            print("Firmware notes", currentMessage[1:].decode("utf-8"))
            client.send_message("/firmwareVersion", currentMessage[1:].decode("utf-8"))
            handshakeStatus=7
            break;
        else:
            print("looking for ESP32")
        time.sleep(0.1)
    print("done setup")

    while(1):   
        currentMessage = readNextMessage() # can be None if nothing in input buffer
        interpretMessage(currentMessage)
        sendSerialBuffer()
        await asyncio.sleep(0)
        time.sleep(0.001)

async def init_main():
    server = AsyncIOOSCUDPServer(("127.0.0.1", 5006), dispatcher, asyncio.get_event_loop())
    
    transport, protocol = await server.create_serve_endpoint()

    if SERIAL_ENABLE: ser.read(ser.in_waiting)
    await loop()
    transport.close()

asyncio.run(init_main())
