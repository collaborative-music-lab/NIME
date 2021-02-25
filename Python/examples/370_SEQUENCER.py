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
[1,3,5,6,7,6,5,4]
]

def GetSequence(add, num):
    global sequences

    address = '/sequence'

    if num < len(sequences):
        val = sequences[int(num)]
    else:
        print("sequence number out of range")
        return 0

    client.send_message(address, val)
    print("sent")

def GetSequence2(add, num):
    global sequences

    address = '/sequence2'

    if num < len(sequences):
        val = sequences[int(num)]
    else:
        print("sequence number out of range")
        return 0

    outputMsg = ['ONE', 0, 1]

    textNum = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT']

    for i in range(len(val)):
        outputMsg[0] = textNum[i]
        outputMsg[1] = (val[i]/27)*127

        client.send_message(address, outputMsg)
        print("sent", address, outputMsg)

#look for incoming OSC messages
dispatcher.map("/getSequence", GetSequence2)

######################
#LOOP
######################

async def loop():
    debugVal = 0
    time.sleep(0.1)
    
    while(1):
        await asyncio.sleep(0)
        time.sleep(0.001)

async def init_main():
    server = AsyncIOOSCUDPServer(("127.0.0.1", 5006), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    await loop()
    transport.close()

asyncio.run(init_main())
