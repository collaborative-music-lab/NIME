class MonoPitch:
	'''use a number of digital values to generate a single output pitch'''
	def __init__(self,numInputs,mode="major", basePitch = 60):
		self.numInputs = numInputs
		self.mode = mode
		self.basePitch = basePitch
		self.curVals = [0] * self.numInputs
		self.prevVals = [0] * self.numInputs
		self.customScale = []
		self.curOutput = 0
		self.transTable = [-7,1,2,4,7]

	#transTable = [-7,1,2,4,7]
	major = [0,2,4,5,7,9,11]
	pent = [0,3,5,7,10]

	scale = {
		"major" : [0,2,4,5,7,9,11],
		"pent" : [0,3,5,7,10],
		"custom" : [0,2,3,6,7],
		"chromatic" : [0,1,2,3,4,5,6,7,8,9,10,11]
	}

	def customScale(self,curScale):
		self.customScale = curScale

	def setIntervals(self, vals):
		self.transTable = vals


	def input(self,num,val):
		print("input",num,val)
		if(self.curVals[num] != val):
			self.curVals[num] = val
			return self.output()
		else: return(-1,0)

	def output(self):
		output = 0
		velocity = 120

		for i in range(self.numInputs):
			output += self.transTable[i] * self.curVals[i]
			#print("trans", self.transTable[i], self.curVals[i])

		#print("output",output)
		
		if self.mode == "major":
			val=output
			output = self.major[output%7]
			#print(self.curOutput, output, int(self.curOutput/12)*12)
			if val >= 0: output += int(val/7)*12
			else: output += int(val/7-1)*12

		output += self.basePitch
		#print(self.curOutput, output)
		if 1:
		#if output != self.curOutput: 
			self.curOutput = output
			#send note off if no notes down
			if self.heldNotes() == 0: 
				return self.curOutput, 0
			else:	
				return self.curOutput,velocity
		else: 
			return -1, 0


	def heldNotes(self):
		notesDown = 0
		for i in range(self.numInputs):
			notesDown +=  self.curVals[i]
		return notesDown



