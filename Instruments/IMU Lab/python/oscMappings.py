import math
global dispatcher

#mappings for imu_lab.py
######################
#INCOMING OSC
# handle messages sent from PD
######################

enableIMUmonitoring = 1

def defineOscHandlers():
	pass

def initSynthParams():
	pass

def setMagnitudeSmooth(add, val):
	tuning['magnitudeSmooth'] = val/127

def setTiltSmooth(add, val):
	tuning['tiltSmooth'] = val/127

def setVelocitySmooth(add, val):
	tuning['velocitySmooth'] = val/127


######################
#SENSOR MAPPINGS
#handle data received from interface
######################
state = {
	#raw data
	'accel': [0,0,0],
	'velocity': [0,0,0], #accel integration
	'jerk': [0,0,0], #accel derivative
	'magnitude': 0, #total acceleration
	'accelTilt': [0,0,0],

	'gyro': [0,0,0],
	'angle': [0,0,0], #gyro integration

	#buffers for data
	'accelIndex': 0,
	'accelBufferLength': 8,
	'accelBuffer': [0,0,0] * 8,

	'gyroBuffer': [[0,0,0]],
	'gyroIndex': 0,
	'gyroBufferLength': 8,
	'tilt': [0,0,0],

	#cooked data
	#smoothed
	'accelSmooth': [0,0,0], #using onepole
	'magnitudeSmooth': 0,
	'accelAvg': [0,0,0], #average of buffer
	'accelMean': [0,0,0], #mean of buffer
	'accelMin': [0,0,0], #minimum val in buffer
	'accelMax': [0,0,0], #maximum val in buffer

	'gyroSmooth': [0,0,0],

	'pitch': -1,
	'curPitchset': 1,
	'detune': 0,
	'pitches': [24,0,12,-12], #basePitch, offset1, offset2, sub
	'pitchGlideRange': 100, #pitchGlide time in ms
	'pitchGlideLag': 0.9, #lowpass coefficient
	'lfoTilt': 0,
	'lfoLeak': 0,
	'pitchGlide': 0
}


tuning = {
	#variables for smoothing filters
	'accelSmooth' : 0.9,
	'magnitudeSmooth': 0.6,
	'magnitudeFade': 0.1,
	'magnitudeGain': 4,
	'tiltSmooth': 0.9,
	'pitchGlideLag': 0.5,
	'pitchGlideLagCurve': 0.5
}

def mapSensor(add, val):
	global state

	sensor,num = splitAddress(add)

	if sensor == "/pot":
		pass

	elif sensor == "/sw":
		pass

	elif sensor == "/cap":
		pass

	elif sensor == "/enc":
		pass

	elif sensor == "/encSw":
		pass

	elif sensor == "/acc":
		sendRawAccel( val)
		#state['jerk'] = calcJerk(val)
		state['velocity'] = calcVelocity(val)
		state['magnitude'] = calcMagnitude(val)
		state['accelTilt'] = calcTiltAccel(val) 
		bufferAccel(val)

		#state['accelSmooth'] = onepole2(state['accelSmooth'],val,0.9) #old, new, alpha
		#state['magnitudeSmooth'] = onepole2(state['magnitudeSmooth'],state['magnitude'],0.9) #old, new, alpha

		state['accel'] = val #last to enable calc of difference between new and old data

		#calculate synth params
		# calcVoiceGains()
		# calcLPF()
		# calcLFOs()
		# calcPitchGlide()

	elif sensor == "/gyro":
		sendRawGyro( val)
		#state['angle'] = calcAngle(val)
		#state['tilt'] = calcTilt(val)
		state['gyro'] = val

	# except:
	# 	print("unrecognized sensorVal", add, val)

#####IMU FUNCTIONS #######	
def calcTiltAccel(vals):
	'''calculates tilt only using a 3-axis accelerometer'''
	outVal = [0] * 3
	#print(vals)
	outX = math.atan(vals[0]/ math.sqrt( math.pow(vals[1],2) + math.pow(vals[2],2) ))
	outY = math.atan(vals[1]/ math.sqrt( math.pow(vals[0],2) + math.pow(vals[2],2) ))
	outZ = math.atan(vals[2]/ math.sqrt( math.pow(vals[0],2) + math.pow(vals[1],2) ))

	outVal = [outX, outY, outZ]

	client.send_message("/tiltX", outVal[0])
	client.send_message("/tiltY", outVal[1])
	client.send_message("/tiltZ", outVal[2])

	return outVal


