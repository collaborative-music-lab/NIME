#not imlpemented

enableMsg = [0,0,0,255]
enableMsg[0] = 1;
def setEnables(ser,s):
    print('\nsetting enabled inputs <input#><enableStatus>')
    #time.sleep(0.25)
    for i in range(len(OSC_INDEX_ARRAY)):
        enableMsg[0] = 1; 
        enableMsg[1]=i;
        enableMsg[2]=OSC_ADDRESSES[OSC_INDEX_ARRAY[i]]['enable']
        if( SERIAL_ENABLE ): ser.write(bytearray(enableMsg)) 
        if( WIFI_ENABLE ): s.sendto(bytearray(enableMsg), (clientAddress) ) 
        print('enable', enableMsg[1], enableMsg[2])
        time.sleep(0.025)


    print('\nsetting sensor data rate <input#><dataRateInMS>')
    for i in range(len(OSC_INDEX_ARRAY)):
        enableMsg[0] = 2; 
        enableMsg[1]=i;
        enableMsg[2]=OSC_ADDRESSES[OSC_INDEX_ARRAY[i]]['rate']
        if( SERIAL_ENABLE ): ser.write(bytearray(enableMsg)) 
        if( WIFI_ENABLE ): s.sendto(bytearray(enableMsg), (clientAddress) ) 
        print('rate', enableMsg[1], enableMsg[2])
        time.sleep(0.025)

    print('\nsetting sensor data mode <input#><mode>')
    for i in range(len(OSC_INDEX_ARRAY)):
        enableMsg[0] = 3; 
        enableMsg[1]=i;
        _mode = OSC_ADDRESSES[OSC_INDEX_ARRAY[i]]['mode']
        enableMsg[2]=ANALOG_MODES[_mode]
        if( SERIAL_ENABLE ): ser.write(bytearray(enableMsg)) 
        if( WIFI_ENABLE ): s.sendto(bytearray(enableMsg), (clientAddress) ) 
        print('mode', enableMsg[1], enableMsg[2])
        time.sleep(0.025)