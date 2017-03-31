### This is a library file for support functions necessary
### for implementing a real-time kNN gesture recongition
### algorithm. See processing_2_v2.py for real-time GRA

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
	fingers[0] = remove(load('pose2.csv'),0,5)
	fingers[1] = remove(load('pose3.csv'),0,5)
	fingers[2] = remove(load('pose4.csv'),0,5)
	fingers[3] = remove(load('pose5.csv'),0,5)
	imu[0] = remove(load('orient1.csv'),5,8)
	imu[1] = remove(load('orient2.csv'),5,8)
	# imu[2] = load('orient3.csv')[5:8]
	# imu[3] = load('orient4.csv')[5:8]
	return fingers, imu

# 1 = open palm down = gesture1
# 2 = open palm up = gesture2
# 3 = closed fist = gesture3
# 4 = gun = gesture4
# 5 = jackal ears = gesture5
# 6 = tea cup pinky
# 7 = index finger down
# 78 = index finger raised

# Function to turn combination value into string
def combinationToString(value):
	if value == 0 : return "Open Hand Palm Down"
	elif value == 10 : return "Open Hand Palm Up"
	elif value == 1 : return "Closed Fist Palm Down"
	elif value == 11 : return "Closed Fist Palm Up"
	elif value == 2 : return "U with Palm Up"
	elif value == 12 : return "U with Palm Down"
	elif value == 3 : return "Cheesy with Palm Down"
	elif value == 13 : return "Cheesy with Palm Up"
	else : return "No recognized gesture"

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
def getKNeighbors (k, test, gestclasses):
	results = []
	distances = []
	gest_idx = 0
	for gesture in gestclasses.values() :
		totaldist = 0
		for gpoint in gesture :
			totaldist += distance(test, gpoint)
			distances.append((totaldist/2.0,gest_idx))
		gest_idx += 1

	distances.sort()
	neighbors = dictionary(len(gestclasses)) 	# dict of gestures and counts
	for dist, gest in distances[:k] :
		neighbors[gest] += 1

	results.append(max(neighbors, key=neighbors.get))

	return results

# Function to combine IMU and Finger clustering algorithms 
def combineClassification(imuResults, fingerResults) :
	combination = []
	for i in range(len(imuResults)):
		combination.append(imuResults[i]*10+fingerResults[i])
	return combination

# get gesture for a single test point
def getGesture(k,test,TrainingData):
	return combinationToString(combineClassification(getKNeighbors(k, test[5:8], TrainingData[1])
															,getKNeighbors(k,test[:5], TrainingData[0]))[0])
