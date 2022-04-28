import socket, sys, time, select
# from threading import Event, Thread
# from pythonosc import osc_message_builder
# from pythonosc import udp_client
# from pythonosc.osc_server import AsyncIOOSCUDPServer
# from pythonosc.dispatcher import Dispatcher

class wifiClass:

    # ser = 0
    inputBuffer = []
    packetList2 = []
    ssid = "none"
    password = "none"
    ESP_IP = "192.168.1.1"

     #setup our default wifi interface
    HOST = '0.0.0.0'   # Symbolic name meaning all available interfaces
    PORT = 1235              # Arbitrary non-privileged port

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.HOST, self.PORT))
        self.s.setblocking(0)
        pass

    def setupAP(self,network,password, IP, port=PORT):
        self.ssid = network
        self.password = password
        self.ESP_IP = IP
        self.port = port+1
        #find serial port
    
        wifi_connected = 0
        self.checkConnection(wifi_connected, network, password)


    def checkConnection(self, connected, network, password): 

        #setup a broadcast wifi interface to look for devices
        BCAST_HOST = '192.168.4.255'                # Symbolic name meaning all available interfaces
        BCAST_PORT = self.port-1                           # Arbitrary non-privileged port

        wifi_connected = connected
        if connected == 1: return 1

        print("Looking for ESP32 on " + network + " ip " + BCAST_HOST + " " + str(BCAST_PORT))

        if (1):
            bcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            bcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            bcast.bind(("",BCAST_PORT))

            wifi_connected = 0
            wifiCounter = 0
            while True:
                print  ("checking WiFi. . . ")
                try:
                    bcast_msg = [253,2,1,255]
                    print("send to ", self.ESP_IP, " ", BCAST_PORT, " ",  bcast_msg)
                    self.s.sendto(bytearray(bcast_msg), (self.ESP_IP, BCAST_PORT) )
                    print("broadcast to ", BCAST_HOST, " ", BCAST_PORT, " ", bcast_msg)
                    bcast.sendto( bytearray(bcast_msg) , ('<broadcast>', BCAST_PORT))
                    data, clientAddress = self.s.recvfrom(1024) # buffer size is 1024 bytes
                    print("received", data, clientAddress)
                    if (len(data) > 0):
                        print ("received message:", data, "address", clientAddress, "length", len(data))
                        print("Wifi connected to ", clientAddress)
                        self.s.sendto(data, (clientAddress) )
                        break

                except socket.error as ex:
                    if(0): print("error", ex)

                time.sleep(0.1)
                wifiCounter+=1
                if(wifiCounter>10):
                    print("No wifi connection established")
                    #break

        #return s, clientAddress

        if wifi_connected == 1:  return 1

        return  wifi_connected  


    def available(self):
        escFlag = 0
        #constants for SLIP encoding
        endByte = 255
        escByte = 254
        wifiInput = []
        #print("avail", len(self.packetList2), self.packetList2)

        inready, outready, excready = select.select([self.s], [], [])

        for s in inready:
            try:
                wifiInput = list(self.s.recv(1024))
                #print(wifiInput)
            except Exception as e:
                print(e)
                    #print("wifi input ," wifiInput)

        #print("wfin", len(wifiInput), wifiInput)

        while len(wifiInput) > 0:
            val = wifiInput.pop(0)
            # #print(val)
            if escFlag == 1:
                self.inputBuffer.append(val)
                escFlag = 0
            elif val == escByte:
                escFlag = 1
            elif val == endByte:
                #print("endbyt", packetBuffer, self.inputbuffer)
                self.packetList2.append(self.inputBuffer)
                #self.packetList2 = (self.inputBuffer)
                self.inputBuffer = []
            else:
                self.inputBuffer.append(val)

        _available =  len(self.packetList2)
        #print("avail", len(self.packetList2), self.packetList2)
        return _available

    

    def get(self):
        """Store available incoming data in inputBuffer.

        return a single slip decoded message."""
        # while(len(self.packetList2)>0):
        outVal = self.packetList2.pop(0)
        #print("get", len(self.packetList2),self.packetList2)
        return outVal #remove and return first element of list

    def slipDecodeData(self, data ):
        #print("slipinput",data)
        """Slip encode data and add to output buffer."""
        inputBuffer = []
        escFlag = 0
        for i in data:
            if escFlag == 1:
                inputBuffer.append(i)
                escFlag = 0
            elif i == self.escByte:
                escFlag = 1
            elif i == self.endByte:
                return inputBuffer
            else:
                inputBuffer.append(i)

        return inputBuffer


    def send( self, data ):
        #print("serial.send", data )
        self.comm.write(bytearray(data))


