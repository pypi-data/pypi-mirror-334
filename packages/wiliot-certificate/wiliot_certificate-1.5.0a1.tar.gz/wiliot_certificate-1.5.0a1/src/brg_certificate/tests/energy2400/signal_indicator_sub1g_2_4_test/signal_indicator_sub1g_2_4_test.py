import random
from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
import brg_certificate.cert_common as cert_common
import brg_certificate.cert_config as cert_config
from brg_certificate.wlt_types import *


# Test MACROS #
DEFAULT_HDR = ag.Hdr(group_id=ag.GROUP_ID_GW2BRG)
NUM_OF_SCANNING_CYCLE = 3
DEFAULT_SCAN_TIME = 60
SCAN_DELAY_TIME = 5
BOARD_TYPES_2_POLARIZATION_ANT_LIST = [ag.BOARD_TYPE_MINEW_SINGLE_BAND_V0, ag.BOARD_TYPE_MINEW_DUAL_BAND_V0, ag.BOARD_TYPE_ENERGOUS_V2, ag.BOARD_TYPE_ERM_V0, ag.BOARD_TYPE_ERM_V1]
ANTENNA_TYPE_2_4 = 0
ANTENNA_TYPE_SUB1G = 1
ANTENNA_TYPE_IDX = 21

# Test functions #
def mqtt_scan_n_create_log_file(test, duration):
    test.mqttc.flush_pkts()
    mqtt_scan_wait(test, duration=duration)
    generate_log_file(test, "15&4")

def get_all_signal_ind_pkt(test=None, rx_brg=None, tx_brg=None):
    if rx_brg == test.brg1:
        all_sensor_packets = cert_mqtt.get_all_brg1_ext_sensor_pkts(mqttc=test.mqttc, test=test)
    elif rx_brg == test.brg0:
        all_sensor_packets = cert_mqtt.get_all_sensor_pkts(mqttc=test.mqttc, test=test)
    signal_ind_pkts = []
    for p in all_sensor_packets:
        if p[SENSOR_UUID] == "{:06X}".format(ag.SENSOR_SERVICE_ID_SIGNAL_INDICATOR) and p[BRIDGE_ID] == rx_brg.id_str and (p[SENSOR_ID] == tx_brg.id_alias or p[SENSOR_ID] == tx_brg.id_str):
            signal_ind_pkts.append(p)
    return signal_ind_pkts

def expected_signal_ind_pkts_calc(tx_brg, rx_brg, antenna_type):
    if (antenna_type == ANTENNA_TYPE_2_4 and tx_brg.board_type in BOARD_TYPES_2_POLARIZATION_ANT_LIST):
        tx_brg_ant_polarization_num = 2
    else:
        tx_brg_ant_polarization_num = 1
    if (antenna_type == ANTENNA_TYPE_2_4 and rx_brg.board_type in BOARD_TYPES_2_POLARIZATION_ANT_LIST):
        rx_brg_ant_polarization_num = 2
    else:
        rx_brg_ant_polarization_num = 1
    return NUM_OF_SCANNING_CYCLE * tx_brg_ant_polarization_num * rx_brg_ant_polarization_num

def terminate_test(test, revert_rx_brg=False, revert_tx_brg=False, rx_modules=[], tx_modules=[]):
    # Temp solution for internal_brg test because test_epilog doesn't support both internal brg and test.brgs
    utPrint("Terminating test!!!!!!!!\n", "BLUE")
    if revert_rx_brg:
        restore_modules = rx_modules
        utPrint(f"reverting rx_brg {test.brg1.id_str} to defaults\n", "BOLD")
        test, response = cert_config.config_brg1_defaults(test, modules=restore_modules)
        if response == NO_RESPONSE and test.exit_on_param_failure:
            test.rc = TEST_FAILED
            test.add_reason(f"BRG {test.brg1.id_str} didn't revert modules "
                                   f"{restore_modules} to default configuration!")

    if revert_tx_brg:
        restore_modules = tx_modules
        utPrint(f"reverting tx_brg {test.brg0.id_str} to defaults\n", "BOLD")
        test, response = cert_config.config_brg_defaults(test, modules=restore_modules)
        if response == NO_RESPONSE and test.exit_on_param_failure:
            test.rc = TEST_FAILED
            test.add_reason(f"BRG {test.brg0.id_str} didn't revert modules"
                                   f"{restore_modules} to default configuration!")
    return cert_common.test_epilog(test)

