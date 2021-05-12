#currentFrameworkLED.py
#Ian Hattwick   
#April 17, 2021

#demonstrates controlling WS2811 or similar LEDs connected to the ESP32
# look in oscMappings.py lines 135 & 759

PACKET_INCOMING_SERIAL_MONITOR = 0
MIDI_ENABLE = 0

CUR_PYTHON_SCRIPT = "currentFrameworkLED.py"
    
import serial, serial.tools.list_ports, socket, sys, asyncio,struct,time, math
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher

#m370 python modules 
import scripts.m370_communication as m370_communication

#for wifi
comms = m370_communication.communication("wifi")

#comms = m370_communication.communication("serial", baudrate = 115200, defaultport="/dev/tty.usbserial-1410")
import scripts.timeout as timeout
#you can change the defaultport to the name your PC gives to the ESP32 serial port


#####midi input######
if MIDI_ENABLE:
    import scripts.midi as midi
    midi.probePorts()
    midi_input = midi.input(0)


##########

import sensorInput as sensor
import oscMappings as osc
osc.comms = comms   

t = timeout.Timeout(5)
osc.t = t 


######################
#SETUP osc
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

    ledNum = 0

    while(t.check()): 
        #t.check checks if timeout has triggered to cancel script
        await asyncio.sleep(0) #listen for OSC 



        while(comms.available() > 0):

            await asyncio.sleep(0) #listen for OSC
            currentMessage = comms.get() # can be None if nothing in input buffer
            
            if currentMessage != None: 
                if PACKET_INCOMING_SERIAL_MONITOR == 0:
                    if 2 < len(currentMessage) < 16:
                        #print("packet3", currentMessage)
                        address, value = sensor.processInput(currentMessage)
                        # if address is not "/acc0" or "/gyro0":
                        #     print(address, value)
                        osc.mapSensor(address,value)
                        client.send_message(address,value)

                else:
                    print("packet", currentMessage)

            
                

            if MIDI_ENABLE:
                msg = midi_input.available()
                if msg is not None: 
                    address, value = sensor.processMidi(msg)
                    if PACKET_INCOMING_SERIAL_MONITOR == 1: print(address, value)
                    osc.mapSensor(address,value)


        if MIDI_ENABLE:
            msg = midi_input.available()
            if msg is not None: address, value = sensor.processMidi(msg)

        time.sleep(0.001) 



async def init_main():
    serverOSC = AsyncIOOSCUDPServer(("127.0.0.1", 5006), dispatcher, asyncio.get_event_loop())
    transport, protocol = await serverOSC.create_serve_endpoint()
    await loop()
    transport.close()

asyncio.run(init_main())
