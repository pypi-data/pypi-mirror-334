# This test check for the algo of the adaptive pacer - run with 1 gw & 1 brg
# In order to have a lot of stress on the BRG you best use ble sim with pacer_algo_test_pkts.csv
from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
from brg_certificate.wlt_types import *
import brg_certificate.cert_common as cert_common
import brg_certificate.cert_config as cert_config

def effective_pacer_increment_highest_get(test):
    cert_config.send_brg_action(test, ag.ACTION_SEND_HB)
    test, mgmt_pkts = cert_common.scan_for_mgmt_pkts(test, [eval_pkt(f'Brg2GwHbV{test.active_brg.api_version}')])
    highest = 0
    if mgmt_pkts:
        for p in mgmt_pkts:
            if p[MGMT_PKT].pkt.effective_pacer_increment:
                highest = p[MGMT_PKT].pkt.effective_pacer_increment if p[MGMT_PKT].pkt.effective_pacer_increment > highest else highest
    return highest

def run(test):

    fields = [BRG_ADAPTIVE_PACER, BRG_PACER_INTERVAL, BRG_PKT_FILTER, BRG_TX_REPETITION]
    values = [ag.ADAPTIVE_PACER_ON, 1, ag.PKT_FILTER_TEMP_ADVANCED_AND_DEBUG_PKTS, 1]
    datapath_module = eval_pkt(f'ModuleDatapathV{test.active_brg.api_version}')
    calib_module = eval_pkt(f'ModuleCalibrationV{test.active_brg.api_version}')

    test = cert_common.test_prolog(test)
    if test.rc == TEST_FAILED:
        return cert_common.test_epilog(test)

    # Turn on adaptive pacer and set cfgs to help activating adaptive pacer algo
    test = cert_config.brg_configure(test, fields=fields, values=values, module=datapath_module)[0]
    if test.rc == TEST_FAILED:
        return cert_common.test_epilog(test, revert_brgs=True, modules=[datapath_module])
    test = cert_config.brg_configure(test, fields=[BRG_CALIB_INTERVAL], values=[30], module=calib_module)[0]
    if test.rc == TEST_FAILED:
        return cert_common.test_epilog(test, revert_brgs=True, modules=[calib_module])

    # Wait for tx rep algo to work & then activate pacing algo
    # Checking effective_pacer_increment every minute untill its
    # stable for 3 mins to start checking tags actual pacing
    effective_pacer_increment = False
    last_incarement = 0
    count = 0
    for i in range(10):
        effective_pacer_increment = effective_pacer_increment_highest_get(test)
        print(f"Current eff_pacer_increment = {effective_pacer_increment}, i = {i}")

        if effective_pacer_increment == 0:
            if i == 10:
                test.rc == TEST_FAILED
                test.add_reason("The effective_pacer_increment is 0 after 10 minutes")
                return cert_common.test_epilog(test)
            cert_common.wait_time_n_print(15)
            continue

        if last_incarement == effective_pacer_increment:
            count += 1
            if count == 3:
                break
        else:
            last_incarement = effective_pacer_increment

    if count != 3:
        test.rc == TEST_FAILED
        test.add_reason("The effective_pacer_increment havn't been stable for 10 minutes")
        return cert_common.test_epilog(test)

    df = cert_common.data_scan(test, scan_time=60, brg_data=(not test.internal_brg), gw_data=test.internal_brg)
    cert_mqtt.dump_pkts(test, log=str(values))
    cert_common.display_data(df, nfpkt=True, pkt_cntr_diff=True, cer_per_tag=True, name_prefix=test.module_name, dir=test.dir)

    test = cert_common.pacing_analysis(test, df=df, pacer_interval=1+effective_pacer_increment)
    if test.rc == TEST_FAILED:
        return cert_common.test_epilog(test, revert_brgs=True, modules=[datapath_module, calib_module])

    return cert_common.test_epilog(test, revert_brgs=True, modules=[datapath_module, calib_module])
