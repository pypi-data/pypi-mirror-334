from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
from brg_certificate.wlt_types import *
import brg_certificate.cert_common as cert_common
import brg_certificate.cert_config as cert_config

def is_primary_channel(channel):
    if channel == ag.RX_CHANNEL_37 or channel == ag.RX_CHANNEL_38 or channel == ag.RX_CHANNEL_39:
        return True
    else:
        return False

def run(test):

    fields = [BRG_RX_CHANNEL]
    print(test.params)
    datapath_module = eval_pkt(f'ModuleDatapathV{test.active_brg.api_version}')
    ble5_state =  False # We use this flag to know whether the BRG is currently in BLE5 mode and needs special configuration next time it is configured

    test = cert_common.test_prolog(test)
    if test.rc == TEST_FAILED:
        return cert_common.test_epilog(test)

    for param in test.params:
        if ble5_state:
            test = cert_config.brg_configure_ble5(test, fields=fields, values=[param.value], module=datapath_module)[0]
        else:
            test = cert_config.brg_configure(test, fields=fields, values=[param.value], module=datapath_module)[0]

        # param epilog
        ble5_state = not is_primary_channel(param.value)
        generate_log_file(test, param.name)
        field_functionality_pass_fail_print(test, fields[0], value=param.name)
        test.set_phase_rc(param.name, test.rc)
        test.add_phase_reason(param.name, test.reason)
        if test.rc == TEST_FAILED and test.exit_on_param_failure:
            break
        else:
            test.reset_result()

    return cert_common.test_epilog(test, revert_brgs=True, modules=[datapath_module], ble5=ble5_state)