import datetime
import time

from gw_certificate.interface.uart_if import UARTInterface
from gw_certificate.common.debug import debug_print
from gw_certificate.interface.if_defines import *

class BLESimulator():
    def __init__(self, uart:UARTInterface):
        self.uart = uart
        self.sim_mode = False

    def set_sim_mode(self, sim_mode):
        self.uart.flush()
        mode_dict = {True: 1, False: 0}
        self.sim_mode = sim_mode
        self.uart.reset_gw()
        self.uart.write_ble_command(f"!ble_sim_init {mode_dict[sim_mode]}")
        if not sim_mode:
            self.uart.reset_gw()
        time.sleep(3)

    def send_packet(self, raw_packet, duplicates=DEFAULT_DUPLICATES, output_power=DEFAULT_OUTPUT_POWER, channel=SEND_ALL_ADV_CHANNELS, delay=DEFAULT_DELAY):
        assert self.sim_mode is True, 'BLE Sim not initialized!'
        if len(raw_packet) == 62:
            # Add ADVA
            raw_packet = DEFAULT_ADVA + raw_packet
        if len(raw_packet) != 74:
            raise ValueError('Raw Packet must be 62/74 chars long!')
        self.uart.write_ble_command(f"!ble_sim {str(raw_packet)} {str(duplicates)} {str(output_power)} {str(channel)} {str(delay)}")
        if delay > 0:
            diff = time.perf_counter()
            time.sleep((delay/1000) * duplicates)
            diff = time.perf_counter() - diff
            debug_print(f'Desired Delay: {(delay/1000) * duplicates} Actual Delay {diff}')

    
    def send_data_si_pair(self, data_packet, si_packet, duplicates, output_power=DEFAULT_OUTPUT_POWER, delay=DEFAULT_DELAY, packet_error=None):
        if packet_error is None:
            packet_error = [True for i in range (duplicates * 2)]
        # debug_print(packet_error)
        # print(f'delay {delay}')
        packet_to_send = data_packet
        def switch_packet(packet_to_send):
            if packet_to_send == data_packet:
                return si_packet
            else:
                return data_packet
        for dup in range(duplicates * 2):
            diff = time.perf_counter()
            if packet_error[dup]:
                debug_print(f'Sending Packet {dup}')
                self.send_packet(packet_to_send, duplicates=1, output_power=output_power, channel=SEND_ALL_ADV_CHANNELS, delay=0)
            else:
                debug_print(f'Dropping Packet {dup}')
            time.sleep(delay/1000)
            diff = time.perf_counter() - diff
            debug_print(f'Desired Delay: {delay/1000} Actual Delay {diff}')
            packet_to_send = switch_packet(packet_to_send)