def calcAngle(vals):
	angleLeak = 0.99
	outVal = [0] * 3

	for i in range (3): 
		if abs(vals[i]) > 0.05:
			filteredGyro = clipBipolar( vals[i] , 0.0, 1000)
			outVal[i] = state['angle'][i] + (filteredGyro/4 )
			outVal[i] *= angleLeak
		else: outVal[i] = state['angle'][i] * 0.999

	return outVal

def calcTilt(vals):
	'''calculate tilt XYZ using a complementary filter'''
	Gweight = 0.95 #weighting for complementary filter

	outAngle = [0] * 3

	#calculate complementary filter
	for i in range(3): 
		outAngle[i] = state['angle'][i] * 1 + state['accelTilt'][i] * (1-Gweight) 

	client.send_message("/tiltX", outAngle[0])
	client.send_message("/tiltY", outAngle[1])
	client.send_message("/tiltZ", outAngle[2])

	return outAngle

def calcMagnitude(vals):
	'''calculate magnitude as the sum of all acceleration vectors'''
	val = math.sqrt( math.pow(vals[0],2) + math.pow(vals[1], 2) + math.pow(vals[2], 2))
	val = abs(val-0.5) #remove static acceleration
	outVal = 0

	if (val - state['magnitude']) > 0.1: #increase in magnitude
		outVal = onepole2(state['magnitude'], val, 0.0)
	else:
		outVal = onepole2(state['magnitude'], val, 0.0)

	client.send_message( "/magnitude", state['magnitude'])
	#print( state['pitch'], state['magnitude'])

	sendOSC("vca", 7, "CV", outVal*127)
	sendOSC("vca", 8, "CV", outVal*127)

	return outVal

def calcVelocity(vals):
	#integrate acceleration
	velocityLeak = 0.99
	outVal = [0] * 3

	for i in range(3):
		outVal[i] += vals[i]
		outVal[i] *= velocityLeak

	client.send_message("/dataX", outVal[0])
	client.send_message("/dataY", outVal[1])
	client.send_message("/dataZ", outVal[2])
	#print(outVal)

	return outVal

def calcJerk(vals):
	'''derivative of acceleration'''
	outVal = [0]*3
	for i in range(3):
		outVal[i] = vals[i] - state['accel'][i]

	if enableIMUmonitoring == 1:
		client.send_message("/dataX", outVal[0])
		client.send_message("/dataY", outVal[1])
		client.send_message("/dataZ", outVal[2])
	#print(state['jerk'])

	return outVal

def calcSmoothAccel(vals,coefficient):
	'''simple lowpass filter for accel'''
	tuning['accelSmooth']
	outVal = [0] * 3
	for i in range(3):
		outVal[i] = onepole2(vals[i],state['accel'], tuning['accelSmooth'])
	#print(state['aMag'])
	sendRawAccel(vals)

	return outVal

def sendRawAccel(vals):
	if enableIMUmonitoring == 1:
		client.send_message("/aX", vals[0])
		client.send_message("/aY", vals[1])
		client.send_message("/aZ", vals[2])

def sendRawGyro(vals):
	if enableIMUmonitoring == 1:
		client.send_message("/gX", vals[0])
		client.send_message("/gY", vals[1])
		client.send_message("/gZ", vals[2])

def bufferAccel(vals):
	state['accelIndex'] += 1
	if state['accelIndex'] >= state['accelBufferLength']: state['accelIndex'] = 0
	state['accelBuffer'][state['accelIndex']] = vals

######SYNTH PARAMS ########

def calcPitchGlide():
	#print('pitchGlide', state['magnitude'], state['pitchGlideRange'], state['pitchGlideLag'])
	outVal = state['magnitude'] * state['pitchGlideRange']
	outVal = onepole2(state['pitchGlide'], outVal, tuning['pitchGlideLag'])

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
	state['lfoTilt'] = onepole2(state['lfoTilt'], val, 0.98)
	val = val - state['lfoTilt']
	
	#remove small values
	val = clipBipolar(val, 0.02, 1)

	state['lfoLeak'] = leakyInt( state['lfoLeak'], val, tuning['lfoLeak'])
	val = state['lfoLeak']

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

def onepole2(old, new, coefficient):
	if isinstance(new, int) is True or isinstance(new, float) is True:
		old = [old]
		new = [new]
	outVal = [0] * len(old)
	clip (coefficient, 0, 1)

	for i in range(len(old)):
		outVal[i] = (new[i]*(1-coefficient) + old[i]*coefficient)

	if len(outVal) == 1:
		return outVal[0]
	return outVal

def leakyInt(bucket, val, leak):
	bucket *= leak 
	bucket += val
	return bucket

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
