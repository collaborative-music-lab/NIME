#Touche.py
#Ian Hattwick
#Apr 19, 2024

#uncommet to see the raw packets coming from the ESP32
# - a quick way to make sure serial communication is working
PACKET_INCOMING_SERIAL_MONITOR = 0

CUR_PYTHON_SCRIPT = "Touche.py"
    
import serial, serial.tools.list_ports, socket, sys, asyncio,struct,time, math
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher

#m370 python modules
import scripts.m370_communication as m370_communication
#you can change the defaultport to the name your PC gives to the ESP32 serial port
comms = m370_communication.communication("serial", baudrate = 115200, defaultport="/dev/tty.SLAB_USBtoUART")

######################
# SET COMMUNICATION MODE
######################
SERIAL_ENABLE = 1
WIFI_ENABLE = 0 

####################
####################
#you don't want to change anything below this point
####################
####################

#the oscMappings and sensorInput files are loaded as osc and sensor
import sensorInput as sensor
import oscMappings as osc

osc.comms = comms
import scripts.timeout as timeout
t = timeout.Timeout(5)
osc.t = t

######################
#SETUP OSC
######################
#initialize UDP client
client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
osc.client = client
# dispatcher in charge of executing functions in response to RECEIVED OSC messages
dispatcher = Dispatcher()
osc.dispatcher = dispatcher

print("Sending OSC to port", 5005, "on localhost")
client.send_message("/scriptName", CUR_PYTHON_SCRIPT)
osc.defineOscHandlers()

#timeout handlers
def updateTimeout(): t.update() #reset timeout
dispatcher.map("/tick", updateTimeout)

def cancelScript(*args): t.cancel()
dispatcher.map("/cancel", cancelScript)

def unknown_OSC(*args): print("unknown OSC message: ", args)
dispatcher.set_default_handler(unknown_OSC)

######################
#LOOP
######################

async def loop():
         
    time.sleep(0.1)
    handshakeStatus = 1 
    print("done setup")
    client.send_message("/init", 0)

    while(t.check()): 
        #t.check checks if timeout has triggered to cancel script
        await asyncio.sleep(0) #listen for OSC
        #print(comms.available())

        while(comms.available() > 0):
            currentMessage = comms.get() # can be None if nothing in input buffer
            
            if currentMessage != None: 
                if PACKET_INCOMING_SERIAL_MONITOR == 0:
                    if 2 < len(currentMessage) < 16:
                        address, value = sensor.processInput(currentMessage)
                        osc.mapSensor(address,value) #send data for mapping
                        #client.send_message(address,value) #monitor data in PD

                else:
                    print("packet", currentMessage) #only for unrecognized input

        time.sleep(0.001) 


async def init_main():
    server = AsyncIOOSCUDPServer(("127.0.0.1", 5006), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    await loop()
    transport.close()

asyncio.run(init_main())
