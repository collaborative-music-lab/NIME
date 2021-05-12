import math, random
global dispatcher
import threading

#demonstrates controlling WS2811 or similar LEDs connected to the ESP32
# look in oscMappings.py lines 135 & 759

######################
#INCOMING OSC
# handle messages sent from PD
######################

enableIMUmonitoring = 1

def defineOscHandlers():
	print('define')
	dispatcher.map("/clock", updateClocks )

def initSynthParams():
	pass

def updateClocks(add, val):
	clock = val % 64
	#print(clock)
	# for i in range(4):
	# 	client.send_message("/module", 'trig'+str(i))
	# 	client.send_message("/param", state['binRhy'][i])
	# 	sendOSC('trig'+str(i), state['binRhy'][i])
	# checkBinRhy(clock)

def checkBinRhy(clock):
	clock = int(clock % 4)

	for i in range(4):
		vals = intToBits( state['binRhy'][i])
		if(vals[clock] == 1):
			sendOSC('trig' + str(i), 1, 1, 1)




def intToBits(inVal, bits=4):
	vals = [0]*bits
	for i in range(bits):
		vals[i] = inVal % 2
		inVal = math.floor(inVal/2)

	return vals


######################
#SENSOR MAPPINGS
#handle data received from interface
######################
state = {
	#placeholders for storing most recent data
	'switch': [0,0,0,0,0],
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
	'encSw': [0,0],
	'detune': 0,
	'pitches': [24,0,12,-12], #basePitch, offset1, offset2, sub
	'binRhy':[[1,15,3,8],[1,15,3,8],[1,15,3,8],[1,15,3,8]],
	'binRhy2':[[1,15,3,8],[1,15,3,8],[1,15,3,8],[1,15,3,8]],
	'rhyFall':[[.1,.2,.2],[.1,.2,.2],[.1,.2,.2]],
	'oscFall': 0,
	'capTouch': [0]*12,
	'encoder2': 0,
	'encoderBass': 0,
	'tempo': 80,
	'fmFilter': 20
}

prev = {
	#variables for storing previous sensor data
	'accel': [0,0,0], 'gyro': [0,0,0], 'velocity': [0,0,0], 'jerk': [0,0,0],
	'magnitude1': 0,
	'tiltX':0 , 'tiltY':0, 'tiltZ':0, #keep
	'rhyGain': [0,0,0,0],
	#bass params
	'osc1index': 0, 'osc2index': 0, 'oscMix': 0, 'oscGain': 0, 'oscFilter': 0,
	'fmAmp1':0,'fmAmp2':0,'fmAmp3':0,'fmAmp4':0
}


tuning = {
	#variables for smoothing filters
	'magnitudeSmooth': 0.9,
	'magnitudeFade': 0.1,
	'magnitudeGain': 4,
	'tiltSmooth': 0.9,
	'velocitySmooth': 1,
	'lfoScale': 0.4, 
	'lfoLeak': 0.97,
	'fmDepth': 64,
	'pitchGlideLagCurve': 0.5
}

bassPitches = [[0,5,3,10],[0,7,-5]]

pitchset = [[0,3,5,7,10,15,17,19,22], 
[0,2,3,5,7,9,10,12,14,15],
[0,3,7,10,12,15,19,22,24]
]

prevNoteTrigger = [0,0,0,0]
curAmplitude = [0,0,0,0]

