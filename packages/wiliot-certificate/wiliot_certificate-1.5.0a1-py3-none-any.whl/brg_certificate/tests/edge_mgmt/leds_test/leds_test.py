from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
from brg_certificate.wlt_types import *
import brg_certificate.cert_common as cert_common
import brg_certificate.cert_config as cert_config

# Tests definitions
BRG_REBOOT_TIME = 30
NUM_OF_LED_BLINKS_ACTION = 10
LEDS_KEEP_ALIVE_PERIOD = 10
LEDS_KEEP_ALIVE_BLINKS_NUM = 2
ENERGIZING_LED_COLOR = "RED"
BOARD_TYPE_2_ECHOING_LED_COLLOR_DICT = {ag.BOARD_TYPE_FANSTEL_SINGLE_BAND_V0: "Green",
                                        ag.BOARD_TYPE_FANSTEL_DUAL_BAND_V0: "Green",
                                        ag.BOARD_TYPE_MINEW_SINGLE_BAND_V0: "Green",
                                        ag.BOARD_TYPE_MINEW_DUAL_BAND_V0: "Blue",
                                        ag.BOARD_TYPE_ENERGOUS_V0: "Blue",
                                        ag.BOARD_TYPE_ENERGOUS_V1: "Blue",
                                        ag.BOARD_TYPE_ENERGOUS_V2: "Blue",
                                        ag.BOARD_TYPE_ENERGOUS_V3: "Blue",
                                        ag.BOARD_TYPE_ENERGOUS_V4: "Blue",
                                        ag.BOARD_TYPE_ERM_V0: "Blue",
                                        ag.BOARD_TYPE_ERM_V1: "Blue",
                                        ag.BOARD_TYPE_KOAMTAC_V0: "Green",
                                        ag.BOARD_TYPE_MINEW_POE_V0: "Yellow"}


# Helper functions
def compare_versions(gw_version, brg_version):
    # Split versions into components
    gw_version_parts = gw_version.split('.')
    brg_version_parts = brg_version.split('.')

    # Compare each component
    if (len(gw_version_parts) == 3 and len(brg_version_parts) == 3 and
            gw_version_parts[0] == brg_version_parts[0] and
            gw_version_parts[1] == brg_version_parts[1] and
            gw_version_parts[2] == brg_version_parts[2]):
        return True
    else:
        return False


