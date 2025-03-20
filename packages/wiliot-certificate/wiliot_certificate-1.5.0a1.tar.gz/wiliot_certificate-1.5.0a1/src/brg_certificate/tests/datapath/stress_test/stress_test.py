from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
from brg_certificate.wlt_types import *
import brg_certificate.cert_common as cert_common
import brg_certificate.cert_config as cert_config
import brg_certificate.cert_data_sim as cert_data_sim
from brg_certificate.cert_gw_sim import DEDUPLICATION_PKTS
import statistics
import time

def configure_pacer_n_times(test, num_of_times, pacer_interval, datapath_module):
    test = cert_config.brg_configure(test, fields=[BRG_PACER_INTERVAL], values=[pacer_interval], module=datapath_module)[0]
    if test.rc == TEST_FAILED:
        for i in range(num_of_times):
            if test.rc == TEST_PASSED:
                return test
            print(f"sleeping for 10 seconds before trying to configure pacer again\n")
            time.sleep(10)
            test = cert_config.brg_configure(test, fields=[BRG_PACER_INTERVAL], values=[pacer_interval], module=datapath_module)[0]
        test.add_reason("Didn't succeed to configure after two attempts - No pkt was found!")
    return test

def metric_checking_HB(test, mgmt_type_list, tx_queue_expected, pacer_increment_expected):
    if not mgmt_type_list:
        test.add_reason("\nDidn't find HB pkt, therefore will not check tx_queue and pacer increment\n")
        print(f"Didn't find HB pkt, therefore will not check tx_queue and pacer increment")
    else:
        #check tx queue 
        watermarks = [pkt.tx_queue_watermark for pkt in mgmt_type_list]
        half_index = len(watermarks) // 2
        tx_queue_HB = statistics.mean(watermarks[half_index:])
        if not (tx_queue_expected[0] <= tx_queue_HB <= tx_queue_expected[1]):
            test.add_reason(f"tx_queue: {tx_queue_HB}")
            print(f"\ntx_queue value is wrong!\nexpected: {tx_queue_expected}, got: {tx_queue_HB}")
        else:
            test.add_reason(f"tx_queue: {tx_queue_HB}")
            print(f"\ntx_queue from HB : {tx_queue_HB}\n")
        
        # check pacer increment
        pacer_increment_HB = [pkt.effective_pacer_increment for pkt in mgmt_type_list]
        average_pacer_increment_HB = statistics.mean(pacer_increment_HB)
        if not (pacer_increment_expected[0] <= average_pacer_increment_HB <= pacer_increment_expected[1]):
            test.add_reason(f"pacer_increment:{average_pacer_increment_HB}")
            print(f"\npacer_increment value is wrong\nexpected: {pacer_increment_expected}\ngot: {average_pacer_increment_HB}")
        else:
            test.add_reason(f"pacer_increment: {average_pacer_increment_HB}")
            print(f"\naverage pacer_increment from HB: {average_pacer_increment_HB}\n")
    return test

def metric_checking_df(test, check,  pacer_interval, df, repetition_value_expected,  brg_latency_expected, num_of_pixels_expected):
    if df.empty:
        print(f" df is empty, therefore will not check repetitions, brg latency and num of tags")
        test.rc = TEST_FAILED
        test.add_reason(f"df is empty, therefore will not check repetitions, brg latency and num of tags")
    else:
        print(f"result of pacer interval: {pacer_interval}\n")
        # check repetition value
        payload_counts_per_tag = df.groupby(TAG_ID)[PAYLOAD].value_counts()
        average_payload_count = round(payload_counts_per_tag.mean(), 2)
        if not repetition_value_expected[0] <= average_payload_count <= repetition_value_expected[1]:
            if check:
                test.rc = TEST_FAILED
                test.add_reason(f"Repetition:{average_payload_count}, expected: {repetition_value_expected},")
                print(f"Repetition value is wrong! \nexpected:{repetition_value_expected}\ngot: {average_payload_count}")
            else:   
                test.add_reason(f"Repetition:{average_payload_count}, expected: {repetition_value_expected},")
                print(f"Repetition value is wrong! \nexpected:{repetition_value_expected}\ngot: {average_payload_count}")
        else:
            test.add_reason(f"Repetition value: {average_payload_count}")
            print(f"Repetition value is correct! got: {average_payload_count}")
    
        # check num of tags, with tolerance of 5%
        num_of_tags = len(df[TAG_ID].unique()) 
        if not num_of_pixels_expected*0.95 <= num_of_tags <= num_of_pixels_expected*1.05:
            test.add_reason(f"num of tags:  {num_of_tags}")
            print(f"\n num of tags is not as expected\nexpected: {num_of_pixels_expected}, got: {num_of_tags}")
        else:
            test.add_reason(f"num of tags: {num_of_tags}")
            print(f"\nnum of tags from df: {num_of_tags}\n")
        
        #check brg_latency
        if check:
            brg_latency_avg = round(df[BRG_LATENCY].mean(),2)
            if not (brg_latency_expected[0] <= brg_latency_avg <= brg_latency_expected[1]):
                test.add_reason(f"brg_latency:{brg_latency_avg}")
                print(f"Average brg_latency: {brg_latency_avg}")
            else:
                test.add_reason(f"brg_latency: {brg_latency_avg}")
                print(f"Average brg_latency: {brg_latency_avg}")
        else:
            brg_latency_avg = round(df[BRG_LATENCY].mean(),2)
            print(f"Average brg_latency: {brg_latency_avg}")
    return test 

