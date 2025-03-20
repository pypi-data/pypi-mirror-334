from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
import brg_certificate.cert_common as cert_common
import brg_certificate.cert_config as cert_config
import brg_certificate.cert_utils as cert_utils
import datetime
import tabulate

# Index 0 = stage name Index 1 = value log to find
BRG_OTA_LOGS = {
    "got ota action": "Got OTA action request for BRG",
    "file download finish dat": "Downloaded files to /sd_images/ble_image_dat_file successfully",
    "dat file open": "file opening /sd_images/ble_image_dat_file success",
    "dat file transfer finish": "BRG_OTA_FILE_TRANSFER_FINISH",
    "file download finish bin": "Downloaded files to /sd_images/ble_image_bin_file successfully",
    "bin file open": "file opening /sd_images/ble_image_bin_file success",
    "bin file transfer finish": "BRG_OTA_FILE_TRANSFER_FINISH",
    "start brg ota": "Starting OTA to BRG",
    "finish brg ota": "BRG OTA finished with status",
}


def get_ts_from_log(log):
    ts_end = log.find(']')
    ts_str = log[1:ts_end]
    # Convers from ms to sec
    return int(ts_str) / 1000


# Prints the time each step individually for regression & follow up purposes
def breakdown_steps_timing(test, start_ts):
    # timing data [step, is_found, time from start, stage timing]
    timing_data = []
    last_ts = start_ts

    # Collect data
    for step, log in BRG_OTA_LOGS.items():
        found = []
        suffix = "(dat)" if step.startswith("dat") else "(bin)" if step.startswith("bin") else ""
        test, res, found = cert_common.single_log_search(test, log, found, fail_on_find=False, print_logs=False, additional_log=suffix)
        time_from_start = -100  # invalid
        step_time = -100  # invalid
        if res:
            found_ts = get_ts_from_log(found[0])
            time_from_start = found_ts - start_ts
            step_time = found_ts - last_ts
            last_ts = found_ts
        timing_data.append([step, res, round(time_from_start, 1), round(step_time, 1)])

    # Create table
    headers = ["Step", "Log Found", "Time From Start (secs)", "Step Time (secs)"]
    print(tabulate.tabulate(tabular_data=timing_data, headers=headers, tablefmt="fancy_grid"))


def run(test):

    test = cert_common.test_prolog(test)
    if test.rc == TEST_FAILED:
        return cert_common.test_epilog(test, revert_brgs=True)

    versions_mgmt = cert_utils.load_module('versions_mgmt.py', f'{UTILS_BASE_REL_PATH}/versions_mgmt.py')
    if test.latest:
        _, version = versions_mgmt.get_versions(env='aws', server='test', ci=True)
    elif test.release_candidate:
        _, version = versions_mgmt.get_versions(env='aws', server='test', rc=True)
    else:
        test.rc = TEST_FAILED
        test.reason = NO_PARAMS_GIVEN
        print(NO_PARAMS_GIVEN)

    #  check for problems in prolog
    if test.rc == TEST_FAILED or not version:
        test = cert_common.test_epilog(test)
        return test

    start_time = datetime.datetime.now()
    test = cert_config.brg_ota(test, gw_ble_version=version)
    generate_log_file(test, f"brg_ota_{version}")

    if test.rc == TEST_PASSED and WANTED_VER_SAME not in test.reason:
        breakdown_steps_timing(test, start_time.timestamp())

    return cert_common.test_epilog(test)
