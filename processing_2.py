# A file to process data coming in from the arduino over a 
# serial port to a csv file.

import serial
import time
import sys

# left port is 1411, right port is 1451 (for Mac)

port = "/dev/cu.usbmodem1411"
baudrate = 38400
trash = 25				# first few values are sometimes trash
linesToRead = 50 + trash		

# -- Include ability to enter filename at command prompt -- 
# open a file for storing data
if len(sys.argv) >= 2 : csv = open(sys.argv[1],'w')
else : csv = open('raw_data.csv', 'w')

# open the serial port
ser = serial.Serial(port, baudrate)

# -- change so that data comes in as a 8 or 10 dimension variable

print("Start Gesture in 3...")
time.sleep(1)
print("2...")
time.sleep(1)
print("1...")
time.sleep(1)
print("go")

# read in 100 lines from the Serial port
for _ in range(linesToRead):
	# values to be ignored
	if trash > 0 : 
		data = ser.readline()
		sys.stdout.flush()
		trash -= 1

	# values to be recorded into csv files
	else :
		# read Acceleration Data
		data = ser.readline()
		#sys.stdout.write(data)
		data = data.split()
		if len(data) < 8 : continue
		csv.write(data[0])
		csv.write(",")
		csv.write(data[1])
		csv.write(",")
		csv.write(data[2])
		csv.write(",")
		csv.write(data[3])
		csv.write(",")
		csv.write(data[4])
		csv.write(",")
		csv.write(data[5])
		csv.write(",")
		csv.write(data[6])
		csv.write(",")
		csv.write(data[7])
		csv.write("\n")
		time.sleep(0.04)
		sys.stdout.flush()
		# time.sleep(0.02)

csv.close()
