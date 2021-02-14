import socket, sys, time
# from threading import Event, Thread
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher

HOST = '192.168.1.100'   # Symbolic name meaning all available interfaces
PORT = 1235              # Arbitrary non-privileged port


clientAddress = ("192.168.1.101",1234)

def run(WIFI_ENABLE, clientAddress):
	BCAST_HOST = '192.168.1.255'                 # Symbolic name meaning all available interfaces
	BCAST_PORT = 2222              # Arbitrary non-privileged port

	if (WIFI_ENABLE):
		bcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		bcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		bcast.bind(("",BCAST_PORT))

		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.bind((HOST, PORT))
		s.setblocking(0)

		wifi_connected = 0
		wifiCounter = 0
		while True:
			print  ("checking WiFi. . . ")
			try:
				print("broadcast")
				bcast.sendto(bytearray([1,1,255]), ('<broadcast>', 1234))
				data, clientAddress = s.recvfrom(1024) # buffer size is 1024 bytes
				print("received", data, clientAddress)
				if (len(data) > 0):
					print ("received message:", data, "address", clientAddress, "length", len(data))
					print("Wifi connected to ", clientAddress)
					s.sendto(data, (clientAddress) )
					break

			except socket.error as ex:
				if(0): print("error", ex)

			time.sleep(0.1)
			wifiCounter+=1
			if(wifiCounter>10):
				"No wifi connection established"
				#break
	else:
		s = 0
	return s, clientAddress

# def send(msg):
# 	s.sendto(msg,clientAddress)

# def recv():
# 	data, address=s.recv(1024)
# 	return data, client

# def broadcastServer(interval, func, *args):
# 	"""Broadcast a server available msg every 5 seconds"""
#     stopped = Event()
#     def loop():
#         while not stopped.wait(interval): # the first call is in `interval` secs
#             func(*args)
#     Thread(target=loop).start()    
#     return stopped.set
