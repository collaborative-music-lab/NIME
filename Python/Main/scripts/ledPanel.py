circularMapping =  [35, 44, 51, 58, 49, 40, 33, 26, 28, 60, 56, 24]

class defLed:

	def __init__(self, num):
		self.num=num
		self.x = num/8
		self.y = num%8
		self.r = [0]*4
		self.g = [0]*4
		self.b = [0]*4
		#print("led",self.num,self.x,self.y)
	

	def set(self,ind,red,green,blue):
		cNum = 0 if ind > 3 else ind
		#print("bfore",self.num,cNum,self.r,self.g,self.b)
		self.r[cNum]=red%256
		self.g[cNum]=green%256
		self.b[cNum]=blue%256
		#print("cnum",self.num,cNum,self.r,self.g,self.b)

	def get(self,i):
		return self.r[i],self.g[i],self.b[i]

led = []

def begin():
	for i in range(64):
		led.append(defLed(i))






