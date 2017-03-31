### This is a library file for support functions necessary
### for implementing a kNN-algorithm for time series motions

import csv
import math

# data is in the form of a matrix 
# data is 8 dimensional along feature axis

# function to load in csv data
def load(file) :
	matrix = []
	with open(file) as csvfile :
		data = csv.reader(csvfile, delimiter=',')
		for row in data :
			row = map(lambda x: float(x), row)
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
	training = {}
	imu = {}
	training[0] = load('movinggesture1.csv')
	training[1] = load('movinggesture2.csv')
	training[2] = load('movinggesture1_1.csv')
	training[3] = load('movinggesture2_1.csv')
	training[4] = load('movinggesture1_2.csv')
	training[5] = load('movinggesture2_2.csv')
	imu[0] = remove(load('movinggesture1.csv'),5,8)
	imu[1] = remove(load('movinggesture2.csv'),5,8)
	imu[2] = remove(load('movinggesture1_1.csv'),5,8)
	imu[3] = remove(load('movinggesture2_1.csv'),5,8)
	imu[4] = remove(load('movinggesture1_2.csv'),5,8)
	imu[5] = remove(load('movinggesture2_2.csv'),5,8)
	return training, imu

# 1 = swipe right = gesture1
# 2 = raise hand = gesture2

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

# Function to find K nearest neighbors for a 
# time series of RPY values
def getKNeighbors (k, test, gestclasses):
	distances = []
	gest_idx = 0
	for gesture in gestclasses.values() :
		totaldist = 0
		for i in range(len(test)) :
			totaldist += distance(gesture[i], test[i].tolist()) # Dot product of two matrices
		distances.append((math.sqrt(totaldist)/2.0,gest_idx))
		gest_idx += 1

	distances.sort()
	neighbors = dictionary(len(gestclasses)) 	# dict of gestures and counts
	for dist, gest in distances[:k] :
		neighbors[gest] += 1

	result = max(neighbors, key=neighbors.get)

	return result, distances

# get gesture for a single test point
def getGesture(k,test,TrainingData):
	return getKNeighbors(k, test, TrainingData)
