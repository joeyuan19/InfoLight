import serial
import time
import io


ser = serial.Serial('/dev/tty.usbmodem1421',9600)

for i in range(100):
	print ser.readline()

ser.close()
