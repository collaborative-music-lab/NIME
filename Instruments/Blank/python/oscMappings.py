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

	if add == "/sw0": 
		if val == 1:
			pass

		



	
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


