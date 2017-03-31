import csv
import math

# data is in the form of arrays of array of arrays
# data is 8 dimensional

def load(file) :
	matrix = []
	with open(file) as csvfile :
		data = csv.reader(csvfile, delimiter=',')
		for row in data :
			matrix.append(row[:8])
	return matrix

# load training data into gesture classes
def getGestureClasses() :
	 # labeled data for each gesture class
	gesture = {}
	gesture[0] = load('gesture1_1.csv')
	gesture[1] = load('gesture1_2.csv')
	gesture[2] = load('gesture1_3.csv')
	gesture[3] = load('gesture1_4.csv')
	gesture[4] = load('gesture1_5.csv')
	gesture[5] = load('gesture2_1.csv')
	gesture[6] = load('gesture2_2.csv')
	gesture[7] = load('gesture2_3.csv')
	gesture[8] = load('gesture2_4.csv')
	gesture[9] = load('gesture2_5.csv')
	gesture[10] = load('gesture3_1.csv')
	gesture[11] = load('gesture3_2.csv')
	gesture[12] = load('gesture3_3.csv')
	gesture[13] = load('gesture3_4.csv')
	gesture[14] = load('gesture3_5.csv')
	gesture[15] = load('gesture4_1.csv')
	gesture[16] = load('gesture4_2.csv')
	gesture[17] = load('gesture4_3.csv')
	gesture[18] = load('gesture4_4.csv')
	gesture[19] = load('gesture4_5.csv')
	gesture[20] = load('gesture5_1.csv')
	gesture[21] = load('gesture5_2.csv')
	gesture[22] = load('gesture5_3.csv')
	gesture[23] = load('gesture5_4.csv')
	gesture[24] = load('gesture5_5.csv')

	return gesture

# load test data
def getTestData() :
	test = {}
	test[0] = load('test1.csv')
	test[1] = load('test2.csv')
	test[2] = load('test3.csv')
	test[3] = load('test4.csv')
	test[4] = load('test5.csv')
	# test[0] = load('test6.csv')
	return test

# test1 = open palm down = gesture1
# test2 = open palm down = gesture2
# test3 = closed fist = gesture3
# test4 = gun = gesture4
# test5 = jackal ears = gesture5
# test6 = tea cup pinky
# test7 = index finger down
# test78 = index finger raised

# calculate distance between 2 N-dimensional vectors
# IMPORTANT: All data values are in angles (degrees)
def distance(x, y) :
	if len(x) != len(y) :
		return "Invalid Vectors" 

	totaldist = 0
	for i in range(len(x)) :
		totaldist += math.pow((float(x[i]) - float(y[i])),2)

	return math.sqrt(totaldist)

# Function to find K nearest neighbors for a given sample 
# and classes of N-dimensional vectors
def getKNeighbors (k, tests, gestclasses):
	results = []
	test_idx = 0
	for test in tests.values() :
		distances = []		# list of (distance, gesture) pairs
		for point in test :	# this is one set of 10 measurements
			gest_idx = 0
			for gesture in gestclasses.values() :
				totaldist = 0
				for gpoint in gesture :
					totaldist += distance(point, gpoint)
				distances.append((totaldist/2.0,int(gest_idx/5.0)))
				gest_idx += 1
		distances.sort()

		neighbors = {0:0,1:0,2:0,3:0,4:0,5:0} 	# dict of gestures and counts
		for dist, gest in distances[:k] :
			neighbors[gest] += 1

		results.append((test_idx, max(neighbors, key=neighbors.get)))
		test_idx += 1

	return results



############## Run the Code
k=1
while k < 16 : 
	print "k : " + str(k) + " | Results : " + str(getKNeighbors(k, getTestData(), getGestureClasses()))
	k += 2
