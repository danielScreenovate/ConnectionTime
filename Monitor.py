__author__ = 'daniel'
from uiautomator import Device
import subprocess

class Monitor():
    def __init__(self):
        self.serial = self.get_serial()
        self.automation_handle = Device(self.serial)
        self.name = self.get_monitor_name()

    def get_serial(self):
        output = subprocess.check_output(["adb", "devices"])
        end_index = output.rfind(" ", 0)
        serial = output[:end_index]
        return serial

    def get_monitor_name(self):
        output = subprocess.check_output(["adb", "shell", "dumpsys", "|", "findstr", "wifiP2pDevice=Device"], shell=True)
        start_index = output.rfind('Device: ', 0)
        start_index = start_index + 8
        end_index = output.rfind("\n", 0)
        name = output[start_index : end_index].strip()
        return name

    def is_mac_address(self, address):
        print "trying address: %s" % address
        return Device(address)(description='VideoView ' + address).exists