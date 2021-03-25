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
	#placeholders for storing most recent data
	'button': [0,0,0,0],
	'encoder': 0,
	'accel': [0,0,0],
	'gyro': [0,0,0],
	'magnitude': 0,
	'eButt': 0,
	'velocity': [0,0,0],
	'gAngle': [0,0,0],
	'tilt': [0,0,0],
	'pitch': -1
}

prev = {
	#variables for storing previous sensor data
	'aX': 0, 'aY': 0, 'aZ': 0,
	'gX': 0, 'gY': 0, 'gZ': 0,
	'vX': 0, 'vY': 0, 'vZ': 0,
	'accel': [0,0,0], 'gyro': [0,0,0], 'velocity': [0,0,0],
	'magnitude1': 0, 'magnitude2': 0, 'magnitude3': 0,
	'angle': [0,0,0],
	'angleX': 0, 'angleY': 0, 'angleZ': 0,
	'tiltaX':0 , 'tiltaY':0, 'tiltaZ':0,
	'lfo': 0, 'lfoTilt': 0, 'lfoLeak': 0
}

tuning = {
	#variables for smoothing filters
	'magnitudeSmooth': 0.6,
	'magnitudeGain': 4,
	'tiltSmooth': 0.5,
	'lfoScale': 0.4, 
	'lfoLeak': 0.97
}


def mapSensor(add, val):
	global state

	sensor,num = splitAddress(add)

	if sensor == "/pot":
		pass

	elif sensor == "/sw":
		state['button'][num] = val
		updateButtonVals(num,val)
		client.send_message( "/sw"+str(num), val)

	elif sensor == "/cap":
		pass

	elif sensor == "/enc":
		state['encoder'] += val
		client.send_message("/enc", state['encoder'])
		sendOSC("/enc", 1, "/num", state['encoder'])

	elif sensor == "/encSw":
		client.send_message("/encSw", val)

	elif sensor == "/acc":
		calcVelocity(val)
		calcMagnitude(val)
		#sendRawAccel( val)
		state['accel'] = val

	elif sensor == "/gyro":
		calcTilt(val)
		sendRawGyro( val)
		state['gyro'] = val 

	calcVoiceGains()
	calcLPF()
	calcLFOs()
	calcWaveshape()


def updateButtonVals(num, val):
	state['button'][num] = val 

	pitchIndex = 0
	for i in range( len(state['button']) -  1): pitchIndex += math.pow(2, i) * state['button'][i+1]
	pitches = [-1,0,3,5,7,10,15,17,19,22]
	outVal = pitches[int(pitchIndex)]
	outVal += 12 * state['button'][0]
	print('pitch', outVal)
	state['pitch'] = outVal
	if outVal >=  0:
		outVal /= 127
		sendOSC('globalpitch', outVal, outVal, outVal)

def calcTilt(vals):
	'''calculate tilt XYZ using a complementary filter'''
	Gweight = 0.9 #weighting for complementary filter

	outAngle = [0] * 3

	#integrate gyroscope and highpass
	for i in range (3): 
		state['gAngle'][i] += vals[i]/10
		state['gAngle'][i] *= (tuning['tiltSmooth']/20 + 0.95)
		outAngle[i] = state['gAngle'][i]

	#calculate complemtary filter
	for i in range(3): 
		outAngle[i] = (state['gAngle'][i] * Gweight + state['accel'][i] * (1-Gweight) )

	client.send_message("/tiltX", outAngle[0])
	client.send_message("/tiltY", outAngle[1])
	client.send_message("/tiltZ", outAngle[2])
	for i in range(3):	state['tilt'][i] = outAngle[i]

def calcMagnitude(vals):
	'''calculate magnitude as the sum of all velocity vectors'''
	val = math.pow( math.pow(state['velocity'][0],2) + math.pow(state['velocity'][1], 2) + math.pow(state['velocity'][2], 2), 0.5)
	
	#if no finger is down fade to silence
	if state['pitch'] < 0 : val = 0

	val = onepole(val, 'magnitude1', tuning['magnitudeSmooth'])
	
	val*= tuning['magnitudeGain']
	client.send_message( "/magnitude", val)
	state['magnitude'] = val

	sendOSC("vca", 7, "CV", (val)*127)
	sendOSC("vca", 8, "CV", (val)*127)

def calcVelocity(vals):
	#integrate acceleration
	vel = ['vX','vY','vZ']
	acc = ['aX','aY','aZ']
	for i in range(3): 
		dx = vals[i] - onepole(vals[i], acc[i] , 0.6) 
		dx = clipBipolar(dx, 0.01, 1) #filter out very small values
		outVal = leakyInt(dx*1, vel[i], 0.8)

		state['velocity'][i] = onepole(outVal, vel[i], 0.9)

	client.send_message("/aX", state['velocity'][0])
	client.send_message("/aY", state['velocity'][1])
	client.send_message("/aZ", state['velocity'][2])


