import sensorInterfaces.pitchMappings as pitchMappings
import sensorInterfaces.imuProcessing as imuProcessing

valveMap = [-7,1,2,4,8]
mono = pitchMappings.MonoPitch(5,"major")
imu = imuProcessing.ThreeAxis()
mono.setIntervals(valveMap)


#https://stackoverflow.com/questions/437589/how-do-i-unload-reload-a-python-module

# def input(incAddress, incVal):
# 	address = "/"
# 	if currentMessage[0] == 50: address += "enc"
# 	elif currentMessage[0] == 99: address += "hall"
# 	elif currentMessage[0] == 100: address += "rotary"
# 	elif currentMessage[0] == 101: address += "switch"
# 	val = (currentMessage[1]<<8) + currentMessage[2] - (1<<15)

# 	address = "/"

# 	#if name == "/enc":

# 	return address,msg;

def scale(val,inlow,inhigh,outlow,outhigh,curve=1):
	val = (val-inlow)/(inhigh-inlow)
	if val >= 0: val = pow(val,curve)
	else: val = pow(abs(val),curve)
	val = val*(outhigh-outlow) + outlow
	return val

def input(client, currentMessage):
	address = currentMessage[0]

	if 0 <= address <= 5:
		buttonNums = {
			50:0, 53:1, 52:2, 51: 3
		}
		address = "/hall/" + str(address)
		val = (currentMessage[1]<<8) + currentMessage[2] - 32768
		client.send_message(address, val) 
	elif 10 <= address <= 15:
		address = "/sw/" + str(address-10)
		val = currentMessage[1];
		client.send_message(address, val)

		address = "/pitch"
		note,velocity = mono.input(currentMessage[0]-10,val)
		#print(note, velocity)
		if note > 0 : client.send_message(address, [note,velocity])
	elif 20 <= address <= 25:
		address = "/enc/" + str(address-20)
		#val = (currentMessage[1]<<8) + currentMessage[2]- 32768
		#print("enc", currentMessage)
		val = (currentMessage[1]) 
		client.send_message(address, val)
	elif 100 <= address <= 102:
		axis = address-100
		val = (currentMessage[1]<<8) + currentMessage[2]- 32768
		imu.in1(axis,val/32768)

		if axis == 2:
			address = "/imu/tilt"
			x,y,z = imu.tilt(0,0,2)
			client.send_message(address, [x,y,z])
			client.send_message("/imu/magnitude", imu.magnitude())
	#else: return
	#print(address)
	#address, val = valveMap.input(address, val)
	#client.send_message(address, val)