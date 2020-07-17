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

CUR_PYTHON_SCRIPT = "370_PRIMARY_v3"

import serial, serial.tools.list_ports, socket, sys
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio
import struct
import time

import scripts.ledPanel as panel


######################
# SET COMMUNICATION MODE
######################
# don't forget to set the ESP32 firmware to match!
SERIAL_ENABLE = 1
WIFI_ENABLE = 0 #!!!! READ FOLLOWING COMMENT
# !!!! WIFI MAY require that you reset ESP32 before running python script
# !!!! and DOES require that you run the python script AFTER resetting the ESP32

######################
#SETUP SERIAL PORT
######################
import scripts.SerialSetup as SerialSetup
ser  = SerialSetup.run(SERIAL_ENABLE, "/dev/cu.usbserial-1430")

serialOutputBuffer= [[0],[0]]

import binascii

def addToSerialBuffer(vals):
    serialOutputBuffer.append(vals)

def sendSerialBuffer():
    if len(serialOutputBuffer)  <  2: return 0
    #print("buffer",(serialOutputBuffer[1]))
    #print("len  of serial  buffer", len(serialOutputBuffer))
    slipOutPacket(serialOutputBuffer[1])
    time.sleep(0.002)
    del(serialOutputBuffer[1])


######################
#SETUP WIFI
######################
import scripts.WifiSetup as WifiSetup
clientAddress = ('192.168.1.8', 1234)
s =  WifiSetup.run(WIFI_ENABLE, clientAddress)

######################
#SETUP OSC
######################
#initialize UDP client
client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
# dispatcher in charge of executing functions in response to RECEIVED OSC messages
dispatcher = Dispatcher()
print("Sending data to port", 5005)
client.send_message("/scriptName", CUR_PYTHON_SCRIPT)


#sensor inputs
OSC_ADDRESSES = {
    27:{ 'address':'/analog0', 'enable': 0, 'rate':250, 'mode':'DIGITAL' },
    33:{ 'address':'/analog1', 'enable': 1, 'rate':25, 'mode':'MEAN' },
    32:{ 'address':'/analog2', 'enable': 1, 'rate':25, 'mode':'MEAN' },
    14:{ 'address':'/analog3', 'enable': 0, 'rate':200, 'mode':'MEAN' },
    4: { 'address':'/analog4', 'enable': 0, 'rate':200, 'mode':'MEAN' },
    0: { 'address':'/analog5', 'enable': 0, 'rate':200, 'mode':'MEAN' },#pulled high by ESP32
    15:{ 'address':'/analog6', 'enable': 0, 'rate':200, 'mode':'MEAN' },#boot fail if pulled low
    13:{ 'address':'/analog7', 'enable': 0, 'rate':200, 'mode':'MEAN' },
    36:{ 'address':'/analog8', 'enable': 0, 'rate':200, 'mode':'MEAN' },
    39:{ 'address':'/analog9', 'enable': 1, 'rate':25, 'mode':'MEAN' },
    #alternate analog inputs
    34:{ 'address':'/button0', 'enable': 0, 'rate':125, 'mode':'MEAN' }, #button
    35:{ 'address':'/button1', 'enable': 0, 'rate':125, 'mode':'MEAN' }, #button
    2: { 'address':'/analog10', 'enable': 0, 'rate':200, 'mode':'DIGITAL' }, #CS0
    12:{ 'address':'/analog11', 'enable': 0, 'rate':200, 'mode':'DIGITAL' }, #CS1, boot fail if pulled high
    25:{ 'address':'/analog12', 'enable': 0, 'rate':125, 'mode':'MEAN' }, #DAC1
    26:{ 'address':'/analog13', 'enable': 0, 'rate':125, 'mode':'MEAN' }, #DAC2
    #I2C and SPI pins,  mode must be  'DIGITAL', can't be used if  I2C  or SPI are  being used
    18:{ 'address':'/digital0', 'enable': 0, 'rate':200, 'mode':'DIGITAL' },#CLK
    19:{ 'address':'/digital1', 'enable': 0, 'rate':200, 'mode':'DIGITAL' },#MISO
    21:{ 'address':'/digital2', 'enable': 0, 'rate':200, 'mode':'DIGITAL' }, #I2C
    22:{ 'address':'/digital3', 'enable': 0, 'rate':200, 'mode':'DIGITAL' },#I2C
    23:{ 'address':'/digital4', 'enable': 1, 'rate':20, 'mode':'DIGITAL' },#MOSI
    5:{ 'address':'/digital5', 'enable': 0, 'rate':200, 'mode':'DIGITAL' },#MIDI, boot fail if pulled low
    #IMU
    150:{ 'address':'/accelX', 'enable': 0, 'rate':200, 'mode':'MEAN' },
    151:{ 'address':'/accelY', 'enable': 0, 'rate':200, 'mode':'MEAN' },
    152:{ 'address':'/accelZ', 'enable': 0, 'rate':200, 'mode':'MEAN' },
    153:{ 'address':'/gyroX',  'enable': 0, 'rate':20, 'mode':'MEAN' },
    154: { 'address':'/gyroY', 'enable': 0, 'rate':20, 'mode':'MEAN' },
    155: { 'address':'/gyroZ', 'enable': 0, 'rate':20, 'mode':'MEAN' },
    156: { 'address':'/temp',  'enable': 0, 'rate':250, 'mode':'MEAN' }
}


