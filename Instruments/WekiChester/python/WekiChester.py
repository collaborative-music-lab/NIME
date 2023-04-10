#WekiChester.py
#Ian Hattwick   
#April 7, 2023

PACKET_INCOMING_SERIAL_MONITOR = 0

CUR_PYTHON_SCRIPT = "WekiChester.py"
    
import serial, serial.tools.list_ports, socket, sys, asyncio,struct,time, math
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher

#m370 python modules

import scripts.m370_communication as m370_communication
#comms = m370_communication.communication("serial", baudrate = 115200, defaultport="/dev/tty.SLAB_USBtoUART")
comms = m370_communication.communication("wifi", SSID="Solaris", ESP_IP="192.168.4.1", port=1236)
#NOTE: you can find your ESP_IP by looking at the serial monitor if you are still connected via SUB
#if you are using your ESP as an Access Pioint (AP) it should be 192.168.4.1
#ports are defined in pairs, where the port defined here is where python listens
# and the port python sends to is port+1

import scripts.timeout as timeout
#you can change the defaultport to the name your PC gives to the ESP32 serial port

import sensorInput as sensor
import oscMappings as osc
osc.comms = comms   

t = timeout.Timeout(5)
osc.t = t

######################
#SETUP osc
######################
#initialize OSC for wekinator
weki = udp_client.SimpleUDPClient("127.0.0.1", 6448)
osc.weki = weki

#initialize OSC client for PD
client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
osc.client = client

# dispatcher in charge of executing functions in response to 
# RECEIVED OSC messages from either weki or PD
dispatcher = Dispatcher()
osc.dispatcher = dispatcher

print("Sending OSC to PD on port", 5005, "on localhost")
client.send_message("/scriptName", CUR_PYTHON_SCRIPT)
osc.defineOscHandlers()

    
#timeout defineOscHandlers
def updateTimeout(*args): t.update() #reset timeout
dispatcher.map("/tick", updateTimeout)

def cancelScript(*args): t.cancel()
dispatcher.map("/cancel", cancelScript)

def unknown_OSC(*args): print("unknown OSC message: ", args)
dispatcher.set_default_handler(unknown_OSC)

####################
#LOOPumjumj
######################

async def loop():
         
    time.sleep(0.1)
    handshakeStatus = 1 
    print("done setup")
    osc.initSynthParams()
    client.send_message("/init", 0)

    while(t.check()): 
        #t.check checks if timeout has triggered to cancel script
        await asyncio.sleep(0) #listen for OSC

        if(comms.available() > 0):
            currentMessage = comms.get() # can be None if nothing in input buffer
            
            if currentMessage != None: 
                if PACKET_INCOMING_SERIAL_MONITOR == 0:
                    address, value = sensor.processInput(currentMessage)
                    #print(address, value)
                    osc.mapSensor(address,value)
                    #client.send_message(address,value)

                else:
                    print("packet", currentMessage)

        # if(comms2.available() > 0):
        #     currentMessage = comms2.get() # can be None if nothing in input buffer
            
        #     if currentMessage != None: 
        #         if PACKET_INCOMING_SERIAL_MONITOR == 0:
        #             address, value = sensor.processInput(currentMessage)
        #             #print(address, value)
        #             osc.mapSensor(address,value)
        #             #client.send_message(address,value)

        #         else:
        #             print("packet2", currentMessage)

        time.sleep(0.001) 


async def init_main():
    server = AsyncIOOSCUDPServer(("127.0.0.1", 5006), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    await loop()
    transport.close()

asyncio.run(init_main())
