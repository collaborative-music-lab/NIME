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

prevTine = [0,0,0,0,0,0]

tineBaseline = [0,0,0,0,0,0]

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

		
tineLowPass = [0,0,0,0,0,0]
tineGain = [1,1,2,1,2,1]

def processTine(num, val):
	num = 5-num
	#global prevTine, tineBaseline
	if tineBaseline[num] == 0:
		tineBaseline[num] = val
	if tineBaseline[num] > val:
		tineBaseline[num] = 0.999*tineBaseline[num]  + 0.001*val
	else:
		tineBaseline[num] = 0.9*tineBaseline[num]  + 0.1*val

	curVal = (tineBaseline[num] - val)

	curVal = curVal * tineGain[num]

	if curVal < 50: curVal = prevTine[num]*0.8 + curVal*.2

	curVal = 0 if (curVal < 5) else curVal-5

	prevTine[num] = curVal
	# if num == 5:
	# 	print(val, curVal)

	print( prevTine)

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


