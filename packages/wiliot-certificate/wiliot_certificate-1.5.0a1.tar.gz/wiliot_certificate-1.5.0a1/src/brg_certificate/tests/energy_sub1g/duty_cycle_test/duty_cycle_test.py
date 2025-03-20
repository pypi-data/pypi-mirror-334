from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
from brg_certificate.wlt_types import *
import brg_certificate.cert_common as cert_common
import brg_certificate.cert_config as cert_config

def run(test):

    fields = [BRG_DUTY_CYCLE]
    sub1g_module = eval_pkt(f'ModuleEnergySub1GV{test.active_brg.api_version}')

    test = cert_common.test_prolog(test)
    if test.rc == TEST_FAILED:
        return cert_common.test_epilog(test)
    for param in test.params:
        param_name = f"{param.name}"
        test = cert_config.brg_configure(test, fields=fields, values=[param.value], module=sub1g_module)[0]
        generate_log_file(test, param_name)
        field_functionality_pass_fail_print(test, fields, value=param_name)
        test.set_phase_rc(param.name, test.rc)
        test.add_phase_reason(param.name, test.reason)
        if test.rc == TEST_FAILED and test.exit_on_param_failure:
            break
        else:
            test.reset_result()

    return cert_common.test_epilog(test, revert_brgs=True, modules=[sub1g_module])