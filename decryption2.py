import serial
import sys
import time

original = [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]

print "Opening serial port"
try:
	s = serial.Serial('/dev/tty.usbmodem1421',9600,timeout=0.1)
except:
	print "Port failed to open, exiting now"
	sys.exit()

data = []

avg = 0.
i = 0

listen_time = (.1 + .013)*(len(original) + 12)

try:
	s.flushInput()
	start = time.time()
	print "Start Read"
	safe_to_record = False
	while True:
		try:
			value = s.readline()
			value = float(value)
			if not safe_to_record:
				safe_to_record = time.time() - start > .500
			if not safe_to_record and i > 0 and value > avg/i + 100:
				start = time.time()
				print "Start data record"
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

def get_avg(data):
	avg = 0.
	for datum in data:
		avg += datum
	return avg/len(data)

print data, len(data)

freq = len(data)/len(original)

itr = freq/2
for i in range(len(original)):
	pass


