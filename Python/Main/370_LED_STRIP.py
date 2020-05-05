# 370_LED_STRIP.py
# Ian Hattwick with Fred Kelly
# This file created May 4 2020
#
# Primary script for interfacing with the ESP32
# Setup for serial communication, change communication mode below to try with ESP32
# For wifi:
# 1. set mode below
# 2. set WIFI network and password in arduino, 
# 3. set arduiino mode to wifi
# 4. reset ESP32 using side button (or power cycling) before running python script


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

######################
# SET COMMUNICATION MODE
######################
# don't forget to set the ESP32 firmware to match!
SERIAL_ENABLE = 1
WIFI_ENABLE = 0 #!!!! READ FOLLOWING COMMENT
# !!!! WIFI requires that you reset ESP32 before running python script

######################
#SETUP SERIAL PORT
######################
if( SERIAL_ENABLE):
    #find serial port
    curSerialPort = "/dev/cu.usbserial-1434120"
    ports = list(serial.tools.list_ports.comports())

    #print ports
    print("available serial ports:")
    for x in range(len(ports)): 
        print(ports[x] )

    #check if cur port is available 
    for x in range(len(ports)):   
        if curSerialPort in ports[x]:
            ser = serial.Serial(curSerialPort)
            ser.baudrate=115200
            ser.setDTR(False) # Drop DTR
            time.sleep(0.022)    # Read somewhere that 22ms is what the UI does.
            ser.setDTR(True)  # UP the DTR back
            ser.read(ser.in_waiting) # if anything in input buffer, discard it
            print(curSerialPort + " connected\n")
            SERIAL_ENABLE = 1
        else: 
            print(curSerialPort + " not available\n")  

######################
#SETUP WIFI
######################
BCAST_HOST = '192.168.1.255'                 # Symbolic name meaning all available interfaces
BCAST_PORT = 1234              # Arbitrary non-privileged port

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((BCAST_HOST, BCAST_PORT))
sock.setblocking(0)

HOST = '192.168.1.100'                 # Symbolic name meaning all available interfaces
PORT = 1234              # Arbitrary non-privileged port

if (WIFI_ENABLE):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    s.setblocking(0)

    clientAddress = ('192.168.1.8', 1234)

    wifiCounter = 0
    while True:
        print  ("checking WiFi. . . ")
        try: 
            data, clientAddress = sock.recvfrom(1024) # buffer size is 1024 bytes
            print ("received message:", data, "address", clientAddress, "length", len(data))
            if (len(data) > 0):  
                print("Wifi connected to ", clientAddress)
                s.sendto(data, (clientAddress) ) 
                break
        
        except socket.error as ex:
            print("error", ex)
        
        
        time.sleep(0.1)
        wifiCounter+=1
        if(wifiCounter>10): 
            "No wifi connection established"
            break

######################
#SETUP OSC
######################
#initialize UDP client
client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
# dispatcher in charge of executing functions in response to RECEIVED OSC messages
dispatcher = Dispatcher()
print("Sending data to port", 5005)

#sensor inputs
OSC_ADDRESSES = {
    27:{ 'address':'/analog0', 'enable': 1, 'rate':200, 'mode':'MEAN' },
    33:{ 'address':'/analog1', 'enable': 1, 'rate':200, 'mode':'MEAN' },
    32:{ 'address':'/analog2', 'enable': 1, 'rate':20, 'mode':'MEAN' },
    14:{ 'address':'/analog3', 'enable': 0, 'rate':200, 'mode':'MEAN' },
    4: { 'address':'/analog4', 'enable': 0, 'rate':200, 'mode':'MEAN' },
    0: { 'address':'/analog5', 'enable': 0, 'rate':200, 'mode':'MEAN' },
    15:{ 'address':'/analog6', 'enable': 0, 'rate':200, 'mode':'MEAN' },
    13:{ 'address':'/analog7', 'enable': 0, 'rate':200, 'mode':'MEAN' },
    36:{ 'address':'/analog8', 'enable': 0, 'rate':200, 'mode':'MEAN' },
    39:{ 'address':'/analog9', 'enable': 0, 'rate':200, 'mode':'MEAN' },
    34:{ 'address':'/button0', 'enable': 0, 'rate':125, 'mode':'MEAN' },
    35:{ 'address':'/button1', 'enable': 0, 'rate':125, 'mode':'MEAN' }
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

enableMsg = [0,0,0,255]
enableMsg[0] = 1;
def setEnables():
    print('\nsetting enabled inputs <input#><enableStatus>')
    time.sleep(0.25)
    for i in range(len(OSC_INDEX_ARRAY)):
        enableMsg[0] = 1; 
        enableMsg[1]=i;
        enableMsg[2]=OSC_ADDRESSES[OSC_INDEX_ARRAY[i]]['enable']
        if( SERIAL_ENABLE ): ser.write(bytearray(enableMsg)) 
        if( WIFI_ENABLE ): s.sendto(bytearray(enableMsg), (clientAddress) ) 
        print('enable', enableMsg[1], enableMsg[2])
        time.sleep(0.025)


    print('\nsetting sensor data rate <input#><dataRateInMS>')
    for i in range(len(OSC_INDEX_ARRAY)):
        enableMsg[0] = 2; 
        enableMsg[1]=i;
        enableMsg[2]=OSC_ADDRESSES[OSC_INDEX_ARRAY[i]]['rate']
        if( SERIAL_ENABLE ): ser.write(bytearray(enableMsg)) 
        if( WIFI_ENABLE ): s.sendto(bytearray(enableMsg), (clientAddress) ) 
        print('rate', enableMsg[1], enableMsg[2])
        time.sleep(0.025)

    print('\nsetting sensor data mode <input#><mode>')
    for i in range(len(OSC_INDEX_ARRAY)):
        enableMsg[0] = 3; 
        enableMsg[1]=i;
        _mode = OSC_ADDRESSES[OSC_INDEX_ARRAY[i]]['mode']
        enableMsg[2]=ANALOG_MODES[_mode]
        if( SERIAL_ENABLE ): ser.write(bytearray(enableMsg)) 
        if( WIFI_ENABLE ): s.sendto(bytearray(enableMsg), (clientAddress) ) 
        print('mode', enableMsg[1], enableMsg[2])
        time.sleep(0.025)


######################
#INITIALIZE CAPACITIVE INPUTS
#Only if using MPR121  else set NUM_ELECTRODES to 0
######################
NUM_ELECTRODES = 0;
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

def interpretMessage(message):
    # print('interp')
    if message is None:
        return

    if(0):
        print ('mirror', message)

    if(len(message) < 3):
        if( SERIAL_ENABLE ): ser.read(ser.in_waiting)
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
    bytesTotal += curByte
    msgInProgress = 1

    while(msgInProgress):
        curByte = ser.read(1)
        if(RAW_INCOMING_SERIAL_MONITOR):
            #print ("raw serial: ", int.from_bytes(curByte,byteorder='big'))
            print(int.from_bytes(curByte,byteorder='big'))

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
    #print(outMessage)
    #outMessage = [0,0,34 ,255]
    ser.write(bytearray(outMessage))

def setLeds(add,num,r,g,b):
    ledMsg = [50,int(num),int(r), int(g),int(b) ]
    #print(ledMsg)
    slipOutPacket(bytearray(ledMsg))

dispatcher.map("/led", setLeds)

######################
#LOOP
######################

async def loop():
    debugVal = 0
    time.sleep(0.1)
    if SERIAL_ENABLE: ser.flushInput() 
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
    if SERIAL_ENABLE: ser.read(ser.in_waiting)
    await loop()
    transport.close()

asyncio.run(init_main())
