# A file to recognize gestures in real time over the serial port
import serial
import time
import sys
import knn_clustering_realtime as knn

################### Real Time Data Analysis #####################

# Load Training Data
TrainingData = knn.getGestureClasses()

k = 5

# left port is 1411, right port is 1451 (for Mac)

port = "/dev/cu.usbmodem1411"
baudrate = 38400	

# open the serial port
ser = serial.Serial(port, baudrate)

# -- change so that data comes in as a 8 or 10 dimension variable

print("Beginning in 3...")
time.sleep(1)
print("2...")
time.sleep(1)
print("1...")
time.sleep(1)
print("go")

while(1) :
	data = ser.readline()
	data = data.split()
	if len(data) != 8 : continue
	print "Raw Data:" + str(data)
	print knn.getGesture(k, data, TrainingData)
	ser.flush()
	time.sleep(10`) # Update only once every second

# Close upon exit
ser.close()

