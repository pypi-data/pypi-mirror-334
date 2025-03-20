from brg_certificate.cert_defines import *
from brg_certificate.cert_prints import *
from brg_certificate.wlt_types import *
import brg_certificate.cert_common as cert_common
import brg_certificate.cert_protobuf as cert_protobuf
import datetime, string, json, random

BLE5_MAX_DURATION = ag.BLE5_PARAM_PRIMARY_CHANNEL_SCAN_CYCLE + 1000 # In MS
BLE5_MAX_RETRIES = BLE5_MAX_DURATION//20

#################################
# GW
#################################

def gw_configure(test, cfg={}, version="", extended_cfg={}, ret_pkt=False, wait=False, serialization_change=False):
    cfg = cfg if cfg else get_default_gw_dict(test)
    if test.gw_lan:
        cfg[GW_MODE] = BLE_LAN
    gw_config = create_gw_config(test, cfg, version)
    gw_config[GW_CONF][ADDITIONAL].update(extended_cfg)
    gw_config[GW_CONF].update(extended_cfg)
    if test.protobuf:
        payload = cert_protobuf.downlink_to_pb(gw_config)
        utPrint(f"Configuring GW with cfg pkt:\n{payload}", "BLUE")
    else:
        if not serialization_change:
            gw_config[GW_CONF][ADDITIONAL][SERIALIZATION_FORMAT] = JSON
        payload = json.dumps(gw_config)
        utPrint(f"Configuring GW with cfg pkt:\n{payload}", "BLUE")
    test.mqttc.flush_pkts()
    test.mqttc.publish(test.mqttc.update_topic, payload=payload, qos=1)
    if wait:
        # Search for update packet
        start_time = datetime.datetime.now()
        while (datetime.datetime.now() - start_time).seconds < DEFAULT_GW_FIELD_UPDATE_TIMEOUT:
            for p in test.mqttc._userdata["pkts"].status:
                if GW_CONF in p.body or GW_STATUS in p.body:
                    print_pkt(p.body)
                    utPrint("SUCCESS: Found GW cfg", "GREEN")
                    cert_common.wait_time_n_print(5)
                    if ret_pkt:
                        return test, p.body
                    else:
                        return test, DONE
            print_update_wait()
        test.rc = TEST_FAILED
        test.add_reason(f"FAILURE: GW cfg not found after {DEFAULT_GW_FIELD_UPDATE_TIMEOUT} seconds!")
        return test, NO_RESPONSE
    else:
        utPrint("Sent GW cfg, Wait is set to False", "BLUE")
        return test, DONE

def create_gw_config(test, cfg, version=""):
    if version:
        return dict({GW_CONF:{LAT: GW_LATITUDE_DEFAULT, LNG: GW_LONGITUDE_DEFAULT, WIFI_VERSION: version[WIFI_VERSION],
                     BLE_VERSION: version[BLE_VERSION], GW_API_VERSION: GW_API_VER_OLD, ADDITIONAL:dict(cfg)}})
    elif test.gw_orig_versions:
        return dict({GW_CONF:{LAT: GW_LATITUDE_DEFAULT, LNG: GW_LONGITUDE_DEFAULT, WIFI_VERSION: test.gw_orig_versions[WIFI_VERSION],
                     BLE_VERSION: test.gw_orig_versions[BLE_VERSION], GW_API_VERSION:  GW_API_VER_OLD, ADDITIONAL:dict(cfg)}})
    # Protection for FDM gw config
    else:
        return dict({GW_CONF:{LAT: GW_LATITUDE_DEFAULT, LNG: GW_LONGITUDE_DEFAULT, GW_API_VERSION: GW_API_VER_OLD,
                     ADDITIONAL:dict(cfg)}})

def gw_downlink(test, raw_tx_data="", is_ota=False, version="", max_duration=100, max_retries=8):
    pkt = create_gw_downlink_pkt(test, raw_tx_data, is_ota, version=version, max_duration=max_duration, max_retries=max_retries)
    print("GW Downlink:", pkt)
    payload = cert_protobuf.downlink_to_pb(pkt) if test.protobuf else json.dumps(pkt)
    test.mqttc.publish(test.mqttc.update_topic, payload=payload, qos=1)

