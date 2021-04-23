import math

class ThreeAxis:
	def __init__(self, bufSize=8):
		self.bufSize = bufSize
		self.buffer = [[0]*bufSize]*3
		self.index = [0]*3
		self.cur = [0]*3


	def tilt(self,ox=0,oy=0,oz=0):
		cx = abs(math.atan2(self.cur[1]+ox, -1*self.cur[2]+ox) * (180 / math.pi))
		cy = abs(math.atan2(self.cur[0]+oy, -1*self.cur[2]+ox) * (180 / math.pi))
		cz = (abs((math.atan2(1*self.cur[0]+0, -1*self.cur[1]+0)+oz)) * (180 / math.pi))

		return cx,cy,cz

	def magnitude(self):
		return math.pow(math.pow(self.cur[0],2)+math.pow(self.cur[1],2)+math.pow(self.cur[2],2),1/3)

	def onepole(self,scalar):
		'''simple one pole LPF. Only argument is scalar'''
		val = [0]*3
		for i in range(3):
			val[i] = self.buffer[i][self.index[num]]*(1-scalar) + self.buffer[i][prev(i)]*scalar
		return val[0],val[1],val[2]

	def prev(self,num): 
		val =  self.index[num]-1
		return val if val >= 0 else val+bufSize

	def input(self,x,y,z):
		val = [x,y,z]
		for i in range(3): 
			self.incIndex(i)
			self.cur[i] = val[i]
			self.buffer[i][self.index[num]] = val[i]

	def in1(self,num,val):
		self.incIndex(num)
		self.cur[num] = val
		self.buffer[num][self.index[num]] = val

	def incIndex(self, num):
		self.index[num] += 1
		if self.index[num] >= self.bufSize: self.index[num] = 0

