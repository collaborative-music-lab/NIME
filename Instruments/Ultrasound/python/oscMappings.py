import math, time
global dispatcher
from sensorInterfaces.m370_sensor import sensor as sensor 

######################
#INCOMING OSC
# handle messages sent from PD
######################

def defineOscHandlers():
	dispatcher.map("/clock", clock)
	dispatcher.map("/setPitches", setPitches)

def clock(*args):
	#global prevTime
	t.update() #reset timeout
	curBeat = args[2]%16

def setPitches(*args):
	print(args)
	for i in range (len(string_pitches)):
		sendOSC('basic-osc', i*10 + 1, 'PITCH', string_pitches[int(args[1])][i] + octave*12)


######################
#SENSOR MAPPINGS
#handle data received from interface
######################

string_pitches = [
	[0, 2, 4, 7, 9],
	[0, 3,5,7,10],
	[0, 3,5,7,11],
	[0, 4,7,11,14]
]
octave = 4

# pot = []
# for i in range(4):
# 	pot.append( sensor(0, 10) ) #initial value, changeThreshold

# #change threshold for synth range pot
# pot[0].changeThreshold = 50

def mapSensor(add, val):

	if add == "/sw0": 
		if val == 1:
			pass

	elif add == "/ultra":
		processUltra(val)

prevUltra = 0
lowPassUltra = 0

		
def processUltra(val):
	global prevUltra, lowPassUltra

	# if val < 80:
	#  	print("ultra", val)

	range = 10

	#if( int(val/20) != int(prevUltra/20)):
	if val < 100:
		sendOSC("trigger", int(val/range)+1, int(val/range)+1, int(val/range+1 ))
		print(val/range)

	prevUltra = val

	coeff = .01

	lowPassUltra = val*coeff + lowPassUltra*(1-coeff)
	lowPassUltra = 0 if lowPassUltra<0  else 120 if lowPassUltra>120  else lowPassUltra

	decay = 127 - lowPassUltra
	
	sendOSC("slope", 1, "FALL", decay)
	#print(lowPassUltra)




	
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


