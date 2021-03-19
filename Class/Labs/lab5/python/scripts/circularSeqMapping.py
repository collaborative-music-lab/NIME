import scripts.seq as sequencer
import sensorInterfaces.capToggle as capToggle

seq = []
for i in range(4):
	seq.append(sequencer.defSeq(8)) #number of instances, number of steps

#placeholders for  OSC client and server
server = None
client = None
panel = None
ser = None

#global variables
numSteps = 8

#button switch modes for encoder
bRotate =  0
bRate =  0
bPitch =  0
bTrigger =  0

#available  modes for encoder
rotate  = [0,0,0]
rate = [0,0,0]
pitch = [0,0,0]
x = [0,0,0]
y =  [0,0,0]

def input(name, num, val):
	outputArray = []

	if name == "cap":
		#print("cap", num, val)
		outputArray.append(  processCap(num,val)  )
		#client.send_message("/test/" + str(num), val)


	elif name == "dial":
		#print("dial", num, val)
		client.send_message("/dial/" + str(num), val)

	elif name == "button":
		if  num == 1: bRotate = val
		elif num == 3: bRate = val
		elif num == 2: bPitch = val
		elif num == 0: bTrigger = val
		#print("button", num, val)

	elif name == "encoder":
		processEncoder(num,val)
		#print("encoder", num, val)
		client.send_message("/encoder/" + str(num), val)
	# else:
	# 	print("unknown signal", name, num, val)

	return outputArray

############################################################
########## encoder
############################################################
def processEncoder(num, val):
	if bRotate==1: 
		rotate[num] = (rotate[num] + val/4  + numSteps) % numSteps
		client.send_message("/rotate/"+str(num), rotate[num])
	elif bRate==1:
		rate[num] = rate[num] + val/4
		rate[num] = 16 if rate[num] > 16 else rate[num]
		rate[num] = 1 if  rate[num] < 1 else rate[num]
		client.send_message("/rate/"+str(num), rate[num])
	elif bPitch==1:
		pitch[num] = pitch[num] + val/4
		pitch[num] = 16 if pitch[num] > 16 else pitch[num]
		pitch[num] = 1 if  pitch[num] < 1  else pitch[num]
		client.send_message("/pitch/"+str(num), pitch[num])
	else:
		x[num] += val/4
		client.send_message("/encoder/"+str(num), x[num])


############################################################
########## capsense
############################################################


capMinMax = [[10000,1] for i in range(13)]

seq[0].led = [22,23,31,39,38,37,29,21]
seq[1].led = [46,47,55,63,62,61,53,45]
seq[2].led = [43,44,52,60,59,58,50,42]
offScalar = 0.01

#ledcolors
ledColors = [
	[227,121,16],
	[217,18,4],
	[194,27,190]
]

prevTouch =  [0,0,0]
lastEnable = 0
prevSeq = [0,0,0,0,0,0,0,0]*3
curTouched = [0]*8

def processCap(pad, inVal):
	global prevSeq
	global lastEnable
	if pad == 0: print("processCap", pad, inVal)

	val = inVal[1]
	touch = inVal[0]
	if pad < 8: curTouched[pad] =  touch

	if touch == 1 and pad < 12:
		 #print("pad", capMinMax[pad])
		 if capMinMax[pad][0] > val:
			 capMinMax[pad][0] = val
			 #print("min", pad, capMinMax[pad][0])
		 elif capMinMax[pad][1] < val:
			 capMinMax[pad][1] = val
			 #print("max", pad, capMinMax[pad][1])

	#only update selected sequence
	enable = [0]*4
	if 7 <pad < 12:
		#print("pad",pad-8,  touch)
		seq[pad-8].enable(touch)

	elif pad == 12:
		address = "/cap/proximity"
		#print("osc", address, steps)
		client.send_message(address,val)

	elif pad < 8:
		for i in range(3):
			if seq[i].enable() == 1:
				lastEnable=i
				prev=prevTouch[i]
				prevTouch[i] = touch
				#print("touch", i, touch-prev)
				if touch - prev == 1:
					
					den = capMinMax[pad][1]-capMinMax[pad][0] #check ranges  are ok
					if(den != 0):

						scaledVal = (val*touch- (capMinMax[pad][0]))/(capMinMax[pad][1]-capMinMax[pad][0])
						scaledVal=1
						cur = seq[i].getStep(pad) > 0
						print("cur",i,pad,cur, scaledVal)
						if cur == False:  seq[i].setStep(pad,1)
						else: seq[i].setStep(pad,0)
						print("seq",i,pad,seq[i].getStep(pad), scaledVal)
						address = "/cap/step/" + str(i)
						steps = [i] + seq[i].get()
						#print("osc", address, steps)

						client.send_message(address,steps)

						return(i, pad, seq[i].getStep(pad))
	#if no sequencers are enabled
	if (seq[0].enable()+seq[1].enable()+seq[2].enable())==0:
		if pad  <  8:
			curSeq = seq[lastEnable].get()
			print("last", lastEnable, "ccurSeq[0]", curSeq[0], "touch0", curTouched[0])
		
			#	for i in range(8):	curSeq[i] = 1 if curTouched[i]==1 else curSeq[i]
			print("post", lastEnable, "ccurSeq[0]", curSeq[0], "touch0", curTouched[0])
			# if pad == 0 :
			# 	print ("lastEnable", lastEnable)
			# 	print ("touch", curTouched)
			# 	print("cur", curSeq)
			# 	print("prev",  prevSeq[lastEnable])
			# if  curSeq  != prevSeq[lastEnable]:
			# 	print("last", lastEnable, "val", curSeq)
			# 	prevSeq[lastEnable]=curSeq
			# 	address = "/cap/step/" + str(lastEnable)
			# 	client.send_message(address,curSeq)
			# 	return(lastEnable, pad, curSeq[pad])


