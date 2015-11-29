__author__ = 'daniel'
import subprocess
import pyuiautomation
import autoit
import time

class Windows10:
    def __init__(self):
        self.root_element = pyuiautomation.GetRootElement()
        self.serial = self._get_serial()

    def _open_connect_bar(self):
        autoit.send("#k")
        time.sleep(1)
        print "1"
        time.sleep(1)
        print "2"
        time.sleep(1)
        print "3"
        time.sleep(1)
        print "4"


    def _open_project_bar(self):
        autoit.send("#p")
        time.sleep(3)

    def _go_to_desktop(self):
        autoit.send("#d")
        time.sleep(3)

    def _get_serial(self):
        output = subprocess.check_output(["wmic", "bios", "get", "serialnumber"], shell=True)
        start_index = output.rfind('SerialNumber', 0)
        start_index = start_index + 12
        end_index = output.rfind("\n", 0)
        serial = output[start_index : end_index].strip()
        return serial

    def _get_connection_button(self, monitor_name):
        button_monitor = None
        starting_time = time.time()
        while button_monitor == None and time.time() < starting_time + 15:
            self._open_connect_bar()
            button_monitor = self.root_element.findfirst('descendants', Name=monitor_name)
        return button_monitor

    def click_enter(self):
        autoit.send("{ENTER}")
        time.sleep(1)

    def connect(self, monitor_name):
        button = self._get_connection_button(monitor_name)
        if type(button) is None:
            print "Could not get connection button for monitor %s" % monitor_name
        #     TODO: raise exception
            return -99999999

        # Invoke connection button and return current time.
        button.Invoke()
        return time.time()

    def get_mac_addresses(self):
        print "getting mac addresses from windows source"
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
        time.sleep(3)
