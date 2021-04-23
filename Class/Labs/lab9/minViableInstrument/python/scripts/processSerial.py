def from_uint8(val):
	return val;

def from_int8(val):
	return val-128;

def from_uint16(val1, val2):
	return (val1<<8)+val2;

def from_int16(val1, val2):
	return ((val1<<8)+val2)-(1<<15);

def from_uint32(val1, val2,val3,val4):
	return val1<<24+val2<<16+val3<<8+val4;

def from_int32(val1, val2,val3,val4):
	return (val1<<24+val2<<16+val3<<8+val4)-(1<<31);