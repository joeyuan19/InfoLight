import serial
import sys
import time

original = [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]

print "Opening serial port"
try:
	s = serial.Serial('/dev/tty.usbmodem1421',9600,timeout=0.1)
except:
	print "Port failed to open, exiting now"
	sys.exit()

data = []

avg = 0.
i = 0

listen_time = (.11)*(len(original) + 24)
safe_to_record = False
print_once = True

try:
	s.flushInput()
	s.readline()
	print "Start Read"
	start = time.time()
	while True:
		try:
			value = s.readline()
			value = float(value)
			if not safe_to_record:
				safe_to_record = time.time() - start > .500
			else:
				if print_once:
					print "Base reading taken"
				print_once = False
			if safe_to_record and i > 0 and value > avg/i + 100:
				print "Start data record"
				start = time.time()
				while listen_time > time.time() - start:
					try:
						data.append(float(s.readline()))
					except:
						print "miss"
						pass
			if len(data) > 0:
				break
			i += 1
			avg += value
		except:
			pass
finally:
	s.close()

print data, len(data)

def get_ave(data):
	avg = 0.
	for datum in data:
		avg += datum
	return avg/len(data)

def get_derivative(data):
	d = []
	for i in range(len(data)-1):
		d.append(data[i+1]-data[i])
	return d

def peaks(data,d_data,avg):
	indices = [0] 
	for i in range(1,len(d_data)):
		if d_data[i-1] > 0 and d_data[i] < 0 and abs(d_data[i]) > 100:
			indices.append(i)
		elif d_data[i-1] < 0 and d_data[i] > 0 and abs(d_data[i]) > 100:
			indices.append(i)
	seq = []
	for i in indices:
		if data[i] > avg:
			seq.append(1)
		else:
			seq.append(0)
	return seq
	
def data_to_binary(data):
	ave = get_ave(data)
	
	return peaks(data,der,get_ave(data))



