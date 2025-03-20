from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
from brg_certificate.wlt_types import *
import brg_certificate.cert_common as cert_common

BRG_STAT_SCAN_TIMEOUT = 65


def scan_for_brg_stat(test, timeout=BRG_STAT_SCAN_TIMEOUT, only_hb=False):
    # In case we want to look for HB pkts only - set all modules to be True --> as if there are alredy found
    found = {HB: False, MODULE_IF: False}
    if only_hb is True:
        for pkt_type in found:
            if pkt_type != HB:
                found[pkt_type] = True
    else:  # flash pkts if only_hb=False
        test.mqttc.flush_pkts()

    start_time = datetime.datetime.now()
    # Search for packets
    while not all(found.values()):
        if (cert_mqtt.get_brg2gw_mgmt_pkts(test.mqttc, test, mgmt_types=[eval_pkt(f'Brg2GwHbV{test.active_brg.api_version}')]) and
                not found[HB]):
            found[HB] = True
            print(f"Got HB packet after {(datetime.datetime.now() - start_time).seconds} sec!")
        if (cert_mqtt.get_brg2gw_mgmt_pkts(test.mqttc, test, mgmt_types=[eval_pkt(f'ModuleIfV{test.active_brg.api_version}')]) and
                not found[MODULE_IF]):
            found[MODULE_IF] = True
            print(f"Got interface module packet after {(datetime.datetime.now() - start_time).seconds} sec!")
        print_update_wait()
        if (datetime.datetime.now() - start_time).seconds > timeout:
            test.rc = TEST_FAILED
            err_print = f"{'HB' if not found[HB] else ''} {'MODULE_IF' if not found[MODULE_IF] else ''}"
            test.add_reason(f"Didn't receive {err_print} pkt after {timeout} seconds!")
            break
    return test


def run(test):

    test = cert_common.test_prolog(test)
    if test.rc == TEST_FAILED:
        return cert_common.test_epilog(test)

    test = scan_for_brg_stat(test)
    generate_log_file(test, "stat")

    return cert_common.test_epilog(test)
