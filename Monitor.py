__author__ = 'daniel'
from uiautomator import Device
import subprocess
import os
import time

class Monitor():
    def __init__(self):
        self.serial = self._get_serial()
        self.automation_handle = Device(self.serial)
        self.name = self._get_monitor_name()


    def _get_serial(self):
        output = subprocess.check_output(["adb", "devices"])
        starting_time = time.time()
        while "offline" in output and time.time() < starting_time + 20:
            subprocess.check_output(["adb", "kill-server"])
            time.sleep(1)
            subprocess.check_output(["adb", "start-server"])
            time.sleep(5)
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
        boo = self.automation_handle.exists(description='VideoView ' + address)
        return boo


    def reboot(self):
        checkBootComp = subprocess.check_output('adb {} shell getprop sys.boot_completed'.format(self.serial))
        print('start rebbot monitor')
        os.system('adb {} reboot'.format(self.serial))
        self.is_boot_completed(checkBootComp)
        print('reboot monitor completed')


    def is_boot_completed(self , bootCompCmd):
        screenUp = '-1'
        while screenUp != bootCompCmd:
            time.sleep(1)
            try:
                screenUp = subprocess.check_output('adb {} shell getprop sys.boot_completed'.format(self.serial))
            except Exception:
                print('waiting for monitor' )
        print('Screen up and fully loaded')
        return True