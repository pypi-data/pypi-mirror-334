
from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
from brg_certificate.wlt_types import *
import brg_certificate.cert_common as cert_common
import brg_certificate.cert_config as cert_config
import brg_certificate.cert_data_sim as cert_data_sim
import time

def cal_scan_time(test, delay, pacer_interval):
    # Calculate the scan time to ensure at least 5 packets are captured in data scan
    # define the num of packet that you want to get 
    num_of_sending_pkt = 2 # actually it will be 3 because the first one always send
    delay = delay/1000
    if delay < pacer_interval :
        scan_time =(pacer_interval*num_of_sending_pkt)+10
    elif pacer_interval <= delay:
        scan_time = (delay*num_of_sending_pkt)+10
    # verify scan time value 
    if scan_time < (2*pacer_interval):
        print(f"scan time is too low in related to pacer interval")
        test.rc == TEST_FAILED
        test.add_reason(f"scan time is too low in related to pacer interval value")
    return test, scan_time

def scan_and_compare(test, pacer_interval, delay ,expected_address_value):
    pixel_sim_thread = cert_data_sim.DataSimThread(test=test, num_of_pixels=1, duplicates=3, delay=delay, pkt_types=[0], pixels_type=GEN2)
    pixel_sim_thread.start()
    test, scan_time = cal_scan_time(test, delay, pacer_interval) 
    df = cert_common.data_scan(test, scan_time=scan_time, brg_data=(not test.internal_brg), gw_data=test.internal_brg)
    pixel_sim_thread.stop()
    cert_mqtt.dump_pkts(test, log="rx_rate")
    cert_common.display_data(df, tbc=True, nfpkt=True, rssi=True, dir=test.dir)
    
    if df.empty:
        print(f"df is empty")
    else:
        df = df[[TAG_ID, TBC]]
        print(f"df:\n {df}") 
        tag_counts = df[TAG_ID].value_counts()
        print(f"Tag counts:\n{tag_counts.to_string(header=False)}")
        most_common_tag = tag_counts.idxmax()
        print(f"Most common tag: {most_common_tag}")
        df = df[df[TAG_ID] == most_common_tag]

        tag = df.iloc[0][TAG_ID]
        # iloc [1:] to skip the first value of tbc_values which could be 0 sometimes. 
        actual_address_value = df.iloc[1:][TBC].mean()  # extract the tbc value from df
        print(f"\nactual address value: {actual_address_value}\nexpected address value: {expected_address_value}")
        THRESHOLD_ADDRESS_VALUE = 5 
        # check if the actual address value is in the range of -+5 of the expected address value
        if not ((expected_address_value-THRESHOLD_ADDRESS_VALUE) <= actual_address_value <= (expected_address_value+THRESHOLD_ADDRESS_VALUE)):
            print(f"\n Address value for tag {tag} is {actual_address_value} when the expected value: {expected_address_value}!\n")
            test.rc = TEST_FAILED
            test.add_reason(f"Address value for tag {tag} is {actual_address_value} instead of {expected_address_value}!")
        if test.params == [mid_values] and delay == 1000:
            # checking 0 value in the first packet.
            first_row = df.iloc[0][TBC]
            second_row = df.iloc[1][TBC]
            if first_row != 0 and second_row != 0:
                test.rc = TEST_FAILED
                test.add_reason(f"first tbc value is not 0 as supposed to be while sanity checking")
    return test 

def mid_values(test, datapath_module):
    # mid values - Sanity check: Generate packets with delays of 1, 5, and 0.5 seconds. Check address values 192, 243, and 128. Verify that the address value is 0 for the first packet.
    SANITY_DELAY_ADDRESS_VALUES = { 1000: 192, 5000: 243, 500: 128 }
    for delay, expected_address_value in SANITY_DELAY_ADDRESS_VALUES.items():
        pacer_interval = 1 
        test = scan_and_compare(test, pacer_interval=pacer_interval, delay=delay, expected_address_value=expected_address_value)  
    time.sleep(2)
    return test
     
def diff_pacer(test, datapath_module):
    # diff pacer - Generate packets with a 1-second delay and pacer intervals of 30 and 60. Ensure the address value remains 192.
    SANITY_ADDRESS_VALUE  = 192 
    PACER_INTERVAL_LIST = [30, 60]
    delay = 1000 # 1 sec
    for pacer_interval in PACER_INTERVAL_LIST:
        test = cert_config.brg_configure(test, fields=[BRG_PACER_INTERVAL], values=[pacer_interval], module=datapath_module)[0]
        if test.rc ==TEST_FAILED:
            test.add_reason(f"Didn't succeed to config pacer interval {pacer_interval}")
            return test 
        test = scan_and_compare(test, pacer_interval=pacer_interval, delay=delay, expected_address_value=SANITY_ADDRESS_VALUE)
    time.sleep(2)
    return test