def create_gw_downlink_pkt(test, raw_tx_data="", is_ota=False, version="", max_duration=100, max_retries=8):
    ret = dict({TX_PKT: raw_tx_data,
                TX_MAX_DURATION_MS: max_duration,
                TX_MAX_RETRIES: max_retries})
    if is_ota == False:
        ret[ACTION] = 0
    else:
        ret[ACTION] = 1
        ret[GW_ID] = str(test.gw)
        ret[BRIDGE_ID] = test.active_brg.id_str
        ret[IMG_DIR_URL] = f"https://api.us-east-2.prod.wiliot.cloud/v1/bridge/type/{test.active_brg.board_type}/version/{version}/binary/"
        # Using a random uuid to force file download on the GW side
        ret[VER_UUID_STR] = ''.join(random.choices(string.digits, k=VER_MAX_LEN))
        ret[UPGRADE_BLSD] = False
        ret[TX_MAX_DURATION_MS] = 150
    return ret

def get_default_gw_dict(test=None):
    return dict({WLT_SERVER: test.server if test else PROD, GW_MODE: BLE_WIFI, USE_STAT_LOC: False,
                 SERIALIZATION_FORMAT: PROTOBUF, ACL:dict({ACL_MODE: ACL_DENY , ACL_BRIDGE_IDS:[]})})

def config_gw_defaults(test, version=""):
    utPrint(f"Configuring gateway {test.gw} to defaults", "BLUE")
    return gw_configure(test, get_default_gw_dict(test), wait=True, version=version)

def config_gw_version(test, version):
    utPrint(f"Updating GW versions to {version[WIFI_VERSION]} , {version[BLE_VERSION]}", "BLUE")
    if version == VERSIONS["3.16.3"]:
        gw_configure(test,
                     dict({WLT_SERVER: test.server if test else PROD, OUTPUT_POWER_2_4: 8, GW_MODE: BLE_WIFI, TX_PERIOD: 3,
                           USE_STAT_LOC: False, GW_DATA_MODE: TAGS_AND_BRGS, PACER_INTERVAL: 60, GW_ENERGY_PATTERN: 17, RX_TX_PERIOD: 100}),
                     version)
    if version == VERSIONS["4.1.0"] or version == VERSIONS["4.1.2"]:
        gw_configure(test,
                     dict({WLT_SERVER: test.server if test else PROD, GW_MODE: BLE_WIFI,
                           USE_STAT_LOC: False}),
                     version)
    else:
        gw_configure(test, get_default_gw_dict(test), version)

def gw_info_action(test):
    pkt = {ACTION: GET_INFO_ACTION}
    payload = cert_protobuf.downlink_to_pb(pkt) if test.protobuf else json.dumps(pkt)
    test.mqttc.publish(test.mqttc.update_topic, payload=payload, qos=1)

def gw_reboot_action(test):
    pkt = {ACTION: REBOOT_GW_ACTION}
    payload = cert_protobuf.downlink_to_pb(pkt) if test.protobuf else json.dumps(pkt)
    test.mqttc.publish(test.mqttc.update_topic, payload=payload, qos=1)

def gw_action(test, action):
    pkt = {ACTION: action}
    payload = cert_protobuf.downlink_to_pb(pkt) if test.protobuf else json.dumps(pkt)
    test.mqttc.publish(test.mqttc.update_topic, payload=payload, qos=1)

def gw_log_period_action(test, period):
    pkt = {ACTION: f"{LOG_PERIOD_ACTION} {period}"}
    payload = cert_protobuf.downlink_to_pb(pkt) if test.protobuf else json.dumps(pkt)
    test.mqttc.publish(test.mqttc.update_topic, payload=payload, qos=1)

def gw_logs_action(test):
    pkt = {ACTION: GET_LOGS}
    payload = cert_protobuf.downlink_to_pb(pkt) if test.protobuf else json.dumps(pkt)
    test.mqttc.publish(test.mqttc.update_topic, payload=payload, qos=1)

def gw_status_wait(test, cond, str, time_limit): #cond gatewayLogs str test type
    test.mqttc.flush_pkts()
    start_time = datetime.datetime.now()
    while (datetime.datetime.now() - start_time).seconds < time_limit:
        for p in test.mqttc._userdata["pkts"].status:
            if cond in p.body:
                if str in p.body[cond]:
                    print_pkt(p.body)
                    return
        print_update_wait()

#################################
# BRG
#################################

get_brg_id_int = lambda test, brg_mac : brg_mac if brg_mac != 0 else test.active_brg.id_int

def fields_n_vals_dict_get(fields, values):
    # initiate fields and values
    fields_and_values = {}
    for field, value in zip(fields, values):
        fields_and_values[field] = int(value)
    # functionality run print
    print_string = generate_print_string(fields_and_values)
    functionality_run_print(print_string)
    return fields_and_values

