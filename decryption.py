import serial
import sys
import time

original = [1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0]
def get_stats(base):
	ave = 0
	for n in base:
		ave += n
	ave = ave/len(base)
	std_dev = 0
	for n in base:
		std_dev += (n-ave)**2
	std_dev = (std_dev/len(base))**.5
	return ave, std_dev

def rough_equal(num1,num2,tol):
	return num1 > num2 - tol and num1 < num2 + tol

def sync(s,base,tol):
	delay = []
	light_on = False
	avg = 0
	while True:
		try:
			value = s.readline()
			n = float(value)
			if light_on:
				if rough_equal(n,base,tol):
					delay.append(time.time())
					light_on = False
			else:
				if n > base + tol:
					delay.append(time.time())
					light_on = True
		except:
			pass
		if len(delay) >= 12:
			break
	temp = []
	for i in range(len(delay)-1):
		temp.append(delay[i+1]-delay[i])
	return get_stats(temp)

def wait_delay(s,delay):
	start = time.time()
	while delay > time.time() - start:
		s.readline()


print "Opening serial port"
try:
	s = serial.Serial('/dev/tty.usbmodem1421',9600,timeout=0.1)
except:
	print "exit"
	sys.exit()


base = []
data = []

#original = [0,1,1,0,0,0,0,1,0,1,1,0,0,0,1,0,0,1,1,0,0,0,1,1,0,1,1,0,0,1,0,0,0,0,1,1,0,0,0,1,0,0,1,1,0,0,1,0,0,0,1,1,0,1,0,0,0,0,1,1,0,1,0,1,0,0,1,1,0,1,1,0,0,1,1,0,0,1,1,1,0,1,1,0,1,0,0,0,0,1,1,0,1,0,1,0,0,0,1,0,0,0,0,1,0,1,0,1,0,0,1,0,0,1,0,0,1,0,1,1,0,0,0,0,1,1,0,1,0,0,0,0,1,0,1,0]	


i = 0
n_base_reading = 20
key_length = len(original)
runs = n_base_reading + key_length
delay = .1

try:
	print "begin read"
	while True:
		try:
			reading = float(s.readline())
			if i < n_base_reading:
				base.append(reading)
			if i == n_base_reading:
				zero, tol = get_stats(base[1:])
				tol += 50
				print "Got base reading:", zero, "+/-", tol
				print "Measuring delay"
				delay,std = sync(s,zero,tol)
				print "Done! Found a delay of", delay, "Syncing..."
				wait_delay(s,delay)
				print "Recording data..."
			if i > n_base_reading:
				if reading > zero + tol:
					data.append(1)
				else:
					data.append(0)
				if i%2 == 0:
					wait_delay(s,delay-std)
				else:
					wait_delay(s,delay+std)
			if i >= runs:
				break
			i += 1
		except:
			pass
	count = 0.
	for i in range(key_length):
		if data[i] == original[i]:
			count += 1
		print original[i], data[i], data[i] == original[i]
	print str(count/key_length) + "%"
finally:
	s.close()




