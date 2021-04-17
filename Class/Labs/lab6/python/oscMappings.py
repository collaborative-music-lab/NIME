import math
global dispatcher

#mappings for chester.py
######################
#INCOMING OSC
# handle messages sent from PD
######################

enableIMUmonitoring = 0

def defineOscHandlers():
	dispatcher.map("/setPitch", setPitch)
	dispatcher.map("/synthDetune", setDetune)
	dispatcher.map("/FMDepth", FMDepth)
	dispatcher.map("/reverb-size", reverbSize )
	dispatcher.map("/waveshape", waveshape )
	dispatcher.map("/ws-lfo-rate", waveshape )
	dispatcher.map("/ws-lfo-depth", waveshape )
	dispatcher.map("/pitch-glide", pitchGlide )
	dispatcher.map("/setMagnitudeSmooth", setMagnitudeSmooth )
	dispatcher.map("/setTiltSmooth", setTiltSmooth )
	dispatcher.map("/setVelocitySmooth", setVelocitySmooth )
	dispatcher.map("/setPitchset", setPitchset )

def initSynthParams():
	pass

def setPitch(add, num, val):
	pitchshift = [24,12,7,4,0]
	index = math.floor(val)

	if num == 0:
		newVal = math.floor(val/5)+19
		if newVal != state['pitches'][0]:
			state['pitches'][0] = newVal
	
	elif num == 1: state['pitches'][1] = pitchshift[index]
	elif num == 2: state['pitches'][2] = pitchshift[index]
	elif num == 3: state['pitches'][3] = (val) * -12

	updatePitches()

def setDetune(add,val): 
	state['detune'] = math.pow(val/127,3)/12
	updatePitches()

def updatePitches():
	sendOSC("bwl-osc", 4, "PITCH", state['pitches'][0] + state['pitches'][3]) #sub
	sendOSC("bwl-osc", 1, "PITCH", state['pitches'][0]) #main osc
	sendOSC("bwl-osc", 2, "PITCH", state['pitches'][1]+state['pitches'][0] + state['pitches'][0]*state['detune'])
	sendOSC("bwl-osc", 3, "PITCH", state['pitches'][2]+state['pitches'][0] - state['pitches'][0]*state['detune'])

def FMDepth(add,val):
	for i in range(4):
		sendOSC("bwl-osc", i, "FM", tuning['fmDepth'])
		sendOSC("vca", i+10 , "VCA", scale(val, 0,127,0, 127, 3))

def reverbSize(add, val):
	sendOSC('millerverb', 1, 'REVERB', val)
	sendOSC('megaverb', 1, 'SIZE', val)

def waveshape(add,val):
	if add == '/waveshape':
		for i in range(3): sendOSC('bwl-osc', i+1, 'WSHAPE', val/2)
	elif add == '/ws-lfo-rate': sendOSC('basic-lfo', 1, 'FREQ', val)
	elif add == '/ws-lfo-depth':  sendOSC('basic-lfo', 1, 'DEPTH', val)

def pitchGlide(add, val):
	state['pitchGlideRange'] = scale(val, 0, 127, 10, 500, 2) #inputVal, inLow, inHigh, outLow, outHigh, exponent
	state['pitchGlideLag'] = scale(val, 0, 127, 0., 1, tuning['pitchGlideLagCurve'])
	#print("oscPitchGlide", val, state['pitchGlideRange'])
	# val = scale(val, 0,127,0, 500, 2)
	# sendOSC('pitchGlide', val, val, val )

def setMagnitudeSmooth(add, val):
	tuning['magnitudeSmooth'] = val/127

def setTiltSmooth(add, val):
	tuning['tiltSmooth'] = val/127

def setVelocitySmooth(add, val):
	tuning['velocitySmooth'] = val/127

def setPitchset(add, val):
	if val < len(pitchset): state['curPitchset'] = int(val)
	else: print("pitchset index out of range")

######################
#SENSOR MAPPINGS
#handle data received from interface
######################
state = {
	#placeholders for storing most recent data
	'switch': [0,0,0,0],
	'accel': [0,0,0],
	'accelInt': [0,0,0],
	'accelSmooth': [0,0,0],
	'aMag': [0,0,0],
	'gyro': [0,0,0],
	'magnitude': 0,
	'velocity': [0,0,0],
	'jerk': [0,0,0],
	'gAngle': [0,0,0],
	'tilt': [0,0,0],
	'pitch': -1,
	'curPitchset': 1,
	'encSw': 0,
	'detune': 0,
	'pitches': [24,0,12,-12], #basePitch, offset1, offset2, sub
	'pitchGlideRange': 100, #pitchGlide time in ms
	'pitchGlideLag': 0.9 #lowpass coefficient
}

