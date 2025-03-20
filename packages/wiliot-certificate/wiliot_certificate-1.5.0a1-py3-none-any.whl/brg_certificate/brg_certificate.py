
# generic
import sys
import os
sys.path.insert(0, os.path.abspath(".."))
import webbrowser
import glob
import datetime
import tabulate
import threading
# Local imports
from brg_certificate.cert_defines import *
from brg_certificate.cert_prints import *
from brg_certificate.wlt_types import *
from brg_certificate.cert_utils import *
import brg_certificate.cert_results as cert_results
import brg_certificate.cert_gw_sim as cert_gw_sim
import brg_certificate.cert_mqtt as cert_mqtt
import brg_certificate.cert_common as cert_common

TEST_LIST_FW_UPDATE_FILE = "ut/fw_update_test_list.txt"
CLEAN_PATTERNS = ['./tests/**/*.html', './tests/**/mqtt_log_*', './tests/**/*.pyc', './tests/**/*.csv']

os.system('')

def filter_tests(tests, run, drun):
    if run:
        tests = [t for t in tests if re.search(run, t.name)]
    if drun:
        tests = [t for t in tests if not re.search(drun, t.name)]
    return tests

def get_important_tests_info():
    patterns = ["DISCONNECTED", "WLT_ERROR", "free heap size", "python_mqtt_disconnect"]
    return "".join([l.strip(' "') for l in open(os.path.join(BASE_DIR, CERT_MQTT_LOG_FILE)).readlines() if any([p in l for p in patterns])])

def skip_test_check(test, args):
    skip_string = ""
    if test.multi_brg and not test.brg1:
        skip_string = f"Skipped {test.module_name} multi brg test because brg1 wasn't given"
    elif args.skip_internal and test.internal_brg:
        skip_string = f"Skipped {test.module_name} for internal brg because skip_internal flag is set"
    elif test.active_brg and not test.active_brg.is_sup_cap(test):
        skip_string = f"Skipped {test.module_name} because {module2name(test.test_module)} module is not supported"
    if skip_string:
        utPrint(f"{SEP}{skip_string}{SEP}", "WARNING")
        test.reason = skip_string
        test.rc = TEST_SKIPPED
    return test

def tests_rtsa_update(tests):
    # Init spectrum analyzer
    rtsa_flag = False
    for t in tests:
        if "rtsa" in t.module_name:
            if not rtsa_flag:
                try:
                    ut_te = load_module('ut_te.py', 'ut/ut_te/ut_te.py')
                except:
                    print("Unable to import UT's test equipment API (ut_te.py), check exceptions for necessary installations!")
                try:
                    myObjTE = ut_te.StationEquipment().GetTEObject()
                    myRTSA = myObjTE['RTSA']
                except:
                    print("No test equipment available!")
                rtsa_flag = True
            t.rtsa = myRTSA

