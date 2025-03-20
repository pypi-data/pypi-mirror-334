# This test will run on "params" mode when it gets parameters in its call - check config only
# Otherwise it will run on "auto" mode - collect packets and analyse packets actual repetitions

from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
from brg_certificate.wlt_types import *
import brg_certificate.cert_common as cert_common
import brg_certificate.cert_config as cert_config
import brg_certificate.cert_data_sim as cert_data_sim
from brg_certificate.cert_gw_sim import DEDUPLICATION_PKTS
import statistics

TX_REPETITION_THRESHOLD =  0.5

def tx_repetitions_analysis(test, repetitions):
    cert_common.wait_time_n_print(CLEAR_DATA_PATH_TIMEOUT)
    test.mqttc.flush_pkts()
    if test.data == DATA_SIMULATION:
        pixel_sim_thread = cert_data_sim.DataSimThread(test=test, num_of_pixels=15, duplicates=1, delay=100, pkt_types=[0])
        pixel_sim_thread.start()
    mqtt_scan_wait(test, 60)
    if test.data == DATA_SIMULATION:
        pixel_sim_thread.stop() # stop generating pkts on data simulator
        cert_common.wait_time_n_print(CLEAR_DATA_PATH_TIMEOUT) # Wait for sim queue to free
    pkts = cert_mqtt.get_unified_data_pkts(test)
    print(f"Found {len(pkts)} packets")
    if len(pkts) == 0:
        test.rc = TEST_FAILED
        test.add_reason(f"For repetitions {repetitions} found 0 pkts!")
        generate_log_file(test, repetitions)
        return test
    pkt_payload_counter = {}
    for p in pkts:
        cur_pkt = p[PAYLOAD]
        if cur_pkt in pkt_payload_counter:
            pkt_payload_counter[cur_pkt] += 1
        else:
            pkt_payload_counter[cur_pkt] = 1
    generate_log_file(test, repetitions)
    avg = statistics.mean([pkt_payload_counter[p] for p in pkt_payload_counter])
    txt = f"For TX repetition = {repetitions}, average {round(avg, 3)} repetitions"
    print(txt)
    if (avg / float(repetitions)) <= TX_REPETITION_THRESHOLD or (avg / float(repetitions)) > 1:
        test.rc = TEST_FAILED
        test.add_reason(txt)
    return test

def run(test):

    fields = [BRG_TX_REPETITION, BRG_PKT_FILTER, BRG_RX_CHANNEL]

    datapath_module = eval_pkt(f'ModuleDatapathV{test.active_brg.api_version}')

    test = cert_common.test_prolog(test)
    if test.rc == TEST_FAILED:
        return cert_common.test_epilog(test)

    print("Configuring GW with !deduplication_pkts 0")
    cert_config.gw_action(test, f"{DEDUPLICATION_PKTS} 0")
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        return cert_common.test_epilog(test, revert_gws=True)

    for param in test.params:
        test = cert_config.brg_configure(test, fields=fields, values=[param.value, ag.PKT_FILTER_RANDOM_FIRST_ARRIVING_PKT, ag.RX_CHANNEL_37], module=datapath_module)[0]
        if test.rc == TEST_FAILED and test.exit_on_param_failure:
            break
        tx_repetitions_analysis(test, param.name)
        field_functionality_pass_fail_print(test, fields[0], value=param.name)
        test.set_phase_rc(param.name, test.rc)
        test.add_phase_reason(param.name, test.reason)
        if test.rc == TEST_FAILED and test.exit_on_param_failure:
            break
        else:
            test.reset_result()

    
    # Re-enable unified packets deduplication
    cert_config.gw_action(test, f"{DEDUPLICATION_PKTS} 1")
    return cert_common.test_epilog(test, revert_brgs=True, revert_gws=True, modules=[datapath_module])