prev = {
	#variables for storing previous sensor data
	'aX': 0, 'aY': 0, 'aZ': 0,
	'aiX': 0, 'aiY': 0, 'aiZ': 0,
	'amX': 0, 'amY': 0, 'amZ': 0,
	'gX': 0, 'gY': 0, 'gZ': 0,
	'vX': 0, 'vY': 0, 'vZ': 0,
	'jX': 0, 'jY': 0, 'jZ': 0,
	'jiX': 0, 'jiY': 0, 'jiZ': 0,
	'accel': [0,0,0], 'gyro': [0,0,0], 'velocity': [0,0,0], 'jerk': [0,0,0],
	'aMag': [0,0,0], 'magnitude1': 0, 'magnitude2': 0, 'magnitude3': 0,
	'angle': [0,0,0],
	'angleX': 0, 'angleY': 0, 'angleZ': 0,
	'tiltX':0 , 'tiltY':0, 'tiltZ':0,
	'tiltaX':0 , 'tiltaY':0, 'tiltaZ':0,
	'lfo': 0, 'lfoTilt': 0, 'lfoLeak': 0,
	'pitchGlide': 0
}

tuning = {
	#variables for smoothing filters
	'magnitudeSmooth': 0.6,
	'magnitudeFade': 0.1,
	'magnitudeGain': 4,
	'tiltSmooth': 0.9,
	'velocitySmooth': 1,
	'lfoScale': 0.4, 
	'lfoLeak': 0.97,
	'fmDepth': 64,
	'pitchGlideLagCurve': 0.5
}

pitchset = [[0,3,5,7,10,15,17,19,22], 
[0,2,3,5,7,9,10,12,14,15],
[0,3,7,10,12,15,19,22,24]
]

def mapSensor(add, val):
	global state

	try:
		sensor,num = splitAddress(add)

		if sensor == "/pot":
			pass

		elif sensor == "/sw":
			state['switch'][num] = val
			updateSwitchVals(num,val)
			client.send_message( "/sw"+str(num), val)

		elif sensor == "/cap":
			pass

		elif sensor == "/enc":
			client.send_message("/enc", val)

		elif sensor == "/encSw":
			state['encSw'] = val
			client.send_message("/encSw", val)

		elif sensor == "/acc":
			calcJerk(val)
			calcVelocity(val)
			calcMagnitude(val)
			#calcTiltAccel(val)

			calcVoiceGains()
			calcLPF()
			calcLFOs()
			calcPitchGlide()

			### one and only one of the below can be active ###
			#calcAccMagnitude(val, 0.5	)
			#calcSmoothAccel(val, 0.9) #second arg is coefficient
			sendRawAccel( val)

			prev['accel'] = state['accel']
			state['accel'] = val
		

		elif sensor == "/gyro":
			calcTilt(val)
			sendRawGyro( val)
	except:
		print("unrecognized sensorVal", add, val)
		print(e)


def updateSwitchVals(num, val):
	'''use our switches to selet pitches from a pitchset'''
	state['switch'][num] = val 

	pitchIndex = 0 #which pitch from our set t0 play
	#below we map which switches are pushed down to which pitch we select from our set
	for i in range( len(state['switch']) -  1): pitchIndex += math.pow(2, i) * state['switch'][i+1]

	#we will draw our pitchset from the 'pitchset' array
	pitches = pitchset[state['curPitchset']]
	#and then prepend with -1 to indicate no switch held down
	pitches = [-1] + pitches

	outVal = pitches[int(pitchIndex)]
	state['pitch'] = outVal
	#don't play if switch 1/2/3 are not held down
	if outVal >=  0:
		outVal += 12 * state['switch'][0] #switch 0 changes ocatve
		print('pitch', pitchIndex, outVal, pitches)	
		outVal /= 127
		sendOSC('globalpitch', outVal, outVal, outVal)


#####IMU FUNCTIONS #######		

def calcTiltAccel(vals):
	'''calculates tilt only using a 3-axis accelerometer'''
	smoothing = 0.0

	outX = math.atan(vals[0]/ math.sqrt( math.pow(vals[1],2) + math.pow(vals[2],2) ))
	outY = math.atan(vals[1]/ math.sqrt( math.pow(vals[0],2) + math.pow(vals[2],2) ))
	outZ = math.atan(vals[2]/ math.sqrt( math.pow(vals[0],2) + math.pow(vals[1],2) ))

	outX = onepole(outX, 'tiltX', smoothing) / 1.57
	outY = onepole(outY, 'tiltY', smoothing) / 1.57
	outZ = onepole(outZ, 'tiltZ', smoothing) / 1.57

	client.send_message("/tiltX", outX)
	client.send_message("/tiltY", outY)
	client.send_message("/tiltZ", outZ)

	state['tilt'][0] = outX
	state['tilt'][1] = outY
	state['tilt'][2] = outZ

