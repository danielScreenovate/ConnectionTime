__author__ = 'daniel'
from uiautomator import Device
import subprocess
import time

class Monitor():
    def __init__(self):
        self.serial = self._get_serial()
        self.automation_handle = Device(self.serial)
        self.name = self._get_monitor_name()

    def _get_serial(self):
        temp = subprocess.check_output(["adb", "devices"])
        time.sleep(2)

        output = subprocess.check_output(["adb", "devices"])
        serial = output.rsplit("\n")[1].rsplit("\t")[0].strip()
        print "Device serial: %s" % serial
        return serial

    def _get_monitor_name(self):
        output = subprocess.check_output(["adb", "shell", "dumpsys", "|", "findstr", "wifiP2pDevice=Device"], shell=True)
        start_index = output.rfind('Device: ', 0)
        start_index = start_index + 8
        end_index = output.rfind("\n", 0)
        name = output[start_index : end_index].strip()
        return name

    def is_mac_address(self, address):
        boo = False
        boo = Device(self.serial)(description='VideoView ' + address).exists

        return boo