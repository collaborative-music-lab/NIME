import math
global dispatcher

#mappings for chester.py
######################
#INCOMING OSC
# handle messages sent from PD
######################

def defineOscHandlers():
	dispatcher.map("/filterFrequency", filterFrequency)
	dispatcher.map("/pitchRange", pitchRange)
	dispatcher.map("/starlight", starlight)
	dispatcher.map("/FMDepth", FMDepth)
	dispatcher.map("/envelope-s", setEnvelope)
	#dispatcher.map("/filterFrequency", filterFrequency)
	#dispatcher.map("/filterFrequency", filterFrequency)
	#dispatcher.map("/filterFrequency", filterFrequency)
	#dispatcher.map("/filterFrequency", filterFrequency)

def filterFrequency(add, val):
	sendOSC("bob-filter", 1, "CUTOFF", scale(val, 0,127,3,20))
	sendOSC("bob-filter", 2, "CUTOFF", scale(val, 0,127,32,110))
	sendOSC("bob-filter", 3, "CUTOFF", scale(val, 0,127,5,40))
	sendOSC("bob-filter", 4, "CUTOFF", scale(val, 0,127,40,127))

def pitchRange(add,val):
	sendOSC("vca", 21, "VCA", scale(val, 0,127,20, 127))
	sendOSC("vca", 22, "VCA", scale(val, 0,127,0, 60))
	sendOSC("vca", 23, "VCA", scale(val, 0,127,0, 60))
	sendOSC("vca", 24, "VCA", scale(val, 0,127,0, 90))

def starlight(add,val):
	sendOSC("vca", 5, "VCA", scale(val, 0,127,0,100))

def FMDepth(add,val):
	sendOSC("bwl-osc", 1, "FM", scale(val, 0,127,0, 75))
	sendOSC("bwl-osc", 2, "FM", scale(val, 0,127,0, 75))
	sendOSC("bwl-osc", 3, "FM", scale(val, 0,127,0, 75))
	sendOSC("bwl-osc", 4, "FM", scale(val, 0,127,0, 75))

def setEnvelope(add,val):
	sendOSC("slope", 1, "RISE", scale(val, 0,127,127,0))
	sendOSC("slope", 1, "FALL", scale(val, 0,127,127,40))
	sendOSC("slope", 2, "RISE", scale(val, 0,127,127,0))
	sendOSC("slope", 2, "FALL", scale(val, 0,127,127,40))
	sendOSC("slope", 3, "RISE", scale(val, 0,127,127,0))
	sendOSC("slope", 3, "FALL", scale(val, 0,127,127,40))
	sendOSC("slope", 4, "RISE", scale(val, 0,127,127,0))
	sendOSC("slope", 4, "FALL", scale(val, 0,127,127,40))

def initSynthParams():
	pass

######################
#SENSOR MAPPINGS
#handle data received from interface
######################
state = {
	'button': [0,0,0,0],
	'encoder': 0,
	'accel': [0,0,0],
	'gyro': [0,0,0],
	'magnitude': 0,
	'eButt': 0
}


def mapSensor(add, val):
	global state

	sensor,num = splitAddress(add)

	if sensor == "/pot":
		pass

	elif sensor == "/sw":
		state['button'][num] = val
		updateButtonVals(num,val)

	elif sensor == "/cap":
		pass

	elif sensor == "/enc":
		state['encoder'] += val
		sendOSC("/enc", 1, "num", state.encoder)


def updateButtonVals(num, val):
	pass



######################
#Helper functions
######################

def scale(input, inLow, inHigh, outLow, outHigh, curve = 1):
	val = (input-inLow)/(inHigh-inLow)
	val = pow(val,curve)
	val = val*(outHigh-outLow) + outLow
	return val

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

def splitAddress(name):
	#print(name[1])
	out = ""
	for i in range(len(name)):
		if name[i].isdigit():
			num = int(name[i])
			return out, num
		else: out = out + (name[i])

def clip(input, low, hi):
	if input > hi: return hi
	elif input < low: return low
	else: return input


