from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
from brg_certificate.wlt_types import *
import brg_certificate.cert_config as cert_config
import brg_certificate.cert_mqtt as cert_mqtt
import datetime
# from ut_te import ut_rtsa
import pandas as pd
import os
import plotly.express as px
import math, random

DEFAULT_HDR = ag.Hdr(group_id=ag.GROUP_ID_GW2BRG)

# Returns a 12 chars long hex string
int2mac_get = lambda int_val: f"{int_val:012X}"

def name_to_val(name):
    return globals()[name]

def test_prolog(test):
    """
    kicks off the test:
    - sets test start time
    - checks to see if brg is DB for DB-only tests
    - setups spectrum analyzer configuration if needed

    :param WltTest test: test to be started
    :return test: returns the test
    """
    test.start_time = datetime.datetime.now()

    test_run_print(test)

    test.mqttc.flush_pkts()

    #TODO - remove/check status later on in the test
    test.set_phase_rc(PRE_CONFIG, rc=test.rc) 
    test.add_phase_reason(PRE_CONFIG, reason=test.reason)
    #

    return test

def test_epilog(test, revert_brgs=False, revert_gws=False, modules=[], brg1_modules=[], ble5=False):
    """
    closes off the test:
    - sets test end time and duration
    - reverts gw/brgs/both to defaults
    - prints test results

    :param WltTest test: test to be finished
    :param bool revert_brgs: reverts brgs to defaults (default ep and config), defaults to False
    :param bool revert_gws: reverts gws to defaults (default config), defaults to False
    :return test: returns the test
    """
    # TODO - REMOVE when rc is re-designed
    if test.get_phase_by_name(TEST_BODY):
        test.set_phase_rc(TEST_BODY, test.rc)
        test.add_phase_reason(TEST_BODY, test.reason)

    test.reset_result()
    test.set_phase_rc(RESTORE_CONFIG, TEST_PASSED)

    if revert_brgs:
        res2 = DONE
        test, res = cert_config.config_brg_defaults(test, modules=modules, ble5=ble5)
        # TODO - REMOVE when rc is re-designed
        test.set_phase_rc(RESTORE_CONFIG, test.rc)
        test.reset_result()
        #
        if test.brg1 and test.multi_brg:
            brg1_modules = modules if not brg1_modules else brg1_modules
            test, res2 = cert_config.config_brg1_defaults(test, modules=brg1_modules)
            # TODO - REMOVE when rc is re-designed
            test.set_phase_rc(RESTORE_CONFIG, test.rc)
            test.reset_result()
            #
        if res == NO_RESPONSE or res2 == NO_RESPONSE:
            txt = "Failed: Revert BRGs to defaults"
            utPrint(txt, "RED")
            test.add_phase_reason(RESTORE_CONFIG, txt)

    if revert_gws:
        test, res = cert_config.config_gw_defaults(test)
        # TODO - REMOVE when rc is re-designed
        test.set_phase_rc(RESTORE_CONFIG, test.rc)
        test.reset_result()
        #
        if res == NO_RESPONSE:
            txt = "Failed: Revert GW to defaults"
            utPrint(txt, "RED")
            test.add_phase_reason(RESTORE_CONFIG, txt)

    test.mqttc.flush_pkts()
    test.end_time = datetime.datetime.now()
    test.duration = str(test.end_time - test.start_time).split(".")[0]

    # patch for nightly pipeline - as long as brg ver is updated, continue
    if ("ota_test" in test.module_name and not "brg2brg" in test.module_name and
        (BRG_VER_SUCCESS in test.get_phase_reason(TEST_BODY) or WANTED_VER_SAME in test.get_phase_reason(TEST_BODY))
        and test.get_phase_rc(TEST_BODY) == TEST_FAILED):
        print("Setting rc to TEST_PASSED for pipeline after BRG OTA succeeded")
        test.set_phase_rc(TEST_BODY, TEST_PASSED)
        test.set_phase_rc(RESTORE_CONFIG, TEST_PASSED)

    test_epilog_print(test)
    return test

def get_gw_versions(test):
    """
    returns gw ble and wifi versions

    :param WltTest test: test (with gw) to be checked
    :return dict[str, str]: dictionary with BLE_VERSION and WIFI_VERSION
    """
    test.mqttc.flush_pkts()
    cert_config.gw_info_action(test)
    found = False
    gw_ble_version, gw_wifi_version = "", ""
    start_time = datetime.datetime.now()
    while not found:
        for p in test.mqttc._userdata[PKTS].status:
            if GW_INFO in p.body:
                print("Config pkts:")
                print_pkt(p.body)
                if test.protobuf:
                    gw_ble_version = p.body[GW_INFO][ENTRIES][BLE_VERSION][STR_VAL]
                    gw_wifi_version = p.body[GW_INFO][ENTRIES][WIFI_VERSION][STR_VAL]
                else:
                    gw_ble_version = p.body[GW_INFO][BLE_VERSION]
                    gw_wifi_version = p.body[GW_INFO][WIFI_VERSION]
                print(f"current versions: wifi {gw_wifi_version} ble {gw_ble_version}")
                found = True
        print_update_wait()
        if (datetime.datetime.now() - start_time).seconds > DEFAULT_GW_FIELD_UPDATE_TIMEOUT:
            test.rc = TEST_FAILED
            test.add_reason(f"{GW_INFO} not found after {DEFAULT_BRG_FIELD_UPDATE_TIMEOUT} seconds!")
            break
    return {BLE_VERSION:gw_ble_version, WIFI_VERSION:gw_wifi_version}

