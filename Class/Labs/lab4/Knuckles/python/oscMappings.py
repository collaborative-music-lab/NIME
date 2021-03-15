import math
global dispatcher
# import knuckles.dispatcher
######################
#INCOMING OSC
# handle messages sent from PD
######################

def defineOscHandlers():
	dispatcher.map("/euclid", setEuclid)
	dispatcher.map("/clock", clock)
	dispatcher.map("/keyDown", keyDown)
	dispatcher.map("/keyUp", keyUp)
	dispatcher.map("/enableToggles", handleMouseToggle)
	dispatcher.map("/setPitch", setPitch)
	dispatcher.map("/synthDetune", setDetune)
	dispatcher.map("/progSynthSeq", setEnableSynthSequence)
	dispatcher.map("/synthAmpSensitivity", setSynthAmpSense)

def setEuclid(*args):
    if args[1] == 0:
        euc.set(args[2],args[3],args[4])
    if args[1] == 1:
        euc2.set(args[2],args[3],args[4])
    if args[1] == 2:
        euc3.set(args[2],args[3],args[4])

def clock(*args):
	t.update() #reset timeout
	
	#array to store which events are triggered on this clock
	triggerArray = [0]*10

	#check euclid objects for triggers
	curBeat = args[2]%16

	euclidTrigger = [
		euc.get(math.floor(curBeat / eucDivisor[0])), 
		euc2.get(math.floor(curBeat / eucDivisor[1])), 
		euc3.get(math.floor(curBeat / eucDivisor[2]))]

	#create an array of triggers to be sent on this beat
	for i in range(10):
		for j in range(3): 
			triggerArray[i] += euclidTrigger[j] * enableArray[i][j]

	#iterate through trigger array to send triggers
	for i in range(10):	
			if triggerArray[i]>0:
				if i > 5 or drumEnable[math.floor(i/2)] == 1:
					#print("trig", i)
					client.send_message("/trigger", i)

	#send triggers for visual feeback
	for i in range(3):
		if euclidTrigger[i] == 1: sendOSC("tr-fbk-r"+str(i),1,"trig",1)

def keyDown(*args):
	if args[1]<10 and args[2]<3:
		x=int(args[1])
		y= int(args[2])
		val = 0
		if enableArray[x][y] == 0: val = 1
		toggleEnableArray(x,y,val)

def keyUp(*args): pass

#handle toggle enable array
#array to store our current clock routing, 10x3
enableArray = [[0 for i in range(3)] for j in range(10)]

def toggleEnableArray(x,y,val):
	#print("toggle", x,y,enableArray[x][y],val)
	toggleKeys = ["dr1","dr2","dr3","synth","sampler"]
	toggleParam = ["decay","tone"]
	address = toggleKeys[math.floor(x/2)]+"_en_"+toggleParam[x%2]+"-r"
	
	if y < 2: address = address + str(3-y)
	#print(address)
	if val != enableArray[x][y]:
		enableArray[x][y] = val
		client.send_message("/module", address)
		client.send_message("/param",val)

def initSynthParams():
	for i in range(10):
		for j in range(3): toggleEnableArray(i,j,1)

	for i in range(10):
		for j in range(3): toggleEnableArray(i,j,0)

	for i in range(3):
		setDrumEnables(i,1)
		# client.send_message('/module', 'drumEnable'+str(i)+'-r')
		# client.send_message('/param', 1)


def handleMouseToggle(*args):
	if len(args) != 6: return
	#print("handle", args)
	xa = 0
	xb=0
	if args[2]=='dr2': xa=1
	elif args[2]=='dr3': xa=2
	elif args[2]=='synth': xa=3
	elif args[2]=='sampler': xa=4
	if args[3] == 'tone': xb=1
	x=xa*2+xb

	y=0
	if args[4] == 's2': y=1
	if args[4] == 's3': y=2
	#print(x,y,args[5])
	toggleEnableArray(x,2-y,int(args[5]))

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
buttonStates = [0,0,0,0]
prevPot = [0,0]
drumEnable = [0,0,0]

enableSynthSequence = 0

def mapSensor(add, val):
	global buttonStates
	global prevPot

	if enableSynthSequence == 1:
		programSynthSequence(add,val)
		#return

	if add == "/sw0": 
		buttonStates[0]=val
		setDrumEnables(0,val)
	elif add == "/sw1": 
		buttonStates[1]=val
		setDrumEnables(1,val)
	elif add == "/sw2": 
		buttonStates[2]=val
		setDrumEnables(2,val)
	elif add == "/sw3": 
		buttonStates[3]=val
		setDrumEnables(3,val)
		
	delta  = 0
	if add == "/pot1":
		if buttonStates[3] == 1:
			for i in range(3): drumTone(i,val)
		synthTone(val)
		synthAmp( abs(val-prevPot[1]))
		prevPot[1]=val

	elif add == "/pot0":
		if buttonStates[3] == 1:
			for i in range(3): drumPattern(i,val)
		synthRange(val)
		synthAmp( abs(val-prevPot[0]))
		prevPot[0]=val

