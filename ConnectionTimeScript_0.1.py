__author__ = 'daniel'

import comtypes
import pyuiautomation
import ctypes
# from comtypes import *
# from comtypes.client import *
comtypes.client.GetModule('UIAutomationCore.dll')
from comtypes.gen.UIAutomationClient import *
import autoit
import os
import time
import subprocess
import csv

# MADE FOR WINDOWS 10

PRINTING_FRAME_LINE = "Entering function void screenovate::WfdDepacketizer::onNewVideoFrame"

def get_connect_time_and_disconnect():
    connection_times = []
    number_of_connections = input("Enter number of connections: ")
    while (not isinstance(number_of_connections, int)) or number_of_connections <= 0:
        number_of_connections = input("Please enter an integer larger than 0:")

    total_connection_time = 0
    for x in range(number_of_connections):
        print("Connection number %s" % (x + 1))
        connection_time = connect()
        connection_times.append(connection_time)
        print("Connection time: %s" % connection_time)
        total_connection_time += connection_time
        disconnect()

    # Write connection times to .csv file
    write_to_csv(connection_times)

    return "Number of connections: %s\n" \
           "Average connection time: %s" % (number_of_connections, total_connection_time / number_of_connections)


#TODO: Implement in a more elegant way
def is_connected():
    print("Is the Source connected to the Monitor?")
    is_connected = True
    root_element = pyuiautomation.GetRootElement()
    open_project_bar()
    #Find 'Disconnect' button
    button_disconnect = root_element.findfirst('descendants', Name='Disconnect')
    if str(button_disconnect) == 'None':
        is_connected = False
        print("Nope")
    else:
        print("Yup")

    go_to_desktop()

    return is_connected

def connect():
    if is_connected():
        disconnect()
    root_element = pyuiautomation.GetRootElement()
    open_connect_bar()

    # Get monitor button:
    button_monitor = get_monitor_button(root_element)
    print("Connecting to monitor")
    time.sleep(3)
    starting_time = time.time()
    button_monitor.Invoke()
    output = subprocess.check_output(["adb", "logcat", "|", "findstr", PRINTING_FRAME_LINE])
    ending_time = time.time()
    print("Successfully connected!")
    time.sleep(4)

    go_to_desktop()
    return ending_time - starting_time

def disconnect():
    print("Disconnecting")
    root_element = pyuiautomation.GetRootElement()
    open_project_bar()
    button_disconnect = root_element.findfirst('descendants', Name='Disconnect')
    if str(button_disconnect) != 'None':
        button_disconnect.Invoke()
        time.sleep(3)
    go_to_desktop()

def open_connect_bar():
    autoit.send("#k")
    time.sleep(3)

def open_project_bar():
    autoit.send("#p")
    time.sleep(3)

def go_to_desktop():
    autoit.send("#d")
    time.sleep(3)

def get_monitor_button(root_element):
    print("retrieveing monitor button")
    monitor_name = subprocess.check_output("adb shell getprop | findstr ssid", shell=True)
    start_index = monitor_name.rfind('Dell', 0)
    monitor_name = monitor_name[start_index:]
    end_index = monitor_name.rfind(']',0)
    monitor_name = monitor_name[:end_index]
    print("Monitor name is: %s" % monitor_name)
    button_monitor = root_element.findfirst('descendants', Name=monitor_name)

    return button_monitor

def write_to_csv(connection_times):
    curr_time = time.time()
    directory = "test_results"
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open('%s/test_%s.csv' % (directory, curr_time), 'w+') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for x in range(len(connection_times)):
            csv_writer.writerow((x + 1, connection_times[x]))


print(get_connect_time_and_disconnect())
autoit.send("#d")
ctypes.windll.user32.MessageBoxA(0, "Finished running connection time measurement script.", "Testing Complete!", 1)