def mapSensor(add, val):
	global state

	global maxCapValues
	global curAmplitude
	global prevNoteTrigger

	capTouchThreshold = 0.5
	capProximityThreshold = 0.01

	try:
		sensor,num = splitAddress(add)
		#print(sensor,num)

		if sensor == "/pot":
			if num is 0:
				outVal = scale(val, 0, 4095, 0, 127, 2)
				sendOSC('slope', 55, 'FALL', outVal)
				sendLED(0, outVal,0,255-outVal)
			elif num is 1:
				outVal = scale(val, 0, 4095, 0, 127, 2)
				sendOSC('vca', 71, 'VCA', outVal)
			elif num is 2:
				outVal = scale(val, 0, 4095, 0, 127, 2)
				sendOSC('vca', 72, 'VCA', outVal)
			#print('pot',num,val)

		elif sensor == "/sw":
			state['switch'][num] = val
			updateSwitchVals(num,val)
			client.send_message( "/sw"+str(num), val)

		elif sensor == "/cap":
			#print(sensor, num)
			if num < 4:
				autoScaleCap(num,val) #calibrate capSense range
				scaledVal = val/maxCapValues[num]

				#when pads are being touched
				# envelope adds to amplitude 
				out = clip(scaledVal - capTouchThreshold , 0 , 1) * 127
				#print("vca", num+1, out)
				curAmplitude[num] += out
				#if num is 1: print('vca', num+51, out)
				sendOSC("vca", num+51, "CV", out)

				#FM amount
				out = clip(scaledVal - capTouchThreshold , 0 , 0.6) * 127
				out = onepole(out, 'fmAmp'+str(num+1), 0.5)
				#print("vca", num+1, out)
				if out > 10: 
					sendOSC("vca", num+61, "CV", out)
					sendOSC("vca", num+61, "VCA", scale(out, 10, 127, 0, 127))
				else:
					#small amount of FMwhen in proximity
					out = clip(scaledVal*10 - capProximityThreshold , 0 , 0.2) * 127
					#print("CV", num+1, out)
					sendOSC("vca", num+61, "CV", out)
					sendOSC("vca", num+61, "VCA", 0)

				#when pads are in proximity
				#proximity controls amplitude
				out = clip(scaledVal*10 - capProximityThreshold , 0 , 0.5) * 127
				out = onepole(out, 'fmAmp'+str(num+1), 0.9)
				#print("CV", num+1, out)
				curAmplitude[num] += out
				#print('amp', num, curAmplitude[num],out)
				sendOSC("vca", num+51, "VCA", out)
			
				outAmp = clip(curAmplitude[num]/4, 0, 127)
				sendOSC("monitor"+str(num+1),outAmp,outAmp,outAmp)
				curAmplitude[num] *= 0.75

				if curAmplitude[num] <= 4:
					if prevNoteTrigger[num] == 0: 
						sendOSC("triggerNote", num, num, num)
						print("trig", num)
						prevNoteTrigger[num] = 1
				elif curAmplitude[num] > 60: prevNoteTrigger[num] = 0

			else: #cap number 4 or more
				state['capTouch'][num] = val>200
				#print(num, state['capTouch'])
				outVal = 0
				for i in range(8):
					outVal += state['capTouch'][i+4]*pow(2,i)
				client.send_message("/module", 'trig5')
				client.send_message("/param", outVal)

		elif sensor == "/enc":
			if num == 0 :
				for k in range(3): #rhythm
					if state['switch'][k+1] == 1:
						for i in range(3): #slope
							state['rhyFall'][k][i] += val/40
							#print(k,i,state['rhyFall'][k][i])
							state['rhyFall'][k][i] = clip( state['rhyFall'][k][i], 0, 4)
							#print(k,i,state['rhyFall'][k][i])
							#sendOSC('slope', 1+k*10+i, 'FALL', state['rhyFall'][k][i])
				if state['switch'][4] == 1:
					state['oscFall'] += val/40
					#print(k,i,state['rhyFall'][k][i])
					state['oscFall'] = clip( state['oscFall'], 0, 4)
					#print(state['oscFall'])

			if num == 1 and state['encSw'][num] == 0:
				state['encoder2'] += val
				outVal = clip(state['encoder2'], 0, 127)
				wavefold = [1,1,1,1]
				ladderFilter = [1,1,1,1]
				outVal = scale(outVal, 0, 127, 0, 127)
				for k in range(3):
					sendOSC('wavefold', k*10+1, 'FOLD', outVal*wavefold[k])
					sendOSC('ladder-filter', k*10+1, 'FREQ', outVal*ladderFilter[k])
			elif num == 1 and state['encSw'][num] == 1:
				state['encoderBass'] += val
				outVal = clip(state['encoderBass'], 0, 127)
				wavefold = [1,1,1,1]
				ladderFilter = [1,1,1,1]
				outVal = scale(outVal, 0, 127, 0, 127)

				sendOSC('wavefold', 31, 'FOLD', outVal)
				sendOSC('ladder-filter', 31, 'FREQ', outVal)

			if num == 2:
				state['tempo'] += val
				state['tempo'] = clip(state['tempo'], 40, 200)
				sendOSC('tempo', state['tempo'],state['tempo'],state['tempo'])

			elif num == 3:
				state['fmFilter'] += val
				state['fmFilter'] = clip( state['fmFilter'], 0, 87)
				#print('fmFilter', state['fmFilter'])
				sendOSC('ladder-filter', 51, 'FREQ', state['fmFilter'])
				sendOSC('ladder-filter', 52, 'FREQ', state['fmFilter']+2)
				sendOSC('ladder-filter', 53, 'FREQ', state['fmFilter'] + 4)
				sendOSC('ladder-filter', 54, 'FREQ', state['fmFilter'] + 6)


						
			client.send_message("/enc",  val)
			#print("/enc", num, val)

		elif sensor == "/encsw":
			state['encSw'][num] = val
			#print('encSw', num, val)
			client.send_message("/encSw", val)

		elif sensor == "/acc":
			calcJerk(val)
			calcVelocity(val)
			calcMagnitude(val)
			#calcTiltAccel(val)

			calcBinRhy()
			calcRhyParams()
			calcRhyGain()
			calcBass()
			# calcVoiceGains()
			# calcLPF()
			# calcLFOs()
			# calcPitchGlide()

			### one and only one of the below can be active ###
			#calcAccMagnitude(val, 0.5	)
			sendRawAccel( val)

			prev['accel'] = state['accel']
			state['accel'] = val
		

		elif sensor == "/gyro":
			calcTilt(val)
			sendRawGyro( val)

	except Exception as e:
		print("unrecognized sensorVal", add, val)
		print(e)


