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
  
#sequence can range from MIDI notes 48 to 76
sequences = [
[60, 62,64,65,67,69,71,72],
[62,63,65,67,71,69,65,64],
[36,43,48,55,60,67,72,79] #goes below 48
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

dispatcher.map("/getSequence", GetSequence)

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
