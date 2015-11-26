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
import multiprocessing

# MADE FOR WINDOWS 10

PRINTING_FIRST_FRAME_LINE = "MediaCodecVideoDecoderNdk::outputThread():"
MAX_CONSECUTIVE_CONNECTION_FAILURES = 10
CONNECTED_LINE = "STA-CONNECTED"
starting_time = 0
consec_fails_list = []
connection_times = []

def get_connect_time_and_disconnect(windows_source, monitor):
    test_start_time = time.time()
    failed_connections = 0
    consecutive_failed_connections = 0
    consecutive_failed_disconnections = 0

    connection_attempts = input("Enter number of connections: ")
    while (not isinstance(connection_attempts, int)) or connection_attempts <= 0:
        connection_attempts = input("Please enter an integer larger than 0: ")

    for x in range(connection_attempts):

        #Setup
        os.system("adb devices")
        time.sleep(2)
        end_time = 0
        consecutive_failed_disconnections = 0

        #Check not connected
        while verify_connected() == True:
            consecutive_failed_disconnections += 1
            if consecutive_failed_disconnections > 3:
                #Consecutive failure to disconnect.
                boo = monitor.reboot()
            windows_source.disconnect()

        if consecutive_failed_connections > 1:
            consec_fails_list.append(consecutive_failed_connections)

        if consecutive_failed_connections >= MAX_CONSECUTIVE_CONNECTION_FAILURES:
            #Write data and stop script
            write_logs(connection_times, failed_connections, consec_fails_list, windows_source.serial, monitor.serial, test_start_time)
            raise ValueError("Couldn't connect %s times in a row.\nStopping script." % MAX_CONSECUTIVE_CONNECTION_FAILURES)


        #Clear logcat
        subprocess.call(["adb", "logcat", "-c"])

        #Connect
        connection_time = connect()

        # if end_time == 0: #Timing failed
        #     if verify_connected():
        #         connection_times.append(-1)
        #         windows_source.disconnect()
        #     continue

        if verify_connected(): #Succesful connection
            consecutive_failed_connections = 0
            print("Connection time: %s" % connection_time)
            connection_times.append(connection_time)
            windows_source.disconnect()
        else: #Connection failed
            failed_connections += 1
            consecutive_failed_connections += 1

    # Write connection times to .csv file
    write_logs(connection_times, failed_connections, consec_fails_list, windows_source.serial, monitor.serial, test_start_time)

def verify_connected():
    print "Verifying connection"
    boo_connected = False
    windows_client_mac_addresses = windows_source.get_mac_addresses()
    print "comparing mac addresses"
    for address in windows_client_mac_addresses:
        if monitor.is_mac_address(address.lower()):
            boo_connected = True
            print "Connection verified, by comparing mac addresses."
            break
    if boo_connected == False:
        print "Not connected."
    return boo_connected

def connect():
    print "Connecting"

    conn_time = listen()
    time.sleep(2)
    return conn_time

def listen():
    starting_time = windows_source.connect(monitor.name)
    print "starting_time = %s" % starting_time
    proc = subprocess.Popen(['adb', 'logcat'], stdout=subprocess.PIPE)
    for line in proc.stdout:
        if PRINTING_FIRST_FRAME_LINE in line:
            end_time = time.time()
            print "FOUND LINE!!"
            print line
            proc.kill()
            break
        if time.time() > starting_time + 20:
            # Failed connection
            print "Failed Connection"
            end_time = 0
            proc.kill()
            break
    proc.wait()
    return end_time - starting_time


#Initialize UIAutomator on Sink
# def manually_run_jars():
#         print("*** Pushing libraries ***")
#         os.system("adb push C:/automator_libs/uiautomator-stub.jar /data/local/tmp")
#         os.system("adb push C:/automator_libs/bundle.jar /data/local/tmp")
#         print("*** Forwarding tcp port ***")
#         os.system("adb forward tcp:9008 tcp:9008")
#         print("*** Running UIAutomator test***")
#         os.system("adb shell uiautomator runtest bundle.jar uiautomator-stub.jar -c com.github.uiautomatorstub.Stub&")
#         time.sleep(1)
#         windows_source.click_enter()
#         print("\nFinished initialization, is RPC server running?\n")
#         os.system("curl -d '{\"jsonrpc\":\"2.0\",\"method\":\"deviceInfo\",\"id\":1}' localhost:9008/jsonrpc/0")

#Setup
end_time = 0
windows_source = Windows10.Windows10()
# manually_run_jars()
os.system("adb forward tcp:9008 tcp:9008")
monitor = Monitor()
get_connect_time_and_disconnect(windows_source, monitor)
ctypes.windll.user32.MessageBoxA(0, "Finished running connection time measurement script.", "Testing Complete!", 1)
exit()