def get_gw_geolocation(test):
    """
    returns gw latitude and longitude from a gw_info action

    :param WltTest test: test (with gw) to be checked
    :return dict[str, float]: dictionary with GW_LATITUDE and GW_LONGITUDE
    """
    test.mqttc.flush_pkts()
    cert_config.gw_info_action(test)
    found = False
    gw_lat, gw_lng = 0.0, 0.0
    start_time = datetime.datetime.now()
    while not found:
        for p in test.mqttc._userdata[PKTS].status:
            if GW_INFO in p.body:
                print_pkt(p.body)
                gw_lat = p.body[GW_INFO][GW_LATITUDE]
                gw_lng = p.body[GW_INFO][GW_LONGITUDE]
                print(f"gw_lat:{gw_lat} \ngw_lng:{gw_lng}")
                found = True
        print_update_wait()
        if (datetime.datetime.now() - start_time).seconds > DEFAULT_GW_FIELD_UPDATE_TIMEOUT:
            test.rc = TEST_FAILED
            test.add_reason(f"{GW_INFO} not found after {DEFAULT_BRG_FIELD_UPDATE_TIMEOUT} seconds!")
            break
    return test, {GW_LATITUDE:gw_lat, GW_LONGITUDE:gw_lng}

def get_gw_info(test):
    """
    gets gw info json dict from a gw_info action

    :param WltTest test: test with gw that it's info will be retreived
    :return str/dict[str, str]: json info dict from an info pkt OR a NO_RESPONSE str
    """
    test.mqttc.flush_pkts()
    # Always send gw info in both JSON and protobuf
    cert_config.gw_info_action(test)
    test.protobuf = not test.protobuf
    cert_config.gw_info_action(test)
    test.protobuf = not test.protobuf

    start_time = datetime.datetime.now()
    while (datetime.datetime.now() - start_time).seconds < DEFAULT_GW_FIELD_UPDATE_TIMEOUT:
        for p in test.mqttc._userdata[PKTS].status:
            if GW_INFO in p.body:
                print_pkt(p.body)
                return p.body
        print_update_wait()
    return NO_RESPONSE

def get_logs(test):
    """
    gets logs info json dict from a gw_logs action

    :param WltTest test: test with gw that it's info will be retreived
    :return str/dict[str, str]: json info dict from an info pkt OR a NO_RESPONSE str
    """
    test.mqttc.flush_pkts()
    cert_config.gw_logs_action(test)
    start_time = datetime.datetime.now()
    while (datetime.datetime.now() - start_time).seconds < DEFAULT_GW_FIELD_UPDATE_TIMEOUT:
        for p in test.mqttc._userdata[PKTS].status:
            if GET_LOGS:
                print_pkt(p.body)
                return p.body
        print_update_wait()
    return NO_RESPONSE

def get_brg_cfg_pkts(test, last=False, cfg_info=False):
    """
    gets brg cfg data pkts (payload)

    :param WltTest test: test to be scanned (it's first brg is the default brg to be scanned for)
    :param bool last: set to True to get only the last pkt caught, defaults to False
    :param bool cfg_info: set to True to get cfg info sent by the brg (msg_type=1 instead of 5 which is the default for this function), defaults to False
    :param int brg_mac: specific brg_mac in case we want to get cfg pkts for a specific brg different than the default, defaults to 0
    :param bool module: Indicates we look for a module pkt as ack for config change
    :return str/list[str]: cfg pkts payloads list/last cfg pkt payload received
    """
    pkts = []
    msg_type = ag.BRG_MGMT_MSG_TYPE_CFG_SET
    if cfg_info:
        msg_type = ag.BRG_MGMT_MSG_TYPE_CFG_INFO

    for p in cert_mqtt.get_brg2gw_mgmt_pkts(test.mqttc, test):
        brg2gw_cfg = p[MGMT_PKT].pkt
        if type(brg2gw_cfg).__name__ in [module.__name__ for module in test.active_brg.modules]:
            if brg2gw_cfg.msg_type == msg_type:
                pkts += [p[PAYLOAD]]
    if pkts and last:
        return pkts[-1]
    return pkts

def get_brg_hb_pkts(test, last=False, brg_id_str=""):
    """
     gets brg hb data pkts (payload)

    :param WltTest test: test to be scanned (it's first brg is the default brg to be scanned for)
    :param bool last:set to True to get only the last pkt caught, defaults to False
    :param str brg_id: specific brg_id in case we want to get hb pkts for a specific brg different than the default, defaults to ""
    :return str/list[str]: hb pkts payloads list/last hb pkt payload received
    """
    pkts = []
    if brg_id_str == "" and test.active_brg:
        brg_id_str = test.active_brg.id_str
    for p in cert_mqtt.get_brg2gw_mgmt_pkts(test.mqttc, test, brg_id_str):
        brg2gw_hb = p[MGMT_PKT].pkt
        if brg_id_str and type(brg2gw_hb) == eval_pkt(f'Brg2GwHbV{test.active_brg.api_version}'):
            pkts += [p[PAYLOAD]]
        elif not brg_id_str and type(brg2gw_hb) == eval_pkt(f'Brg2GwHbV{test.active_brg.api_version}'):
            pkts += [p[PAYLOAD]]
    if pkts and last:
        return pkts[len(pkts)-1]
    return pkts

