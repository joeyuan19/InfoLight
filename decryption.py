import serial
import sys


try:
	s = serial.Serial('/dev/tty.usbmodem1421',9600)
except:
	try:
		s = serial.Serial('/dev/tty.usbmodem1411',9600)
	except:
		print "exit"
		sys.exit()

def process_base(base):
	ave = 0
	for n in base:
		ave += n
	return ave/len(base), 50

def rough_equal(num1,num2,tol):
	return num1 > num2 - tol and num1 < num2 + tol


base = []
header = []
data = []

i = 0
n_base_reading = 10
runs = n_base_reading + 10

while True:
	try:
		reading = float(s.readline())
		if i < n_base_reading:
			base.append(reading)
		elif i == n_base_reading:
			zero, tol = process_base(base)
			print "Got base reading:", zero, "+/-", tol
			print "waiting for header",
			while len(header) < 5:
				print len(header),
				try:
					reading = float(s.readline())
					if reading > zero + 2*tol:
						header.append(reading)
					else:
						header = []
				except:
					pass
			print "Done!\nRecording data..."
		if i > n_base_reading:
			if rough_equal(reading,zero,tol):
				data.append(0)
			else:
				data.append(1)
		if i > runs:
			break
		print i, reading
		i += 1
		sys.wait(500)
	except:
		print "error"

print data







