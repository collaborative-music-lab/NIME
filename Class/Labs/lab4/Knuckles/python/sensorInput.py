#knuckles sensor input
#two pots and four buttons

def processInput(*args):
	address = args[0][0]
	val = btoi(args[0][1], args[0][2])

	# I like to write this out longform in case I need
	#to change the order of sensors in a group
	if address == 0: return("/pot1", val)
	elif address == 1: return("/pot0", val)

	elif 10 <= address <= 14:
		#buttons
		if address == 10: return("/sw0", val)
		if address == 11: return("/sw1", val)
		if address == 12: return("/sw2", val)
		if address == 13: return("/sw3", val)



def btoi(high,low):
	#convert two bytes to a single int
	return (high << 8) + low 