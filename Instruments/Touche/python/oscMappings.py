import math, time
global dispatcher
from sensorInterfaces.m370_sensor import sensor as sensor 

import math

class Touche:
    def __init__(self, in_min, in_max, out_min, out_max, curve):
        self.in_min = in_min
        self.in_max = in_max
        self.out_min = out_min
        self.out_max = out_max
        self.curve = curve
        self.prev = 0

    def scale(self, input_val):
        if self.in_max == self.in_min:
            return self.out_min  # Avoid division by zero

        # Normalize input_val to range 0-1
        normalized_val = (input_val - self.in_min) / (self.in_max - self.in_min)
        normalized_val = max(0, min(1, normalized_val))  # Ensure value is within [0, 1]

        # Apply exponential scaling
        scaled_val = (normalized_val ** self.curve) * (self.out_max - self.out_min) + self.out_min

        # Ensure scaled_val is within [out_min, out_max]
        scaled_val = max(self.out_min, min(self.out_max, scaled_val))

        # Apply one-pole filter if necessary
        if normalized_val < 0.5:
            scaled_val = self.one_pole(scaled_val, 1 - normalized_val)
        else:
            scaled_val = self.one_pole(scaled_val, 0.0)

        print(input_val, "\t", scaled_val, "\t",  normalized_val)
        return math.floor(scaled_val)

    def one_pole(self, input_val, alpha):
        return self.prev * alpha + input_val * (1 - alpha)


touche = Touche(400,1000,0,127,.75)

######################
#INCOMING OSC
# handle messages sent from PD
######################
def defineOscHandlers():
	dispatcher.map("/min", setMin)
	dispatcher.map("/max", setMax)
	dispatcher.map("/curve", setCurve)
	dispatcher.map("/clock", clock)

def setMin(add,val):
	touche.in_min = val

def setMax(add,val):
	touche.in_max = val

def setCurve(add,val):
	touche.curve = val


def clock(*args):
	global eucClock, synthProgramEnable, synthNewNote, synthClock, synthRange, synthClockDivider, prevTime
	t.update() #reset timeout
	curBeat = args[2]%16 #clock is just an ascending integer
	
	#drum sequencers
	euclidTrigger = []
	for i in range(3):
		euclidTrigger.append( euc[i].get(math.floor(eucClock[i] / eucDivisor[i])) )
		if switch[i].val > 0 and monitorEuclidPatterns is 1: print(eucClock[i] , euc[i].pattern)
		eucClock[i] += 1
		if eucClock[i] >= 16/eucDivisor[i]: 
			eucClock[i] = 0 
	
	for i in range(3):	
		# if i == 1: print('trig', i, eucClock[i], eucDivisor[i], switch[i].val)
		if euclidTrigger[i]>0 and switch[i].val > 0:
			#if i == 1: print('trig', curBeat, i, eucClock[i], eucDivisor[i], switch[i].val)
			client.send_message("/trigger", i*2)
			toneTrigger = i*2-1
			if toneTrigger < 0: toneTrigger = 5
			client.send_message("/trigger", toneTrigger)


	#synth
	if curBeat % synthClockDivider == 0: #synth clock is divided by N
		if synthProgramEnable == 1:
			setSynthSeqStep(synthClock,pot[0].val)
			setSynthRange(synthClock * (4095/16) 	)
			client.send_message("/trigger", 6)
			synthClock += 1
			if synthClock >= 16: synthClock = 0
		elif synthNewNote == 1:
			client.send_message("/trigger", 6)
			#print("synth trig", synthNewNote)
			synthNewNote = 0
			
synthDetune = 0
synthPitches = [24,0,12,-12] #basePitch, offset1, offset2, sub

def setPitch(add, num, val):
	pitchshift = [0,4,7,12,24]
	index = math.floor(val)

	if num == 0:
		newVal = math.floor(val/5)+19
		if newVal != synthPitches[0]:
			synthPitches[0] = newVal
	
	elif num == 1: synthPitches[1] = pitchshift[index]
	elif num == 2: synthPitches[2] = pitchshift[index]
	elif num == 3: synthPitches[3] = (val-2) * -12

	updatePitches()

def setDetune(add,val): 
	global synthDetune
	synthDetune = math.pow(val/127,3)/12
	updatePitches()

def updatePitches():
	sendOSC("bwl-osc", 1, "PITCH", synthPitches[0] - synthPitches[3]) #sub
	sendOSC("bwl-osc", 2, "PITCH", synthPitches[0]) #main osc
	sendOSC("bwl-osc", 3, "PITCH", synthPitches[1]+synthPitches[0] + synthPitches[0]*synthDetune)
	sendOSC("basic-osc", 2, "PITCH", synthPitches[2]+synthPitches[0] - synthPitches[0]*synthDetune)
	#print("pitches", synthPitches, synthPitches[1]+synthPitches[0] + synthDetune*synthPitches[0], synthPitches[0],synthDetune)

def setEnableSynthSequence(add,val):
	global enableSynthSequence
	enableSynthSequence = val>0

def setSynthAmpSense(*args):
	global potAmpGain, potAmpLeak
	potAmpGain = math.pow(args[1]/127,1.25)*20 + 0.5
	synthAmpLeak.leakFactor = 0.5 - math.pow(args[2]/127,0.5)/2 + 0.001

potAmpGain = 4

######################
#SENSOR MAPPINGS
#handle data received from interface
######################

def mapSensor(add, val):
	global synthNewNote, synthProgramEnable, synthClock

	if add == "/pot0":
		sendOSC("vca",1,"VCA",math.floor(touche.scale(val)))
		client.send_message("/cap0", val/1)
		return 0
	
######################
#Helper functions
######################

def sendOSC(module, instance, param, val):
	client.send_message('/module', module)
	msg = [param, val, instance]
	client.send_message('/param', msg)


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

synthAmpLeak = leakyIntegrator()
synthAmpLeak.leakFactor = 0.025

