# Testing the m370_communication.py script
# adds support for storing mappings in json files

RAW_INCOMING_SERIAL_MONITOR = 0
PACKET_INCOMING_SERIAL_MONITOR = 1  

CUR_PYTHON_SCRIPT = "370_commTest2"
    
import serial, serial.tools.list_ports, socket, sys, asyncio,struct,time, math
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
 

import scripts.m370_communication as m370_communication
comms = m370_communication.communication("serial", baudrate = 115200, defaultport="/dev/tty.SLAB_USBtoUART")



######################
# SET COMMUNICATION MODE
######################
# don't forget to set the ESP32 firmware to match!
#SERIAL_ENABLE = 1
#WIFI_ENABLE = 0 #!!!! READ FOLLOWING COMMENT
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


######################
#LOOP
######################




async def loop():
    
    time.sleep(0.01)
    handshakeStatus = 1
    print("done setup")

    while(1):   
        while(comms.available()>0):
            #print("available: ", numAvailableBytes)
            currentMessage = comms.get() # can be None if nothing in input buffer
            
            if currentMessage != None: 
                if PACKET_INCOMING_SERIAL_MONITOR == 0:
                    address = currentMessage[0]

                else:
                    print("rawinput", currentMessage)

        time.sleep(0.01)    

async def init_main():
    server = AsyncIOOSCUDPServer(("127.0.0.1", 5006), dispatcher, asyncio.get_event_loop())
    
    transport, protocol = await server.create_serve_endpoint()
    await loop()
    transport.close()

asyncio.run(init_main())
