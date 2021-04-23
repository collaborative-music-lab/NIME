class defSeq:
	"""Sequencer class which parses input, stores values, and maps to  LEDs."""

	def __init__(self, size):
		self.step = [0] * size
		self.size = size #length of the sequence
		self.enableEdit = 1 #does input affect the sequence
		self.led = [] #array for led numbers

	def set(self,val):
		self.step = val

	def setStep(self,num, val):
		#print("seq.py",num,val)
		cnum = (self.size-1) if num >= self.size else num
		self.step[cnum] = val

	def getStep(self,num):
		cnum = (self.size-1) if num >= self.size else num
		return self.step[cnum]

	def get(self):
		return self.step

	def enable(self, val=None):
		if val is not None:
			self.enableEdit = val
		return self.enableEdit

	def clear():
		for i in range(self.size):
			self.step[i]=0

	def rotate(val):
		amt = 1 if val > 0 else -1

		if amt > 0: temp = self.step[0] 
		else: temp = self.step(self.size-1
			)
		for i in range(self.size-1):
			self.step[i] = self.step[i+amt]

		if amt > 0 : self.step[self.size-1] = temp
		else: self.step[0] = temp

# seq=[]

# def begin(num, steps):
# 	for i in range(num):
# 		seq.append(defSeq(steps))