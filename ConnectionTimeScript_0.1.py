__author__ = 'daniel'
from LogTools import write_to_csv
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
CONNECTED_LINE = "STA-CONNECTED"

def get_connect_time_and_disconnect(windows_source, monitor):
    connection_times = []
    number_of_connections = input("Enter number of connections: ")
    while (not isinstance(number_of_connections, int)) or number_of_connections <= 0:
        number_of_connections = input("Please enter an integer larger than 0:")

    total_connection_time = 0
    for x in range(number_of_connections):
        #Setup
        #Check not connected
        if verify_connected() == True:
            windows_source.disconnect()

        lock2.acquire()
        #start thread
        thread = threading.Thread(target=thread_target)
        ending_time = thread.start()

        lock2.acquire()
        try:
            starting_time = windows_source.connect()
        finally:
            lock1.release()

        connection_time = ending_time - starting_time

        connection_times.append(connection_time)
        print("Connection time: %s" % connection_time)
        total_connection_time += connection_time
        windows_source.disconnect()

    # Write connection times to .csv file
    write_to_csv(connection_times)

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

def thread_target():
    lock1.acquire()
    try:
        subprocess.check_output(["adb", "logcat", "|", "findstr", CONNECTED_LINE], shell=True)
    finally:
        lock2.release()

    try:
        lock1.acquire()

        #critical section 2
        subprocess.check_output(["adb", "logcat", "|", "findstr", PRINTING_FRAME_LINE], shell=True)
        ending_time = time.time()
        #end critical section 2

    finally:
        lock1.release()
        lock2.release()

    return ending_time

#setup
windows_source = Windows10.Windows10()
monitor = Monitor()

lock1 = threading.Lock()
lock2 = threading.Lock()

print(get_connect_time_and_disconnect(windows_source, monitor))
ctypes.windll.user32.MessageBoxA(0, "Finished running connection time measurement script.", "Testing Complete!", 1)