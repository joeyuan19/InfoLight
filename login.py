import sys
import foursquare
import urllib2 as url2
import urllib as url
import webbrowser
import serial


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
			print value
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

try:
	s = serial.Serial('/dev/tty.usbmodem1421',9600,timeout=0.1)
except:
	print "could not open Port" 
	sys.exit()

base = []
input_data = []

i = 0
n_base_reading = 20
key_length = 296
runs = n_base_reading + key_length
delay = .1

try:
	print "Calibrating..."
	while True:
		try:
			reading = float(s.readline())
			if i < n_base_reading:
				base.append(reading)
			if i == n_base_reading:
				zero, tol = get_stats(base[1:])
				tol += 50
				print "Calibrated to ", zero, "+/-", tol
				print "Enter Key now please"
				delay,std = sync(s,zero,tol)
				wait_delay(s,delay)
			if i > n_base_reading:
				if reading > zero + tol:
					input_data.append(1)
				else:
					input_data.append(0)
				if i%2 == 0:
					wait_delay(s,delay-std)
				else:
					wait_delay(s,delay+std)
			if i >= runs:
				break
			i += 1
		except:
			pass	
	#
	#count = 0.
	#for i in range(key_length):
	#	if input_data[i] == original[i]:
	#		count += 1
	#	print original[i], input_data[i], input_data[i] == original[i]
	#print str(count/key_length) + "%"
finally:
	s.close()

def data_to_binary(input_data):
	return ''.join(str(i) for i in input_data)

data = data_to_binary(input_data)

print data

n = int(data, 2)
access_token = binascii.unhexlify('%x' %n)

client.set_access_token(access_token)

# Get the user's data
user = client.users()

venue_id = '4d0683609d33a14365b8c678'

url = 'https://api.foursquare.com/v2/checkins/add?oauth_token='+access_token+'&venueId='+venue_id

webbrowser.open(url)