OSC_INDEX_ARRAY = [27,33,32,14,4, 0,15,13,36,39, 34,35,2,12,25, 26,18,19,21,22,  23,5, #analog pins
    150,151,152,153,154,155,156 ] #IMU
ANALOG_MODES = {
    'MEAN':0,
    'MEDIAN':1,
    'MIN':2,
    'MAX':3,
    'PEAK_DEVIATION': 4,
    'CAP_SENSE':5,
    'DIGITAL':6,
    'ECHO':11,
    'TRIG':10
}

enableMsg = [0,0,0,255]
enableMsg[0] = 1;
def setEnables():
    print('\nsetting enabled inputs <input#><enableStatus>')
    #time.sleep(0.25)
    for i in range(len(OSC_INDEX_ARRAY)):
        enableMsg[0] = 1; 
        enableMsg[1]=i;
        enableMsg[2]=OSC_ADDRESSES[OSC_INDEX_ARRAY[i]]['enable']
        if( SERIAL_ENABLE ): ser.write(bytearray(enableMsg)) 
        if( WIFI_ENABLE ): s.sendto(bytearray(enableMsg), (clientAddress) ) 
        #print('enable', enableMsg[1], enableMsg[2])
        time.sleep(0.025)


    print('\nsetting sensor data rate <input#><dataRateInMS>')
    for i in range(len(OSC_INDEX_ARRAY)):
        enableMsg[0] = 2; 
        enableMsg[1]=i;
        enableMsg[2]=OSC_ADDRESSES[OSC_INDEX_ARRAY[i]]['rate']
        if( SERIAL_ENABLE ): ser.write(bytearray(enableMsg)) 
        if( WIFI_ENABLE ): s.sendto(bytearray(enableMsg), (clientAddress) ) 
        #print('rate', enableMsg[1], enableMsg[2])
        time.sleep(0.025)

    print('\nsetting sensor data mode <input#><mode>')
    for i in range(len(OSC_INDEX_ARRAY)):
        enableMsg[0] = 3; 
        enableMsg[1]=i;
        _mode = OSC_ADDRESSES[OSC_INDEX_ARRAY[i]]['mode']
        enableMsg[2]=ANALOG_MODES[_mode]
        if( SERIAL_ENABLE ): ser.write(bytearray(enableMsg)) 
        if( WIFI_ENABLE ): s.sendto(bytearray(enableMsg), (clientAddress) ) 
        #print('mode', enableMsg[1], enableMsg[2])
        time.sleep(0.025)