time_in_sec = lambda t : t.seconds + t.microseconds / 1000000

# Pandas DataFrame documentation: https://pandas.pydata.org/docs/reference/frame.html

def get_all_brg_pkts(test):
    utPrint(f"Collecting all BRG pkts", "BLUE")
    return cert_mqtt.get_unified_data_pkts(test, only_active_brg=True)

def get_all_brgs_pkts(test):
    utPrint(f"Collecting all BRG pkts", "BLUE")
    return cert_mqtt.get_unified_data_pkts(test, only_active_brg=False)

def get_pkts_data_frame(test, gw_data=False, brg_data=False, per_pkt_type=False):
    pkts = []
    tags_last_pkt_cntr = {}
    tags_received_per_src =  {}
    tbc = None
    gw_pkts = 0
    brg_pkts = 0
    all_data = {TIMESTAMP:[],TAG_ID:[],SRC_ID:[],NFPKT:[],TBC:[],PACKET_CNTR:[],PKT_CNTR_DIFF:[],CER:[],RSSI:[],BRG_LATENCY:[],PAYLOAD:[],SEQUENCE_ID:[],GW_ID:[], PACKET_TYPE:[]}
    if gw_data:
        pkts += cert_mqtt.get_internal_brg_unified_data_pkts(test)
    if brg_data:
        if test.brg1 and test.multi_brg:
            pkts += get_all_brg_pkts(test)
            test.active_brg = test.brg1
            pkts += get_all_brg_pkts(test)
            test.active_brg = test.brg0
        else:
            pkts += get_all_brg_pkts(test)
    for p in pkts:
        # Protection from pkts of type "test_mode" from old tags
        if type(p[DECODED_DATA][PACKET_TYPE]) == str or p[DECODED_DATA][PACKET_TYPE] == None:
            print(f"Skipped packet {p}")
            continue
        if per_pkt_type:
            tag_id = p[DECODED_DATA][TAG_ID] + "_" + str(p[DECODED_DATA][PACKET_TYPE])
        else:
            tag_id = p[DECODED_DATA][TAG_ID]

        if UNIFIED_PKT in p:
            src_id = p[ALIAS_BRIDGE_ID]
            nfpkt = p[UNIFIED_PKT].pkt.nfpkt
            rssi = p[UNIFIED_PKT].pkt.rssi
            brg_latency = p[UNIFIED_PKT].pkt.brg_latency
            if isinstance(p[UNIFIED_PKT].pkt, ag.UnifiedEchoPktV1) or isinstance(p[UNIFIED_PKT].pkt, ag.UnifiedEchoExtPkt):
                tbc = p[UNIFIED_PKT].pkt.tbc

        all_data[TIMESTAMP] += [p[TIMESTAMP]]
        all_data[TAG_ID] += [tag_id]
        all_data[GW_ID] +=  [p[GW_ID]]
        all_data[SRC_ID] += [src_id]
        all_data[NFPKT] += [nfpkt]
        all_data[TBC] += [tbc]
        all_data[PACKET_CNTR] += [p[DECODED_DATA][PACKET_CNTR]]
        all_data[RSSI] += [rssi]
        all_data[BRG_LATENCY] += [brg_latency]
        all_data[PAYLOAD] += [p[PAYLOAD]]
        all_data[SEQUENCE_ID] += [p[SEQUENCE_ID]]
        all_data[PACKET_TYPE] += [p[DECODED_DATA][PACKET_TYPE]]

        # handling pkt_cntr_diff
        pkt_cntr_diff = (p[DECODED_DATA][PACKET_CNTR] - tags_last_pkt_cntr[tag_id])%255 if tag_id and tag_id in tags_received_per_src and src_id and src_id in tags_received_per_src[tag_id] else None
        all_data[PKT_CNTR_DIFF] += [pkt_cntr_diff]
        cer = 1-(nfpkt/pkt_cntr_diff) if pkt_cntr_diff else None
        all_data[CER] += [cer]

        # saving last pkt_cntr per tag
        tags_last_pkt_cntr[tag_id] = p[DECODED_DATA][PACKET_CNTR]

        # saving all srcs a tag was received from
        if tag_id and src_id:
            if tag_id not in tags_received_per_src:
                tags_received_per_src[tag_id] = [src_id]
            elif not src_id in tags_received_per_src[tag_id]:
                tags_received_per_src[tag_id] += [src_id]

            if gw_data:
                if src_id == test.internal_id_alias():
                    gw_pkts += 1
            if brg_data:
                if src_id != test.internal_id_alias():
                    brg_pkts += 1

    if gw_data:
        print(f"Found {gw_pkts} gw_tags_pkts")
    if brg_data:
        print(f"Found {brg_pkts} brg_tags_pkts")

    df = pd.DataFrame.from_dict(all_data)
    df = df.sort_values(by=TIMESTAMP)
    return df

