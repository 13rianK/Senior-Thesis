import csv
import math

# data is in the form of arrays of array of arrays
# data is 8 dimensional

# function to load in csv data
def load(file) :
	matrix = []
	with open(file) as csvfile :
		data = csv.reader(csvfile, delimiter=',')
		for row in data :
			matrix.append(row[:8])
	return matrix

# Function to remove dimensions not necessary
def remove(matrix, start, end) : 
	new_matrix = []
	for vector in matrix :
		new_matrix.append(vector[start:end])
	return new_matrix

# load training data into gesture classes
def getGestureClasses() :
	 # labeled data for each gesture class
	fingers = {}
	imu = {}
	fingers[0] = remove(load('pose1.csv'),0,5)
	fingers[1] = remove(load('pose2.csv'),0,5)
	fingers[2] = remove(load('pose3.csv'),0,5)
	fingers[3] = remove(load('pose4.csv'),0,5)
	fingers[4] = remove(load('pose5.csv'),0,5)
	imu[0] = remove(load('orient1.csv'),5,8)
	imu[1] = remove(load('orient2.csv'),5,8)
	# imu[2] = load('orient3.csv')[5:8]
	# imu[3] = load('orient4.csv')[5:8]
	return fingers, imu

# load test data
def getTestData() :
	testFingers = {}
	testIMU = {}
	testFingers[0] = remove(load('test1.csv'),0,5)
	testIMU[0] = remove(load('test1.csv'),5,8)
	testFingers[1] = remove(load('test2.csv'),0,5)
	testIMU[1] = remove(load('test2.csv'),5,8)
	testFingers[2] = remove(load('test3.csv'),0,5)
	testIMU[2] = remove(load('test3.csv'),5,8)
	testFingers[3] = remove(load('test4.csv'),0,5)
	testIMU[3] = remove(load('test4.csv'),5,8)
	testFingers[4] = remove(load('test5.csv'),0,5)
	testIMU[4] = remove(load('test5.csv'),5,8)
	
	return testFingers, testIMU

# test1 = open palm down = gesture1
# test2 = open palm up = gesture2
# test3 = closed fist = gesture3
# test4 = gun = gesture4
# test5 = jackal ears = gesture5
# test6 = tea cup pinky
# test7 = index finger down
# test78 = index finger raised

givenPose = ["Palm Open", "Closed Fist", "U", "Cheesy"]
givenOrientation = ["Palm Down", "Palm Up", "Palm Down", "None", "None"]

def orientationToString(gest) :
	if gest == 0 :
		return "Palm Down"
	if gest == 1 :
		return "Palm Up" 
	# if gest == 2 :
	# 	return "Palm Left"
	# if gest == 3 :
	# 	return "Palm Right"

def poseToString(gest) :
	if gest == 0 :
		return "Open Hand"
	if gest == 1 :
		return "Closed Fist" 
	if gest == 2 :
		return "U"
	if gest == 3 :
		return "Cheesy"

# calculate distance between 2 N-dimensional vectors
# IMPORTANT: All data values are in angles (degrees)
def distance(x, y) :
	if len(x) != len(y) :
		return "Invalid Vectors" 

	totaldist = 0
	for i in range(len(x)) :
		totaldist += math.pow((float(x[i]) - float(y[i])),2)

	return totaldist

def dictionary(length):
	x = {}
	for i in range(length) :
		x[i] = 0
	return x

# Function to find K nearest neighbors for a given sample 
# and classes of N-dimensional vectors
def getKNeighbors (k, tests, gestclasses):
	results = []
	test_idx = 0
	for test in tests.values() :
		distances = []			# list of (distance, gesture) pairs
		for point in test :		# this is one set of 10 measurements
			gest_idx = 0
			for gesture in gestclasses.values() :
				totaldist = 0
				for gpoint in gesture :
					totaldist += distance(point, gpoint)
					distances.append((totaldist/2.0,gest_idx))
				gest_idx += 1

			distances.sort()
			neighbors = dictionary(len(gestclasses)) 	# dict of gestures and counts
			for dist, gest in distances[:k] :
				neighbors[gest] += 1

			results.append((test_idx, max(neighbors, key=neighbors.get)))
		test_idx += 1

	return results

# Function to combine IMU and Finger clustering algorithms 
def combineClusters(imuResults, fingerResults) :
	# TODO
	return None

############## Run the Code ###############


k=1
trainFingers, trainIMU = getGestureClasses()
testFingers, testIMU = getTestData()
while k <= 50 : 
	print k
	pose = getKNeighbors(k, testFingers, trainFingers)
	orientation = getKNeighbors(k, testIMU, trainIMU)
	print pose
	print orientation
	# for i in range(len(pose)):
	# 	print "Pose : " + str(givenPose[int(i/10)]) + " -- " + str(givenPose[pose[i][1]])
	# 	print "Orientation : " + str(givenOrientation[orientation[i][1]])
	# 	print "\n"
	k += 2
