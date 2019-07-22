import serial, serial.tools.list_ports, socket, sys
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio

# input message id's from Teensy
ROW_0_STATES_ID = 0
ROW_1_STATES_ID = 1
ROW_2_STATES_ID = 2
ROW_3_STATES_ID = 3
BUTTON_DOWN_ID = 4
BUTTON_UP_ID = 5

# output message id's to Teensy
UPDATE_LED_ID = 0

endByte = bytes([255])
escByte = bytes([254])

ledMsg = bytes() # message byte format: [Message Id][Pixel Number][Red Val][Green Val][Blue Val]

# sending button states and presses to PD
def deslipToPd():
    bytesTotal = bytes()
    escFlag = False
    curByte = bytes()

    while (ser.in_waiting):
        curByte = ser.read()
        if (escFlag):
            bytesTotal += curByte
            escFlag = False
        elif (curByte == endByte):
            processAndSend(bytesTotal)
            break
        elif (curByte == escByte):
            escFlag = True
        else:
            bytesTotal += curByte

def slipToTeensy(msg):
    print("incoming message")
    print(msg)
    outBuf = bytes()
    for b in msg:
        if (b == endByte[0] or b == escByte[0]):
            outBuf += escByte
        outBuf += bytes([b])
    outBuf += endByte
    print("slip encoded message")
    print(outBuf)
    ser.write(outBuf)

def processRow(row):
    # convert bytes object to 4-bit string
    rowStr = "{0:04b}".format(int.from_bytes(row, 'big'))
    return rowStr[::-1] # reverse string for readability in PD

def processBtn(btn):
    return int.from_bytes(btn, "big")

def processAndSend(messageBytes):
    # print(messageBytes);
    # based on the first byte, determine address of message
    address = addresses.get(messageBytes[0])
    # process byte with different functions based on the type of data
    value = functionMap.get(messageBytes[0])(messageBytes[1:])
    client.send_message(address, value)

# always know order of OSC messages is: pixel -> red -> green -> blue
def pixelHandler(address, *osc_args):
    global ledMsg
    ledMsg = bytes() # clear old message
    val = int(osc_args[0])
    pixel = min(val, 16)
    ledMsg += bytes([UPDATE_LED_ID])
    ledMsg += bytes([pixel])

def redHandler(address, *osc_args):
    global ledMsg
    val = int(osc_args[0])
    red = min(val, 255)
    ledMsg += bytes([red])

def greenHandler(address, *osc_args):
    global ledMsg
    val = int(osc_args[0])
    green = min(val, 255)
    ledMsg += bytes([green])

def blueHandler(address, *osc_args):
    global ledMsg
    val = int(osc_args[0])
    blue = min(val, 255)
    ledMsg += bytes([blue])
    slipToTeensy(ledMsg)


addresses = {
    ROW_0_STATES_ID: "/row0",
    ROW_1_STATES_ID: "/row1",
    ROW_2_STATES_ID: "/row2",
    ROW_3_STATES_ID: "/row3",
    BUTTON_DOWN_ID: "/button_down",
    BUTTON_UP_ID: "/button_up"
}

functionMap = {
    ROW_0_STATES_ID: processRow,
    ROW_1_STATES_ID: processRow,
    ROW_2_STATES_ID: processRow,
    ROW_3_STATES_ID: processRow,
    BUTTON_DOWN_ID: processBtn,
    BUTTON_UP_ID: processBtn
}

ports = list(serial.tools.list_ports.comports())

for port in ports:
    if ("USB Serial" in port.description):
        ser = serial.Serial(port.device)
        ser.baudrate=57600

client = udp_client.SimpleUDPClient("127.0.0.1", 5005)

dispatcher = Dispatcher()
dispatcher.map("/pixel", pixelHandler)
dispatcher.map("/red", redHandler)
dispatcher.map("/green", greenHandler)
dispatcher.map("/blue", blueHandler)

async def loop():
    while(1):
        deslipToPd()
        await asyncio.sleep(0)

async def init_main():
    server = AsyncIOOSCUDPServer(("127.0.0.1", 5006), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    await loop()
    transport.close()


asyncio.run(init_main())
# while(1):
    # deslipToPd()