def data_scan(test, gw_data=False, brg_data=False, scan_time=0, per_pkt_type=False, pkt_filter_cfg=0, flush_pkts=True, first_pkt_is_start_time=False):
    # MQTT scan
    if flush_pkts:
        test.mqttc.flush_pkts()
    start_time = datetime.datetime.now()
    if scan_time:
        mqtt_scan_start(test, scan_time)
        chars = ["|", "/", "-", "\\"]
        start_time = datetime.datetime.now()
        i = 0
        while not test.rc:
            cur_duration = (datetime.datetime.now() - start_time).seconds
            if cur_duration >= scan_time:
                break
            if pipeline_running():
                sys.stdout.write(".")
            else:
                sys.stdout.write("\r"+chars[i%4]*20+" "+str(cur_duration)+" "+chars[i%4]*20+" {} pkts captured".format(len(test.mqttc._userdata[PKTS].data)))
            sys.stdout.flush()
            time.sleep(0.25)
            i += 1
        print("\n")

    if per_pkt_type:
        cert_mqtt.dump_pkts(test, log=str(pkt_filter_cfg))
        if pkt_filter_cfg == ag.PKT_FILTER_RANDOM_FIRST_ARRIVING_PKT:
            # When PKT_FILTER_RANDOM_FIRST_ARRIVING_PKT we don't want to split the tags to be per pkt_type
            per_pkt_type = False
    df = get_pkts_data_frame(test, gw_data=gw_data, brg_data=brg_data, per_pkt_type=per_pkt_type)
    if not df.empty:
        df['gw_id'] = test.internal_id_alias()
        if first_pkt_is_start_time:
            start_time = min(df[TIMESTAMP])
            df[TIMESTAMP_DELTA] = (df[TIMESTAMP]- start_time) / 1000
        else:
            df[TIMESTAMP_DELTA] = (df[TIMESTAMP] / 1000) - start_time.timestamp()
    return df

def pacing_analysis(test, pacer_interval, df, pkt_filter_cfg=ag.PKT_FILTER_RANDOM_FIRST_ARRIVING_PKT, num_of_pixels=0, is_ble5_test=False):
    ROUND = 3

    # Validate pkts amount
    if df[TAG_ID].nunique() == 0:
        if pkt_filter_cfg == ag.PKT_FILTER_DISABLE_FORWARDING:
            print("Packets echo disabled and no packets were found accordingly")
        else:
            test.rc = TEST_FAILED
            test.add_reason("No packets found!\nMake sure you have an energizing BRG around you.")
            print(test.reason)
        return test
    elif pkt_filter_cfg == ag.PKT_FILTER_DISABLE_FORWARDING:
        test.rc = TEST_FAILED
        test.add_reason("Packets were found while packets echo is turned off!")
        print(test.reason)
        return test

    # Verify received pkt types are correct when cfg is not PKT_FILTER_RANDOM_FIRST_ARRIVING_PKT
    if pkt_filter_cfg != ag.PKT_FILTER_RANDOM_FIRST_ARRIVING_PKT:
        for pkt_type in list(df[PACKET_TYPE].unique()):
            if ((pkt_filter_cfg & (1 << pkt_type)) == 0
                and not (is_ble5_test and test.internal_brg and pkt_type == ag.PKT_TYPE_BLE5_EXTENDED_TEMP_ADVANCED)):
                test.rc = TEST_FAILED
                test.add_reason(f"Tag is of packet type {pkt_type} which is turned off in packet_types_mask configuration!")
                return test

    # Verify the tags count according to simulation data and pkt_filter_cfg
    tags_count = len(list(df[TAG_ID].unique()))
    if test.data == DATA_SIMULATION and num_of_pixels:
        if pkt_filter_cfg == ag.PKT_FILTER_TEMP_AND_ADVANCED_PKTS or pkt_filter_cfg == ag.PKT_FILTER_TEMP_AND_DEBUG_PKTS:
            expected_tags_count = num_of_pixels * 2
        elif pkt_filter_cfg == ag.PKT_FILTER_TEMP_ADVANCED_AND_DEBUG_PKTS:
            expected_tags_count = num_of_pixels * 3
        else:
            expected_tags_count = num_of_pixels
        if tags_count != expected_tags_count:
            test.rc = TEST_FAILED
            test.add_reason(f"Expected {expected_tags_count} pixels but found {tags_count}!")
            print(test.reason)
            return test

    # Verify the tags pacer interval
    failed_tags = 0
    for tag in list(df[TAG_ID].unique()):
        pkts = df.query('tag_id == @tag')
        avg_pacer = round(pkts.timestamp.diff().mean(skipna=True)/1000, ROUND)
        print(f"Tag: {tag} avg_pacer={avg_pacer} num_of_pkts={len(pkts)}")
        if ((avg_pacer / pacer_interval) < PACER_INTERVAL_THRESHOLD_HIGH and (pacer_interval - avg_pacer) > 1):
            failed_tags += 1
            test.rc = TEST_FAILED
            print(f"Tag {tag} with diff_time {list(pkts.timestamp.diff().div(1000))}, avg_pacer={avg_pacer} exceeds {PACER_INTERVAL_THRESHOLD_HIGH} minimum threshold!")
        if test.data == DATA_SIMULATION and (avg_pacer / pacer_interval) > PACER_INTERVAL_CEIL_THRESHOLD:
            failed_tags += 1
            print(f"Tag {tag} with diff_time {list(pkts.timestamp.diff().div(1000))}, avg_pacer={avg_pacer} exceeds {PACER_INTERVAL_CEIL_THRESHOLD} maximum threshold!")
            if failed_tags > 1: # Fail the test on ceil threshold only when more than one tag failed
                test.rc = TEST_FAILED

    # PASS test if only 1 tag out of many failed - this could be an issue with the tag
    if tags_count >= PACER_INTERVAL_MIN_TAGS_COUNT and failed_tags <= PACER_INTERVAL_MAX_FAILED_TAGS:
        test.rc = TEST_PASSED
    # Addition to understand how many tags failed in total
    if test.rc == TEST_FAILED:
        test.add_reason(f"{failed_tags}/{tags_count} tags with wrong time diff")
        print(test.reason)
        return test
    return test

