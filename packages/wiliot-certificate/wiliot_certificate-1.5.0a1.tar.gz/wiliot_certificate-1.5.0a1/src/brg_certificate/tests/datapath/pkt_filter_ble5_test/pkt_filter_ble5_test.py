from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
from brg_certificate.ag.wlt_types_ag import *
import brg_certificate.cert_common as cert_common
import brg_certificate.cert_config as cert_config

PKT_FILTER_TEST_PACER_INTERVAL = 10

def run(test):

    fields = [BRG_PKT_FILTER, BRG_RX_CHANNEL, BRG_PACER_INTERVAL]
    datapath_module = eval(f'ModuleDatapathV{test.active_brg.api_version}')

    test = cert_common.test_prolog(test)
    if test.rc == TEST_FAILED:
        return cert_common.test_epilog(test)


    for param in test.params:
        test = cert_config.brg_configure_ble5(test, fields=fields, values=[param.value, RX_CHANNEL_10_250K, PKT_FILTER_TEST_PACER_INTERVAL], module=datapath_module)[0]
        test.set_phase_rc(param.name, test.rc)
        test.add_phase_reason(param.name, test.reason)
        if test.rc == TEST_FAILED and test.exit_on_param_failure:
            break
        else:
            test.reset_result()
        print("waiting 5 seconds for datapath to clear")
        print_update_wait(5)
        num_of_pixels = 0
        if test.data == DATA_SIMULATION:
            # start generating pkts and send them using data simulator
            num_of_pixels = 5
            pixel_sim_thread = cert_data_sim.DataSimThread(test=test, num_of_pixels=num_of_pixels, duplicates=2, delay=0, pkt_types=[2], pixels_type=GEN3_EXTENDED)
            pixel_sim_thread.start()
        df = cert_common.data_scan(test, brg_data=(not test.internal_brg), gw_data=test.internal_brg, scan_time=PKT_FILTER_TEST_PACER_INTERVAL*6, per_pkt_type=True, pkt_filter_cfg=param.value, flush_pkts=True)
        if test.data == DATA_SIMULATION:
            # stop generating pkts with data simulator and wait a few seconds for full flush
            pixel_sim_thread.stop()
            time.sleep(5)
        cert_common.display_data(df, nfpkt=True, tbc=True, name_prefix=f"{param.name}_", dir=test.dir)
        test = cert_common.pacing_analysis(test, pacer_interval=PKT_FILTER_TEST_PACER_INTERVAL, df=df, pkt_filter_cfg=param.value, num_of_pixels=num_of_pixels, is_ble5_test=True)
        generate_log_file(test, param.name)
        field_functionality_pass_fail_print(test, fields[0], value=param.name)
        test.set_phase_rc(param.name, test.rc)
        test.add_phase_reason(param.name, test.reason)
        if test.rc == TEST_FAILED and test.exit_on_param_failure:
            break
        else:
            test.reset_result()

    return cert_common.test_epilog(test, revert_brgs=True, revert_gws=test.internal_brg, modules=[datapath_module], ble5=True)
