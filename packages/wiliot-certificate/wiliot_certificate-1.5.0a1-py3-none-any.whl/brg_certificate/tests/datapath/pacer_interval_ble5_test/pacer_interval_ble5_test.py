from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
from brg_certificate.wlt_types import *
import brg_certificate.cert_common as cert_common
import brg_certificate.cert_config as cert_config

def run(test):

    fields = [BRG_PACER_INTERVAL, BRG_RX_CHANNEL, BRG_PKT_FILTER]
    datapath_module = eval_pkt(f'ModuleDatapathV{test.active_brg.api_version}')

    test = cert_common.test_prolog(test)
    if test.rc == TEST_FAILED:
        return cert_common.test_epilog(test)

    for param in test.params:
        test = cert_config.brg_configure_ble5(test, fields=fields, values=[param.value, ag.RX_CHANNEL_10_250K, ag.PKT_FILTER_TEMP_PKT], module=datapath_module)[0]
        if test.rc == TEST_FAILED and test.exit_on_param_failure:
            break
        num_of_pixels = 0
        if test.data == DATA_SIMULATION:
            # start generating pkts and send them using data simulator
            num_of_pixels = 10
            pixel_sim_thread = cert_data_sim.DataSimThread(test=test, num_of_pixels=num_of_pixels, duplicates=2, delay=0, pkt_types=[2], pixels_type=GEN3_EXTENDED)
            pixel_sim_thread.start()
        df = cert_common.data_scan(test, scan_time=param.value*4, brg_data=(not test.internal_brg), gw_data=test.internal_brg)
        if test.data == DATA_SIMULATION:
            # stop generating pkts with data simulator and wait a few seconds for full flush
            pixel_sim_thread.stop()
            time.sleep(5)
        cert_mqtt.dump_pkts(test, log=param.name)
        cert_common.display_data(df, nfpkt=True, tbc=True, name_prefix=f"brg_pacer_{param.name}_", dir=test.dir)
        test = cert_common.pacing_analysis(test, df=df, pacer_interval=param.value, num_of_pixels=num_of_pixels)
        generate_log_file(test, param.name)
        field_functionality_pass_fail_print(test, fields[0], value=param.name)
        test.set_phase_rc(param.name, test.rc)
        test.add_phase_reason(param.name, test.reason)
        if test.rc == TEST_FAILED and test.exit_on_param_failure:
            break
        else:
            test.reset_result()

    return cert_common.test_epilog(test, revert_brgs=True, revert_gws=test.internal_brg, modules=[datapath_module], ble5=True)
