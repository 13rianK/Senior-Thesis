import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART
import ctypes

import os
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


def getData(uart):
	while (1):
		d1 = uart.read(timeout_sec=5)
		d2 = uart.read(timeout_sec=5)
		d3 = uart.read(timeout_sec=5)
		if d1 is not None and d2 is not None and d3 is not None : 
			if d1[0] == 'A' :
				if d2[0] == 'B' :
					data = d1[1:]+' '+d2[1:]+' '+d3[1:]
				else :
					data = d1[1:]+' '+d3[1:]+' '+d2[1:]
			elif d1[0] == 'B' :
				if d2[0] == 'A' :
					data = d2[1:]+' '+d1[1:]+' '+d3[1:]
				else : data = d3[1:]+' '+d1[1:]+' '+d2[1:]
			else : 
				if d2[0] == 'A' : 
					data = d2[1:]+' '+d3[1:]+' '+d1[1:]
				else : data = d3[1:]+' '+d2[1:]+' '+d1[1:]
			data = data.split()
			if len(data) == 11 : 
				try :
					data = map(lambda x: float(x), data)
					return data
				except : continue # Failed to map floats onto vector
			else : continue	# Failed to get the right size vector
		else: 
			return None

def main():
    ble.clear_cached_data() # Clear Cached Data

    # Get the first available BLE network adapter
    adapter = ble.get_default_adapter()
    adapter.power_on()
    print('Using adapter: {0}'.format(adapter.name))

    # Disconnect any currently connected UART devices
    print('Disconnecting any connected UART devices...')
    UART.disconnect_devices()

    # Scan for UART devices.
    print('Searching for UART device...')
    try:
        adapter.start_scan()
        # Search for the first UART device found
        device = UART.find_device()
        if device is None:
            raise RuntimeError('Failed to find UART device!')
    finally:
        # Make sure scanning is stopped before exiting.
        adapter.stop_scan()

    print('Connecting to device...')
    device.connect()  # Will time out after 60 second

    try:
        # Wait for service discovery to complete for UART service
        print('Discovering services...')
        UART.discover(device)

        uart = UART(device)

        while(1):
        	data = getData(uart)
        	print data
    finally:
        # Make sure device is disconnected on exit.
        device.disconnect()

########################################################

# Initialize the BLE system and begin main loop
ble.initialize()
ble.run_mainloop_with(main)