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

# MADE FOR WINDOWS 10

DEFAULT_MONITOR_NAME = "Dell 3a59"
PRINTING_FRAME_LINE = "Entering function void screenovate::WfdDepacketizer::onNewVideoFrame"

def get_connect_time_and_disconnect():
    number_of_connections = input("Enter number of connections: ")
    while (not isinstance(number_of_connections, int)) or number_of_connections <= 0:
        number_of_connections = input("Please enter an integer larger than 0:")

    total_connection_time = 0
    for x in range(number_of_connections):
        total_connection_time += connect()
        disconnect()

    return "Number of connections: %s\n" \
           "Average connection time: %s" % (number_of_connections, total_connection_time / number_of_connections)

def connect():
    root_element = pyuiautomation.GetRootElement()
    autoit.send("#k")
    time.sleep(3)

    # Get monitor button:
    button_monitor = get_monitor_button(root_element)
    print("Connecting to monitor")
    print(str(button_monitor))
    time.sleep(2)
    starting_time = time.time()
    button_monitor.Invoke()
    output = subprocess.check_output(["adb", "logcat", "|", "findstr", PRINTING_FRAME_LINE])
    ending_time = time.time()
    print("output type is: %s" % type(output))
    return ending_time - starting_time

def disconnect():
    root_element = pyuiautomation.GetRootElement()
    autoit.send("#p")
    time.sleep(2)
    button_disconnect = root_element.findfirst('descendants', Name='Disconnect')
    if str(button_disconnect) == 'None':
        button_disconnect = root_element.findfirst('descendants', Name='PC screen only')
        
    button_disconnect.Invoke()
    time.sleep(2)

def get_monitor_button(root_element):
    monitor_name = subprocess.check_output("adb shell getprop | findstr ssid", shell=True)
    print("Full output: %s" % monitor_name)
    start_index = monitor_name.rfind('Dell', 0)
    print(monitor_name[start_index:])
    monitor_name = monitor_name[start_index:]
    end_index = monitor_name.rfind(']',0)
    print("end_index is: %s" % end_index)
    print("Monitor name is: %s" % monitor_name[:end_index])

    # monitor_name = DEFAULT_MONITOR_NAME
    # button_monitor = root_element.findfirst('descendants', monitor_name)
    # if button_monitor == None:
    #     monitor_name = raw_input("Please insert Monitor name, for example: \nDell 5a74")
    #     button_monitor = root_element.findfirst('descendants', monitor_name)
    #
    # while button_monitor == None:
    #     print 'Monitor name not found'
    #     monitor_name = raw_input("Please insert Monitor name, for example: \nDell 5a74")
    button_monitor = root_element.findfirst('descendants', Name=monitor_name)
    print("Root element = %s" % str(root_element))

    return button_monitor

print(get_connect_time_and_disconnect())