def drumTone(num,val):
	global buttonStates

	if buttonStates[num]>0:
		val = val/4095
		outVal=1
		chText = ["CH1", "CH2", "CH3"]
		if val < 0.1: 
			outVal = val*10
		# elif val > 0.9: 
		# 	outVal = (1-val)*10
		client.send_message('/module', 'mixer4')
		msg = [chText[num], outVal*127, 1]
		client.send_message('/param', msg)

		outVal = math.pow(val*0.8+0.2,2)
		if num == 1: outVal = math.pow(val*0.8+0.2,2)
		if num == 2: outVal = math.pow(val*0.9+0.1,2)
		sendOSC("decay", num+2, "D", outVal*127)
		sendOSC("decay", num+12, "D", math.pow(outVal,2)*127)


def setDrumEnables(num,val):
	#print("set",num,val)
	if buttonStates[3] == 1:
		#print("set3",num,val,buttonStates, drumEnable)
		for i in range(3):
			if buttonStates[i] > 0 : drumEnable[i] = 1

	elif val == 1 and num < 3:
		#print("set0")
		drumEnable[num] = 0 if drumEnable[num] == 1 else 1
		#print(drumEnable)

		client.send_message('/module', 'drumEnable'+str(num)+'-r')
		client.send_message('/param', drumEnable[num])

def drumPattern(num,val):
	val = val/4095
	global buttonStates
	if buttonStates[0]==1: euc.setPulses(val*6+1)
	elif buttonStates[1]==1: euc2.setPulses(val*12+1)
	elif buttonStates[2]==1: euc3.setPulses(val*15+1)

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

prevSynthRange = [0,0]
def synthRange(val):
	global prevSynthRange
	val = val/4095
	begin = math.floor(val*8)
	end = math.floor(val*16)

	if begin != prevSynthRange[0]:
		client.send_message('/module', '16steps')
		msg = ['BEGIN',begin, 1]
		client.send_message('/param', msg)
		prevSynthRange[0]=begin
	if end != prevSynthRange[1]:
		client.send_message('/module', '16steps')
		msg = ['END', end, 1]
		client.send_message('/param', msg)
		
		prevSynthRange[1]=end

synSeqAmps = [0,0,0]
synSeqFreqs = [0,0,0]

#use the interface to set the values of the synth sequencer
def programSynthSequence(add, val):

	for i in range(3):
		if buttonStates[i]==1:
			if add == '/pot0':synSeqAmps[i] = val/4095
			elif add == '/pot1':synSeqFreqs[i] = math.pow(val/4095,1.5) * 4

	seq = [0]*16

	for i in range(16):
		wave = [0,0,0]
		for j in range(2):
			wave[j] = (math.sin(synSeqFreqs[j]*i)/2 + 0.5) * synSeqAmps[j]
			wave[2] = ((synSeqFreqs[2]*i) % 4)  * synSeqAmps[2]
		seq[i] = wave[0]+wave[1]+wave[2]
		seq[i] = math.floor(seq[i]*40)

		sendOSC("16steps", 1, "s"+str(i+1), seq[i])

	print(seq)


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

#########
#EUCLIDIAN SEQUENCER
#########
class Euclid:
	beats = 16
	pulses = 3
	rotation = 8
	bucket = 0
	prevBeat = -1

	pattern = []

	def __init__(self,beats,pulses,rotation=0):
		self.setBeats(beats)
		self.setPulses(pulses)
		self.rotation = rotation

	def setBeats(self,num):
		self.beats = num
		if self.pulses > self.beats:
			self.pulses = self.beats
		self.calcPattern()

	def setPulses(self,num):
		val = math.floor(num)
		if val != self.pulses: 
			self.pulses = val
			if self.pulses > self.beats:
				self.pulses = self.beats
			self.calcPattern()
			print("euclid", self.pattern)

	def set(self, pulses, beats=8, rotation=0):
		self.setBeats(beats)
		self.setPulses(pulses)
		self.rotation=rotation

	def calcPattern(self):
		self.pattern = []
		for i in range(int(self.beats)):
			self.bucket += self.pulses
			if self.bucket > self.beats:
				self.bucket -= self.beats
				self.pattern.append(1)
			else: self.pattern.append(0)
		#print("pattern", len(self.pattern), self.pattern)

	def get(self,_beat):
		if _beat != self.prevBeat:
			self.prevBeat = _beat
			num = int((_beat+self.rotation)%self.beats)
			return self.pattern[num]
		else: return 0

eucDivisor = [2,1,1]
euc = Euclid(8,3,0) #bass drum
euc2 = Euclid(16,3,4) # snare
euc3 = Euclid(16,9,0) #hihat