######################
#INITIALIZE CAPACITIVE INPUTS
#Only if using MPR121  else set NUM_ELECTRODES to 0
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
#INTERPRET MESSAGE
######################  

analogBaseAddress = 10
digitalBaseAddress = 50
encoderBaseAddress = 100
capsenseBaseAddress = 150
imuBaseAddress = 200

import scripts.processSerial as ps
import sensorInterfaces.capToggle as capToggle



def interpretMessage(message):
    # print('interp')
    if message is None:
        return

    if(0):
        for i in range(len(message)):
            print ('mirror', message[i])

    # if(len(message) < 3):
    #     if( SERIAL_ENABLE ): ser.read(ser.in_waiting)
    #     return

    if( message[0]==1):
        print(message[1],message[2])
        return

    # if( message[0]==255):
    #     sendSerialBuffer()
    #     return

    address="/default"
    val=0

    # #analog inputs
    if( analogBaseAddress <= message[0] < digitalBaseAddress):
        address = "/analog/" + str(message[0]-analogBaseAddress)
        val = ps.from_uint16(message[1],message[2])

    # #digital inputs
    if( digitalBaseAddress <= message[0] < encoderBaseAddress):
        address = "/digital/" + str(message[0]-digitalBaseAddress)
        val = ps.from_uint8(message[1])

    # #encoder inputs
    if( encoderBaseAddress <= message[0] < capsenseBaseAddress):
        address = "/encoder/" + str(message[0]-encoderBaseAddress)
        val = ps.from_int8(message[1]) 


    # #cap inputs
    # cap input data  consistss of:
    # -LSB= touch  status
    # -capacitance is stored in next 10 bits
    if( capsenseBaseAddress <= message[0] < imuBaseAddress):
        capNum  = message[0]-capsenseBaseAddress
        val=ps.from_uint16(message[1],message[2])
        pinMap =  [9,2,8,1, 7,0,6,11, 5,3,10,4, 12,13]
        capNum = pinMap[capNum]

        address,seq,new = capToggle.input(capNum,val&1) 
        if new:
            #print("main",seq)
            # print("new")
            ledMap  = [35, 44, 51, 58, 49, 40, 33, 26, 28, 60, 56, 24]
            for i in range(len(seq)):
                panel.led[ledMap[i]].set(2,seq[i]*100,seq[i]*(i%2)*50,0)
                bufferLeds(ledMap[i])
                #time.sleep(0.01)
                #print(i)
            client.send_message(address, seq)
            writeLed()

        address = "/cap/touch/" + str(capNum)
        client.send_message(address, message[2]&1)

        address = "/cap/val/" + str(capNum)
        val = val>>1
            

    # #encoder inputs
    if( imuBaseAddress <= message[0] < 210):
        address = "/imu/" + str(message[0]-imuBaseAddress)
        val = ps.from_int8(message[1],message[2])


    if( PACKET_INCOMING_SERIAL_MONITOR ):
        print(address,val)
    client.send_message(address, val)

######################
#COMMUNICATION INPUT
######################

def readNextMessage():
    """Reads new messages over Serial or wifi."""
    if SERIAL_ENABLE:
        return checkSerial()

    elif WIFI_ENABLE:
        return checkWiFi()

#dispatcher.map("/serialRate", rateHandler)

def checkSerial():
    """Checks Serial port for incoming messages."""
    bytesTotal = bytes()

    # defines reserved bytes signifying end of message and escape character
    endByte = bytes([255])
    escByte = bytes([254])

    
    curByte = ser.read(1)
    #print(int.from_bytes(curByte,byteorder='big'))
    bytesTotal += curByte
    msgInProgress = 1

    while(msgInProgress):
        curByte = ser.read(1)
        if(RAW_INCOMING_SERIAL_MONITOR):
            #print ("raw serial: ", int.from_bytes(curByte,byteorder='big'))
            print(int.from_bytes(curByte,byteorder='big'))

        if (curByte == endByte):
            #if we reach a true end byte, we've read a full message, return buffer
            msgInProgress = 0
            return bytesTotal
        elif (curByte == escByte):
            # if we reach a true escape byte, set the flag, but don't write the reserved byte to the buffer
            curByte = ser.read()
            bytesTotal += curByte

        else:
            bytesTotal += curByte