def run(test):
    test = cert_common.test_prolog(test)
    if test.rc == TEST_FAILED:
        return cert_common.test_epilog(test)

    test.mqttc.flush_pkts()
    # --------------------- Pre stage ------------------------------ #
    utPrint("Pre state - Please make sure you have a registerd GW connected to the UT BRG!!!", "WARNING")
    utPrint("Press 'y' if the GW is registered and connected to the UT BRG", "BLUE")
    value = cert_common.check_input_n_try_again(input())
    test = cert_common.value_check_if_y(test, value, "PRE STAGE")
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        return cert_common.test_epilog(test)
    utPrint("GW is registered and connected to UT BRG!", "GREEN")

    # Determine LED colors according to the board type
    test, interface = cert_common.get_module_if_pkt(test)
    if test.rc == TEST_FAILED:
        utPrint("Failed to get the GW interface packet!", "RED")
        return cert_common.test_epilog(test)
    board_type = interface.board_type
    if board_type not in BOARD_TYPE_2_ECHOING_LED_COLLOR_DICT:
        utPrint(f"Unknown board type: {board_type}", "RED")
        return cert_common.test_epilog(test)
    else:
        ECHOING_LED_COLOR = BOARD_TYPE_2_ECHOING_LED_COLLOR_DICT[board_type]
    if board_type == ag.BOARD_TYPE_MINEW_POE_V0:
        NUS_INDICATION_LED_COLOR = "Green"
    else:
        NUS_INDICATION_LED_COLOR = ECHOING_LED_COLOR

    # Version verification
    gw_ble_version = test.gw_orig_versions.get(BLE_VERSION)
    bridge_ble_version = test.active_brg.version
    if gw_ble_version and bridge_ble_version:
        if compare_versions(gw_ble_version, bridge_ble_version) is False:
            utPrint("Versions are not alligned - Please make sure the BLE versions are the same", "RED")
            return cert_common.test_epilog(test)
        else:
            utPrint("GW & BRG versions are the same - Pre stage Passed!", "GREEN")
    else:
        utPrint("Failed to get the BLE versions, please try again!", "RED")
        return cert_common.test_epilog(test)

    utPrint("Starting examining the LED's, Please pay attention to the following steps!", "WARNING")
    # ---------------------  Advertising LED  --------------------- #
    utPrint("Advertising LED check - sending Reboot action to BRG!", "HEADER")
    cert_config.send_brg_action(test, ag.ACTION_REBOOT)
    reboot_start_ts = int(datetime.datetime.now().timestamp())
    utPrint(f"The BRG was rebooted - is the advertising LED ({NUS_INDICATION_LED_COLOR}) continuously "
            "on and all other LED's are off? (Y/N)", "BLUE")
    value = cert_common.check_input_n_try_again(input())
    test = cert_common.value_check_if_y(test, value, "Advertising LED check")
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        return cert_common.test_epilog(test)
    # wait for advertisement phase to finish
    if (int(datetime.datetime.now().timestamp()) - reboot_start_ts < BRG_REBOOT_TIME):
        utPrint(f"Now we'll wait for the BRG to finish his {BRG_REBOOT_TIME} advertismeent!", "BLUE")
        cert_common.wait_time_n_print(BRG_REBOOT_TIME - (int(datetime.datetime.now().timestamp()) - reboot_start_ts))
    utPrint("Advertisement LED check completed!\n", "GREEN")

    # ------------------  Eenergizing LED check  ------------------ #
    #  Energizing is ON (Non default for SUB1G, but for UT purposses we'll set it to ON)
    utPrint("Energizing LED check!", "HEADER")
    utPrint(f"Is the Energizing LED ({ENERGIZING_LED_COLOR}) on? (Y/N)", "BLUE")
    value = cert_common.check_input_n_try_again(input())
    test = cert_common.value_check_if_y(test, value, "Eenergizing LED check")
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        return cert_common.test_epilog(test)

    # Energizing is OFF
    #  Default cfg for 2400 is 0 == no energizing so we only eliminating sub1g energizing
    utPrint("Configuring the BRG to no energizing in sub1g", "WARNING")
    sub1g_module = eval(f'ModuleEnergySub1GV{test.active_brg.api_version}')
    test = cert_config.brg_configure(test, fields=[BRG_PATTERN], values=[ag.SUB1G_ENERGY_PATTERN_NO_ENERGIZING], module=sub1g_module)[0]
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        return cert_common.test_epilog(test, revert_brgs=True, modules=[sub1g_module])
    utPrint(f"wait a few seconds for the change to apply - Is the Energizing LED ({ENERGIZING_LED_COLOR}) off? (Y/N)", "BLUE")
    value = cert_common.check_input_n_try_again(input())
    test = cert_common.value_check_if_y(test, value, "Eenergizing LED check")
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        return cert_common.test_epilog(test, revert_brgs=True, modules=[sub1g_module])
    utPrint("Energizing LED check completed!\n", "GREEN")

    # ------------------- Echo LED check -------------------------- #
    utPrint("Echoing LED check!", "HEADER")
    utPrint("Please make sure you have tags around you before answering!", "WARNING")
    utPrint(f"Is the Echoing LED ({ECHOING_LED_COLOR}) blinking? (Y/N)", "BLUE")
    value = cert_common.check_input_n_try_again(input())
    test = cert_common.value_check_if_y(test, value, "Echoing LED check")
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        return cert_common.test_epilog(test)
    utPrint("Echoing LED check completed!\n", "GREEN")

    # ---------------- LEDS_KEEP_ALIVE_PERIOD_CHECK --------------- #
    utPrint("LEDS_KEEP_ALIVE_PERIOD check!", "HEADER")
    utPrint("Please remove all tags from the bridge surrounding for this check!", "WARNING")
    utPrint(f"Look at the LEDS - Are both LED's off except for {LEDS_KEEP_ALIVE_BLINKS_NUM} blinks \n"
            f"of the Echoing LED ({ECHOING_LED_COLOR}) every {LEDS_KEEP_ALIVE_PERIOD} seconds? (Y/N)", "BLUE")
    value = cert_common.check_input_n_try_again(input())
    test = cert_common.value_check_if_y(test, value, "LEDS_KEEP_ALIVE_PERIOD check")
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        return cert_common.test_epilog(test, revert_brgs=True, modules=[sub1g_module])
    utPrint("LEDS_KEEP_ALIVE_PERIOD check completed! - please restore the tags to position around the bridge\n", "GREEN")

    # Revert to default
    utPrint("Reverting the BRG to default configuration", "WARNING")
    test = cert_config.config_brg_defaults(test, modules=[sub1g_module])[0]
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        return cert_common.test_epilog(test, revert_brgs=True, modules=[sub1g_module])
    utPrint(f"wait a few seconds for the change to apply - Is the Energizing LED ({ENERGIZING_LED_COLOR}) back on \n"
            f" and the Echoing LED ({ECHOING_LED_COLOR}) blinking? (Y/N)", "BLUE")
    value = cert_common.check_input_n_try_again(input())
    test = cert_common.value_check_if_y(test, value, "Eenergizing LED check")
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        return cert_common.test_epilog(test, revert_brgs=True, modules=[sub1g_module])
    utPrint("Succesfully Reverted the BRG to default configuration!\n", "GREEN")

    # -----------------------  Blink check  ----------------------- #
    utPrint("Blink action check - pay attention to the LED's", "HEADER")
    cert_config.send_brg_action(test, ag.ACTION_BLINK)
    if board_type == ag.BOARD_TYPE_MINEW_POE_V0:
        utPrint(f"wait a few seconds for the action to apply - "
                f"Did you see all 4 LED's blink {NUM_OF_LED_BLINKS_ACTION} times? (Y/N)", "BLUE")
    else:
        utPrint(f"wait a few seconds for the action to apply - "
                f"Did you see both LED's blink {NUM_OF_LED_BLINKS_ACTION} times? (Y/N)", "BLUE")
    value = cert_common.check_input_n_try_again(input())
    test = cert_common.value_check_if_y(test, value, "Blink check")
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        return cert_common.test_epilog(test)
    utPrint("Blink action check completed!\n", "GREEN")

    # ------------- Power management sleep & Keep Alive Mode ------------- #
    utPrint("Power management Sleep state & Keep Alive Mode check!", "HEADER")
    utPrint("Sending the BRG power management configuration in order to enter sleep state", "WARNING")
    pwr_mgmt_module = eval(f'ModulePwrMgmtV{test.active_brg.api_version}')
    test, wltpkt = cert_common.brg_pwr_mgmt_turn_on(test)
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        # Preventing leaving brg in pwr mgmt, protection for on that worked yet no ack was received
        test = cert_common.brg_pwr_mgmt_turn_off(test)
        return cert_common.test_epilog(test, revert_brgs=True, modules=[pwr_mgmt_module])
    utPrint("pwr mgmt static mode turned on!", "GREEN")
    utPrint("Waiting for on_duration to expire!", "BLUE")
    cert_common.wait_time_n_print(wltpkt.pkt.static_on_duration)
    sleep_state_start_ts = int(datetime.datetime.now().timestamp())
    utPrint("Now we'll check sleep_Keep_Alive state blink .\n", "WARNING")
    utPrint(f"look ath the LEDS - Are all leds off, besides 1 blink ({wltpkt.pkt.static_keep_alive_scan} msec period) of the \n"
            f"Echoing LED ({ECHOING_LED_COLOR}) every {wltpkt.pkt.static_keep_alive_period} seconds? (Y/N)", "BLUE")
    value = cert_common.check_input_n_try_again(input())
    test = cert_common.value_check_if_y(test, value, "Sleep Keep Alive mode check")
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        return cert_common.test_epilog(test, revert_brgs=True, modules=[pwr_mgmt_module])
    # wait for sleep_duration to expire to revert the bridge to defualt configuration
    if wltpkt.pkt.static_sleep_duration - (int(datetime.datetime.now().timestamp()) - sleep_state_start_ts) > 0:
        utPrint("Waiting for sleep_duration to expire", "BLUE")
        cert_common.wait_time_n_print(wltpkt.pkt.static_sleep_duration - (int(datetime.datetime.now().timestamp()) - sleep_state_start_ts))
    # Revert to default
    test = cert_common.brg_pwr_mgmt_turn_off(test)
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        test = cert_common.brg_pwr_mgmt_turn_off(test)
        return cert_common.test_epilog(test, revert_brgs=True, modules=[pwr_mgmt_module])
    utPrint("Keep Alive Mode check completed!", "GREEN")

    # ---------------------  Post stage ----------------------------- #
    utPrint("Test is completed, Good job!!!", "GREEN")
    return cert_common.test_epilog(test)
