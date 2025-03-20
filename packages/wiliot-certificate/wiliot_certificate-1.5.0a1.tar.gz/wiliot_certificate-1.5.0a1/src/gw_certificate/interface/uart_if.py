import datetime
import subprocess
import serial
import serial.tools.list_ports
import time
import os
import stat
import platform
from packaging import version
import pkg_resources

from gw_certificate.common.debug import debug_print
from gw_certificate.interface.if_defines import *

LATEST_VERSION = '4.4.52'
LATEST_VERSION_FILE = f'{LATEST_VERSION}_sd_bl_app.zip'
LATEST_VERSION_PATH = pkg_resources.resource_filename(__name__, LATEST_VERSION_FILE)
LATEST_VERSION_FILE_APP = f'{LATEST_VERSION}_app.zip'
LATEST_VERSION_PATH_APP = pkg_resources.resource_filename(__name__, LATEST_VERSION_FILE_APP)

FIRST_UNIFIED_BL_VERSION = version.parse('4.4.44')

NRFUTIL_FW_TOO_LOW_ERROR = 'Error 0x05: The firmware version is too low'

class UARTError(Exception):
    pass

class UARTInterface:
    def __init__(self, comport, update_fw=True):
        self.comport = comport
        self.serial = serial.Serial(port=comport, baudrate=921600, timeout=SERIAL_TIMEOUT)
        self.serial.flushInput()
        self.gw_app_rx = None
        self.fw_version, self.mac = self.get_version_mac()

        if self.fw_version is None:
            raise UARTError("Cannot initialize board! Please try disconnecting and connecting USB cable")
        self.fw_version = version.parse(self.fw_version)

        version_supported = self.check_fw_supported()
        if not version_supported and update_fw:
            update_status = self.update_firmware()
            if not update_status:
                raise UARTError('Update Failed! Update FW manually using NRF Tools')
            if self.fw_version >= version.Version('3.17.0'):
                self.write_ble_command(GATEWAY_APP)
                self.flush()
        debug_print(f'Serial Connection {comport} Initialized')

    @staticmethod
    def get_comports():
        ports = serial.tools.list_ports.comports()
        debug_print(SEP + "\nAvailable ports:")
        for port, desc, hwid in sorted(ports):
            debug_print("{}: {} [{}]".format(port, desc, hwid))
        debug_print(SEP + "\n")
        return ports

    def read_line(self):
        # This reads a line from the ble device (from the serial connection using ble_ser),
        # strips it from white spaces and then decodes to string from bytes using the "utf-8" protocol.
        answer = self.serial.readline().strip().decode("utf-8", "ignore")
        if len(answer) == 0:
            return None
        return answer

    def write_ble_command(self, cmd, read=False):
        # This function writes a command (cmd) to the ble using a serial connection (ble_ser) that are provided to it beforehand.. and returns the answer from the device as string
        debug_print("Write to BLE: {}".format(cmd))
        # Shows on terminal what command is about to be printed to the BLE device
        bytes_to_write = bytes(cmd.encode("utf-8")) + b'\r\n'
        self.serial.write(bytes_to_write)
        answer = None
        if read:
            # The "bytes" function converts the command from string to bytes by the specified "utf-8" protocol then we use .write to send the byte sequence to the ble device using the serial connection that we have for this port (ble_ser)
            # Pauses the program for execution for 0.01sec. This is done to allow the device to process the command and provide a response before reading the response.
            time.sleep(1)
            answer = self.read_line()
            debug_print(answer)
        return answer
    
    def flush(self):
        self.serial.close()
        time.sleep(2)
        self.serial.open()
        self.serial.flushInput()
        self.serial.flush()
        self.serial.reset_output_buffer()

    def reset_gw(self, stop_advertising=True):
        self.flush()
        self.write_ble_command(RESET_GW)
        self.gw_app_rx = None
        time.sleep(3)
        if stop_advertising:
            self.write_ble_command(STOP_ADVERTISING)
            time.sleep(3)

    def cancel(self):
        self.write_ble_command(CANCEL)

    def set_rx(self, rx_channel):
        assert rx_channel in RX_CHANNELS
        if self.gw_app_rx is None:
            self.reset_gw()

        if self.fw_version >= version.Version('3.17.0'):
            # from 3.17.0, only full_cfg can be used to configure channels. sending it with:
            # Data coupling(DC) off, wifi(NW) and mqtt(MQ) on.
            rx_ch_to_fw_enums = {37: 2, 38: 3, 39: 4}
            cmd = f'!full_cfg DM {rx_ch_to_fw_enums[rx_channel]} DC 0 NW 1 MQ 1 CH {rx_channel}'
            # cmd = '!gateway_app'
        else:
            cmd = f'!gateway_app {rx_channel} 30 0 17'

        self.write_ble_command(cmd)
        self.gw_app_rx = rx_channel

    def set_sniffer(self, rx_channel):
        self.set_rx(rx_channel)
        self.flush()
        time.sleep(1)
        if self.fw_version >= version.Version('4.1.0'):
            self.write_ble_command(f'{SET_SNIFFER} {rx_channel}')
        else:
            self.write_ble_command(SET_SNIFFER)
        self.flush()
        time.sleep(1)

    def cancel_sniffer(self):
        self.write_ble_command(CANCEL_SNIFFER)
        self.flush()

    def get_version_mac(self):
        self.reset_gw()
        self.flush()
        timeout = datetime.datetime.now() + datetime.timedelta(seconds=15)
        while datetime.datetime.now() < timeout:
            raw_version = self.write_ble_command(VERSION, read=True)
            if raw_version is not None:
                if GW_APP_VERSION_HEADER in raw_version:
                    return (raw_version.split(' ')[0].split('=')[1], raw_version.split(' ')[1].split('=')[1])
        return None, None

    def get_version(self):
        self.reset_gw()
        self.flush()
        timeout = datetime.datetime.now() + datetime.timedelta(seconds=15)
        while datetime.datetime.now() < timeout:
            raw_version = self.write_ble_command(VERSION, read=True)
            if raw_version is not None:
                if GW_APP_VERSION_HEADER in raw_version:
                    return raw_version.split(' ')[0].split('=')[1]
        return None
    
    def get_mac(self):
        self.reset_gw()
        self.flush()
        timeout = datetime.datetime.now() + datetime.timedelta(seconds=15)
        while datetime.datetime.now() < timeout:
            reply = self.write_ble_command(VERSION, read=True)
            if reply is not None:
                if GW_MAC_ADDRESS_HEADER in reply:
                    return reply.split(' ')[1].split('=')[1]
        return None
    
    def check_fw_supported(self):
        hex_version = version.parse(os.path.splitext(os.path.basename(LATEST_VERSION_PATH))[0].split('_')[0])
        if self.fw_version >= hex_version:
            debug_print(f'GW Running version {self.fw_version}')
            return True
        return False
    
    def make_executable(self, file_path):
        """Set execute permissions for a file (chmod +x).
        For windows, having the file suffix as .exe is enough. """
        # Get current file permissions
        current_permissions = os.stat(file_path).st_mode
        # Add execute permissions for the user, group, and others
        os.chmod(file_path, current_permissions | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    def update_firmware(self):
        NRFUTIL_MAP = {"Linux": "nrfutil-linux", "Darwin": "nrfutil-mac", "Windows": "nrfutil.exe"}
        nrfutil_file = pkg_resources.resource_filename(__name__, NRFUTIL_MAP[platform.system()])
        if platform.system() != "Windows":
            self.make_executable(nrfutil_file)
        # In order to support NRF UART FW update with protobuf > 3.20.0
        os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
        
        self.reset_gw()
        self.write_ble_command('!move_to_bootloader', read=True)
        self.serial.close()
        p = None
        dfu_full_process = subprocess.Popen(f'{nrfutil_file} dfu serial --package "{LATEST_VERSION_PATH}" -p {self.comport} -fc 0 -b 115200 -t 10',
                            stderr=subprocess.PIPE, shell=True, text=True)
        dfu_full_process.wait()
        return_code = dfu_full_process.returncode
        for line in dfu_full_process.stderr:
            if NRFUTIL_FW_TOO_LOW_ERROR in line:
                debug_print(f"DFU failed due to firmware (bootloader/application) version being too low.")
                debug_print(f"Probably since bootloader is already upgraded. Attempting to upgrade application only..")
                dfu_app_process = subprocess.Popen(f'{nrfutil_file} dfu serial --package "{LATEST_VERSION_PATH_APP}" -p {self.comport} -fc 0 -b 115200 -t 10',
                                    stderr=subprocess.PIPE, shell=True, text=True)
                dfu_app_process.wait()
                return_code = dfu_app_process.returncode
        debug_print('Waiting for the certificate kit to apply the update and boot...')
        timeout = datetime.datetime.now() + datetime.timedelta(minutes=2)
        current_ver = ''
        time.sleep(15)
        self.serial.open()
        self.flush()
        while GW_APP_VERSION_HEADER not in current_ver and datetime.datetime.now() < timeout:
            current_ver = self.write_ble_command(VERSION, read=True)
            if current_ver is None:
                current_ver = ''
            time.sleep(1)
        if current_ver.split(' ')[0].split('=')[1] != LATEST_VERSION:
            return False
        if return_code == 0:
            self.fw_version = version.parse(current_ver.split(' ')[0].split('=')[1])
            debug_print(f"Certification kit upgraded to {LATEST_VERSION} successfully")
            return True
        return False