def updateSwitchVals(num, val):
	'''use our switches to select pitches from a pitchset'''
	state['switch'][num] = val 

	if num is 4 and val is 1:
		outVal = bassPitches[0][random.randint(0,3)]+bassPitches[1][random.randint(0,2)]
		outVal += 36
		sendOSC('2op-fm', 31, 'CARRIER', outVal)
		sendOSC('2op-fm', 32, 'CARRIER', outVal+7)
		sendOSC('bwl-osc', 1, 'PITCH', outVal+0)
		sendOSC('bwl-osc', 2, 'PITCH', outVal+7)
		sendOSC('bwl-osc', 3, 'PITCH', outVal-5)


	pitchIndex = 0 #which pitch from our set t0 play
	#below we map which switches are pushed down to which pitch we select from our set
	for i in range( len(state['switch']) -  1): pitchIndex += math.pow(2, i) * state['switch'][i+1]

	#we will draw our pitchset from the 'pitchset' array
	pitches = pitchset[state['curPitchset']]
	#and then prepend with -1 to indicate no switch held down
	pitches = [-1] + pitches

	outVal = pitches[int(pitchIndex)]
	state['pitch'] = outVal
	print(state['switch'])
	#don't play if switch 1/2/3 are not held down
	if outVal >=  0:
		outVal += 12 * state['switch'][0] #switch 0 changes ocatve
		#print('pitch', pitchIndex, outVal, pitches)	
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
	val = math.sqrt( math.pow(state['jerk'][0],2) + math.pow(state['jerk'][1], 2) + math.pow(state['jerk'][2], 2))
	
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
	total=0
	for i in range(3):
		outVal[i] = vals[i] - state['accel'][i]
		prev['jerk'][i] = state['jerk'][i]
		state['jerk'][i] = outVal[i]
		total+= abs(outVal[i])
	total = clip(total,0,1)
	sendOSC('vca', 3, 'VCA', 25 + total * 60 )
	sendOSC('vca', 13, 'VCA', 10 + total * 45 )
	sendOSC('vca', 23, 'VCA', 25 + total *60 )
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
######SYNTH PARAMS ########
######SYNTH PARAMS ########
######SYNTH PARAMS ########
######SYNTH PARAMS ########