def combination_func(test, datapath_module, pacer_interval, num_of_sim_tags, repetition_value_expected, tx_queue_expected, pacer_increment_expected, brg_latency_expected):
    test = configure_pacer_n_times(test, 2, pacer_interval, datapath_module)
    time.sleep(30)
# first df 
    df = cert_common.data_scan(test, scan_time=30, brg_data=(not test.internal_brg), gw_data=test.internal_brg)
    cert_common.display_data(df, nfpkt=True, tbc=True, name_prefix=f"stress_{pacer_interval}_", dir=test.dir)
    test, hbs = cert_common.scan_for_mgmt_pkts(test, [eval_pkt(f'Brg2GwHbV{test.active_brg.api_version}')])
    print(f"number of HB packets: {len(hbs)}") # TODO remove
    for p in hbs: # TODO remove
        print(f"WATERMARK:{p[MGMT_PKT].pkt.tx_queue_watermark}, pacer increment:{p[MGMT_PKT].pkt.effective_pacer_increment} ") # TODO remove
    hbs = [p[MGMT_PKT].pkt for p in hbs] 
    print(f"result of first df\n")
    check = False
    test = metric_checking_df(test, check, pacer_interval, df, repetition_value_expected, brg_latency_expected, num_of_sim_tags)
    time.sleep(30)
# second df
    df = cert_common.data_scan(test, scan_time=60, brg_data=(not test.internal_brg), gw_data=test.internal_brg)
    cert_common.display_data(df, nfpkt=True, tbc=True, name_prefix=f"stress_{pacer_interval}_", dir=test.dir)
    test, hbs = cert_common.scan_for_mgmt_pkts(test, [eval_pkt(f'Brg2GwHbV{test.active_brg.api_version}')])
    hbs = [p[MGMT_PKT].pkt for p in hbs] 
    print(f"result of second df\n")
    check = True
    test = metric_checking_df(test, check, pacer_interval, df, repetition_value_expected, brg_latency_expected, num_of_sim_tags)
    test = metric_checking_HB(test, hbs, tx_queue_expected, pacer_increment_expected)
    return test

def rep3(test, datapath_module, num_of_sim_tags, pixel_sim_thread):
    # step 1 - config pacer interval=15 , then check repetition value = 3, tx_queue ~ 0, pacer increment ~ 0, brg latency ~ 0 , num of tags = all tags.
    pacer_interval = 20 
    test = combination_func(test, datapath_module, pacer_interval=pacer_interval, num_of_sim_tags=num_of_sim_tags, repetition_value_expected=[2,3], tx_queue_expected=[20,40], pacer_increment_expected=[0,2], brg_latency_expected=[0,10])
    time.sleep(5)
    return test

def rep2(test, datapath_module, num_of_sim_tags, pixel_sim_thread):
    #"step 2 - config pacer interval 9, then check repetition value = 2, tx_queue = 20-40, pacer increment = 0, brg latency = 0-200, num of tags = all tags"
    pacer_interval = 15
    test = combination_func(test, datapath_module, pacer_interval=pacer_interval, num_of_sim_tags=num_of_sim_tags, repetition_value_expected=[1.5,2.5], tx_queue_expected=[20,40], pacer_increment_expected=[0,2], brg_latency_expected=[10,200])
    # for checking if it's affect of the running that df is empty.
    time.sleep(5)
    return test

def rep1(test, datapath_module, num_of_sim_tags, pixel_sim_thread):
    # "step 3 - config pacer interval 6 , then check repetition value = 1, tx_queue 40-60, pacer increment ~ 0, brg latency 200-300 , num of tags = all tags"
    pacer_interval = 9
    test = combination_func(test, datapath_module, pacer_interval=pacer_interval, num_of_sim_tags=num_of_sim_tags, repetition_value_expected=[1,2], tx_queue_expected=[20,40], pacer_increment_expected=[0,2], brg_latency_expected=[200,300])
    time.sleep(5)
    return test

