import math, time
global dispatcher
from sensorInterfaces.m370_sensor import sensor as sensor 
from scripts.euclideanSequencer import Euclid as euclid

#########
#EUCLIDIAN SEQUENCER
#########
# the code for this is in scripts/euclideanSequencer
eucDivisor = [1,1,1]
eucClock = [0,0,0]
euc = []
#euclid parameters are number of beats, number of hits, rotation
euc.append( euclid(16,16,0)) #bass drum
euc.append( euclid(16,16,0)) # snare
euc.append( euclid(16,16,0)) #hihat

monitorEuclidPatterns = 0

#########
#SYNTH AND SEQUENCER
#########
synthClock = 0
synthRange = 0
synthProgramEnable = 0
synthNewNote = 0
synthClockDivider = 2

######################
#INCOMING OSC
# handle messages sent from PD
######################
def defineOscHandlers():
	dispatcher.map("/clock", clock)
	dispatcher.map("/setPitch", setPitch)
	dispatcher.map("/synthDetune", setDetune)


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

#Store potentiometer data and only process when the potentiometer is moved
#the sensor class code is in sensorInterfaces/m370_sensor
#but you don't need to change anything in it
#the code below shows how to use it
pot = []
for i in range(4):
	pot.append( sensor(0, 10) ) #initial value, changeThreshold

#change threshold for synth range pot
pot[0].changeThreshold = 50

switch = []
for i in range(4):
	switch.append( sensor(0) )

def mapSensor(add, val):
	global synthNewNote, synthProgramEnable, synthClock

	if add == "/sw0": 
		if switch[0].new(val) == 1: #sensor.new lets us know if there is new data
			eucClock[0] = 0
	elif add == "/sw1": 
		if switch[1].new(val) == 1:
			eucClock[1] = 0
	elif add == "/sw2": 
		if switch[2].new(val) == 1:
			eucClock[2] = 0
	elif add == "/sw3": 
		if switch[3].new(val) is not None:
			#print("sw3", val)
			pass
		
	#pots to control drum values
	if add == "/pot2":
		"""set drum tone"""
		if pot[2].new(val) is not None:
			if switch[3].val > 0:
				for i in range(3): 
					if switch[i].val > 0:
						drumTone(i,val)
	elif add == "/pot1":
		"""set drum pattern"""
		#print( pot[0].new(val) )
		if pot[1].new(val) is not None:
			if switch[3].val > 0:
				for i in range(3): 
					if switch[i].val > 0:
						drumPattern(i,val)
	elif add == "/pot0":
		"""set synth pitch and trigger"""
		#print(pot[0].val, pot[0].changeThreshold, pot[1].changeThreshold)
		if pot[0].new(val) is not None:
			if switch[3].val > 0 and synthProgramEnable == 0:
				synthClock = 0
				synthProgramEnable = 1
			elif switch[3].val == 0 and synthProgramEnable == 1:
				synthProgramEnable = 0
			elif synthProgramEnable == 0:
				setSynthRange(val)
				synthNewNote = 1
				#print(pot[0].val)

	elif add == "/pot3":
		if pot[3].new(val) is not None:
			setSynthTone(val)	

def setSynthTone(val):
	val = val/4095
	sendOSC('bob-filter', 1, 'CUTOFF', (val) * 100 + 2)
	sendOSC('bob-filter', 1, 'FM-/+', (val) * 35 + 60)	
	sendOSC('slope', 1, 'FALL', (1-(val)) * 75 + 1)
	sendOSC('decay', 1, 'D', (1-(val)) * 75 + 1)


def drumTone(num,val):
	if switch[num].val > 0:
		val = val/4095
		outVal=1
		chText = ["CH1", "CH2", "CH3"]
		if val < 0.1: 
			outVal = val*10
		# elif val > 0.9: 
		# 	outVal = (1-val)*10

		#below is basically what sendOSC() does
		client.send_message('/module', 'mixer4')
		msg = [chText[num], outVal*127, 1]
		client.send_message('/param', msg)

		outVal = math.pow(val*0.8+0.2,2)
		if num == 1: outVal = math.pow(val*0.8+0.2,2)
		if num == 2: outVal = math.pow(val*0.9+0.1,2)
		sendOSC("decay", num+2, "D", outVal*127) #module name, instance, parameter name, value
		sendOSC("decay", num+12, "D", math.pow(outVal,2)*127)

def drumPattern(num,val):
	val = val/4095
	euc[num].setPulses(val* (euc[num].beats-1) )
	print("euc", num, euc[num].pattern)

def synthTone(val):
	val = val/4095
	client.send_message('/module', 'bob-filter')
	msg = ['CUTOFF', (val*0.95+0.05)*127, 1]
	client.send_message('/param', msg)
	client.send_message('/module', 'slope')
	msg = ['FALL', (val*0.2)*127, 1]
	client.send_message('/param', msg)
	client.send_message('/module', 'decay')
	msg = ['D', (val*0.8+0.2)*127, 1]
	client.send_message('/param', msg)

def synthAmp(val):
	global potAmpGain
	if val < 50: val = 0
	else: val = val-50

	outVal = synthAmpLeak.update( val * potAmpGain )
	outVal = math.pow(outVal/(4095), 0.5)
	#print(val, outVal)
	sendOSC("vca", 6, "VCA", outVal*127)


def setSynthRange(val):
	global synthRange
	val = val/4095
	_range = math.floor(val*15)+1

	if _range != synthRange:
		synthRange = _range
		#print("range", synthRange)

		client.send_message('/module', '16steps')
		msg = ['BEGIN',_range, 1]
		client.send_message('/param', msg)
		
		client.send_message('/module', '16steps')
		msg = ['END', _range, 1]
		client.send_message('/param', msg)


def setSynthSeqStep(num,val):
	val =  math.floor(val/4095 * 127)
	sendOSC("16steps", 1, "s"+str(num+1), val)
	#print("setStep", num, val)


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

