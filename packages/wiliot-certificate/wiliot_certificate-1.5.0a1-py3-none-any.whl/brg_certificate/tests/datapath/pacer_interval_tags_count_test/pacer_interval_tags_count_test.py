from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
from brg_certificate.wlt_types import *
import brg_certificate.cert_common as cert_common
import brg_certificate.cert_config as cert_config

def run(test):
    pacer_threshold = PACER_INTERVAL_THRESHOLD_HIGH if test.private_setup else PACER_INTERVAL_THRESHOLD

    fields = [BRG_PACER_INTERVAL, BRG_TX_REPETITION]
    datapath_module = eval_pkt(f'ModuleDatapathV{test.active_brg.api_version}')

    test = cert_common.test_prolog(test)
    if test.rc == TEST_FAILED:
        return cert_common.test_epilog(test)

    # Configure the GW to receive tags pkt
    if test.internal_brg:
        test = cert_config.brg_configure(test, fields=[BRG_RX_CHANNEL], values=[ag.RX_CHANNEL_37], module=datapath_module, wait=True)[0]
        if test.rc == TEST_FAILED:
            return cert_common.test_epilog(test, revert_gws=True)

    num_of_pixels = 200
    if test.data == DATA_SIMULATION:
        # start generating pkts and send them using data simulator
        pixel_sim_thread = cert_data_sim.DataSimThread(test=test, num_of_pixels=num_of_pixels, duplicates=3, delay=0, pkt_types=[0])
        pixel_sim_thread.start()

    tags_count_per_pacer = {}
    for param in test.params:
        test = cert_config.brg_configure(test, fields=fields, values=[param.value, 1], module=datapath_module)[0]
        if test.rc == TEST_FAILED and test.exit_on_param_failure:
            generate_log_file(test, param.name)
            return cert_common.test_epilog(test, revert_brgs=True, revert_gws=test.internal_brg, modules=[datapath_module])
        df = cert_common.data_scan(test, scan_time=120, brg_data=True)
        cert_common.display_data(df, nfpkt=True, tbc=True, name_prefix=f"brg_pacer_tags_count_{param.name}_", dir=test.dir)
        tags_count_per_pacer[param.value] = df[TAG_ID].nunique()
        generate_log_file(test, param.name)
        test.set_phase_rc(param.name, test.rc)
        test.add_phase_reason(param.name, test.reason)
        if test.rc == TEST_FAILED and test.exit_on_param_failure:
            return cert_common.test_epilog(test, revert_brgs=True, revert_gws=test.internal_brg, modules=[datapath_module])
        else:
            test.reset_result()

    if test.data == DATA_SIMULATION:
        # stop generating pkts with data simulator and wait a few seconds for full flush
        pixel_sim_thread.stop()
        time.sleep(5)

    print("tags_count_per_pacer: ", tags_count_per_pacer)
    max_count = max([tags_count_per_pacer[pacer] for pacer in tags_count_per_pacer])
    for param in test.params:
        if test.data == DATA_SIMULATION:
            if tags_count_per_pacer[param.value] != num_of_pixels:
                test.set_phase_rc(param.name, TEST_FAILED)
                test.add_phase_reason(param.name, f"received_tags={tags_count_per_pacer[param.value]} num_of_pixels={num_of_pixels}")
        # make sure minimal received tags number is more than minimal threshold (precentile from max) (diff of less than 3 tags will be accepted anyway)
        elif tags_count_per_pacer[param.value] < (pacer_threshold * max_count) and (max_count - tags_count_per_pacer[param.value]) > 3:
            test.set_phase_rc(param.name, TEST_FAILED)
            test.add_phase_reason(param.name, f"received_tags={tags_count_per_pacer[param.value]} max_tags={max_count} less than {int(pacer_threshold * 100)}%")

    return cert_common.test_epilog(test, revert_brgs=True, revert_gws=test.internal_brg, modules=[datapath_module])
