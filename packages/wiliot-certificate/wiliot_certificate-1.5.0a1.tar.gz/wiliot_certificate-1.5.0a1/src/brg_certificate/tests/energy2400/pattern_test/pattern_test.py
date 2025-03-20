from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
from brg_certificate.wlt_types import *
import brg_certificate.cert_common as cert_common
import brg_certificate.cert_config as cert_config

def run(test):

    fields = [BRG_PATTERN]
    energy2400_module = eval_pkt(f'ModuleEnergy2400V{test.active_brg.api_version}')

    test = cert_common.test_prolog(test)
    if test.rc == TEST_FAILED:
        return cert_common.test_epilog(test)

    for param in test.params:
        test = cert_config.brg_configure(test, fields=fields, values=[param.value], module=energy2400_module)[0]
        # param epilog
        generate_log_file(test, param.name)
        field_functionality_pass_fail_print(test, fields[0], value=param.name)
        test.set_phase_rc(param.name, test.rc)
        test.add_phase_reason(param.name, test.reason)
        if test.rc == TEST_FAILED and test.exit_on_param_failure:
            break
        else:
            test.reset_result()

    return cert_common.test_epilog(test, revert_brgs=True, modules=[energy2400_module])