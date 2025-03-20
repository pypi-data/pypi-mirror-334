
import time
from argparse import ArgumentParser

from gw_certificate.common.debug import debug_print
from gw_certificate.gw_certificate import GWCertificate, GW_CERT_VERSION
from gw_certificate.tests import TESTS
from gw_certificate.tests.actions import ACTIONS_STAGES
from gw_certificate.tests.throughput import STRESS_DEFAULT_PPS, StressTest
from gw_certificate.tests.registration import REG_CERT_OWNER_ID, RegistrationTest
from gw_certificate.tests.uplink import UplinkTest

def filter_by_args(args_list, list_to_filter):
    chosen_list = []
    for entry in list_to_filter:
        for arg in args_list:
            if arg in entry.__name__.lower() and entry not in chosen_list:
                chosen_list.append(entry)
    return chosen_list

def filter_tests(tests_names):
    return filter_by_args(tests_names, TESTS)

def filter_actions(actions_names):
    return filter_by_args(actions_names, ACTIONS_STAGES)

def main():
    usage = (
        "usage: wlt-gw-certificate [-h] -owner OWNER -gw GW\n"
        f"                          [-tests {{connection, uplink, downlink, stress}}] [-update] [-pps {STRESS_DEFAULT_PPS}]\n"
        "                           [-agg AGG] [-env {prod, test, dev}] [-no-reboot]"
        )

    parser = ArgumentParser(prog='wlt-gw-certificate',
                            description=f'Gateway Certificate v{GW_CERT_VERSION} - CLI Tool to test Wiliot GWs', usage=usage)

    required = parser.add_argument_group('required arguments')
    required.add_argument('-gw', type=str, help="Gateway ID", required=True)
    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('-owner', type=str, help="Owner ID", required=False, default=REG_CERT_OWNER_ID)
    optional.add_argument('-suffix', type=str, help="Topic suffix", default='', required=False)
    optional.add_argument('-tests', type=str, choices=['registration', 'connection', 'uplink', 'downlink', 'actions', 'stress'],
                          help="Tests to run. Registration omitted by default.", required=False, nargs='+',
                          default=['connection', 'uplink', 'downlink', 'actions', 'stress'])
    optional.add_argument('-actions', type=str, choices=['info', 'reboot', 'bridgeota'],
                          help="Action stages to run under ActionsTest", required=False, nargs='+', default=['info', 'reboot', 'ota'])
    optional.add_argument('-update', action='store_true', help='Update test board firmware', default=False, required=False)
    optional.add_argument('-pps', type=int, help='Single packets-per-second rate to simulate in the stress test',
                          choices=STRESS_DEFAULT_PPS, default=None, required=False)
    optional.add_argument('-agg', type=int, help='Aggregation time [seconds] the Uplink stages wait before processing results',
                          default=0, required=False)
    optional.add_argument('-env', type=str, help='Environment for the RegistrationTest & BridgeOTAStage',
                          choices=['prod', 'test', 'dev'], default='prod', required=False)
    args = parser.parse_args()

    topic_suffix = '' if args.suffix == '' else '-'+args.suffix
    tests = filter_tests(args.tests)
    actions = filter_actions(args.actions)

    # Validate args combination before running
    if args.pps != None and StressTest not in tests:
        parser.error("Packets per second (-pps) flag can only be used when 'stress' is included in test list (e.g. -tests stress)")
    if args.agg != 0 and not any(t in tests for t in (UplinkTest, StressTest)):
        parser.error("Aggregation time (-agg) flag can only be used when 'uplink' or 'stress' are included in test list (e.g. -tests uplink)")

    if RegistrationTest in tests:
        if not all(test == RegistrationTest for test in tests):
            parser.error("The registration test must be run on it's own, without any others tests.")
        if args.owner != REG_CERT_OWNER_ID:
            parser.error(f"The registration test must be run without the -owner flag (defaults to {REG_CERT_OWNER_ID}).")
    elif args.owner == REG_CERT_OWNER_ID:
        parser.error("When running any test other than registration, the gateway must be registered to an owner which should be provided using the '-owner' flag.")


    gwc = GWCertificate(gw_id=args.gw, owner_id=args.owner, topic_suffix=topic_suffix, tests=tests, update_fw=args.update,
                        stress_pps=args.pps, aggregation_time=args.agg, env=args.env, actions=actions)
    debug_print(f"All arguments: {vars(args)}")
    gwc.run_tests()
    gwc.create_results_html()

def main_cli():
    main()

if __name__ == '__main__':
    main()
    