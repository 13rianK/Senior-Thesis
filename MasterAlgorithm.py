# Example of interaction with a BLE UART device using a UART service
# implementation.
# Author: Tony DiCola
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART
import math, sys, csv, os, time
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
from pykalman import KalmanFilter

cmd = """
osascript -e 'tell application "System Events" to keystroke "m" 
    using {command down}' """
right = """
osascript -e 'tell application "System Events" to key code 124'
"""
left = """
osascript -e 'tell application "System Events" to key code 123'
"""

# Get the BLE provider for the current platform.
ble = Adafruit_BluefruitLE.get_provider()

# function to load in csv data
def load(file) :
    matrix = []
    with open(file) as csvfile :
        data = csv.reader(csvfile, delimiter=',')
        for row in data :
            matrix.append(map(lambda x: float(x), row[5:8]))
    return matrix

def getData(uart):
    while (1):
        d1 = uart.read(timeout_sec=5)
        d2 = uart.read(timeout_sec=5)
        d3 = uart.read(timeout_sec=5)
        if d1 is not None and d2 is not None and d3 is not None : 
            if d1[0] == 'A' :
                if d2[0] == 'B': data = d1[1:]+' '+d2[1:]+' '+d3[1:]
                else : data = d1[1:]+' '+d3[1:]+' '+d2[1:]
            elif d1[0] == 'B' :
                if d2[0] == 'A' : data = d2[1:]+' '+d1[1:]+' '+d3[1:]
                else : data = d3[1:]+' '+d1[1:]+' '+d2[1:]
            else :
                if d2[0] == 'A': data = d2[1:]+' '+d3[1:]+' '+d1[1:]
                else : data = d3[1:]+' '+d2[1:]+' '+d1[1:]

            data = data.split()
            if len(data) == 11 : 
                try :
                    data = map(lambda x: float(x), data)
                    return data
                except : continue # Failed to map floats onto vector
            else : continue	# Failed to get the right size vector

# specify parameters
freq = 1/20
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
initial_observation_covariance = np.eye(9) + random_state.randn(9,9) * 0.05
initial_state_mean = np.array(np.array([0,0,0,0,0,0,0,0,0]))
initial_state_covariance = np.array([[freq*freq,0,0,0,0,0,0,0,0],
                                     [0,freq*freq,0,0,0,0,0,0,0],
                                     [0,0,freq*freq,0,0,0,0,0,0],
                                     [0,0,0,0.01*freq,0,0,0,0,0],
                                     [0,0,0,0,0.01*freq,0,0,0,0],
                                     [0,0,0,0,0,0.01*freq,0,0,0],
                                     [0,0,0,0,0,0,0.03*freq,0,0],
                                     [0,0,0,0,0,0,0,0.03*freq,0],
                                     [0,0,0,0,0,0,0,0,0.03*freq]])
n_timesteps = 20
n_dim_state = transition_matrix.shape[0]
filtered_state_means = np.zeros((n_timesteps, n_dim_state))
filtered_state_covariances = np.zeros((n_timesteps, n_dim_state, n_dim_state))
filtered_state_means[0] = initial_state_mean
filtered_state_covariances[0] = initial_state_covariance

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

def main():
    ble.clear_cached_data()

    # Get the first available BLE network adapter and make sure it's powered on.
    adapter = ble.get_default_adapter()
    adapter.power_on()
    print('Using adapter: {0}'.format(adapter.name))
    print('Disconnecting any connected UART devices...')
    UART.disconnect_devices()

    # Scan for UART devices.
    print('Searching for UART device...')
    try:
        adapter.start_scan()
        device = UART.find_device()
        if device is None:
            raise RuntimeError('Failed to find UART device!')
    finally:
        # Make sure scanning is stopped before exiting.
        adapter.stop_scan()

    print('Connecting to device...')
    device.connect()  # Will time out after 60 seconds

    try:
        # Wait for service discovery to complete for UART service
        print('Discovering services...')
        UART.discover(device)

        uart = UART(device)

        dataIMU = []
        dataFlex = []
        t = 0

        # Fill in initial data buffer
        while len(dataIMU) < n_timesteps :
            t += 1
            raw = getData(uart)
            IMU = raw[5:]
            IMU.extend([0,0,0])
            dataIMU.append(IMU)
            dataFlex.append(raw[:5])
            filtered_state_means[len(dataIMU)-1], 
              filtered_state_covariances[len(dataIMU)-1] = (
                    kf.filter_update(
                        filtered_state_means[len(dataIMU)-2],
                        filtered_state_covariances[len(dataIMU)-2],
                        dataIMU[len(dataIMU)-1],
                        transition_offset=transition_offset
                    )
                )

        pl.figure()
        pl.ion()
        while(t < 50):
            t+=1
            # Collect the data
            dataIMU.pop(0)
            dataFlex.pop(0)
            np.delete(filtered_state_means,0,0)
            np.delete(filtered_state_covariances,0,0)
            raw = getData(uart)
            IMU = raw[5:]
            IMU.extend([0,0,0])
            dataIMU.append(IMU)
            dataFlex.append(raw[:5])

            # Filter Data
            nxt_filtered_state_means, nxt_filtered_state_covariances=
                    (kf.filter_update(
                        filtered_state_means[-1],
                        filtered_state_covariances[-1],
                        dataIMU[-1],
                        transition_offset=transition_offset,
                    )
                )
            np.vstack((filtered_state_means,nxt_filtered_state_means))
            np.concatenate((filtered_state_covariances,
                            [nxt_filtered_state_covariances]), axis=0)

            # Run classifiers
                # TO DO
            print t

        # Plot Data
        # print filtered_state_means
        # print dataIMU
        # pl.figure()
        # pl.ion()
        lines_true = pl.plot(dataIMU, color='b')
        lines_filt = pl.plot(filtered_state_means, color='r')
        pl.legend((lines_true[0], lines_filt[0]), ('true', 'filtered'))
        pl.show()
        time.sleep(30)

    finally:
        device.disconnect()


# Initialize the BLE system and start main loop
ble.initialize()
ble.run_mainloop_with(main)