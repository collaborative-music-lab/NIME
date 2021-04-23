class simpleSeq:
	isNew=0

	def __init__(self,size):
		self.touchStates=[0]*size
		self.prevStates=[0]*size

	def toggle(self, num, val):
		if (val&1) > self.prevStates[num]: #only happens on transition from 0 to 1
			self.touchStates[num] = 0 if (self.touchStates[num] == 1) else 1
			self.isNew = 1
		else: self.isNew=0
	
		self.prevStates[num]=val&1
		return self.touchStates, self.isNew

seq  = [simpleSeq(8),simpleSeq(8),simpleSeq(8),simpleSeq(8)]
whichSeq = 0
prevSeq = 0
prevVal = [0] * 8

def input(num,val):
	#print("input",num,val)
	isNew=0
	global whichSeq, prevSeq, prevVal
	
	if 7 < num < 12 :
		if val == 1:
			whichSeq = num-8
			if prevSeq != whichSeq:
				print("seqNum", whichSeq)
				prevSeq=whichSeq
				isNew=1

	if num<8:
		val,isNew = seq[whichSeq].toggle(num,val)
	
	address = "/cap/seq/"+ str(whichSeq)
	if(isNew): val = seq[whichSeq].touchStates
	else: val = [0,0]

	#print(isNew,"new",val)


	return address,val, isNew