def brg_configure(test, cfg_pkt=None, module=None, fields=None, values=None, wait=True, ret_cfg_pkt=False):
    retries = 3
    if not cfg_pkt:
        fields_n_vals = fields_n_vals_dict_get(fields, values)
        cfg_pkt = get_default_brg_pkt(test, pkt_type=module, **fields_n_vals)
    # Search for update packet
    test.mqttc.flush_pkts()
    if not wait:
        gw_downlink(test=test, raw_tx_data=cfg_pkt.dump())
        utPrint("Wait is set to False, not waiting for Bridge cfg ACK", "CYAN")
        return test, DONE

    for retry in range(retries):
        gw_downlink(test=test, raw_tx_data=cfg_pkt.dump())
        pkts_found = False
        seq_ids = []
        wlt_pkt = WltPkt()
        start_time = datetime.datetime.now()
        while (datetime.datetime.now() - start_time).seconds < DEFAULT_BRG_FIELD_UPDATE_TIMEOUT:
            pkts = cert_common.get_brg_cfg_pkts(test=test)
            if pkts:
                pkts_found = True
                for p in pkts:
                    wlt_pkt = WltPkt(p)
                    if seq_ids == [] or wlt_pkt.pkt.seq_id not in seq_ids:
                        print(wlt_pkt.pkt)
                        if cfg_pkt.pkt == wlt_pkt.pkt:
                            utPrint("SUCCESS: Bridge cfg", "GREEN")
                            return (test, DONE) if not ret_cfg_pkt else (test, wlt_pkt)
                        seq_ids.append(wlt_pkt.pkt.seq_id)
            print_update_wait()
        utPrint(f"brg_configure: No pkts found retry={retry}!", "WARNING")
    if not pkts_found:
        utPrint(f"brg_configure: No pkts found retry={retry}!", "RED")
        test.add_reason(f"brg_configure: No pkts found. retry={retry}")
    test.rc = TEST_FAILED
    if wlt_pkt.pkt:
        # In case of failure, we want to see if it's api version issue
        test.active_brg.api_version = wlt_pkt.pkt.api_version
        print(f"-->> api_version:{test.active_brg.api_version}\nFailed brg_configure with pkt ({cfg_pkt.pkt.__dict__})")
        test.add_reason(f"Failed brg_configure")
    return test, NO_RESPONSE

def brg_configure_ble5(test, cfg_pkt=None, module=None, fields=None, values=None, ret_cfg_pkt=False, wait=True):
    if not cfg_pkt:
        fields_n_vals = fields_n_vals_dict_get(fields, values)
        cfg_pkt = get_default_brg_pkt(test, pkt_type=module, **fields_n_vals)
    # Search for update packet
    test.mqttc.flush_pkts()

    num_of_tries = 0
    pkts_found = False
    seq_ids = []
    wlt_pkt = WltPkt()
    start_time = datetime.datetime.now()
    gw_downlink(test=test, raw_tx_data=cfg_pkt.dump(), max_duration=BLE5_MAX_DURATION, max_retries=BLE5_MAX_RETRIES)
    while not pkts_found and wait:
        if ((datetime.datetime.now() - start_time).seconds > ((ag.BLE5_PARAM_PRIMARY_CHANNEL_SCAN_CYCLE/1000)+1)):
            if num_of_tries < 3:
                num_of_tries += 1
                start_time = datetime.datetime.now()
                gw_downlink(test=test, raw_tx_data=cfg_pkt.dump(), max_duration=BLE5_MAX_DURATION, max_retries=BLE5_MAX_RETRIES)
                print(f"Brg configure - BLE5 mode : No pkts found after {(ag.BLE5_PARAM_PRIMARY_CHANNEL_SCAN_CYCLE/1000)+1} seconds, in try number {num_of_tries}")
            else:
                test.add_reason(f"Brg configure - BLE5 mode : No pkts found after {BLE5_MAX_DURATION} seconds, in 3 tries")
                test.rc = TEST_FAILED
                time.sleep(1)
                test.mqttc.flush_pkts()
                return test, NO_RESPONSE
        pkts = cert_common.get_brg_cfg_pkts(test=test)
        if pkts:
            for p in pkts:
                wlt_pkt = WltPkt(p)
                if seq_ids == [] or wlt_pkt.pkt.seq_id not in seq_ids:
                    print(wlt_pkt.pkt)
                    if cfg_pkt.pkt == wlt_pkt.pkt:
                        utPrint("SUCCESS: Bridge cfg", "GREEN")
                        time.sleep(15)
                        test.mqttc.flush_pkts()
                        return (test, DONE) if not ret_cfg_pkt else (test, wlt_pkt)
                    seq_ids.append(wlt_pkt.pkt.seq_id)
        print_update_wait()