def calcBinRhy():
	outVal = [0,0,0]
	magThreshold = 0.25
	for i in range(4):
		if(state['switch'][i+1] == 1):
			for k in range(3):
				val = math.floor((state['tilt'][k]+1)*12)
				val = clip(val, 0, 15)
				if(state['switch'][0]==1):
					if(state['magnitude'] < magThreshold): state['binRhy'][i][k] = 0
					else: state['binRhy'][i][k] = val
				else:
					if(state['magnitude'] < magThreshold): state['binRhy2'][i][k] = 0
					else: state['binRhy2'][i][k] = val
				outVal[k] = state['binRhy'][i][k] + state['binRhy2'][i][k]*16
			#print(i, state['binRhy'][i])
			client.send_message("/module", 'trig'+str(i))
			client.send_message("/param", outVal)

def calcRhyParams():
	for i in range(3): #shich switch is down
		if(state['switch'][i+1] == 1):
			for k in range(3): #axis
				val = (state['velocity'][k])
				if k is 0: 
					val = scale(val, -.3, .3, 50, 88)
					val = clip(val, 0, 127)
					sendOSC('2op-fm', i*10+1, "CV2(INDEX)", val)
				elif k is 1: 
					val = scale(val, -.3, .3, 5, 30,2)
					val *= state['rhyFall'][i][k]
					val = clip(val, 0, 127)
					sendOSC('slope', i*10+1, "FALL", val)
					#if i is 2: sendOSC('slope', i*10+1, "RISE", val/5)
				elif k is 2: 
					val = scale(val, -.3, .3, 10, 30,2)
					val *= state['rhyFall'][i][k]
					val = clip(val, 0, 127)
					sendOSC('slope', i*10+2, "FALL", val)


					val = (state['velocity'][k])
					val = scale(val, -.3, .3, 1, 11,2)
					val *= state['rhyFall'][i][k]
					val = clip(val, 0, 127)
					#print(i, val)
					sendOSC('slope', i*10+3, "FALL", val)

					val = (state['velocity'][k])
					val = scale(val, -.3, .3, 77, 61)
					val = clip(val, 64, 127)
					sendOSC('slope', i*10+3, "DEPTH-/+", val)

def calcRhyGain():
	for i in range(3):
		if(state['switch'][i+1] == 1):
			coefficient = 0.5
			outVal = (state['magnitude']*(1-coefficient) + prev['rhyGain'][i]*coefficient)
			outVal *= 0.5
			outVal += 0.5
			outVal -= 0.1
			outVal = clip(outVal, 0, 1)
			prev['rhyGain'][i] = outVal
			#print('rhyGai',state['magnitude'], outVal)
			sendOSC('vca', i*10+1, 'CV',outVal*127)

