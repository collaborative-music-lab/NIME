#nobby sensor input
#four pots and four buttons

def processInput(*args):
	address = args[0][0]
	val = bto_ui16(args[0][1], args[0][2])

	# I like to write this out longform in case I need
	#to change the order of sensors in a group
	#print(address, val)
	if address == 0: return("/tine0", val)
	elif address == 1: return("/tine1", val)
	elif address == 2: return("/tine2", val)
	elif address == 3: return("/tine3", val)
	elif address == 4: return("/tine4", val)
	elif address == 5: return("/tine5", val)
	
	elif 10 <= address <= 14:
		#buttons
		#print("button", address)
		if address == 10: return("/sw1", val)
		if address == 11: return("/sw3", val)
		if address == 12: return("/sw0", val)
		if address == 13: return("/sw2", val)



def bto_ui16(high,low):
	#convert two bytes to a single unsigned 16-bit int
	return (high << 8) + low 