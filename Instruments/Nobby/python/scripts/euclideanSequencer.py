import math, time

#########
#EUCLIDIAN SEQUENCER
#########
class Euclid:
	beats = 16
	pulses = 3
	rotation = 8
	bucket = 0
	prevBeat = -1

	pattern = []

	def __init__(self,beats,pulses,rotation=0):
		self.setBeats(beats)
		self.setPulses(pulses)
		self.rotation = rotation

	def setBeats(self,num):
		self.beats = num
		if self.pulses > self.beats:
			self.pulses = self.beats
		self.calcPattern()

	def setPulses(self,num):
		val = math.floor(num)
		if val != self.pulses: 
			self.pulses = val
			if self.pulses > self.beats:
				self.pulses = self.beats
			self.calcPattern()
			#print("euclid", self.pattern)

	def set(self, pulses, beats=8, rotation=0):
		self.setBeats(beats)
		self.setPulses(pulses)
		self.rotation=rotation

	def calcPattern(self):
		self.pattern = []
		for i in range(int(self.beats)):
			self.bucket += self.pulses
			if self.bucket > self.beats:
				self.bucket -= self.beats
				self.pattern.append(1)
			else: self.pattern.append(0)
		#print("pattern", len(self.pattern), self.pattern)

	def get(self,_beat):
		if _beat != self.prevBeat:
			self.prevBeat = _beat
			num = int((_beat+self.rotation)%self.beats)
			return self.pattern[num]
		else: return 0

	def length(self): return self.beats