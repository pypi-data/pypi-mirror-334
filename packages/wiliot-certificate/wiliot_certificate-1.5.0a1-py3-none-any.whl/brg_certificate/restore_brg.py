import sys
import os
sys.path.insert(0, os.path.abspath(".."))
import argparse
import brg_certificate.cert_common as cert_common
from brg_certificate.cert_utils import *

os.system('')

def main():

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--brg', '-b', required=True, help='Bridge id to restore')
    parser.add_argument('--gw', '-g', required=True, help='GW id to use')
    args = parser.parse_args()
    utPrint(str(args.__dict__))

    mqttc = cert_mqtt.mqttc_init(args.gw, data="sim")
    brg = Bridge(args.brg)
    test = WltTest("", args.gw, mqttc, brg0=brg, server="prod")

    utPrint(SEP)
    utPrint(f"Getting GW {args.gw} Information", "BLUE")
    response = cert_common.get_gw_info(test)
    if response == NO_RESPONSE:
        error = f"ERROR: Didn't get response from {args.gw} !"
        utPrint(error, "red")
        sys.exit(-1)
    else:
        if ENTRIES in response[GW_INFO]:
            test.protobuf = True

    utPrint(SEP)
    utPrint(f"Getting BRG {brg.id_str} interface pkt", "BLUE")
    test, _ = cert_common.get_module_if_pkt(test)
    if test.rc == TEST_PASSED:
        utPrint("Success! Done!", "green")
        sys.exit(0)
    else:
        error = f"ERROR: Didn't get ModuleIfV{test.active_brg.api_version} from BRG:{brg.id_str}!"
        utPrint(error, "red")
        # Send restore defaults for 16 seconds
        test.rc = TEST_PASSED
        print(f"\nSending {ag.ACTIONS_DICT[ag.ACTION_RESTORE_DEFAULTS]}{test.active_brg.api_version} for 16 seconds")
        action_pkt = cert_config.get_default_brg_pkt(test, pkt_type=eval_pkt(f'{ag.ACTIONS_DICT[ag.ACTION_RESTORE_DEFAULTS]}{test.active_brg.api_version}'))
        cert_config.gw_downlink(test, raw_tx_data=action_pkt.dump(), max_retries=cert_config.BLE5_MAX_RETRIES*2)

        print("Waiting for 16*2 seconds broadcast + 30 seconds reboot!")
        for _ in range(16*2 + 30):
            print_update_wait(1)
        test, _ = cert_common.get_module_if_pkt(test)
        if test.rc == TEST_PASSED:
            utPrint("Success! Done!", "green")
            sys.exit(0)
        else:
            error = f"ERROR: Still Didn't get ModuleIfV{test.active_brg.api_version} from BRG:{brg.id_str}!"
            utPrint(error, "red")
            sys.exit(-1)

if __name__ == "__main__":
    main()