def min_value(test, datapath_module):
    # min_value -  Minimum value: Generate packets with a 0.1-second delay. Verify that the address value is 1.
    MIN_ADDRESS_VALUE = 1 
    pacer_interval = 1 
    test = cert_config.brg_configure(test, fields=[BRG_PACER_INTERVAL], values=[pacer_interval], module=datapath_module)[0]
    if test.rc ==TEST_FAILED:
        test.add_reason(f"Didn't succeed to config pacer interval {pacer_interval}")
        return test 
    delay = 100
    test = scan_and_compare(test, pacer_interval=pacer_interval ,delay=delay, expected_address_value=MIN_ADDRESS_VALUE)
    time.sleep(2)
    return test 

def max_value(test, datapath_module):
    # max value - Maximum value: Generate packets with a 70-second delay and a pacer interval of 80. Verify that the address value is 255.
    MAX_ADDRESS_VALUE = 255
    pacer_interval = 80
    test = cert_config.brg_configure(test, fields=[BRG_PACER_INTERVAL], values=[pacer_interval], module=datapath_module)[0]
    if test.rc ==TEST_FAILED:
        test.add_reason(f"Didn't succeed to config pacer interval {pacer_interval}")
        return test 
    delay = 70000
    test = scan_and_compare(test, pacer_interval=pacer_interval ,delay=delay, expected_address_value=MAX_ADDRESS_VALUE)
    time.sleep(2)
    return test 

def diff_rate(test, datapath_module):
    # diff rate - a filter: Generate packets with delay 1 and change to 5, according the delay change test the tolerance address value
    pacer_interval = 1 
    delay_duration = [[500, 5], [3000, 3]]
    first_delay = delay_duration[0][0] 
    first_duration = delay_duration[0][1] 
    second_delay = delay_duration[1][0] 
    test = cert_config.brg_configure(test, fields=[BRG_PACER_INTERVAL], values=[pacer_interval], module=datapath_module)[0]
    if test.rc ==TEST_FAILED:
        test.add_reason(f"Didn't succeed to config pacer interval {pacer_interval}")
        return test 
    pixel_sim_thread = cert_data_sim.DataSimThread(test=test, num_of_pixels=1, duplicates=2, delay=first_delay, pkt_types=[0],pixels_type=GEN2)
    pixel_sim_thread.start()
    time_sleep = first_duration-((first_delay/1000)/2)
    print(f"time_sleep:{time_sleep}")
    time.sleep(time_sleep)
    pixel_sim_thread.delay = second_delay
    scan_time = sum(duration for _, duration in delay_duration)+20
    df = cert_common.data_scan(test, scan_time=scan_time, brg_data=(not test.internal_brg), gw_data=test.internal_brg)
    pixel_sim_thread.stop()
    df = df[[TAG_ID, TBC]]
    print(f"df: {df}")

    #NOTE: all the next code rows are specific for the values: delay 0.5 and 3, and in relation address values 128 and 235 
    # check if the last tbc value is as we expected  for delay 3 sec we need to get 235 according to LUT  table
    # we define tolerance of +-2 units for address value 
    if df.iloc[-1][TBC] not in range(232, 237):
        test.rc = TEST_FAILED
        test.add_reason(f"Last tbc value is not within the range of 232 to 236 as expected with delay:{second_delay/1000} sec")

    # verify the first tbc value 
    first_tbc = df.iloc[0][TBC]
    if first_tbc not in range(123,134):
        test.rc = TEST_FAILED
        test.add_reason(f"tbc value of last packet before the delay change is incorrect")

    # check the first change of tbc value after delay changing 
    second_tbc = df.iloc[1][TBC] 
    expected_address_value = 200 
    if not  expected_address_value-2 <= second_tbc <= expected_address_value+2:
        test.rc = TEST_FAILED
        test.add_reason(f"the first change of address value is not correct, alpha filter probably is not define well")
    return test

def run(test):
    # "Test prolog"
    datapath_module = eval_pkt(f'ModuleDatapathV{test.active_brg.api_version}')
    test = cert_common.test_prolog(test)
    if test.rc == TEST_FAILED:
        return cert_common.test_epilog(test)
    
    pacer_interval =1 
    test = cert_config.brg_configure(test, fields=[BRG_PACER_INTERVAL], values=[pacer_interval], module=datapath_module)[0]
    if test.rc ==TEST_FAILED:
        test.add_reason(f"Didn't succeed to config pacer interval {pacer_interval}")
        return test 

    RX_RATE_TEST_MAP = {"mid_values": mid_values, "diff_pacer": diff_pacer, "min_value": min_value, "max_value": max_value, "diff_rate": diff_rate }
    for param in test.params:
        functionality_run_print(param.name)
        test = RX_RATE_TEST_MAP[param.value](test, datapath_module)
        generate_log_file(test, param.name)
        field_functionality_pass_fail_print(test, param.name)
        test.set_phase_rc(param.name, test.rc)
        test.add_phase_reason(param.name, test.reason)
        if test.rc == TEST_FAILED and test.exit_on_param_failure:
            break
        else:
            test.reset_result()

    return cert_common.test_epilog(test)