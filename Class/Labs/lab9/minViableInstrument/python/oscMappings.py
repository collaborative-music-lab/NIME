import math
global dispatcher

#mappings for chester.py
######################
#INCOMING OSC
# handle messages sent from PD
######################

enableIMUmonitoring = 0

def defineOscHandlers():
	pass

def initSynthParams():
	pass

######################
#SENSOR MAPPINGS
#handle data received from interface
######################
state = {
	#placeholders for storing most recent data
	'opto': 0,
	'optoDelta': 0
}

prev = {
	#variables for storing previous sensor data
	'opto': 0
}

tuning = {
	#variables for smoothing filters
	'optoDeltaSmoothing' : 30,
	'optoLimit1': [0.25,0.95, 1],
	'optoLimit2': [0.6, 0., 0.5],
	'optoDeltaScale': 2
}


def mapSensor(add, val):
	global state

	try:
		sensor,num = splitAddress(add)

		if sensor == "/opto":
			state['opto'] = val/4095
			state['optoDelta'] = state['opto'] - prev['opto']
			prev['opto'] = state['opto']

			mapOptoDelta()
			mapOptoPosition()

			pass

		else:
			print("unmapped sensor", sensor, num, val)
			

	except Exception as e:
		print("unrecognized sensorVal", add, val)
		print(e)



######SYNTH PARAMS ########
def mapOptoDelta():
	outVal = state['optoDelta']
	client.send_message('/optoDelta', outVal)
	if outVal < 0:
		sendOSC("optoDelta", outVal, outVal, 20) #instanceNum, paramName, val


def mapOptoPosition():
	val1 = scale(state['opto'], 0.7, 1, tuning['optoLimit1'][0], tuning['optoLimit1'][1], tuning['optoLimit1'][2])
	val1 = clip(val1, 0, 1)
	val2 = scale(state['opto'], 0., 0.7, tuning['optoLimit2'][0], tuning['optoLimit2'][1], tuning['optoLimit2'][2])
	val1 = clip(val1, 0, 1)

	client.send_message('/optoScale1', val1)
	client.send_message('/optoScale2', val2)
	sendOSC("optoScale1", val1, val1, 50)
	sendOSC("optoScale2", val2, val2, 100)
	pass

######################
#Helper functions
######################

def scale(input, inLow, inHigh, outLow, outHigh, curve = 1):
	val = (input-inLow)/(inHigh-inLow)
	val = pow( clip(val,0,1),curve)
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
