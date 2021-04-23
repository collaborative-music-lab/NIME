import math

class MonoPitch:
	'''use a number of digital values to generate a single output pitch'''
	def __init__(self,numInputs,mode="major", basePitch = 60):
		self.numInputs = numInputs
		self.mode = mode
		self.basePitch = basePitch
		self.curVals = []
		self.customScale = []

	transTable = [1,2,4,7,-7]
	major = [0,2,4,5,7,9,11]
	pent = [0,3,5,7,10]
	

	def input(self,num,val):
		self.curVals[num] = val
		print(self.mode, num)
		return self.output()

	def output(self):
		print(self.mode)

		for i in range(numInputs):
			self.curOutput += transTable[curVals]

		if self.mode == "major":

			self.curOutput = major[self.curOutput%7]
			self.curOutput += floor(self.curOutput/7)*12

		self.curOutput += self.basePitch

		return self.curOutput



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
