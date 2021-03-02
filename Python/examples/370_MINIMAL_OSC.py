# 370_PRIMARY.py
# Ian Hattwick with Fred Kelly
# This file created Mar 2 2021

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


######################
#OSC MESSAGES
######################
def mirror(*args) -> None:
    address = args[0] #the osc address is always the first element

    arg_list = list(args) #convert tuple to lists as tuples are immutable

    arg_list.pop(0) # remove first element (the address)

    vals = arg_list #now the list only contains the values without the address

    print(address, vals)

    client.send_message(address, vals)

#look for incoming OSC messages
dispatcher.map("/mirror", mirror)

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
