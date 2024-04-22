#include: wifiSetup and serialSetup
import scripts.SerialSetup3 
ser = scripts.SerialSetup3.serialClass()

import scripts.WifiSetup 

import asyncio
import struct
import time 

class communication:
	"""Class to manage communication with a microcontroller over wifi, serial, or bluetooth."""

	#__mode = "serial" #can be "serial", "wifi", or "bluetooth"
	__outBuffer = bytearray([])

	#constants for SLIP encoding
	endByte = 255
	escByte = 254

	###INIT ################################################################
	def __init__( self, mode, baudrate=115200, wifimode="STA", defaultport="none" ):
		"""1 mandatory argument 'mode': serial, wifi, or bluetooth

		Options:
		baudrate (def 115200): baudrate for serial/bluetooth connection
		wifimode (def STA): STA or AP mode for bluetooth.

		Bluetooth support not added yet."""
		self.__mode=mode
		print("init", self.__mode, baudrate)

		if self.__mode == "wifi" :
			if wifimode=="AP" :
				wf.setupAP()
			else: 
				wf.setupSta()
			print("wifi")
		elif self.__mode == "serial" :
			print(baudrate)
			ser.begin( baudrate, defaultport=defaultport )
			print("serial initialized")
		elif self.__mode == "bluetooth" :
			print("bluetooth support not added yet. . . .")
			#todo


	###SEND ################################################################
	def send(self, data):
		"""Send (bytearray) data buffer to selected comms mode."""
		dataToSend = data
		if type(data) is not list:
			dataToSend = [data]
		returnval = self.slipEncodeData( dataToSend )
		self.sendOutputBuffer()
		return returnval

	def buffer(data):
		returnval = self.slipEncodeData( data )
		return returnval

	###AVAILABLE ################################################################
	def available(self):
		"""returns number of available bytes."""
		returnval = 0
		if self.__mode == "serial":
			returnval = ser.available()
		elif self.__mode == "wifi":
			returnval = wf.available()
		elif self.__mode == "bluetooth":
			pass

		return returnval

	#GET ################################################
	def get(self):
		"""Returns decoded byte array from buffer."""
		returnval = 0

		inputBuffer = []
		if self.__mode == "serial":
			inputBuffer = ser.get()
		elif self.__mode == "wifi":
			inputBuffer = wf.get()
		elif self.__mode == "bluetooth":
			pass
		if inputBuffer == None: return None
		return  inputBuffer 


	#slipDecodeData ################################################
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

	#slipEncodeData ################################################
	def slipEncodeData(self, data ):
		"""Slip encode data and add to output buffer."""

		global  __outBuffer
		for i in data:
			if i == self.endByte:
				self.__outBuffer.append(self.escByte)
				self.__outBuffer.append(i)
			elif i == self.escByte:
				self.__outBuffer.append(self.escByte)
				self.__outBuffer.append(i)
			else :
				self.__outBuffer.append(i)
		return len(data)


################################################################
	def sendOutputBuffer(self):
		"""Add end byte to slip encoded buffer and send it out. 

		Returns number of slip encoded bytes sent."""
		self.__outBuffer

		self.__outBuffer.append(self.endByte)
		returnval = 0
		if self.__mode == "serial":
			returnval = ser.send(self.__outBuffer)
		elif self.__mode == "wifi":
			returnval = wf.send(self.__outBuffer)
		elif __mode == "bluetooth":
			pass

		self.__outBuffer = bytearray(0)
		#print("out array", self.__outBuffer)

		return returnval

