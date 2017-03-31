# Random Forest Classifier for recognizing static gestures

import csv
import math
from sklearn.ensemble import RandomForestClassifier
import numpy as np

################ Functions ################

# function to load in csv data
def load(file) :
	matrix = []
	with open(file) as csvfile :
		data = csv.reader(csvfile, delimiter=',')
		for row in data :
			matrix.append(map(lambda x : float(x), row[:8]))
	return matrix

def loadOutput(file) :
	matrix = []
	with open(file) as csvfile :
		data = csv.reader(csvfile, delimiter=',')
		for row in data :
			matrix.append(map(lambda x : float(x), row)[0])
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
	fingers = []
	imu = []
	fingers.extend(remove(load('pose2.csv'),0,5)[:])
	fingers.extend(remove(load('pose3.csv'),0,5)[:])
	fingers.extend(remove(load('pose4.csv'),0,5)[:])
	fingers.extend(remove(load('pose5.csv'),0,5)[:])
	imu.extend(remove(load('orient1.csv'),5,8)[:])
	imu.extend(remove(load('orient2.csv'),5,8)[:])
	# imu[2] = load('orient3.csv')[5:8]
	# imu[3] = load('orient4.csv')[5:8]
	return fingers, imu

# load test data
def getTestData() :
	testFingers = []
	testIMU = []
	testFingers.extend(remove(load('test1.csv'),0,5)[:])
	testIMU.extend(remove(load('test1.csv'),5,8)[:])
	testFingers.extend(remove(load('test2.csv'),0,5)[:])
	testIMU.extend(remove(load('test2.csv'),5,8)[:])
	testFingers.extend(remove(load('test3.csv'),0,5)[:])
	testIMU.extend(remove(load('test3.csv'),5,8)[:])
	testFingers.extend(remove(load('test4.csv'),0,5)[:])
	testIMU.extend(remove(load('test4.csv'),5,8)[:])
	testFingers.extend(remove(load('test5.csv'),0,5)[:])
	testIMU.extend(remove(load('test5.csv'),5,8)[:])
	
	return testFingers, testIMU

# function to import in data 
def collectData():
	X_Test_pose, X_Test_orient = getTestData()
	X_train_pose, X_train_orient = getGestureClasses()
	Y_train_pose = loadOutput('Y_train_pose.csv')
	Y_train_orient = loadOutput('Y_train_orient.csv')
	return X_train_pose, X_train_orient, Y_train_pose, 
			Y_train_orient, X_Test_pose, X_Test_orient

# function to perform RF classification
def RFClassifier(X_train, Y_train, X_Test, n):
	RF = RandomForestClassifier(n_estimators=n)
	RF.fit(X_train,Y_train)
	prediction = RF.predict(X_Test)
	return prediction

# Function to combine IMU and Finger clustering algorithms 
def combineClassification(imuResults, fingerResults) :
	combination = []
	for i in range(len(imuResults)):
		combination.append(imuResults[i]*10+fingerResults[i])
	return combination

def poseToString(gest) :
	if gest == 0 :
		return "Open Hand"
	if gest == 1 :
		return "Closed Fist" 
	if gest == 2 :
		return "U"
	if gest == 3 :
		return "Cheesy"

def orientationToString(gest) :
	if gest == 0 :
		return "Palm Down"
	if gest == 1 :
		return "Palm Up" 
	# if gest == 2 :
	# 	return "Palm Left"
	# if gest == 3 :
	# 	return "Palm Right"

############ Run the Random Forest ##############
	
X_train_pose, X_train_orient, Y_train_pose, Y_train_orient, 
				X_Test_pose, X_Test_orient = collectData()
trials = 50

# do a grid search over various values of 
for i in range(24):
	estimators = 10*i+10
	avg_corr = 0.0
	err = []
	for k in range(trials): 
		pose_pred = RFClassifier(X_train_pose, Y_train_pose, 
								X_Test_pose,estimators)
		orient_pred = RFClassifier(X_train_orient, Y_train_orient, 
								X_Test_orient,estimators)

		prediction = combineClassification(orient_pred, pose_pred)

		incorrect = 0.0
		correct = 0.0
		testCombos = [[0],[10],[11,1],[12,2],[13,3]]
		for j in range(len(prediction)) :
			if prediction[j] in testCombos[int(j/100)] : correct += 1
			else : 
				incorrect += 1
		err.append(correct/(incorrect+correct))
		avg_corr = (avg_corr*k+(correct/(incorrect+correct)))/(k+1)

	variance = 0
	for error in err :
		variance += math.pow(error-avg_corr,2) 
	print str(avg_corr) + ',' + str(variance/trials)