def reboot_config_analysis(test, expected_hash, timeout=ACTION_LONG_TIMEOUT, ble_version=None, bl_version=None):
    utPrint("Analyzing Reboot", "BLUE")
    # start with a 5 sec wait time before searching interface to allow the BRG to reboot
    time.sleep(5)

    start_time = datetime.datetime.now()
    seq_ids = []
    found = {ag.MODULE_IF : False, ag.MODULE_DATAPATH: False}
    received_hash = 0
    # Flush data pkts only to keep the GW logs which are in status topic
    test.mqttc.flush_data_pkts()

    while not all(found.values()):
        # scan for ModuleIf and ModuleDatapath pkts of all api versions to support api version change on update
        # ModuleDatapath arrival shows that the BLE really rebooted
        if_pkts_list = [eval_pkt(f'ModuleIfV{i}') for i in range(ag.API_VERSION_V9, ag.API_VERSION_LATEST+1)]
        datapath_pkts_list = [eval_pkt(f'ModuleDatapathV{i}') for i in range(ag.API_VERSION_V9, ag.API_VERSION_LATEST+1)]
        pkts = cert_mqtt.get_brg2gw_mgmt_pkts(test.mqttc, test, mgmt_types=if_pkts_list+datapath_pkts_list)
        for p in pkts:
            if (not seq_ids or p[SEQUENCE_ID] not in seq_ids):
                seq_ids.append(p[SEQUENCE_ID])
                module_pkt = p[MGMT_PKT].pkt
                if not found[module_pkt.module_type]:
                    print("\nGot {} packet after {} sec!".format(type(module_pkt).__name__, (datetime.datetime.now() - start_time).seconds))
                    print(module_pkt)
                    if module_pkt.module_type == ag.MODULE_IF:
                        test.active_brg.api_version = module_pkt.api_version
                        print(f"received ModuleIfV{test.active_brg.api_version} pkt:")
                        # get received cfg_hash & expected cfg_hash
                        received_hash = module_pkt.cfg_hash
                        print(f"\nexpected cfg_hash: {hex(expected_hash)}")
                        print(f"received cfg_hash: {hex(received_hash)}")
                        # brg version update (OTA) analysis
                        if ble_version:
                            brg_version = f"{module_pkt.major_ver}.{module_pkt.minor_ver}.{module_pkt.patch_ver}"
                            print(f"\nBRG version: {brg_version}, expected version: {ble_version}")
                            # compare wanted version to received version
                            if brg_version == ble_version:
                                test.add_reason(BRG_VER_SUCCESS)
                                # ALSO compare received cfg_hash to expected cfg_hash
                                # expected_hash will be 1 if api_version was updated
                                if received_hash == expected_hash or expected_hash == 1:
                                    found[module_pkt.module_type] = True
                        elif bl_version:
                            brg_bl_version = module_pkt.bl_version
                            print(f"\nBRG bootloader version: {brg_bl_version}, expected bootloader version: {bl_version}")
                            # compare wanted version to received version
                            if brg_bl_version == bl_version:
                                test.add_reason(BRG_BL_VER_SUCCESS)
                                found[module_pkt.module_type] = True
                        # analysis of any other reboot actions with no version update (relevant only for api version 8 or higher)
                        # compare received cfg_hash to expected cfg_hash
                        elif received_hash == expected_hash:
                            found[module_pkt.module_type] = True
                    else:
                        found[module_pkt.module_type] = True
        print_update_wait()

        if (datetime.datetime.now() - start_time).seconds > timeout:
            test.rc = TEST_FAILED
            unfound = [f'{ag.MODULES_DICT[m]}{test.active_brg.api_version}' for m in found if not found[m]]
            test.add_reason(f"{unfound} not received in {timeout} sec")
            break
    return test

def scan_for_mgmt_pkts(test, mgmt_type):

    start_time = datetime.datetime.now()
    # Search for module packets
    found = False
    ret_pkts = []
    while DEFAULT_BRG_FIELD_UPDATE_TIMEOUT > (datetime.datetime.now() - start_time).seconds:
        print_update_wait()
        pkts_collected = cert_mqtt.get_brg2gw_mgmt_pkts(test.mqttc, test, mgmt_types=mgmt_type)
        if pkts_collected:
            utPrint("Found brg2gw_mgmt_pkts:", "GREEN")
            seq_ids = []
            for p in pkts_collected:
                if seq_ids == [] or p[SEQUENCE_ID] not in seq_ids:
                    seq_ids.append(p[SEQUENCE_ID])
                    print(p[MGMT_PKT].pkt)
                    ret_pkts.append(p)
            found = True
            break
    if not found:
        test.rc = TEST_FAILED
        test.add_reason(f"Didn't receive {mgmt_type[0].__name__} pkt after {DEFAULT_BRG_FIELD_UPDATE_TIMEOUT} seconds!")
    return test, ret_pkts

