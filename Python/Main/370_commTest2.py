# Testing the m370_communication.py script

RAW_INCOMING_SERIAL_MONITOR = 0
PACKET_INCOMING_SERIAL_MONITOR = 0   

CUR_PYTHON_SCRIPT = "370_commTest2"
    
import serial, serial.tools.list_ports, socket, sys, asyncio,struct,time
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher


import scripts.m370_communication as m370_communication
comms = m370_communication.communication("serial", baudrate = 115200, defaultport="/dev/tty.usbserial-1430")
######################
# SET COMMUNICATION MODE
######################
# don't forget to set the ESP32 firmware to match!
SERIAL_ENABLE = 0
WIFI_ENABLE = 1 #!!!! READ FOLLOWING COMMENT
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

async def loop():
    
    time.sleep(0.1)

    handshakeStatus = 1
    while(1):
        while(comms.available()):
            #print("AVAIL", comms.available())
            #comms.send([handshakeStatus,0])
            currentMessage = comms.get()
            if currentMessage is None:
                pass
            elif len(currentMessage)==3:
                val = ((currentMessage[1]<<8) +  currentMessage[2]) - (1<<15)
                print( currentMessage )
                #print(currentMessage[0], abs(val))
                client.send_message("/analog/0", abs(val))
            else: 
                res = ''.join(map(chr, currentMessage) )
                print("ERROR", currentMessage)
            
                #print("waiting")
            # #else: print(currentMessage)
            # elif currentMessage[0] == 1:
            #     print("ESP32  found")
            #     handshakeStatus=2
            # elif currentMessage[0] == 2:
            #     print("Firmware name", currentMessage[1:].decode("utf-8"))
            #     client.send_message("/firmwareName", currentMessage[1:].decode("utf-8"))
            #     handshakeStatus=3
            # elif currentMessage[0] == 3:
            #     print("Firmware version", currentMessage[1:].decode("utf-8"))
            #     client.send_message("/firmwareVersion", currentMessage[1:].decode("utf-8"))
            #     handshakeStatus=4
            # elif currentMessage[0] == 4:
            #     print("Firmware author", currentMessage[1:].decode("utf-8"))
            #     client.send_message("/firmwareVersion", currentMessage[1:].decode("utf-8"))
            #     handshakeStatus=5
            # elif currentMessage[0] == 5:
            #     print("Firmware date", currentMessage[1:].decode("utf-8"))
            #     client.send_message("/firmwareVersion", currentMessage[1:].decode("utf-8"))
            #     handshakeStatus=6
            # elif currentMessage[0] == 6:
            #     print("Firmware notes", currentMessage[1:].decode("utf-8"))
            #     client.send_message("/firmwareVersion", currentMessage[1:].decode("utf-8"))
            #     handshakeStatus=7
            #     break;
            # else:
            #     print("looking for ESP32")
        time.sleep(0.002)
    print("done setup")

    print("done setup")

    while(1):   
        if comms.available():
            currentMessage = comms.get() # can be None if nothing in input buffer
            if currentMessage != None: print(currentMessage)
        #interpretMessage(currentMessage)
        #sendSerialBuffer()
        #await asyncio.sleep(0)

        time.sleep(0.01)

async def init_main():
    server = AsyncIOOSCUDPServer(("127.0.0.1", 5006), dispatcher, asyncio.get_event_loop())
    
    transport, protocol = await server.create_serve_endpoint()

    #if SERIAL_ENABLE: ser.read(ser.in_waiting)
    await loop()
    transport.close()

asyncio.run(init_main())
