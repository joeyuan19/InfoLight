import array
import urllib2 as url2
import urllib as url1
import sys
import dropbox
#from Selenium import webdriver

fileName = sys.argv[1]

app_key = 'uqzp24pob7zakxn'
app_secret = 's3pdcfy7zhycxcv'
access_type = "dropbox"

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

authorize_url = flow.start()

"""
session = dropbox.session.DropboxSession(app_key,app_secret,access_type)
request_token = session.obtain_request_token()
webbrowser.open(authorize_url)

selenium.

access_token = "Bnv5cWNiXqUAAAAAAAAAAbVZNYMPAi9QoTX-OODenus"

"""

print '1. Go to:\n' + authorize_url
print '2. Click "Allow" (you might have to log in first)'
print '3. Copy the authorization code.'
code = raw_input("Enter the authorization code here: ").strip()

access_token, user_id = flow.finish(code)


clientDrop = dropbox.client.DropboxClient(access_token)
f = clientDrop.get_file(fileName)
out = open(fileName, 'w')

out.write(f.read())
out.close()

with open(fileName, 'r') as f:
    data = f.read()

publicKey = int(data.split('\n', 1)[0])


import serial
import sys
import time

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
	print "Could not open port, exiting now.."
	sys.exit()


base = []
input_data = []



i = 0
n_base_reading = 20
key_length = 3
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
	return int(''.join(str(i) for i in input_data),2)

privateKey = data_to_binary(input_data) # will be reading this from the LAZORSDNRDNAKDN
s


wholeThing = privateKey * publicKey

key_str = "{0:b}".format(wholeThing)
key_arr = array.array('B',[])

for c in key_str:
    key_arr.append(int(c))

encryptedContent = str(data[2:])


encrypted = array.array('B', encryptedContent)

isLonger = True
tmp_arr = key_arr

while isLonger:
    if len(encrypted) > len(key_arr):
        howLong = len(encrypted) - len(key_arr)
        key_arr = key_arr + tmp_arr
    else:
        isLonger = False

for i in range(len(encrypted)):
    encrypted[i] ^= key_arr[i]

out = open('decrypted.txt', 'w')

out.write(encrypted.tostring())

out.close()

