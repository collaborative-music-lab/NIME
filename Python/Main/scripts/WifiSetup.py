import socket, sys, time
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher


def run(WIFI_ENABLE, clientAddress):
	BCAST_HOST = '192.168.1.255'                 # Symbolic name meaning all available interfaces
	BCAST_PORT = 1234              # Arbitrary non-privileged port

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((BCAST_HOST, BCAST_PORT))
	sock.setblocking(0)

	HOST = '192.168.1.100'                 # Symbolic name meaning all available interfaces
	PORT = 1234              # Arbitrary non-privileged port

	if (WIFI_ENABLE):
	    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	    s.bind((HOST, PORT))
	    s.setblocking(0)

	    wifiCounter = 0
	    while True:
	        print  ("checking WiFi. . . ")
	        try: 
	            data, clientAddress = sock.recvfrom(1024) # buffer size is 1024 bytes
	            print ("received message:", data, "address", clientAddress, "length", len(data))
	            if (len(data) > 0):  
	                print("Wifi connected to ", clientAddress)
	                s.sendto(data, (clientAddress) ) 
	                break
	        
	        except socket.error as ex:
	            print("error", ex)
	        
	        
	        time.sleep(0.1)
	        wifiCounter+=1
	        if(wifiCounter>10): 
	            "No wifi connection established"
	            break
	else:
		s = 0
	return s