def calcBass():
	masterFade = 0.95 * state['oscFall']
	masterFade = clip(masterFade, 0, 0.99)

	if (state['switch'][4] == 1):

		#osc 1 index
		coefficient = 0.8 #* state['oscFall']
		coefficient = clip(coefficient, 0,0.95)
		outVal = (abs(state['accel'][0])*(1-coefficient) + prev['osc1index']*coefficient)
		outVal = scale((outVal), 0, 1, 0, 1)
		outVal = clip(outVal, 0, 1)
		prev['osc1index'] = outVal
		#print('osc1 index', outVal)
		sendOSC('2op-fm', 31, 'INDEX',outVal*127)

		#osc 2 index
		coefficient = 0.8 #* state['oscFall']
		coefficient = clip(coefficient, 0,0.95)
		outVal = (abs(state['accel'][1]+0.2)*(1-coefficient) + prev['osc2index']*coefficient)
		outVal = scale((outVal), 0, 1, 0, 1)
		outVal = clip(outVal, 0, 1)
		prev['osc2index'] = outVal
		#print('osc2 index', outVal)
		sendOSC('2op-fm', 32, 'INDEX',outVal*127)

		#osc mix
		coefficient = 0.9 #* state['oscFall']
		coefficient = clip(coefficient, 0,0.95)

		outVal = (abs(state['gyro'][2])*(1-coefficient) + prev['oscMix']*coefficient)
		outVal = scale((outVal), 0, 1, 0, 1)
		outVal = clip(outVal, 0, 1)
		prev['oscMix'] = outVal
		#print('osc1 index', outVal)
		sendOSC('vca', 33, 'VCA',outVal*127)
		sendOSC('vca', 32, 'VCA',127-outVal*127)

		#vca gain
		coefficient = 0.9 #* state['oscFall']
		coefficient = clip(coefficient, 0,0.95)
		magnitude = pow( pow(state['gyro'][0],2) + pow(state['gyro'][1],2) +  pow(state['gyro'][2],2), 0.5)
		outVal = leakyInt(magnitude, 'oscGain', 0.95)
		#outVal = (magnitude*(1-coefficient) + prev['oscMix']*coefficient)
		outVal = scale((outVal), 0, 1, 0, 0.5)
		outVal = clip(outVal, 0, 1)
		prev['oscGain'] = outVal
		#print('osc1 gain', outVal)
		sendOSC('vca', 31, 'VCA',outVal*127)

		#filter freq
		coefficient = 0.6 * state['oscFall']
		coefficient = clip(coefficient, 0,0.95)
		outVal = (abs(state['accel'][1])*(1-coefficient) + prev['oscFilter']*coefficient)
		outVal = scale((outVal), 0, 1, 0, 40)
		outVal = clip(outVal, 0, 127)
		prev['oscFilter'] = outVal
		#print('osc filter', outVal)
		sendOSC('ladder-filter', 1, 'FREQ',outVal)
		#sendOSC('vca', 33, 'VCA',127-outVal)

	else:

		prev['osc1index'] = prev['osc1index'] * masterFade
		sendOSC('2op-fm', 31, 'INDEX', prev['osc1index']*127)

		prev['osc2index'] = prev['osc2index'] * masterFade
		sendOSC('2op-fm', 32, 'INDEX', prev['osc2index']*127)

		# # prev['oscMix'] = prev['oscMix'] * masterFade
		# # sendOSC('2op-fm', 31, 'INDEX', prev['oscMix']*127)

		prev['oscGain'] = prev['oscGain'] * masterFade
		sendOSC('vca', 31, 'VCA', prev['osc1index']*127)
		#print('osc1 gain', prev['oscGain'])

		# prev['oscFilter'] = prev['oscFilter'] * masterFade
		# sendOSC('ladder-filter', 1, 'FREQ',prev['oscFilter'])		


######################
#capSense
#####################
maxCapValues = [100,100,100,100]
def autoScaleCap(num,val):
	global maxCapValues
	maxCapValues[num] = maxCapValues[num] * 0.999
	if val > maxCapValues[num]: maxCapValues[num] = val




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
	num = 0
	digit = 0
	for i in range(len(name)):
		if name[i].isdigit():
			if digit is 0: 
				num += int(name[i])
				digit = 1
			elif digit is 1:
				num = num*10
				num += int(name[i])
		else: out = out + (name[i])
	return out, num

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

def sendLED(num,r,g,b):
	ledColor = [100,int(num),int(r),int(g),int(b)]
	comms.send(ledColor)
	comms.send([110])
	print(ledColor)

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
