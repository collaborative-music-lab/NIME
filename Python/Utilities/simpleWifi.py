# # ----- An example UDP client in Python that uses recvfrom() method -----

import socket, time



# # Create an UDP based server socket

# socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# socket.bind(("192.168.1.100", 4141))

# while(True):
#     socket.sendto(bytearray([1,1,255]),("192.168.1.13",1234))
#     msgAndAddress = socket.recvfrom(1024)
#     incName = msgAndAddress[0].decode()
#     print(msgAndAddress)

####################################################################
#################
####################################################################


def run():
    HOST = "192.168.1.100"   # Symbolic name meaning all available interfaces
    PORT = 4141              # Arbitrary non-privileged port

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))

    s.setblocking(0)

    while True:
        print  ("checking WiFi. . . ")
        try:
            s.sendto(bytearray([1,1,255]), ("192.168.1.13", 1234))
            data, clientAddress = s.recvfrom(1024) # buffer size is 1024 bytes
            if (len(data) > 0):
                print ("received message:", data, "address", clientAddress, "length", len(data))
                print("Wifi connected to ", clientAddress)
                s.sendto(data, (clientAddress) )
                #break

        except socket.error as ex:
            print("error", ex)

        time.sleep(0.1)

    else:
        t = 0
    return s

run()