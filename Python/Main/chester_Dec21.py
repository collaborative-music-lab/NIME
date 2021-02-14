# Testing the m370_communication.py script
# adds support for storing mappings in json files

RAW_INCOMING_SERIAL_MONITOR = 0
PACKET_INCOMING_SERIAL_MONITOR = 0 

CUR_PYTHON_SCRIPT = "chester_dec21"
    
import serial, serial.tools.list_ports, socket, sys, asyncio,struct,time, math
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher

#m370 python modules
import scripts.m370_communication as m370_communication
import sensorInterfaces.pitchMappings as pitchMappings
import sensorInterfaces.imuProcessing as imuProcessing

comms = m370_communication.communication("serial", baudrate = 115200, defaultport="/dev/tty.SLAB_USBtoUART")
mono = pitchMappings.MonoPitch(5)
imu = imuProcessing.ThreeAxis()

#import scripts.m370_mapping as mp 

import valveMap1 as valve

#cmap = mp.loadMap('scripts/data_file.json')

######################
# SET COMMUNICATION MODE
######################
SERIAL_ENABLE = 1
WIFI_ENABLE = 0 

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

async def loop():
    
    time.sleep(0.1)
    handshakeStatus = 1
    print("done setup")

    for i in range(4):
        msg = [100,i*30+10]
        comms.send(msg)
        time.sleep(0.1)

    while(1):
        while(comms.available()>0):
            #print("available: ", numAvailableBytes)
            currentMessage = comms.get() # can be None if nothing in input buffer
            #print("get", currentMessage)

            #valveMap.mapName("default")

            if currentMessage != None: 
                if PACKET_INCOMING_SERIAL_MONITOR == 0:
                    valve.input(client, currentMessage)
                else:
                    print("rawinput", currentMessage)

    while(0):   
        while(comms.available()>0):
            #print("available: ", numAvailableBytes)
            currentMessage = comms.get() # can be None if nothing in input buffer
            #print("get", currentMessage)

            #valveMap.mapName("default")

            if currentMessage != None: 
                if PACKET_INCOMING_SERIAL_MONITOR == 0:
                    address = currentMessage[0]

                    if 0 <= address <= 5:
                        buttonNums = {
                            50:0, 53:1, 52:2, 51: 3
                        }
                        address = "/hall/" + str(address)
                        val = (currentMessage[1]<<8) + currentMessage[2] - 32768
                        client.send_message(address, val) 
                    elif 10 <= address <= 15:
                        address = "/sw/" + str(address-10)
                        val = currentMessage[1];
                        client.send_message(address, val)

                        address = "/pitch"
                        note,velocity = mono.input(currentMessage[0]-10,val)
                        if note > 0 : client.send_message(address, [note,velocity])
                    elif 20 <= address <= 25:
                        address = "/enc/" + str(address-20)
                        #val = (currentMessage[1]<<8) + currentMessage[2]- 32768
                        #print("enc", currentMessage)
                        val = (currentMessage[1]) 
                        client.send_message(address, val)
                    elif 100 <= address <= 102:
                        axis = address-100
                        val = (currentMessage[1]<<8) + currentMessage[2]- 32768
                        imu.in1(axis,val/32768)

                        if axis == 2:
                            address = "/imu/tilt"
                            x,y,z = imu.tilt(0,0,2)
                            client.send_message(address, [x,y,z])
                            client.send_message("/imu/magnitude", imu.magnitude())
                    #else: return
                    #print(address)
                    #address, val = valveMap.input(address, val)
                    #client.send_message(address, val)

                else:
                    print("rawinput", currentMessage)

        time.sleep(0.01)

async def init_main():
    server = AsyncIOOSCUDPServer(("127.0.0.1", 5006), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    await loop()
    transport.close()

asyncio.run(init_main())