# Plotly graphing libraries documentation: https://plotly.com/python/

def display_data(df, csv=True, nfpkt=False, pkt_cntr_diff=False, cer_per_tag=False, tbc=False, rssi=False, ttfp=False, start_time=None, name_prefix="", dir=""):
    print("\nGenerating data analysis graphs and CSV file\n")
    df[DATETIME] = df[TIMESTAMP].apply(lambda x: datetime.datetime.fromtimestamp(x/1e3))
    df = df.sort_values(by=DATETIME)
    symbol_sequence = ["hourglass", "bowtie", "cross", "x"]
    all_graphs = []
    ttfp_graph = None
    # insert new start_time to override timestamp_delta from data_scan()
    if start_time:
        df[TIMESTAMP_DELTA] = (df[TIMESTAMP] / 1000) - start_time.timestamp()
    if nfpkt:
        nfpkt_graph = px.scatter(df, title=NFPKT, x=DATETIME,  y=NFPKT, color=TAG_ID, symbol=SRC_ID, symbol_sequence=symbol_sequence)
        nfpkt_graph.update_traces(marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')), selector=dict(mode='markers'))
        all_graphs.append(nfpkt_graph)
    if rssi:
        rssi_graph = px.scatter(df, title=RSSI, x=DATETIME, y=RSSI, color=TAG_ID, symbol=SRC_ID, symbol_sequence=symbol_sequence)
        rssi_graph.update_traces(marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')), selector=dict(mode='markers'))
        all_graphs.append(rssi_graph)
    if pkt_cntr_diff:
        pkt_cntr_diff_graph = px.scatter(df, title=PKT_CNTR_DIFF, x=DATETIME, y=PKT_CNTR_DIFF, color=TAG_ID, symbol=SRC_ID, symbol_sequence=symbol_sequence)
        pkt_cntr_diff_graph.update_traces(marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')), selector=dict(mode='markers'))
        all_graphs.append(pkt_cntr_diff_graph)
    if cer_per_tag:
        cer_per_tag_graph = px.scatter(df, title=CER, x=DATETIME, y=CER, color=TAG_ID, symbol=SRC_ID, symbol_sequence=symbol_sequence)
        cer_per_tag_graph.update_traces(marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')), selector=dict(mode='markers'))
        all_graphs.append(cer_per_tag_graph)
    if tbc:
        tbc_graph = px.scatter(df, title=TBC, x=DATETIME, y=TBC, color=TAG_ID, symbol=SRC_ID, symbol_sequence=symbol_sequence)
        tbc_graph.update_traces(marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')), selector=dict(mode='markers'))
        all_graphs.append(tbc_graph)
    if ttfp:
        data = {TIMESTAMP_DELTA:[], TAGS_COUNT:[], NEW_TAGS:[]}
        tags_count = []
        # iterate all integers from 0 to the largest timestamp_delta as values for X
        for i in range(int(math.ceil(df[TIMESTAMP_DELTA].iloc[-1]))+1):
            new_tags = []
            # for every timestamp_delta value (i) add all NEW tags received in that timestamp_delta
            for row in df.query('timestamp_delta < @i').itertuples(index=False):
                if not row.tag_id in tags_count and not row.tag_id in new_tags:
                    new_tags += [row.tag_id]
            tags_count += new_tags
            data[TIMESTAMP_DELTA] += ([i])
            data[TAGS_COUNT] += [len(tags_count)]
            data[NEW_TAGS] += [new_tags]
        ttfp_graph = px.line(pd.DataFrame(data), x=TIMESTAMP_DELTA, y=TAGS_COUNT, title=TTFP,hover_data=[TIMESTAMP_DELTA,TAGS_COUNT,NEW_TAGS], markers=True)
        all_graphs.append(ttfp_graph)
    #generate
    with open(os.path.join(BASE_DIR, dir, f"{name_prefix}data_graphs.html"), 'w') as f:
        for g in all_graphs:
            f.write(g.to_html(full_html=False, include_plotlyjs='cdn', include_mathjax='cdn'))
            f.write("<br>")
    if csv:
        df.to_csv(os.path.join(BASE_DIR, dir, f"{name_prefix}all_data.csv"), index=False)

    return ttfp_graph

def single_log_search(test, s, found, fail_on_find=False, print_logs=True, additional_log=""):
    res = False
    for p in test.mqttc._userdata[PKTS].status:
        if GW_LOGS in p.body:
            if test.protobuf and p.body[GW_LOGS]:
                # handle protobuf structure (when GW_LOGS is not empty)
                logs = p.body[GW_LOGS][LOGS]
            else:
                logs = p.body[GW_LOGS]
            for log in logs:
                if any([s in log]) and any([additional_log in log]) and (log not in found):
                    print(f"Log: {log}, Additional Log: {additional_log}")
                    found += [log]
                    res = True
                    if fail_on_find:
                        if test.rc == TEST_PASSED:
                            test= test.add_reason("Test functionality passed")
                        test.add_reason(f"Found {s}")
                        test.rc = TEST_FAILED
                        print(found)
                        return test, res, found
                    if print_logs:
                        print_pkt(s)
    return test, res, found

def gw_logs_search(test, strings, scan_time=GW_LOG_PERIOD+5, print_logs=False, fail_on_find=False):
    """searching for specific logs in mqtt status topic in GW_LOGS field

    :param WltTest test: test running
    :param [str] strings: list of logs to search
    :param int scan_time: time to scan for logs, defaults to GW_LOG_PERIOD+5
    :return WltTest: test with updated results
    """
    start_time = datetime.datetime.now()
    print(f"Searching for {strings} log in MQTT status topic.\nFail on find is set to {fail_on_find}")
    found = []
    while (len(strings) > len(found)):
        for s in strings:
            test, res, found = single_log_search(test, s, found, fail_on_find, print_logs)
            if res:
                break
        if (datetime.datetime.now() - start_time).seconds >= scan_time:
            if not fail_on_find:
                test.add_reason(f"Didnt find logs in [{scan_time}] seconds")
                print(test.reason)
                test.rc = TEST_FAILED
            break
    if test.rc == TEST_PASSED:
        if not fail_on_find:
            print(f"SUCCESS found all [{strings}]")
        else:
            print(f"SUCCESS Didnt find [{strings}]")
    return test

def gw_action_status_search(test, action_idx, status_code):
    """searching for action returned status code in mqtt status topic in ACTION field

    :param WltTest test: test running
    :param int action_idx: sent action index
    :param int status_code: expected status code for action
    :return WltTest: test with updated results
    """
    start_time = datetime.datetime.now()
    print(f"Searching for action idx ({action_idx}) update log in MQTT status topic")
    while (datetime.datetime.now() - start_time).seconds < GW_LOG_PERIOD:
        for p in test.mqttc._userdata[PKTS].status:
            # JSON
            if ((ACTION in p.body) and (p.body[ACTION] == action_idx) and
                (STATUS_CODE_STR in p.body) and (p.body[STATUS_CODE_STR] == status_code)):
                return test
            # Protobuf - when succeed status is not sent
            if ((ACTION_STATUS in p.body) and (p.body[ACTION_STATUS][ACTION] == action_idx) and
                (STATUS_CODE not in p.body[ACTION_STATUS])):
                return test
    test.add_reason(f"action_idx={action_idx} status_code={status_code} not found in logs after {GW_LOG_PERIOD} seconds\n")
    print(test.reason)
    test.rc = TEST_FAILED
    return test

def get_gw_logs_packets(test, last=False, print_log=True):
    """
    gets gw logs pkts
    :param WltTest test: test with gw that it's info will be retreived
    :param bool last: set to True to get only the last pkt caught, defaults to False
    :return pkt/list[pkt]: logs pkts list/last status pkt received
    """
    cert_config.gw_logs_action(test)
    pkts = []
    for p in test.mqttc._userdata[PKTS].status:
        if GW_LOGS in p.body:
            if print_log:
                print("GW logs packet:\n", p.body[GW_LOGS])
            logs = p.body[GW_LOGS][LOGS] if test.protobuf else p.body[GW_LOGS]
            pkts += [log for log in logs]
    if pkts and last:
        return pkts[len(pkts)-1]
    return pkts

def wait_time_n_print(secs):
    utPrint(f"Waiting for {secs} seconds", "CYAN")
    while secs:
        print_update_wait()
        secs -= 1

def get_module_if_pkt(test):
    cert_config.send_brg_action(test, ag.ACTION_GET_MODULE, interface=1)
    test, pkts = scan_for_mgmt_pkts(test, mgmt_type=[eval_pkt(f'ModuleIfV{test.active_brg.api_version}'),
                                                     eval_pkt(f'ModuleIfV{test.active_brg.api_version - 1}'),])
    if test.rc == TEST_FAILED:
        return test, NO_RESPONSE
    else:
        print(pkts[-1][MGMT_PKT].pkt)
        return test, pkts[-1][MGMT_PKT].pkt

def get_cfg_hash(test):
    utPrint(f"Fetching BRG cfg hash for BRG {test.active_brg.id_str}", "BLUE")
    test, module_if_pkt = get_module_if_pkt(test)
    if test.rc == TEST_FAILED:
        return test, 0
    else:
        return test, module_if_pkt.cfg_hash

def module_ack_search(test, test_pkt, mgmt_type, wait=True):
    """
    module ack search
    wait=False is for pwr mgmt off - in order to send the "off" pkt repeatidly while searching for the ack
    """
    if wait:
        test, mgmt_pkts = scan_for_mgmt_pkts(test, [mgmt_type])
    else:
        mgmt_pkts = cert_mqtt.get_brg2gw_mgmt_pkts(test.mqttc, test, mgmt_types=[mgmt_type])
    if not test.rc:
        for p in mgmt_pkts:
            pkt = p[MGMT_PKT].pkt
            if (pkt == test_pkt.pkt):
                return test, True
        if wait:
            test.rc = TEST_FAILED
            test.add_reason(f"{mgmt_type} module does not match pkt received")
            print(test.reason)
    return test, False

def brg_restore_defaults_check(test):
    print("Starting Restore Defaults Check")
    start_time = datetime.datetime.now()
    found = False
    revived = False
    output = ""
    while not found:
        last_pkt = get_brg_cfg_pkts(test=test, cfg_info=True, last=True)
        if last_pkt:
            print(f"Got pkt after {(datetime.datetime.now() - start_time).seconds} sec!")
            wlt_pkt = WltPkt(last_pkt)
            print(f"SUCCESS: Found pkt from brg: {wlt_pkt}")
            found = True # exit
            revived = True
            output = "SUCCESS: brg is alive and restored to defaults!"
        if (datetime.datetime.now() - start_time).seconds > ACTION_LONG_TIMEOUT:
            print(f"FAILURE: Can't find bridge! Didn't get config pkt after {ACTION_LONG_TIMEOUT} seconds!")
            break
        print_update_wait()
    return test, revived, output

def erase_sensors(test):
    module = eval_pkt(f'ModuleExtSensorsV{test.active_brg.api_version}')
    wltpkt = WltPkt(hdr=DEFAULT_HDR, pkt=eval_pkt(f'ModuleExtSensorsV{test.active_brg.api_version}')(brg_mac=test.active_brg.id_int, msg_type=ag.BRG_MGMT_MSG_TYPE_CFG_SET, seq_id=random.randrange(99),
                                                                                   sensor0=0, sensor1=0))
    print("Erasing all sensors from BRG {}".format(test.active_brg.id_int))
    test = cert_config.brg_configure(test=test, cfg_pkt=wltpkt)[0]

    if test.rc == TEST_FAILED:
        test.add_reason("Failed to erase sensors! Didn't receive module ext sensors pkt")
    else:
        utPrint("SUCCESS! Module ext_sensors returned to default!", "GREEN")
    return test

# Pwr Mgmt
def brg_pwr_mgmt_turn_on(test):
    utPrint("Sending pwr_mgmt static mode configuration - 30 seconds ON, 60 seconds SLEEP!", "BLUE")
    module = eval_pkt(f'ModulePwrMgmtV{test.active_brg.api_version}')
    # send pwr mgmt module packet
    wltpkt = WltPkt(hdr=DEFAULT_HDR, pkt=module(module_type=ag.MODULE_PWR_MGMT, msg_type=ag.BRG_MGMT_MSG_TYPE_CFG_SET,
                                                      api_version=ag.API_VERSION_LATEST,seq_id=random.randrange(99),
                                                      brg_mac=test.active_brg.id_int, static_on_duration=30, static_sleep_duration=60,
                                                      dynamic_leds_on=0,dynamic_keep_alive_period=0, dynamic_keep_alive_scan=0,
                                                      dynamic_on_duration=0,dynamic_sleep_duration=0))
    cert_config.gw_downlink(test, raw_tx_data=wltpkt.dump())
    test = module_ack_search(test, test_pkt=wltpkt, mgmt_type=module)[0]

    if test.rc == TEST_FAILED:
        test.add_reason("Turning pwr mgmt ON failed, Didn't receive GW MEL pwr mgmt ON pkt")
    else:
        utPrint("SUCCESS! pwr mgmt static mode turned on!", "GREEN")
    return test, wltpkt

def brg_pwr_mgmt_turn_off(test):
    utPrint("Turning pwr mgmt OFF - sending default configuration!", "BLUE")
    module = eval_pkt(f'ModulePwrMgmtV{test.active_brg.api_version}')
    start_time = datetime.datetime.now()
    wltpkt = WltPkt(hdr=DEFAULT_HDR, pkt=module(module_type=ag.MODULE_PWR_MGMT, msg_type=ag.BRG_MGMT_MSG_TYPE_CFG_SET,
                                                      api_version=ag.API_VERSION_LATEST,seq_id=random.randrange(99),
                                                      brg_mac=test.active_brg.id_int,static_leds_on=1,
                                                      static_keep_alive_period=0,static_keep_alive_scan=0,
                                                      static_on_duration=0,static_sleep_duration=0,
                                                      dynamic_leds_on=0,dynamic_keep_alive_period=0,
                                                      dynamic_keep_alive_scan=0,dynamic_on_duration=0,dynamic_sleep_duration=0))
    found = False
    while not found:
        cert_config.gw_downlink(test, raw_tx_data=wltpkt.dump())
        test, found = module_ack_search(test, wltpkt, module, wait=False)
        if ((datetime.datetime.now() - start_time).seconds > (ag.PWR_MGMT_DEFAULTS_KEEP_ALIVE_PERIOD + 1)):
            test.add_reason(f"Didn't receive GW MEL pwr mgmt OFF ack after {ag.PWR_MGMT_DEFAULTS_KEEP_ALIVE_PERIOD + 1} seconds")
            test.rc = TEST_FAILED
            break
        print_update_wait()
    if found:
        utPrint(f"FOUND off pkt after {(datetime.datetime.now() - start_time)} secs", "GREEN")
        utPrint("SUCCESS! pwr mgmt static mode turned off!", "GREEN")
    return test

# LEDs tests funcs
def check_input_n_try_again(value):
    # check for valid input char - only 'Y', 'y', 'N' or 'n'
    while value.lower() != 'y' and value.lower() != 'n':
        utPrint("Wrong input, Please try Again!\n", "RED")
        value = input()
    return value

# Executed only when the received value is 'n'!
def value_check_if_y(test, received_value, stage):
    # check if the received value is different from the expected value
    if 'y' != received_value.lower():
        test.rc = TEST_FAILED
        test.add_reason(f"{stage} failed")
    return test