def calcTilt(vals):
	'''calculate tilt XYZ using a complementary filter'''
	Gweight = 0.9 #weighting for complementary filter

	outAngle = [0] * 3

	#integrate gyroscope and highpass
	for i in range (3): 
		state['gAngle'][i] += vals[i]/10
		state['gAngle'][i] *= (tuning['tiltSmooth']/10 + 0.9)
		outAngle[i] = state['gAngle'][i]

	#calculate complementary filter
	for i in range(3): 
		outAngle[i] = (state['gAngle'][i] * Gweight + state['accel'][i] * (1-Gweight) )

	client.send_message("/tiltX", outAngle[0])
	client.send_message("/tiltY", outAngle[1])
	client.send_message("/tiltZ", outAngle[2])
	for i in range(3):	state['tilt'][i] = outAngle[i]

def calcMagnitude(vals):
	'''calculate magnitude as the sum of all velocity vectors'''
	val = math.sqrt( math.pow(state['velocity'][0],2) + math.pow(state['velocity'][1], 2) + math.pow(state['velocity'][2], 2))
	
	#if no finger is down fade to silence
	if state['pitch'] < 0 : val = onepole(0, 'magnitude1', tuning['magnitudeFade'])

	#Smooth and scale the output
	else: val = onepole(val, 'magnitude1', tuning['magnitudeSmooth'])
	val*= tuning['magnitudeGain']

	client.send_message( "/magnitude", val)
	state['magnitude'] = val

	sendOSC("vca", 7, "CV", (val)*127)
	sendOSC("vca", 8, "CV", (val)*127)

def calcVelocity(vals):
	#integrate acceleration
	vel = ['vX','vY','vZ']
	acc = ['aiX','aiY','aiZ']
	jerk = ['jiX','jiY','jiZ']

	for i in range(3):
		#remove gravity
		state['accelInt'][i] *= tuning['velocitySmooth'] * 0.9
		state['accelInt'][i] += state['jerk'][i]
		 
		state['velocity'][i]*= tuning['velocitySmooth'] * 0.95
		state['velocity'][i] += state['accelInt'][i]/5 

		state['velocity'][i] *= scale( 1-tuning['velocitySmooth'], 0, 1, 1, 2, 2 )
		

	client.send_message("/velocityX", state['velocity'][0])
	client.send_message("/velocityY", state['velocity'][1])
	client.send_message("/velocityZ", state['velocity'][2])
	#print(tuning['velocitySmooth'])

def calcJerk(vals):
	'''derivative of acceleration'''
	outVal = [0]*3
	for i in range(3):
		outVal[i] = vals[i] - state['accel'][i]
		prev['jerk'][i] = state['jerk'][i]
		state['jerk'][i] = outVal[i]
	if enableIMUmonitoring == 1:
		client.send_message("/jX", state['jerk'][0])
		client.send_message("/jY", state['jerk'][1])
		client.send_message("/jZ", state['jerk'][2])
	#print(state['jerk'])

def calcAccMagnitude(vals, coefficient):
	'''calculates magnitude of a single axis'''
	mag = ['amX','amY','amZ']
	for i in range(3):
		state['aMag'][i] = onepole(abs(vals[i]),mag[i], coefficient)
	#print(state['aMag'])
	if enableIMUmonitoring == 1:	sendRawAccel(state['aMag'])

def calcSmoothAccel(vals,coefficient):
	'''simple lowpass filter for accel'''
	prevAcc = ['aX','aY','aZ']
	for i in range(3):
		state['accelSmooth'][i] = onepole((vals[i]),prevAcc[i], coefficient)
	#print(state['aMag'])
	sendRawAccel(vals)

def sendRawAccel(vals):
	if enableIMUmonitoring == 1:
		client.send_message("/aX", vals[0])
		client.send_message("/aY", vals[1])
		client.send_message("/aZ", vals[2])

def sendRawGyro(vals):
	prev['gyro'] = vals
	if enableIMUmonitoring == 1:
		client.send_message("/gX", vals[0])
		client.send_message("/gY", vals[1])
		client.send_message("/gZ", vals[2])
	state['gyro'] = vals

######SYNTH PARAMS ########

def calcPitchGlide():
	#print('pitchGlide', state['magnitude'], state['pitchGlideRange'], state['pitchGlideLag'])
	outVal = state['magnitude'] * state['pitchGlideRange']
	outVal = onepole(outVal,'pitchGlide', state['pitchGlideLag'])

	sendOSC("pitchGlide", outVal, outVal, outVal)


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

#GREY CODE

def processOptoButton(num):
    client.send_message("/button", [num,optoButton[num]])

    if num < 4:
        outVal=0
        for i in range(4): 
            if optoButton[i]>0: 
                outVal += pow(2,i) #standard valve pitches

        pitches = [0,3,5,7,10]

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
