    # 370_PRIMARY.py
# Ian Hattwick with Fred Kelly
# This file created Feb 15 2021

import socket, sys
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio
import struct
import time 

#number of minutes after which python script will automatically
#cancel itself if it hasn't received an OSC message
class Timeout: 
    _interval = 5
    _prevTime = 0
    _unit = 60 # timeout = interval*unit seconds
    _counter = 0
    
    def __init__(self,interval):
      """ Sets the timeout period"""
      _interval = interval

    def check(self):
        if time.perf_counter() - self._counter > self._interval * self._unit:
            #cancel this script
            #print("cancelled script")
            return 1
        return 1

    def update(self):
        self._counter = time.perf_counter()

    def cancel(self):
        self._counter = 0

t = Timeout(5)

######################
#SETUP OSC
######################
#initialize UDP client
client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
# dispatcher in charge of executing functions in response to RECEIVED OSC messages
dispatcher = Dispatcher()
print("Sending data to port", 5005)
  
#sequence is in scale degrees
sequences = [
[0,1,2,3,4,5,6,7],
[2,0,3,1,4,2,5,3],
[0,4,7,11,14,18,14,7],
[0,2,4,7,1,3,5,8]
]

decayTime = [20,50, 90,127]

def GetSequence(add, num):
    t.update() #reset timeout 
    global sequences

    textNum = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT']

    if num < len(sequences):
        val = sequences[int(num)]
    else:
        print("sequence number out of range")
        return 0

    for i in range(len(val)):
        sendOSC('8steps', 1, textNum[i], (val[i]/27)*127)
        print("sent", '8steps', textNum[i], (val[i]/27)*127, 1)
        #Sequence

    sendOSC('decay', 1, 'D', decayTime[int(num)])

def mirror(add, val):
    t.update() #reset timeout 
    print(add, val)
    client.send_message(add, val)

def cancelScript():
    t.cancel() #reset timeout 

#look for incoming OSC messages
dispatcher.map("/getSequence", GetSequence)
dispatcher.map("/paramName", mirror)
dispatcher.map("/cancel", cancelScript)

def sendOSC(module, instance, param, val):
    client.send_message('/module', module)
    msg = [param, val, instance]
    client.send_message('/param', msg)


######################
#LOOP
######################

async def loop():
    debugVal = 0
    time.sleep(0.1)
    
    while(t.check()):
        await asyncio.sleep(0)
        time.sleep(0.001)

async def init_main():
    server = AsyncIOOSCUDPServer(("127.0.0.1", 5006), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    await loop()
    transport.close()

asyncio.run(init_main())
