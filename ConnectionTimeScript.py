__author__ = 'daniel'
from LogTools import write_logs
import comtypes
import ctypes
from comtypes import *
from comtypes.client import *
comtypes.client.GetModule('UIAutomationCore.dll')
from comtypes.gen.UIAutomationClient import *
import time
import subprocess
from Monitor import Monitor
import Windows10
import threading

# MADE FOR WINDOWS 10

PRINTING_FRAME_LINE = "Entering function void screenovate::WfdDepacketizer::onNewVideoFrame"

def get_connect_time_and_disconnect(windows_source, monitor):
    successful_connections = []
    number_of_connections = input("Enter number of connections: ")
    while (not isinstance(number_of_connections, int)) or number_of_connections <= 0:
        number_of_connections = input("Please enter an integer larger than 0:")

    total_connection_time = 0
    failed_connections = 0
    consecutive_failures = 0
    consec_fails_list = []
    for x in range(number_of_connections):
        #Setup
        #Check not connected
        if verify_connected() == True:
            windows_source.disconnect()

        if consecutive_failures > 2: #Remove monitor from device list
            consec_fails_list.append(consecutive_failures)
            windows_source.remove_monitor()

        #Clear logcat
        subprocess.call(["adb", "logcat", "-c"])
        starting_time = windows_source.connect()
        subprocess.check_output(["timeout", "/t", "20", "adb", "logcat", "|", "findstr", PRINTING_FRAME_LINE])
        ending_time = time.time()

        if verify_connected(): #Succesful connection
            consecutive_failures = 0
            connection_time = ending_time - starting_time
            successful_connections.append(connection_time)
            print("Connection time: %s" % connection_time)
            total_connection_time += connection_time
            windows_source.disconnect()
        else: #Connection failed
            failed_connections += 1
            consecutive_failures += 1


    # Write connection times to .csv file
    write_logs(number_of_connections, successful_connections, failed_connections, consec_fails_list)

    return "Number of connections: %s\n" \
           "Average connection time: %s" % (number_of_connections, total_connection_time / number_of_connections)

def verify_connected():
    boo_connected = False
    windows_client_mac_addresses = windows_source.get_mac_addresses()
    print "got mac addresses: \n%s\n" % windows_client_mac_addresses
    for address in windows_client_mac_addresses:

        if monitor.is_mac_address(address.lower()):
            boo_connected = True
            break
    print "boo_connected = %s" % boo_connected
    return boo_connected

#setup
windows_source = Windows10.Windows10()
monitor = Monitor()

print(get_connect_time_and_disconnect(windows_source, monitor))
ctypes.windll.user32.MessageBoxA(0, "Finished running connection time measurement script.", "Testing Complete!", 1)