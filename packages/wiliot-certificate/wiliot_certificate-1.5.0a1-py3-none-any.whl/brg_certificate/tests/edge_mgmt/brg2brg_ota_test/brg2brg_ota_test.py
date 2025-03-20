from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
from brg_certificate.wlt_types import *
import brg_certificate.cert_common as cert_common
import brg_certificate.cert_config as cert_config

# Test Description:
# Requires 1 GW and 2 BRGs where the BRGs aren't of the same FW version.
# Initiates BRG2BRG OTA - have the bridge with the newer FW version (source) update the bridge with the older
# FW version (destination). Source bridge will get a gw2brg message initiating the ota process from the firmware
# code, making the source bridge copy its image to the destination bridge.
# For a bootloader image OTA, the gw2brg message includes a "bootloader" field and it is updated to True if the OTA
# required is for bootloader image. The FW and bootloader images can currently only be updated separately.

# Test Defines
VERSIONS_SAME = "Both bridges FW versions are the same!"
BL_VERSIONS_SAME = "Both bridges Bootloader versions are the same!"
BOARDS_MISMATCH = "Bridges are of different board types!"


def run(test):

    # Test initialization
    is_bl_ota = "BOOTLOADER" in test.params[0].name

    test = cert_common.test_prolog(test)
    # Initialize bridges
    brg0 = test.brg0
    brg1 = test.brg1

    # Protections from same version & different board types
    if not is_bl_ota and brg0.version == brg1.version:
        utPrint(VERSIONS_SAME, "RED")
        test.add_reason(VERSIONS_SAME)
        test.rc = TEST_FAILED
    if is_bl_ota and brg0.bl_version == brg1.bl_version:
        utPrint(BL_VERSIONS_SAME, "RED")
        test.add_reason(BL_VERSIONS_SAME)
        test.rc = TEST_FAILED
    if brg0.board_type != brg1.board_type:
        utPrint(BOARDS_MISMATCH, "RED")
        test.add_reason(BOARDS_MISMATCH)
        test.rc = TEST_FAILED

    if test.rc == TEST_FAILED:
        return cert_common.test_epilog(test, revert_brgs=True)

    # Decide on source and destination bridges
    if is_bl_ota:
        if brg0.bl_version > brg1.bl_version:
            src_brg = brg0
            dest_brg = brg1
        else:
            src_brg = brg1
            dest_brg = brg0
    else:
        if brg0.version > brg1.version:
            src_brg = brg0
            dest_brg = brg1
        else:
            src_brg = brg1
            dest_brg = brg0
        test.active_brg = src_brg

    desired_version_print = src_brg.bl_version if is_bl_ota else src_brg.version
    older_version_print = dest_brg.bl_version if is_bl_ota else dest_brg.version
    utPrint(f"Source {"bootloader" if is_bl_ota else ""} bridge version: {desired_version_print}. "
            f"Destination bridge {"bootloader" if is_bl_ota else ""} version: {older_version_print}", "BLUE")

    # Send BRG2BRG_OTA message to source bridge
    functionality_run_print(f"BRG2BRG OTA - Source Bridge MAC: {src_brg.id_str}, Destination Bridge MAC: {dest_brg.id_str}")
    brg2brg_ota_pkt = eval_pkt(f'Brg2BrgOtaV{test.active_brg.api_version}')(src_brg_mac=src_brg.id_int,
                                                                            dest_brg_mac=dest_brg.id_int,
                                                                            seq_id=test.get_seq_id(),
                                                                            bootloader=is_bl_ota)
    brg2brg_ota_pkt_downlink = WltPkt(hdr=ag.Hdr(group_id=ag.GROUP_ID_GW2BRG), pkt=brg2brg_ota_pkt)
    # BRG OTA - Flush pkts ONLY before starting to avoid deletion of needed GW Logs
    test.mqttc.flush_pkts()
    cert_config.gw_downlink(test, raw_tx_data=brg2brg_ota_pkt_downlink.dump())

    # Get version of the destination bridge
    test.active_brg = dest_brg
    # expected_hash=1 due to different cfgs and versions between builds
    test = cert_common.reboot_config_analysis(test=test, expected_hash=1, ble_version=src_brg.version if not is_bl_ota else None,
                                              bl_version=src_brg.bl_version if is_bl_ota else None, timeout=VER_UPDATE_TIMEOUT)

    return cert_common.test_epilog(test)
