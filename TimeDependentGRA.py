import math, sys, csv
import kNN_Motion as knn
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
from pykalman import KalmanFilter

plt.rcParams.update({'font.size': 16}) # make text bigger

training, training_imu = knn.getGestureClasses()
fulldata = knn.load('testmotion9.csv')
fingerdata = np.array(knn.remove(fulldata,0,5))
imudata = np.array(knn.remove(fulldata,5,8))

imudata = np.hstack((imudata, np.zeros((100,6))))

freq = 1/50
random_state = np.random.RandomState(0)
transition_matrix = np.array([[1,0,0,freq,0,0,-freq,0,0],
                             [0,1,0,0,freq,0,0,-freq,0],
                             [0,0,1,0,0,freq,0,0,-freq],
                             [0,0,0,1,0,0,0,0,0],
                             [0,0,0,0,1,0,0,0,0],
                             [0,0,0,0,0,1,0,0,0],
                             [0,0,0,0,0,0,1,0,0],
                             [0,0,0,0,0,0,0,1,0],
                             [0,0,0,0,0,0,0,0,1]])
transition_offset = np.array([0,0,0,0,0,0,0,0,0])
observation_matrix = np.eye(9) + random_state.randn(9,9) * 0.05
observation_offset = np.array([0,0,0,0,0,0,0,0,0])
initial_transition_covariance = np.eye(9)
initial_observation_covariance = np.eye(9) + 
                                random_state.randn(9,9) * 0.05
initial_state_mean = imudata[0]
initial_state_covariance = np.array([[freq*freq,0,0,0,0,0,0,0,0],
                                     [0,freq*freq,0,0,0,0,0,0,0],
                                     [0,0,freq*freq,0,0,0,0,0,0],
                                     [0,0,0,0.01*freq,0,0,0,0,0],
                                     [0,0,0,0,0.01*freq,0,0,0,0],
                                     [0,0,0,0,0,0.01*freq,0,0,0],
                                     [0,0,0,0,0,0,0.03*freq,0,0],
                                     [0,0,0,0,0,0,0,0.03*freq,0],
                                     [0,0,0,0,0,0,0,0,0.03*freq]])

# Initialize the Kalman Filter
kf = KalmanFilter(
    transition_matrix,
    observation_matrix,
    initial_transition_covariance,
    initial_observation_covariance,
    transition_offset,
    observation_offset,
    initial_state_mean,
    initial_state_covariance,
    random_state=0
)

# Estimation using Kalman filter
n_timesteps = imudata.shape[0]
n_dim_state = transition_matrix.shape[0]
filtered_state_means = np.zeros((n_timesteps, n_dim_state))
filtered_state_covariances = np.zeros((n_timesteps, 
                                n_dim_state, n_dim_state))
for t in range(n_timesteps - 1):
    if t == 0:
        filtered_state_means[t] = initial_state_mean
        filtered_state_covariances[t] = initial_state_covariance
    filtered_state_means[t + 1], filtered_state_covariances[t + 1] =
         (kf.filter_update(
            filtered_state_means[t],
            filtered_state_covariances[t],
            imudata[t + 1],
            transition_offset=transition_offset,
        )
    )

smoothed_state_estimates = kf.smooth(imudata)[0]
# print smoothed_state_estimates

fulldata = np.hstack((fingerdata,smoothed_state_estimates[:,:3]))

result, distances = knn.getGesture(1,smoothed_state_estimates[:,:3]
                                    ,training_imu)

print "Smoothed Result: " + str(result)
print "Distances: " + str(distances)