def main(args):
    args.gw = get_gw_id(args.gw)

    utPrint(str(args.__dict__))
    start_time = datetime.datetime.now()

    # Clean
    if os.path.exists(CERT_MQTT_LOG_FILE):
        os.remove(CERT_MQTT_LOG_FILE)
    if os.path.exists(DATA_SIM_LOG_FILE):
        os.remove(DATA_SIM_LOG_FILE)
    if args.clean:
        for clean_pattern in CLEAN_PATTERNS:
            for f in glob.glob(clean_pattern, recursive=True):
                os.remove(f)
        if not args.gw and not args.brg:
            utPrint("Clean only - Done!")
            sys.exit(0)

    # Init mqtt client
    mqttc = cert_mqtt.mqttc_init(args.gw, data=args.data)

    # Run Gateway Simulator in separated thread if exists
    gw_sim_thread = None
    if GW_SIM_PREFIX in args.gw:
        gw_sim_thread = threading.Thread(target=cert_gw_sim.gw_sim_run, daemon = True, kwargs={'port':args.port, 'gw_id': args.gw,
                                                                              'analyze_interference':args.analyze_interference})
        gw_sim_thread.start()
        sleep_time = (len(cert_gw_sim.CHANNELS_TO_ANALYZE) * 30) + 15 if args.analyze_interference else 10
        time.sleep(sleep_time)

    # Collecting the tests
    if args.latest or args.rc:
        test_list = TEST_LIST_FW_UPDATE_FILE
    else:
        test_list = args.tl

    # Prepare GW
    if gw_sim_thread:
        gw, internal_brg, gw_server, gw_version, protobuf = cert_gw_sim.prep_gw(args, mqttc, start_time)
    else:
        gw, internal_brg, gw_server, gw_version, protobuf = ut_prep_gw(args, mqttc, start_time)

    brg0, brg1 = None, None
    if args.brg:
        brg0 = ut_prep_brg(args, mqttc, start_time, gw, args.brg, gw_server, protobuf)
        if args.brg1:
            brg1 = ut_prep_brg(args, mqttc, start_time, gw, args.brg1, gw_server, protobuf)

    # Collecting the tests
    tests = []
    for l in open(os.path.join(BASE_DIR, test_list)).readlines():
        if l.strip() and not l.strip().startswith("#"):
            test = (WltTest(l.strip(), gw, mqttc, exit_on_param_failure=args.exit_on_param_failure, gw_lan=args.lan,
                    gw_orig_versions={BLE_VERSION:gw_version[BLE_VERSION], WIFI_VERSION:gw_version[WIFI_VERSION]},
                    server=gw_server, latest=args.latest, release_candidate=args.rc, private_setup=args.private_setup, internal_brg_obj=internal_brg,
                    gw_sim=gw_sim_thread, data=args.data, port=args.port, protobuf=protobuf))
            test.brg0 = brg0
            test.brg1 = brg1
            if test.internal_brg and test.multi_brg:
                test.brg1 = internal_brg
            elif test.internal_brg and not test.multi_brg:
                test.brg0 = internal_brg
            elif not test.internal_brg and not test.gw_only and not test.brg0:
                continue
            test.active_brg = test.brg0
            tests += [test]
    tests = filter_tests(tests=tests, run=args.run, drun=args.drun)

    # Init spectrum analyzer
    tests_rtsa_update(tests)

    # Running the tests
    utPrint(SEP)
    utPrint("\n - ".join([f"\nRunning {len(tests)} tests:"] + [t.name if not t.internal_brg else f"{t.name} (internal brg)" for t in tests]))

    failures, skipped = 0, 0
    exit_on_test_failure = args.exit_on_test_failure
    i = 0

    for i, test in enumerate(tests):
        test_module_name = load_module(f'{test.module_name}.py', f'{test.dir}/{test.module_name}.py')
        test = skip_test_check(test, args)
        if test.rc == TEST_SKIPPED:
            skipped += 1
        else:
            test = test_module_name.run(test)
            test.update_overall_rc()
        if test.rc == TEST_FAILED:
            failures += 1
            if "versions_test" in test.module_name and f"EXITING CERTIFICATE" in test.reason:
                exit_on_test_failure = True
        print(f"Test Duration: {test.duration}")
        print(tabulate.tabulate([[i+1, i+1-(failures+skipped), skipped, failures, len(tests)]],
                            headers=["FINISHED", "PASSED", "SKIPPED", "FAILED", "TOTAL"], tablefmt="pretty"))
        cert_common.wait_time_n_print(2)
        if exit_on_test_failure and test.rc == TEST_FAILED:
            break

    # Print results
    print(SEP)
    duration = (datetime.datetime.now()-start_time)
    print("Tests duration: {}".format(str(duration).split(".")[0]))
    brg_version = ''
    if test.active_brg:
        brg_version =  test.active_brg.version
        print("Bridge version: {}".format(brg_version))
    print(cert_results.generate_tests_table(tests))
    print(tabulate.tabulate([[i+1, i+1-(failures+skipped), skipped, failures, len(tests)]],
                            headers=["FINISHED", "PASSED", "SKIPPED", "FAILED", "TOTAL"], tablefmt="pretty"))

    print(WIL_CERT_TEXT)
    print_warn(get_important_tests_info())
    print_pass_or_fail(not failures, f"Wiliot Certificate")

    pipeline = cert_common.pipeline_running()
    cert_results.generate_results_files(html=True, pdf=True, failures=failures, skipped=skipped, start_time=start_time, duration=duration, brg_version=brg_version,
                                        brg=args.brg, gw_ble_version = gw_version[BLE_VERSION], gw_ble_mac = internal_brg.id_str, tests=tests, pipeline=pipeline)
    if not pipeline:
        webbrowser.open('file://' + os.path.realpath(os.path.join(BASE_DIR, UT_RESULT_FILE_PDF)))

    if failures:
        sys.exit(-1)

if __name__ == '__main__':
    main()