def brg1_configure(test, cfg_pkt=None, module=None, fields=None, values=None, wait=True, ret_cfg_pkt=False, ble5=False):
    test.active_brg = test.brg1
    if ble5:
        test, res = brg_configure_ble5(test, cfg_pkt, module, fields, values, ret_cfg_pkt)
    else:
        test, res = brg_configure(test, cfg_pkt, module, fields, values, wait, ret_cfg_pkt)
    test.active_brg = test.brg0
    return test, res

def internal_brg_configure(test, cfg_pkt=None, module=None, fields=None, values=None, wait=True, ret_cfg_pkt=False):
    test.active_brg = test.internal_brg_obj
    if not cfg_pkt:
        fields_n_vals = fields_n_vals_dict_get(fields, values) if fields and values else {}
        cfg_pkt = get_default_brg_pkt(test, pkt_type=module, **fields_n_vals)
    test, res = brg_configure(test, cfg_pkt, module, fields, values, wait, ret_cfg_pkt)
    test.active_brg = test.brg0
    return test, res

def send_brg_action(test, action_id, **kwargs):
    print(f"\nSending {ag.ACTIONS_DICT[action_id]}{test.active_brg.api_version} with parameters={kwargs if kwargs else None}")
    test.mqttc.flush_pkts()
    action_pkt = get_default_brg_pkt(test, pkt_type=eval_pkt(f'{ag.ACTIONS_DICT[action_id]}{test.active_brg.api_version}'), **kwargs)
    gw_downlink(test, raw_tx_data=action_pkt.dump())

def get_default_brg_pkt(test, pkt_type, group_id=ag.GROUP_ID_GW2BRG, seq_id=0, **kwargs):
        seq_id = test.get_seq_id() if seq_id == 0 else seq_id
        # Bypass from default sub1g ep cfg of 0 (no energizing)
        if "ModuleEnergySub1G" in pkt_type.__name__ and BRG_PATTERN not in kwargs:
            # TODO - Remove on next api_version update - this is a patch for parameter name change from api version 11 to 12
            brg_pattern = "sub1g_energy_" + BRG_PATTERN if test.active_brg.api_version < ag.API_VERSION_V12 else BRG_PATTERN
            kwargs.update({brg_pattern: ag.SUB1G_ENERGY_PATTERN_ISRAEL})
        brg_pkt = WltPkt(hdr=ag.Hdr(group_id=group_id), pkt=pkt_type(brg_mac=test.active_brg.id_int if test.active_brg else 0, seq_id=seq_id, **kwargs))
        return brg_pkt

def config_brg_defaults(test, modules=[], ble5=False):
    failed_cfg = False
    modules = test.active_brg.modules if not modules else modules
    for module in modules:
        utPrint(f"Configuring {module.__name__} to defaults. board type[{test.active_brg.board_type}] api version[{test.active_brg.api_version}]", "BLUE")
        cfg_pkt = get_default_brg_pkt(test, module)
        if ble5:
            test, res = brg_configure_ble5(test=test, cfg_pkt=cfg_pkt)
        else:
            test, res = brg_configure(test=test, cfg_pkt=cfg_pkt)
        if res == NO_RESPONSE:
            utPrint(f"FAILURE: {module.__name__} not configured to defaults", "RED")
            failed_cfg = True
        else:
            utPrint(f"SUCCESS: {module.__name__} configured to defaults", "GREEN")
    return (test, DONE) if not failed_cfg else (test, NO_RESPONSE)

def config_brg1_defaults(test, modules=[], ble5=False):
    test.active_brg = test.brg1
    test, res = config_brg_defaults(test, modules, ble5)
    test.active_brg = test.brg0
    return test, res

def print_cur_modules(test, modules):
    start_time = datetime.datetime.now()
    # Print all pkts
    for module in modules:
        pkts = cert_mqtt.get_brg2gw_mgmt_pkts(test.mqttc, test, mgmt_types=[module])
        if pkts:
            print("\nGot {} packet after {} sec!".format(module, (datetime.datetime.now() - start_time).seconds))
            print(pkts[-1][MGMT_PKT].pkt)

    return test

