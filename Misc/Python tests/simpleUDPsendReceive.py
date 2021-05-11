import socket, sys, time, select


UDP_IP = "192.168.4.1"
UDP_PORT = 1234
MESSAGE = b"Hello, World!"

myIP = "192.168.4.2"
myPort = 1235

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((myIP, myPort))

while True:
	print("UDP target IP: %s" % UDP_IP)
	print("UDP target port: %s" % UDP_PORT)
	print("message: %s" % MESSAGE)

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
	sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

	data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
	print("received message: %s" % data)

	time.sleep(0.1)

