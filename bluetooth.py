import Adafruit_BluefruitLE, ctypes, os
from Adafruit_BluefruitLE.services import UART

cmd = """
osascript -e 'tell application "System Events" to keystroke "m" 
    using {command down}' 
"""
right = """
osascript -e 'tell application "System Events" to key code 124'
"""
left = """
osascript -e 'tell application "System Events" to key code 123'
"""
Full = """
osascript -e 'tell application "System Events" to keystroke "f" 
    using {shift down} '
"""
pause = """
osascript -e 'tell application "System Events" to keystroke space'
"""
vdown = """
osascript -e 'tell application "System Events" to keystroke ">" '
"""
vup = """
osascript -e 'tell application "System Events" to key code 126'
"""


# Get the BLE provider for the current platform.
ble = Adafruit_BluefruitLE.get_provider()


# Main Function
def main():
    ble.clear_cached_data() # Clear Cached Data

    # Get the first available BLE network adapter
    adapter = ble.get_default_adapter()
    adapter.power_on()
    print('Using adapter: {0}'.format(adapter.name))

    # Disconnect any currently connected UART devices.
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
        # Make sure scanning is stopped before exiting
        adapter.stop_scan()

    print('Connecting to device...')
    device.connect()  # Will time out after 60 seconds

    try:
        print('Discovering services...')
        UART.discover(device)
        uart = UART(device)
 
        while(1):
            received = uart.read(timeout_sec=5)
            print received
            if received is not None :
                if received == '20' :
                    os.system(right)
                    print('right')
                elif received == '21' :
                    os.system(left)
                    print('left')
                elif received == '30' :
                    os.system(Full)
                    print('Full')
                elif received == '31' :
                    os.system(pause)
                    print('pause')
                elif received == '10' :
                    os.system(vdown)
                    print('vdown')
                elif received == '11' :
                    os.system(vup)
                    print('vup')
            else: 
                print('Received no data!')
    finally:
        # Disconeect device on exit
        device.disconnect()

###########################################################

# Initialize the BLE system and start main loop
ble.initialize()
ble.run_mainloop_with(main)