def brg_ota(test, gw_ble_version=None, search_ack=True):
    if not gw_ble_version:
        gw_ble_version = cert_common.get_gw_versions(test)[BLE_VERSION]
        if not gw_ble_version:
            test.rc = TEST_FAILED
            test.add_reason("Couldn't get GW versions!")
            return test

    if gw_ble_version != test.active_brg.version:
        utPrint(f"Updating BRG version to {gw_ble_version}", "BLUE")
        ota_updates = [f"Starting OTA to BRG WLT_{test.active_brg.id_str}",
                       f"BRG OTA finished with status 0 for bridge {test.active_brg.id_str}"]
        functionality_run_print(f"OTA for brg: {test.active_brg.id_str}")
        action_pkt = get_default_brg_pkt(test=test, pkt_type=eval_pkt(f'ActionGenericV{test.active_brg.api_version}'), action_id=ag.ACTION_REBOOT)
        # BRG OTA - Flash pkts ONLY before starting to avoid deletion of needed GW Logs which are in the status topic
        test.mqttc.flush_status_pkts()
        gw_downlink(test, raw_tx_data=action_pkt.dump(), is_ota=True, version=gw_ble_version)
        # expected_hash=1 due to different cfgs and versions between builds
        test = cert_common.reboot_config_analysis(test=test, expected_hash=1, ble_version=gw_ble_version, timeout=VER_UPDATE_TIMEOUT)

        # for debug - print all logs to see failure reason
        cert_common.get_gw_logs_packets(test, print_log=True)
        if test.rc == TEST_FAILED and test.exit_on_param_failure:
            return test
        elif search_ack:
            test = cert_common.gw_logs_search(test, ota_updates)
            if test.rc == TEST_FAILED and test.exit_on_param_failure:
                return test
            test = cert_common.gw_action_status_search(test, ag.BRG_MGMT_MSG_TYPE_OTA_UPDATE, 0)
            if test.rc == TEST_FAILED and test.exit_on_param_failure:
                return test
    else:
        test.add_reason(WANTED_VER_SAME)
    test.active_brg.version = gw_ble_version
    test.active_brg.update_modules()
    return test

def update_versions(test, versions, update_gw=True, update_brg=True):
    #update gw versions
    if update_gw:
        config_gw_version(test, versions)
        # Search for update packet
        start_time = datetime.datetime.now()
        found = {BLE_VERSION: False, WIFI_VERSION: False}
        # First pkt received is GW "cfg ack"
        tries = 0
        while not all([found[version] for version in found]):
            for p in test.mqttc._userdata["pkts"].status:
                if GW_CONF in p.body or GW_STATUS in p.body:
                    print("\nConfig pkts:")
                    print_pkt(p.body)
                    bkv = BLE_VERSION.replace('Chip', '') if test.protobuf else BLE_VERSION
                    wkv = WIFI_VERSION.replace('Chip', '') if test.protobuf else WIFI_VERSION
                    ckv = GW_STATUS if test.protobuf else GW_CONF
                    if p.body[ckv][bkv] == versions[BLE_VERSION]:
                        found[BLE_VERSION] = True
                    if p.body[ckv][wkv] == versions[WIFI_VERSION]:
                        found[WIFI_VERSION] = True
                    if not all([found[version] for version in found]):
                        # WIFI configured, need to configure again for BLE
                        if tries > 0:
                            # First pkt received is GW "cfg ack"
                            print(f"\nVersions Update Status:\n{found}\nTries: {tries}\nUpdate Time: {(datetime.datetime.now() - start_time).seconds} seconds")
                            config_gw_version(test, versions)
                        tries += 1
                    test.mqttc.flush_pkts()
            print_update_wait()
            if (datetime.datetime.now() - start_time).seconds > VER_UPDATE_TIMEOUT:
                test.rc = TEST_FAILED
                failed_versions = " & ".join([f"{k}={v}" for k,v in versions.items() if not found[k]])
                test.add_reason(f"{failed_versions} not found after {VER_UPDATE_TIMEOUT} seconds in {tries} tries!")
                print(f"\n{test.reason}")
                break
        cert_common.wait_time_n_print(10)
    if not test.rc:
        if update_gw:
            print(f"\nGW versions updated successfully in {tries if tries > 0 else 1} tries!\n")
        # update brg version if test is not an internal_brg test
        if update_brg and not test.internal_brg:
            test = brg_ota(test, gw_ble_version=versions[BLE_VERSION], search_ack=False)

    return test
