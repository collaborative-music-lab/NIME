# Testing the m370_communication.py script
# adds support for storing mappings in json files

RAW_INCOMING_SERIAL_MONITOR = 0
PACKET_INCOMING_SERIAL_MONITOR = 0   

CUR_PYTHON_SCRIPT = "370_commTest2"
    
import serial, serial.tools.list_ports, socket, sys, asyncio,struct,time, math
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher


import scripts.m370_communication as m370_communication
comms = m370_communication.communication("serial", baudrate = 115200, defaultport="/dev/tty.SLAB_USBtoUART")

import scripts.m370_mapping as mp 
#cmap = mp.loadMap('scripts/data_file.json')

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

######################
#SETUP OSC
######################
#initialize UDP client
client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
# dispatcher in charge of executing functions in response to RECEIVED OSC messages
dispatcher = Dispatcher()
print("Sending OSC to port", 5005, "on localhost")
client.send_message("/scriptName", CUR_PYTHON_SCRIPT)


def setOptoInterval(add, onInterval, offInterval):
    msg = [200,bytes(onInterval), bytes(offInterval)]
    comms.send(msg)

dispatcher.map("/optoInterval", setOptoInterval)

######################
#LOOP
######################

optoMin = [300,300,300,300,300,300]
optoMax = [1,1,1,1,1,1]
optoButton = [0,0,0,0,0,0]
optoMean = [500,500,500,500,500,500]

def processOpto(num,val):
    optoMean[num] = optoMean[num]*0.9 + val*0.1

    if optoMean[num] > optoMax[num]:
        optoMax[num]=optoMean[num]
    elif optoMean[num] < optoMin[num]:
        optoMin[num]=optoMean[num]

    outVal = (val-optoMin[num]/optoMax[num]-optoMin[num])

    outVal = outVal * (1000/optoMax[num])

    if (outVal < 500): optoMax[num] = optoMax[num]*0.999
    else :optoMin[num] = optoMin[num]*1.001

    button = optoschmitt(outVal,300, 500)
    #print("processopto", outVal, num, button)
    if button != optoButton[num] and button >=0:
        optoButton[num] = button
        processOptoButton(num)

    return [outVal/1000, optoButton[num]] 

def optoschmitt(val, low, high):
    if val < low: return 0
    elif val >high: return 1
    else: return -1 

pitches = [0,3,5,7,10]

def processOptoButton(num):
    client.send_message("/button", [num,optoButton[num]])

    if num < 4:
        outVal=0
        for i in range(4): 
            if optoButton[i]>0: 
                outVal += pow(2,i) #standard valve pitches

        #outVal = [0,1,2,3,4,5,6,7,8][outVal] #no remapping
        outVal = [0,1,3,2,7,6,4,5,15,14,12,13,8,9,11,10][outVal] #gray code
        #outVal = [0,1,2,3,4,5,6,7,8][outVal]
        #outVal = [0,1,2,3,4,5,6,7,8][outVal]

        print(outVal, pitches[outVal%len(pitches)], math.floor(outVal/len(pitches))*12)
        outVal = pitches[outVal%len(pitches)] + math.floor(outVal/len(pitches)) *12

        client.send_message("/pitch", outVal)
        #print(num, outVal)

#gray code:
# https://mathworld.wolfram.com/GrayCode.html
# gray  binary  pow2
# 0     0       0
# 1     1       1
# 2     11      3
# 3     10      2
# 4     110     6
# 5     111     7
# 6     101     5
# 7     100     4
# 8     1100    12
# 9     1101    13
# 10    1111    15
# 11    1110    14
# 12    1010    10
# 13    1011    11
# 14    1001    9
# 15    1000    8


async def loop():
    
    time.sleep(0.1)

    handshakeStatus = 1

    print("done setup")

    timerr = 0.0
    interval = 0.5 #in seconds
    testVal = 0

    while(1):   
        #numAvailableBytes = comms.available()
        while(comms.available()>0):
            #print("available: ", numAvailableBytes)
            currentMessage = comms.get() # can be None if nothing in input buffer
            #print("get", currentMessage)

            if currentMessage != None: 
                if 0: 
                    if 98 < currentMessage[0] < 106:
                        val = (currentMessage[1]<<8) + currentMessage[2] - (1<<15)
                        address = "/opto" 
                        curNum = [0,2,1,3,4,5][currentMessage[0]-99]
                        #print(currentMessage[0], curNum)
                        val, button = processOpto(curNum,val)
                        msg = [curNum, val,button]
                        client.send_message(address, msg)
                        #print("opto1", currentMessage[0], val)
                elif 1:
                    address = "/"
                    if currentMessage[0] == 50: address += "enc"
                    elif currentMessage[0] == 99: address += "hall"
                    elif currentMessage[0] == 100: address += "rotary"
                    elif currentMessage[0] == 101: address += "switch"
                    val = (currentMessage[1]<<8) + currentMessage[2] - (1<<15)
                    #print(address)
                    client.send_message(address, val)

                else:
                    print("rawinput", currentMessage)

        time.sleep(0.01)

async def init_main():
    server = AsyncIOOSCUDPServer(("127.0.0.1", 5006), dispatcher, asyncio.get_event_loop())
    
    transport, protocol = await server.create_serve_endpoint()

    #if SERIAL_ENABLE: ser.read(ser.in_waiting)
    await loop()
    transport.close()

asyncio.run(init_main())