prevUdpMsgNum = 0

def checkWiFi():
    """Checks WiFi UDP for incoming messages."""
    global prevUdpMsgNum
    index = 1;

    bytesTotal = bytes()

    try:
        data, clientAddress = s.recvfrom(1024) # buffer size is 1024 bytes
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
        else :
            outMessage.append(i)
    outMessage += (endByte)
    #print("slip", outMessage)
    #outMessage = [0,0,34 ,255]
    ser.write(bytearray(outMessage))

def setLeds(add,num,r,g,b):
    ledMsg = [50,int(num),int(r), int(g),int(b) ]
    #print("setLed", ledMsg)
    addToSerialBuffer(bytearray(ledMsg))


def seqLed(add,num):
    ledMap  = [35, 44, 51, 58, 49, 40, 33, 26, 28, 60, 56, 24]
    panel.led[ledMap[num]].set(0,0,0,200)
    bufferLeds(ledMap[num])
    prev = num-1 if num>0 else 7
    panel.led[ledMap[prev]].set(0,0,0,0)
    bufferLeds(ledMap[prev])
    #print("seqLed", num, ledMap[num],prev, ledMap[prev] )
    writeLed()

def bufferLeds(num):
    r=0
    g=0
    b=0
    for i in range(3):
        #print(num,i,panel.led[num].r[i])
        cur  = panel.led[num].get(i)
        r = cur[0] if cur[0]>r else r
        g = cur[1] if cur[1]>g else g
        b = cur[2] if cur[2]>b else b
    ledMsg = [51,int(num),int(r), int(g),int(b) ]
    #print("bufferLed", ledMsg)
    addToSerialBuffer(bytearray(ledMsg))

def writeLed():
    ledMsg = [52]
    #print("writeLed", ledMsg)
    addToSerialBuffer(bytearray(ledMsg))

def testLeds():
    for  i in range(64):
        setLeds("/led",i,100,0,100)
        #time.sleep(0.05)
    #writeLed()

def  updateLed(add,num):
    for i in range(4):
        print("update", num, i, panel.led[num].get(i))

dispatcher.map("/led", setLeds)
dispatcher.map("/seqIndex", seqLed)
dispatcher.map("/updateLed", updateLed)


######################
#LOOP
######################

async def loop():
    debugVal = 0
    panel.begin()
    time.sleep(0.1)
    if SERIAL_ENABLE: 
        print("Resetting  ESP32")
        ser.flushInput()
        time.sleep(0.1)
        while(1):
            currentMessage = readNextMessage()
            if currentMessage is None:
                print("waiting")
            #else: print(currentMessage)
            elif currentMessage[0] == 1:
                print("ESP32  found")
                slipOutPacket([1,1])
                temp=0
            elif currentMessage[0] == 2:
                print("Firmware name", currentMessage[1:].decode("utf-8"))
                client.send_message("/firmwareName", currentMessage[1:].decode("utf-8"))
                slipOutPacket([2,2])
            elif currentMessage[0] == 3:
                print("Firmware version", currentMessage[1:].decode("utf-8"))
                client.send_message("/firmwareVersion", currentMessage[1:].decode("utf-8"))
                slipOutPacket([3,3])
                break;
            else:
                print("looking for ESP32")
            time.sleep(0.1)
    setEnables()
    setCapSense()
    #testLeds()

    
    while(1):
        currentMessage = readNextMessage() # can be None if nothing in input buffer
        interpretMessage(currentMessage)
        sendSerialBuffer()
        await asyncio.sleep(0)
        time.sleep(0.001)

async def init_main():
    server = AsyncIOOSCUDPServer(("127.0.0.1", 5006), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    print (ser.timeout)
    if SERIAL_ENABLE: ser.read(ser.in_waiting)
    await loop()
    transport.close()

asyncio.run(init_main())
