__author__ = 'daniel'
import subprocess
import pyuiautomation
import autoit
import time

class Windows10:
    def __init__(self):
        self.root_element = pyuiautomation.GetRootElement()

    def _open_connect_bar(self):
        autoit.send("#k")
        time.sleep(3)

    def _open_project_bar(self):
        autoit.send("#p")
        time.sleep(3)

    def _go_to_desktop(self):
        autoit.send("#d")
        time.sleep(3)

    def _get_connection_button(self, monitor_name):
        self._open_connect_bar()
        button_monitor = self.root_element.findfirst('descendants', Name=monitor_name)
        return button_monitor

    def click_enter(self):
        autoit.send("{ENTER}")
        time.sleep(1)

    def connect(self, monitor_name):
        button = self._get_connection_button(monitor_name)
        button.Invoke()
        return time.time()

    def get_mac_addresses(self):
        addresses = []
        getmac = subprocess.check_output(["ipconfig", "/all", "|", "findstr", "Physical"], shell=True)
        rows = getmac.count(':')
        for i in range(rows):
            index = getmac.find(":") + 2
            getmac = getmac[index:]
            mac = getmac[0:17].replace('-',':')
            addresses.append(mac)
        return addresses

    def disconnect(self):
        time.sleep(2)
        print("Disconnecting")
        self._open_project_bar()
        button_disconnect = self.root_element.findfirst('descendants', Name='Disconnect')
        if str(button_disconnect) == 'None':
            button_disconnect = self.root_element.findfirst('descendants', Name='PC screen only')

        button_disconnect.Invoke()
        time.sleep(2)
        self._go_to_desktop()

    def remove_monitor(self, monitor_name):
        self._open_connect_bar()
        button_devices = self.root_element.findfirst('descendants', Name='find other devices')
        time.sleep(2)
        button_monitor = self.root_element.findfirst('descendants', Name=monitor_name)
        button_monitor.Invoke()
        time.sleep(1)
        button_remove = self.root_element.findfirst('descendants', Name='Remove')
        button_remove.Invoke()
        time.sleep(1)
        self._go_to_desktop()
