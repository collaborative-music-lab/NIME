import math
global dispatcher

#mappings for capacit.py
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
prevNoteTrigger = [0,0,0,0]
curAmplitude = [0,0,0,0]

prevFoo = 0

def mapSensor(add, val):
	global buttonStates
	global prevPot
	global maxCapValues
	global curAmplitude
	global prevNoteTrigger
	global prevFoo

	capTouchThreshold = 0.5
	capProximityThreshold = 0.01

	sensor,num = splitAddress(add)

	if sensor == "/pot":
		pass

	elif sensor == "/sw":
		pass

	elif sensor == "/cap":
		if num <= 4:
			autoScaleCap(num,val) #calibrate capSense range
			scaledVal = val/maxCapValues[num]

			#when pads are being touched
			# envelope adds to amplitude 
			out = clip(scaledVal - capTouchThreshold , 0 , 1) * 127
			#print("vca", num+1, out)
			curAmplitude[num] += out
			if num == 0:
				
				print((val))
				prevFoo = val

			sendOSC("vca", num+1, "CV", val)

			#FM amount
			out = clip(scaledVal - capTouchThreshold , 0 , 0.6) * 127
			#print("vca", num+1, out)
			if out > 10: 
				sendOSC("vca", num+11, "CV", out)
				sendOSC("vca", num+11, "VCA", scale(out, 10, 127, 0, 127))
			else:
				#small amount of FMwhen in proximity
				out = clip(scaledVal*10 - capProximityThreshold , 0 , 0.2) * 127
				#print("CV", num+1, out)
				sendOSC("vca", num+11, "CV", out)
				sendOSC("vca", num+11, "VCA", 0)

			#when pads are in proximity
			#proximity controls amplitude
			out = clip(scaledVal*10 - capProximityThreshold , 0 , 0.5) * 127
			#print("CV", num+1, out)
			curAmplitude[num] += out
			sendOSC("vca", num+1, "VCA", out)
		
			outAmp = clip(curAmplitude[num]/4, 0, 127)
			sendOSC("monitor"+str(num+1),outAmp,outAmp,outAmp)
			curAmplitude[num] *= 0.75

			if curAmplitude[num] <= 1:
				if prevNoteTrigger[num] == 0: 
					sendOSC("triggerNote", num, num, num)
					print("trig", num)
					prevNoteTrigger[num] = 1
			elif curAmplitude[num] > 60: prevNoteTrigger[num] = 0
	

maxCapValues = [100,100,100,100,100,100,100,100]

def autoScaleCap(num,val):
	global maxCapValues
	maxCapValues[num] = maxCapValues[num] * 0.999
	if val > maxCapValues[num]: maxCapValues[num] = val




	# if add == "/sw0": 
	# 	buttonStates[0]=val
	# 	setDrumEnables(0,val)
	# elif add == "/sw1": 
	# 	buttonStates[1]=val
	# 	setDrumEnables(1,val)
	# elif add == "/sw2": 
	# 	buttonStates[2]=val
	# 	setDrumEnables(2,val)
	# elif add == "/sw3": 
	# 	buttonStates[3]=val
	# 	setDrumEnables(3,val)
		
	# delta  = 0
	# if add == "/pot1":
	# 	if buttonStates[3] == 1:
	# 		for i in range(3): drumTone(i,val)
	# 	synthTone(val)
	# 	synthAmp( abs(val-prevPot[1]))
	# 	prevPot[1]=val

	# elif add == "/pot0":
	# 	if buttonStates[3] == 1:
	# 		for i in range(3): drumPattern(i,val)
	# 	synthRange(val)
	# 	synthAmp( abs(val-prevPot[0]))
	# 	prevPot[0]=val




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


