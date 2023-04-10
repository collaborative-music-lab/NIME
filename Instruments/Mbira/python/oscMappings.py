import math, time
global dispatcher
from sensorInterfaces.m370_sensor import sensor as sensor 

######################
#INCOMING OSC
# handle messages sent from PD
######################

def defineOscHandlers():
	dispatcher.map("/clock", clock)

def clock(*args):
	#global prevTime
	t.update() #reset timeout
	curBeat = args[2]%16



######################
#SENSOR MAPPINGS
#handle data received from interface
######################


# pot = []
# for i in range(4):
# 	pot.append( sensor(0, 10) ) #initial value, changeThreshold

# #change threshold for synth range pot
# pot[0].changeThreshold = 50

def mapSensor(add, val):
	global prevTine

	if add == "/tine0": 
		processTine(0, val)
		#print("tine0 ", val)
	elif add == "/tine1": 
		processTine(1, val)
		#print("tine1 ", val)
	elif add == "/tine2": 
		processTine(2, val)
		#print("tine2", val)
	elif add == "/tine3": 
		processTine(3, val)
		#print("tine3 ", val)
	elif add == "/tine4": 
		processTine(4, val)
		#print("tine4 ", val)
	elif add == "/tine5": 
		processTine(5, val)
		#print("tine5 ", val)

prevTine = [0]*6
tineBaseline = [0]*6
tineLowPass = [0]*6
tineGain = [1,1,2,1.5,2.5,1.5]
deltaTine = [0]*6
accelTine = [0]*6
tineVal = [0]*6

def processTine(num, val):
	num = 5-num #reverse order of tines

	tineVal[num] = val
	#if abs(tineVal[num]) < 5: tineVal[num] = 0
	if num == 5: print(tineVal)

	#update baseline data
	if tineBaseline[num] == 0:
		tineBaseline[num] = val
	if tineBaseline[num] > val:
		tineBaseline[num] = 0.999*tineBaseline[num]  + 0.001*val
	else:
		tineBaseline[num] = 0.9*tineBaseline[num]  + 0.1*val


	curVal = (tineBaseline[num] - val)

	# tineVal[num] = curVal
	# if abs(tineVal[num]) < 5: tineVal[num] = 0
	# if num == 5: print(tineVal)

	curVal = curVal * tineGain[num]
	curVal = prevTine[num]*0.8 + curVal*.2
	#offset small values
	curVal = 0 if (curVal < 5) else curVal-5

	#lowpass filter for small values
	if curVal < 20: curVal = prevTine[num]*0.9 + curVal*.1
	elif curVal < 15: curVal = prevTine[num]*0.5 + curVal*.5
	#lowpass filter for high values
	else : curVal = prevTine[num]*0. + curVal*1

	if curVal < 1: curVal = 1

	#calculate sudden changes
	delta = curVal - prevTine[num]
	#if abs(delta) <5: delta = 0
	accelTine[num] = delta - deltaTine[num]
	deltaTine[num] = delta
	accelThreshold = .5 * curVal + .1
	if accelTine[num] <accelThreshold: accelTine[num] = 0
	elif accelTine[num]>accelThreshold: 
		accelTine[num] = accelTine[num]-accelThreshold
		sendOSC('vca', num*10+1, 'CV', accelTine[num] * 20 + 25)
		sendOSC('trigger', num+1, num+1, num+1)
		#print(accelTine[num]-accelThreshold)
	else: accelTine[num] = accelTine[num] - accelThreshold
	#if num == 5: print(prevTine)

	# deltaThreshold = .1
	# if delta <deltaThreshold: deltaTine[num] = 0
	# elif delta>deltaThreshold and delta-deltaThreshold > deltaTine[num]: 
	# 	deltaTine[num] = delta-deltaThreshold
	# 	sendOSC('vca', num*10+1, 'CV', deltaTine[num] * 4 + 25)
	# 	sendOSC('trigger', num+1, num+1, num+1)
	# 	print(delta-deltaThreshold)
	# else: deltaTine[num] = delta - deltaThreshold

	prevTine[num] = curVal
	#if num == 5: print(prevTine)

	# if num == 5:
	#print( deltaTine)
	#if abs(deltaTine[num]) > 5: print(deltaTine[num])

	pitches = [48,52,55,60,64,67]

	#sendOSC('basic-osc', num*10 + 1, 'PITCH', pitches[num]	)
	sendOSC('vca', num*10+1, 'VCA', curVal)

	
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