# Test execution #
def run(test):

    # Test modules evaluation #
    energy2400_module = eval(f'ModuleEnergy2400V{test.active_brg.api_version}')
    ext_sensors_module = eval(f'ModuleExtSensorsV{test.active_brg.api_version}')
    energy_sub1g_module = eval(f'ModuleEnergySub1GV{test.active_brg.api_version}')

    # Transmitter related defines #
    tx_brg_ = test.brg0

    # Receiver related defines #
    rx_brg_ = test.brg1

    # Test prolog
    test = cert_common.test_prolog(test)
    if test.rc == TEST_FAILED:
        return terminate_test(test)

    tx_signal_ind_cycle, tx_signal_ind_rep = 15, 4
    utPrint(f"TX BRG with RX- cycle = {tx_signal_ind_cycle}, repetition = {tx_signal_ind_rep}\n", "HEADER")

    # configuring receiver #
    utPrint(f"Configuring BRG {rx_brg_.id_str} as Signal Indicator Receiver", "BOLD")
    test =  cert_config.brg1_configure(test=test, module=ext_sensors_module, fields=[BRG_SENSOR0], values=[ag.EXTERNAL_SENSORS_SIGNAL_INDICATOR])[0]
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        test.add_reason(f"BRG {rx_brg_.id_str}: didn't receive signal indicator receiver configuration!")
        return terminate_test(test, revert_rx_brg=True, rx_modules=[ext_sensors_module])
    utPrint(f"BRG {rx_brg_.id_str} succesfully configured to be receiver", "GREEN")

    # configuring transmitter 2_4 #
    utPrint(f"Configuring BRG {tx_brg_.id_str} as Signal Indicator 2_4 Transmitter", "BOLD")
    transmitter_cfg_pkt_2_4 = WltPkt(hdr=DEFAULT_HDR, pkt=energy2400_module(seq_id=random.randrange(99), brg_mac=tx_brg_.id_int, signal_indicator_cycle=tx_signal_ind_cycle, signal_indicator_rep=tx_signal_ind_rep))
    test = cert_config.brg_configure(test=test, cfg_pkt=transmitter_cfg_pkt_2_4)[0]
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        test.add_reason(f"BRG {tx_brg_.id_str}: didn't receive signal indicator 2_4 transmitter configuration!")
        return terminate_test(test, revert_rx_brg=True,revert_tx_brg=True)
    utPrint(f"BRG {tx_brg_.id_str} succesfully configured to be 2_4 transmitter - cycle = {tx_signal_ind_cycle},"
              f"repetition = {tx_signal_ind_rep}", "GREEN")
    
    # configuring transmitter sub1g #
    utPrint(f"Configuring BRG {tx_brg_.id_str} as Signal Indicator sub1g Transmitter", "BOLD")
    transmitter_cfg_pkt_sub1g = WltPkt(hdr=DEFAULT_HDR, pkt=energy_sub1g_module(seq_id=random.randrange(99), brg_mac=tx_brg_.id_int, signal_indicator_cycle=tx_signal_ind_cycle, signal_indicator_rep=tx_signal_ind_rep, pattern=ag.SUB1G_ENERGY_PATTERN_ISRAEL))
    test = cert_config.brg_configure(test=test, cfg_pkt=transmitter_cfg_pkt_sub1g)[0]
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        test.add_reason(f"BRG {tx_brg_.id_str}: didn't receive signal indicator sub1g transmitter configuration!")
        return terminate_test(test, revert_rx_brg=True,revert_tx_brg=True, rx_modules=[ext_sensors_module], tx_modules=[energy2400_module, energy_sub1g_module])
    utPrint(f"BRG {tx_brg_.id_str} succesfully configured to be Sub1g transmitter - cycle = {tx_signal_ind_cycle},"
              f"repetition = {tx_signal_ind_rep}, EP = {ag.SUB1G_ENERGY_PATTERN_ISRAEL}", "GREEN")
    
    # analysis #
    mqtt_scan_n_create_log_file(test, (NUM_OF_SCANNING_CYCLE * tx_signal_ind_cycle) + SCAN_DELAY_TIME)
    received_signal_ind_pkts = get_all_signal_ind_pkt(test=test, rx_brg=rx_brg_, tx_brg=tx_brg_)
    expected_signal_ind_2_4_pkts = expected_signal_ind_pkts_calc(tx_brg_, rx_brg_, ANTENNA_TYPE_2_4)
    expected_signal_ind_sub1g_pkts = expected_signal_ind_pkts_calc(tx_brg_, rx_brg_, ANTENNA_TYPE_SUB1G)
    signal_indicator_2_4_packets = 0
    signal_indicator_sub1g_packets = 0
    for p in received_signal_ind_pkts:
        if int(p[PAYLOAD][ANTENNA_TYPE_IDX]) == ANTENNA_TYPE_SUB1G and p[SENSOR_ID] == tx_brg_.id_str:
            signal_indicator_sub1g_packets += 1
        elif int(p[PAYLOAD][ANTENNA_TYPE_IDX]) == ANTENNA_TYPE_2_4 and p[SENSOR_ID] == tx_brg_.id_alias:
            signal_indicator_2_4_packets += 1
    utPrint(f"Received {signal_indicator_2_4_packets} 2_4 signal indicator packets and {signal_indicator_sub1g_packets} subg signal indicator packets", "BLUE")

    # Test evaluation #
    if len(received_signal_ind_pkts) < expected_signal_ind_2_4_pkts + expected_signal_ind_sub1g_pkts:
        test.rc = TEST_FAILED
        test.add_reason(f"Test failed - BRG {rx_brg_.id_str} received wrong number of "
                                    f"total signal indicator packets\n received {len(received_signal_ind_pkts)} packets, "
                                    f"expected {expected_signal_ind_2_4_pkts + expected_signal_ind_sub1g_pkts} packets")
    elif signal_indicator_2_4_packets < expected_signal_ind_2_4_pkts:
        test.rc = TEST_FAILED
        test.add_reason(f"Test failed - BRG {rx_brg_.id_str} received wrong number of "
                                f"signal indicator 2.4 packets\n received {signal_indicator_2_4_packets} packets, "
                                f"expected {expected_signal_ind_2_4_pkts} packets")
    elif signal_indicator_sub1g_packets < expected_signal_ind_sub1g_pkts:
        test.rc = TEST_FAILED
        test.add_reason(f"Test failed - BRG {rx_brg_.id_str} received wrong number of "
                                f"signal indicator sub1g packets\n received {signal_indicator_sub1g_packets} packets, "
                                f"expected {expected_signal_ind_sub1g_pkts} packets")

    field_functionality_pass_fail_print(test,'Signal Indicator Functionality 2_4 & Sub1g')

    # Test epilog
    return terminate_test(test, revert_rx_brg=False,revert_tx_brg=True, rx_modules=[ext_sensors_module], tx_modules=[energy2400_module, energy_sub1g_module])