def calcVoiceGains():
	gains = [0]*4
	#print(state['tilt'][1])
	for i in range(2):
		gains[i]  = scale( (i*2-1) *   state['tilt'][1], -.2, .4, 0, 1)
		gains[i] = clip( gains[i], 0, 1)

		sendOSC( 'vca', i+2, "VCA", gains[i]*127)

def calcLPF():
	val = clip ( state['tilt'][2], -0.5, 0.5)
	val = scale( -val, -.5, .5, 0, 1.)

	sendOSC('analog-filter', 1, "CUTOFF", val*80 + 2)
	sendOSC('bob-filter', 2, "CUTOFF", val*60 + 5)
	sendOSC('bob-filter', 3, "CUTOFF", val*60 + 10)
	sendOSC('bob-filter', 4, "CUTOFF", val*60 + 20)

def calcLFOs():
	#print(state['tilt'][0])
	val = clip ( state['tilt'][0], -0.5, 0.5)

	#use a highpass filter to remove DC offset
	val = val - onepole(val, 'lfoTilt', 0.98)
	
	#remove small values
	val = clipBipolar(val, 0.02, 1)

	val = leakyInt( val, 'lfoLeak', tuning['lfoLeak'])
	clip(val, -1, 1)
	val1 = scale( -val, -1, 1, -tuning['lfoScale'], tuning['lfoScale'])
	val2 = scale( val, -1, 1, -tuning['lfoScale'], tuning['lfoScale'])

	sendOSC('slope', 1, "DEPTH-/+", val1*60 + 64)
	sendOSC('slope', 2, "DEPTH-/+", val2*60 + 64)
	sendOSC('slope', 3, "DEPTH-/+", val1*50 + 64)
	sendOSC('slope', 4, "DEPTH-/+", val2*50 + 64)

	#Z axis affects LFO speed
	val = clip ( -state['tilt'][2], -0.5, 0.5)
	val = scale( -val, -.5, .5, 0, 1.)

	sendOSC('slope', 1, "RISE", val*30 + 0)
	sendOSC('slope', 2, "RISE", val*-30 + 34)
	sendOSC('slope', 3, "RISE", val*-20 + 24)
	sendOSC('slope', 4, "RISE", val*20 + 0)
	sendOSC('slope', 1, "FALL", val*30 + 0)
	sendOSC('slope', 2, "FALL", val*-30 + 34)
	sendOSC('slope', 3, "FALL", val*-20 + 34)
	sendOSC('slope', 4, "FALL", val*20 + 0)

def calcWaveshape():
	val = clip ( state['tilt'][0], -0.5, 0.5)

	sendOSC('bwl-osc', 2, "WSHAPE", val*60 + 60)
	sendOSC('bwl-osc', 3, "WSHAPE", val*60 + 60)
	sendOSC('bwl-osc', 4, "WSHAPE", val*60 + 60)



def sendRawAccel(vals):
	client.send_message("/aX", vals[0])
	client.send_message("/aY", vals[1])
	client.send_message("/aZ", vals[2])

def sendRawGyro(vals):
	client.send_message("/gX", vals[0])
	client.send_message("/gY", vals[1])
	client.send_message("/gZ", vals[2])

def onepole(val, name, coefficient): 
	clip (coefficient, 0, 1)
	outVal = (val*(1-coefficient) + prev[name]*coefficient)
	prev[name] = outVal
	return outVal

def leakyInt(val, name, leak):
	outVal = prev[name]
	outVal *= leak 
	outVal += val
	prev[name] = outVal
	return outVal

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

def clipBipolar(input, low, hi):
	'''filters out small numbers from bipolar variables'''
	sign = 1
	if input<0: sign = -1
	outVal = abs(input)

	if outVal > hi: outVal =  hi
	elif outVal < low: outVal =  low
	
	return (outVal-low) * sign 

pitches = [0,3,5,7,10]

#GREY CODE

def processOptoButton(num):
    client.send_message("/button", [num,optoButton[num]])

    if num < 4:
        outVal=0
        for i in range(4): 
            if optoButton[i]>0: 
                outVal += pow(2,i) #standard valve pitches

        #outVal = [0,1,2,3,4,5,6,7,8][outVal] #no remapping
        outVal = [0,1,3,2,7,6,4,5,15,14,12,13,8,9,11,10][outVal] #gray code
        #outVal = [0,1,2,3,4,5,6,7,8][outVal]
        #outVal = [0,1,2,3,4,5,6,7,8][outVal]

        print(outVal, pitches[outVal%len(pitches)], math.floor(outVal/len(pitches))*12)
        outVal = pitches[outVal%len(pitches)] + math.floor(outVal/len(pitches)) *12

        client.send_message("/pitch", outVal)
        #print(num, outVal)

#gray code:
# https://mathworld.wolfram.com/GrayCode.html
# gray  binary  pow2
# 0     0       0
# 1     1       1
# 2     11      3
# 3     10      2
# 4     110     6
# 5     111     7
# 6     101     5
# 7     100     4
# 8     1100    12
# 9     1101    13
# 10    1111    15
# 11    1110    14
# 12    1010    10
# 13    1011    11
# 14    1001    9
# 15    1000    8