def rep1_adaptive_pacer(test, datapath_module, num_of_sim_tags, pixel_sim_thread):
    # "step 4 - config pacer interval 1  , then check repetition value = 1, tx_queue > 60, pacer increment = 3 , brg latency > 300 , num of tags = all tags"
    pacer_interval = 1 
    test = combination_func(test, datapath_module, pacer_interval=pacer_interval, num_of_sim_tags=num_of_sim_tags, repetition_value_expected=[1,2], tx_queue_expected=[20,40], pacer_increment_expected=[2,20], brg_latency_expected=[300,1000])
    time.sleep(5)
    return test

def pixels_burst(test, datapath_module, num_of_sim_tags, pixel_sim_thread):
    #NOTE: I had to change the pattern because there isn't option to increase the the pixels number in the same thread it will cause error "index out of bound"
    # "step 5- config pacer interval 15 , then add more 200 packets with 0 delay(0.02 sec) , then check repetition value = 1 and not 2 "
    pixel_sim_thread.stop()
    pacer_interval = 15
    test = configure_pacer_n_times(test, 2, pacer_interval, datapath_module)
    pixel_sim_thread = cert_data_sim.DataSimThread(test=test, num_of_pixels=num_of_sim_tags, duplicates=1, delay=0, pkt_types=[0],pixels_type=GEN2)
    pixel_sim_thread.start()
    df = cert_common.data_scan(test, scan_time=180 , brg_data=(not test.internal_brg), gw_data=test.internal_brg)
    check = True
    test = metric_checking_df(test, check, pacer_interval, df, [2,3], [0,10], 200)
    # we must have df, so we will try twice again to get it
    if test.rc == TEST_FAILED:
        for i in range(2):
            if test.rc == TEST_PASSED:
                break
            df = cert_common.data_scan(test, scan_time=30 , brg_data=(not test.internal_brg), gw_data=test.internal_brg)
            test =metric_checking_df(test, check, pacer_interval, df, [2,3], [0,10], 200)    
    pixel_sim_thread.stop()
    #change the number of pixels to 400, and check that the repetition value is 1 in short time 
    pixel_sim_thread = cert_data_sim.DataSimThread(test=test, num_of_pixels=400, duplicates=1, delay=0, pkt_types=[0],pixels_type=GEN2)
    pixel_sim_thread.start()
    df = cert_common.data_scan(test, scan_time=30 , brg_data=(not test.internal_brg), gw_data=test.internal_brg)
    test = metric_checking_df(test, check, pacer_interval, df, [1,2], [0,10], 400)    
    pixel_sim_thread.stop()
    return test

def run(test):
    # Test prolog
    datapath_module = eval_pkt(f'ModuleDatapathV{test.active_brg.api_version}')
    test = cert_common.test_prolog(test)
    if test.rc == TEST_FAILED:
        return cert_common.test_epilog(test)
    #config GW deduplication pkts = 0  "
    print("Configuring GW with !deduplication_pkts 0")
    cert_config.gw_action(test, f"{DEDUPLICATION_PKTS} 0")
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        return cert_common.test_epilog(test, revert_gws=True)

    STRESS_TEST_MAP = {"rep3":rep3, "rep2": rep2 ,"rep1": rep1,  "rep1_adaptive_pacer":rep1_adaptive_pacer, "pixels_burst":pixels_burst}
    num_of_pixels = 300
    pixel_sim_thread = cert_data_sim.DataSimThread(test=test, num_of_pixels=num_of_pixels, duplicates=1, delay=0, pkt_types=[0],pixels_type=GEN2)
    pixel_sim_thread.start()
    time.sleep(30)
    for param in test.params:
        functionality_run_print(param.name)
        test = STRESS_TEST_MAP[param.value](test, datapath_module, num_of_pixels, pixel_sim_thread)
        generate_log_file(test, param.name)
        field_functionality_pass_fail_print(test, param.name)
        test.set_phase_rc(param.name, test.rc)
        test.add_phase_reason(param.name, test.reason)
        if test.rc == TEST_FAILED and test.exit_on_param_failure:
            break
        else:
            test.reset_result()
        time.sleep(5)
    pixel_sim_thread.stop()
    # Re-enable unified packets deduplication
    cert_config.gw_action(test, f"{DEDUPLICATION_PKTS} 1")

    return cert_common.test_epilog(test, revert_brgs=True, revert_gws=True, modules=[datapath_module])