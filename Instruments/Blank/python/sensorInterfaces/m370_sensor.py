import math

class sensor:

	def __init__(self, val=0, changeThreshold = 1):
		self.val = val
		self.prev = 0
		self.changeThreshold = changeThreshold
		print(self.changeThreshold)

	def new(self, val):
		self.val = val
		return self.changed(self.val)

	def changed(self,val):
		if abs(val - self.prev) >= self.changeThreshold:
			self.prev = val
			return val
		else:
			return None

	def val(self, _val):
		return self.val
