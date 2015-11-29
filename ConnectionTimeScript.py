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
from Windows10 import Windows10

# MADE FOR WINDOWS 10

PRINTING_FIRST_FRAME_LINE = "MediaCodecVideoDecoderNdk::outputThread():"
MAX_CONSECUTIVE_CONNECTION_FAILURES = 10
CONNECTED_LINE = "STA-CONNECTED"


def setup():
    global windows_source
    global monitor

    windows_source = Windows10()
    os.system("adb forward tcp:9008 tcp:9008")
    monitor = Monitor()


def finish(connection_times_list, failed_connections_count, consec_fails_list, script_start_time):
    write_logs(connection_times_list, failed_connections_count, consec_fails_list, windows_source.serial, monitor.serial, script_start_time)
    exit()


def get_number_of_attempts_from_user():
    connection_attempts = input("Enter number of connections: ")
    while (not isinstance(connection_attempts, int)) or connection_attempts <= 0:
        connection_attempts = input("Please enter an integer larger than 0: ")

    return connection_attempts


def handle_consecutive_disconnection_fails():
    consecutive_failed_disconnections = 0
    disconnection_success = True
    while verify_connected() == True:
        consecutive_failed_disconnections += 1
        if consecutive_failed_disconnections > 3:
            #Consecutive failure to disconnect.
            boo = monitor.reboot()
        if consecutive_failed_disconnections > 5:
            disconnection_success = False
            break
        windows_source.disconnect()

    return disconnection_success


def get_connect_time_and_disconnect():

    setup()
    connection_times_list = []
    consec_fails_list = []
    failed_connections_count = 0
    consecutive_failed_connections = 0
    script_start_time = time.strftime("%Y_%m_%d-%H_%M_%S")


    connection_attempts = get_number_of_attempts_from_user()

    for x in range(connection_attempts):
        #Setup
        os.system("adb devices")
        time.sleep(2)

        #Check not connected
        if verify_connected() == True:
            if not handle_consecutive_disconnection_fails():
                finish(connection_times_list, failed_connections_count, consec_fails_list, script_start_time)

        if consecutive_failed_connections > 1:
            consec_fails_list.append(consecutive_failed_connections)

        if consecutive_failed_connections >= MAX_CONSECUTIVE_CONNECTION_FAILURES:
            finish(connection_times_list, failed_connections_count, consec_fails_list, script_start_time)

        #Clear logcat
        subprocess.call(["adb", "logcat", "-c"])

        #Connect
        connection_time = connect()

        if verify_connected(): #Succesful connection
            consecutive_failed_connections = 0
            print("Connection time: %s" % connection_time)
            connection_times_list.append(connection_time)
            windows_source.disconnect()
        else: #Connection failed
            failed_connections_count += 1
            consecutive_failed_connections += 1

    finish(connection_times_list, failed_connections_count, consec_fails_list, script_start_time)


def verify_connected():
    print "Verifying connection"
    boo_connected = False
    windows_client_mac_addresses = windows_source.get_mac_addresses()
    print "comparing mac addresses"
    for address in windows_client_mac_addresses:
        if monitor.is_mac_address(address.lower().strip()):
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
    conn_end_time = 0
    test_start_time = windows_source.connect(monitor.name)
    proc = subprocess.Popen(['adb', 'logcat'], stdout=subprocess.PIPE)
    for line in proc.stdout:
        if PRINTING_FIRST_FRAME_LINE in line:
            conn_end_time = time.time()
            proc.kill()
            break
        if time.time() > test_start_time + 20:
            # Failed connection
            print "Failed Connection"
            conn_end_time = 0
            proc.kill()
            break
    proc.wait()
    return conn_end_time - test_start_time

if __name__ == "__main__":

    #Run test
    get_connect_time_and_disconnect()
