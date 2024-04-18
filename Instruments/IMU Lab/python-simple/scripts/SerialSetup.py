import serial, serial.tools.list_ports, sys
import time

def run(SERIAL_ENABLE,port,_baudrate):
    if( SERIAL_ENABLE):
        #find serial port
        curSerialPort = port
        ports = list(serial.tools.list_ports.comports())

        #print ports
        print("available serial ports:")
        for x in range(len(ports)): 
            print(ports[x] )
        print("___")

        #check if cur port is available 
        for x in range(len(ports)):   
            if curSerialPort in ports[x]:
                ser = serial.Serial(curSerialPort)
                #setserial curSerialPort low_latency #https://stackoverflow.com/questions/13126138/low-latency-serial-communication-on-linux
                ser.baudrate=_baudrate
                ser.setDTR(False) # Drop DTR
                time.sleep(0.022)    # Read somewhere that 22ms is what the UI does.
                ser.setDTR(True)  # UP the DTR back
                ser.read(ser.in_waiting) # if anything in input buffer, discard it
                print(curSerialPort + " connected\n")
                SERIAL_ENABLE = 1
            else: 
                print(curSerialPort + " not available\n")  
    else: 
        ser = 0

    return ser

