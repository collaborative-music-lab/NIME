# keySynth.py
# Ian Hattwick
# This file created Mar 2

import socket, sys
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio
import struct
import time 
from pynput.mouse import Button, Controller

mouse = Controller()

######################
#CONFIGURE TIMEOUT
######################
#number of minutes after which python script will automatically
#cancel itself if it hasn't received an OSC message
class Timeout: 
    _interval = 5
    _unit = 60 # timeout = (interval*unit) seconds
    _counter = 0
    _cancel = 0
    
    def __init__(self,interval):
      """ Sets the timeout period"""
      _interval = interval

    def check(self):
        if time.perf_counter() - self._counter > self._interval * self._unit:
            #cancel this script
            print("cancelled script")
            return 0
        if self._cancel == 1:
            print("cancelled script")
            return 0
        return 1

    def update(self):
        self._counter = time.perf_counter()

    def cancel(self):
        self._cancel = 1

t = Timeout(5) # argument is number of minutes after which script will cancel itself

#you can also cancel the script by calling t.cancel()
# sending an OSC "/cancel" message

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
bitwiseKeyMapping = [0,0,0,0]

pitchSequence = [
[7,4,7,10,11,10,8,4],
[7,10,8,11,9,12,11,8],
[8,8,10,10,11,11,9,8],
[12,11,10,9,11,10,9,8]
]

def keyDown(*args):
    t.update() #reset timeout

    #in this example, key is getting info from the pd keyGrid object, which
    #always sends keypresses in (column,row) format
    #- also remember the first argument sent to an OSC callback is the address
    # so this function gets the arguments <address><col><row>
    
    #print(args)
    
    col = int(args[1])
    row = int(args[2])
    
    if row == 0:
        #maps bottom row of keyboard to pitches
        address = '/pitch'
        myScale = [60,63,65,67,70,72,75,77,79,82,84]
        val = myScale[int(col)]
        client.send_message(address, val/127) #CV pitch in automatonism is 0-1
        print(address,val)

    if row == 1:
        #maps a,s,d,f to polysynth release time
        if 0 <= col < 4:
            calcBitMap(col,1)

    if row == 2:
        #maps q,w,e,r to new pitch sequences
        if 0<= col < 4:
            client.send_message("/module", "8steps")
            vals = pitchSequence[col]
            textNum = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT']
            for i in range(len(vals)):
                msg = [textNum[i],vals[i]/28*127,1]
                client.send_message("/param", msg)



def keyUp(*args):
    t.update() #reset timeout
    #handles when keys are released
    #print(args)
    
    col = int(args[1])
    row = int(args[2])

    if row == 1:
        if 0 <= col < 4:
            calcBitMap(col,0)
            

def calcBitMap(col,state):
    #creates a bitwise grouping of a,s,d,f keys to control release time
    global bitwiseKeyMapping
    bitwiseKeyMapping[col] = state

    sum=0
    for i in range(4):
        sum = sum + bitwiseKeyMapping[i]*pow(2,i)
    #print(sum) 

    client.send_message('/module', 'polysynth')
    address = '/param'  
    msg = ['RELEASE', sum*5 + 5, 1]
    client.send_message(address, msg)

def cancelScript(*args):
    print("cancel")
    t.cancel()

#look for incoming OSC messages
#map(OSC address to match, function to call when address is received)
dispatcher.map("/keydown", keyDown) 
dispatcher.map("/keyup", keyUp) 
dispatcher.map("/cancel", cancelScript) 

######################
#Track mouse movements
######################

class leakyIntegrator:
    #keeps a bucket of all input values
    #adds current input value to the bucket
    #scales the bucket by a fixed leak factor
    bucket = 0
    leakFactor = 0.1

    def update(self, input):
        self.bucket = self.bucket + input
        self.bucket = self.bucket * (1-self.leakFactor)

        if self.bucket < 1: self.bucket = 0
        return self.bucket

class OnePole:
    #simple one pole lowpass filter
    prev = 0
    output = 0
    factor = 0.9

    def __init__(self, factor):
        self.factor = factor

    def update(self,input):
        self.output = self.prev*self.factor + input*(1-self.factor)
        self.prev=self.output
        return self.output

leaky = leakyIntegrator()
leaky.leakFactor = 0.1

cutoff = OnePole(0.9)
vca = OnePole(0.5)
timbre = OnePole(0.9)

#global variables to remember previous values
prevMousePosition = mouse.position
    
def updateMouse(position):
    global prevMousePosition
    #print(position)

    #calculate average magnitude of mouse movement using a leaky integrator
    magnitude = pow(pow(position[0]-prevMousePosition[0],2) + pow(position[1]-prevMousePosition[1],2),0.5)
    prevMousePosition = position
    magnitude = leaky.update(magnitude)
    #print(magnitude)

    outVal = clip(magnitude/10,0,127)
    #print (outVal)
    client.send_message('/module', 'vca')
    msg = ['VCA', vca.update(outVal), 2]
    client.send_message('/param', msg)

    #use X position of mouse to control filter cutoff
    #print(position[0])
    val = pow(position[0]/1600,2) #normalize to 0-1 and make exponential
    outVal = clip(val*100+2 ,0,127)
    #print (outVal)
    client.send_message('/module', 'bob-filter')
    msg = ['CUTOFF', cutoff.update(outVal), 1]
    client.send_message('/param', msg)

    #use Y position of mouse to control oscillator shape
    #print(position[1])
    val = pow(position[1]/1050,1) #normalize to 0-1 and keep linear
    
    outVal = clip(timbre.update(val)*127 ,0,127)
    #print (outVal)
    client.send_message('/module', 'polysynth')
    msg = ['SAW->PULSE', outVal, 1]
    client.send_message('/param', msg)


def clip(input,min,max):
    outVal = input
    if input < min: outVal = min
    elif input > max: outVal = max
    return outVal

######################
#LOOP
######################

async def loop():
    debugVal = 0
    time.sleep(0.1)
    
    while(t.check()):
        updateMouse(mouse.position)
        await asyncio.sleep(0)
        time.sleep(0.1) #latency in seconds

async def init_main():
    server = AsyncIOOSCUDPServer(("127.0.0.1", 5006), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    await loop()
    transport.close()

asyncio.run(init_main())

