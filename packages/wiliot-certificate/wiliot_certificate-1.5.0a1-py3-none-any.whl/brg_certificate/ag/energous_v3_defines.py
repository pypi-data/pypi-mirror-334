# This is an auto generated file! Don't edit this file manually!!!

import bitstruct
import binascii
import tabulate
from brg_certificate.ag.wlt_types_ag import API_VERSION_V0, API_VERSION_V1, API_VERSION_V2, API_VERSION_V5, API_VERSION_V6, API_VERSION_V7, API_VERSION_V8, API_VERSION_V9, API_VERSION_V10, API_VERSION_V11, API_VERSION_V12, API_VERSION_LATEST, MODULE_EMPTY, MODULE_GLOBAL, MODULE_IF, MODULE_DATAPATH, MODULE_ENERGY_2400, MODULE_ENERGY_SUB1G, MODULE_CALIBRATION, MODULE_PWR_MGMT, MODULE_EXT_SENSORS, MODULE_CUSTOM, SUB1G_ENERGY_PATTERN_NO_ENERGIZING, SUB1G_ENERGY_PATTERN_SINGLE_TONE_915000, SUB1G_ENERGY_PATTERN_FCC_HOPPING, SUB1G_ENERGY_PATTERN_JAPAN_1W, SUB1G_ENERGY_PATTERN_JAPAN_350MW, SUB1G_ENERGY_PATTERN_KOREA, SUB1G_ENERGY_PATTERN_SINGLE_TONE_916300, SUB1G_ENERGY_PATTERN_SINGLE_TONE_917500, SUB1G_ENERGY_PATTERN_AUSTRALIA, SUB1G_ENERGY_PATTERN_ISRAEL, SUB1G_ENERGY_PATTERN_NZ_HOPPING, SUB1G_ENERGY_PATTERN_LAST, CHANNEL_FREQ_37, CHANNEL_FREQ_38, CHANNEL_FREQ_39, CHANNEL_37, CHANNEL_38, CHANNEL_39, OUTPUT_POWER_2_4_NEG_12, OUTPUT_POWER_2_4_NEG_8, OUTPUT_POWER_2_4_NEG_4, OUTPUT_POWER_2_4_POS_0, OUTPUT_POWER_2_4_POS_2, OUTPUT_POWER_2_4_POS_3, OUTPUT_POWER_2_4_POS_4, OUTPUT_POWER_2_4_POS_5, OUTPUT_POWER_2_4_POS_6, OUTPUT_POWER_2_4_POS_7, OUTPUT_POWER_2_4_POS_8, RX_CHANNEL_37, RX_CHANNEL_38, RX_CHANNEL_39, RX_CHANNEL_10_250K, RX_CHANNEL_10_500K, RX_CHANNEL_V11_37, RX_CHANNEL_V11_38, RX_CHANNEL_V11_39, RX_CHANNEL_V11_4_1MBPS, RX_CHANNEL_V11_10_1MBPS, RX_CHANNEL_V11_4_2MBPS, RX_CHANNEL_V11_10_2MBPS, SECONDARY_RX_CHANNEL_10, SUB1G_OUTPUT_POWER_11, SUB1G_OUTPUT_POWER_14, SUB1G_OUTPUT_POWER_17, SUB1G_OUTPUT_POWER_19, SUB1G_OUTPUT_POWER_20, SUB1G_OUTPUT_POWER_23, SUB1G_OUTPUT_POWER_25, SUB1G_OUTPUT_POWER_26, SUB1G_OUTPUT_POWER_27, SUB1G_OUTPUT_POWER_29, SUB1G_OUTPUT_POWER_32, SUB1G_OUTPUT_POWER_PROFILE_14, SUB1G_OUTPUT_POWER_PROFILE_17, SUB1G_OUTPUT_POWER_PROFILE_20, SUB1G_OUTPUT_POWER_PROFILE_23, SUB1G_OUTPUT_POWER_PROFILE_26, SUB1G_OUTPUT_POWER_PROFILE_29, SUB1G_OUTPUT_POWER_PROFILE_32, SIGNAL_INDICATOR_REP_1, SIGNAL_INDICATOR_REP_2, SIGNAL_INDICATOR_REP_3, SIGNAL_INDICATOR_REP_4, SIGNAL_INDICATOR_SUB1G_REP_1, SIGNAL_INDICATOR_SUB1G_REP_2, SIGNAL_INDICATOR_SUB1G_REP_3, SIGNAL_INDICATOR_SUB1G_REP_4, SIGNAL_INDICATOR_REP_PROFILE_1, SIGNAL_INDICATOR_REP_PROFILE_2, SIGNAL_INDICATOR_REP_PROFILE_3, SIGNAL_INDICATOR_REP_PROFILE_4, SIGNAL_INDICATOR_SUB1G_REP_PROFILE_1, SIGNAL_INDICATOR_SUB1G_REP_PROFILE_2, SIGNAL_INDICATOR_SUB1G_REP_PROFILE_3, SIGNAL_INDICATOR_SUB1G_REP_PROFILE_4, BRG_DEFAULT_CALIBRATION_INTERVAL, BRG_DEFAULT_CALIBRATION_OUTPUT_POWER, BRG_DEFAULT_CALIBRATION_PATTERN, BRG_DEFAULT_DATAPATH_PATTERN, BRG_DEFAULT_PKT_FILTER, BRG_DEFAULT_RX_CHANNEL_OR_FREQ, BRG_DEFAULT_DATAPATH_OUTPUT_POWER, BRG_DEFAULT_TX_REPETITION, BRG_DEFAULT_PACER_INTERVAL, BRG_DEFAULT_RSSI_THRESHOLD, BRG_DEFAULT_RX_CHANNEL, BRG_DEFAULT_ENERGY_PATTERN_2_4, BRG_DEFAULT_ENERGY_DUTY_CYCLE_2_4, BRG_DEFAULT_OUTPUT_POWER_2_4, BRG_DEFAULT_SIGNAL_INDICATOR_REP, BRG_DEFAULT_SIGNAL_INDICATOR_REP_PROFILE, BRG_DEFAULT_SIGNAL_INDICATOR_CYCLE, BRG_DEFAULT_SUB1G_DUTY_CYCLE, BRG_DEFAULT_OUTPUT_POWER_SUB1G, BRG_DEFAULT_OUTPUT_POWER_SUB1G_PROFILE, BRG_DEFAULT_SUB1G_ENERGY_PATTERN, BRG_DEFAULT_SIGNAL_INDICATOR_SUB1G_REP, BRG_DEFAULT_SIGNAL_INDICATOR_SUB1G_REP_PROFILE, BRG_DEFAULT_SIGNAL_INDICATOR_SUB1G_CYCLE, BRG_DEFAULT_EXTERNAL_SENSOR_CFG, BRG_DEFAULT_TX_PERIOD, BRG_DEFAULT_TRANSMIT_TIME_SUB1G, BRG_DEFAULT_SUB1G_FREQ, BRG_DEFAULT_SUB1G_FREQ_PROFILE, BRG_DEFAULT_ENERGY_PATTERN_IDX_OLD, BRG_DEFAULT_RXTX_PERIOD, BRG_DEFAULT_PKT_TYPES_MASK, BRG_MGMT_MSG_TYPE_CFG_INFO, BRG_MGMT_MSG_TYPE_OTA_UPDATE, BRG_MGMT_MSG_TYPE_HB, BRG_MGMT_MSG_TYPE_REBOOT, BRG_MGMT_MSG_TYPE_LED_BLINK, BRG_MGMT_MSG_TYPE_CFG_SET, BRG_MGMT_MSG_TYPE_ACTION, BRG_MGMT_MSG_TYPE_BRG2BRG, BRG_MGMT_MSG_TYPE_HB_SLEEP, PWR_MGMT_DEFAULTS_LEDS_ON, PWR_MGMT_DEFAULTS_KEEP_ALIVE_PERIOD, PWR_MGMT_DEFAULTS_KEEP_ALIVE_SCAN, PWR_MGMT_DEFAULTS_ON_DURATION, PWR_MGMT_DEFAULTS_SLEEP_DURATION, LIS2DW12_DEFAULTS_PACKET_VERSION, LIS2DW12_DEFAULTS_STATE_THRESHOLD, LIS2DW12_DEFAULTS_WAKE_UP_DURATION, LIS2DW12_DEFAULTS_SLEEP_DURATION

# Board Overwritten defines
BRG_DEFAULT_CALIBRATION_OUTPUT_POWER = OUTPUT_POWER_2_4_POS_3
BRG_DEFAULT_DATAPATH_OUTPUT_POWER = OUTPUT_POWER_2_4_POS_3
BRG_DEFAULT_OUTPUT_POWER_2_4 = OUTPUT_POWER_2_4_POS_3

class ModuleIfV12():
    def __init__(self, raw='', module_type=MODULE_IF, msg_type=BRG_MGMT_MSG_TYPE_CFG_INFO, api_version=API_VERSION_V12, seq_id=0, brg_mac=0, board_type=0, bl_version=0, major_ver=0, minor_ver=0, patch_ver=0, sup_cap_glob=0, sup_cap_datapath=0, sup_cap_energy2400=0, sup_cap_energy_sub1g=0, sup_cap_calibration=0, sup_cap_pwr_mgmt=0, sup_cap_sensors=0, sup_cap_custom=0, cfg_hash=0, unused0=0):
        self.module_type = module_type
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.board_type = board_type
        self.bl_version = bl_version
        self.major_ver = major_ver
        self.minor_ver = minor_ver
        self.patch_ver = patch_ver
        self.sup_cap_glob = sup_cap_glob
        self.sup_cap_datapath = sup_cap_datapath
        self.sup_cap_energy2400 = sup_cap_energy2400
        self.sup_cap_energy_sub1g = sup_cap_energy_sub1g
        self.sup_cap_calibration = sup_cap_calibration
        self.sup_cap_pwr_mgmt = sup_cap_pwr_mgmt
        self.sup_cap_sensors = sup_cap_sensors
        self.sup_cap_custom = sup_cap_custom
        self.cfg_hash = cfg_hash
        self.unused0 = unused0
        if raw:
            self.set(raw)

    def __repr__(self) -> str:
        return "\n==> Packet module_if_v12 <==\n" + tabulate.tabulate([['module_type', f"0x{self.module_type:X} ({self.module_type})"],['msg_type', f"0x{self.msg_type:X} ({self.msg_type})"],['api_version', f"0x{self.api_version:X} ({self.api_version})"],['seq_id', f"0x{self.seq_id:X} ({self.seq_id})"],['brg_mac', f"0x{self.brg_mac:X} ({self.brg_mac})"],['board_type', f"0x{self.board_type:X} ({self.board_type})"],['bl_version', f"0x{self.bl_version:X} ({self.bl_version})"],['major_ver', f"0x{self.major_ver:X} ({self.major_ver})"],['minor_ver', f"0x{self.minor_ver:X} ({self.minor_ver})"],['patch_ver', f"0x{self.patch_ver:X} ({self.patch_ver})"],['sup_cap_glob', f"0x{self.sup_cap_glob:X} ({self.sup_cap_glob})"],['sup_cap_datapath', f"0x{self.sup_cap_datapath:X} ({self.sup_cap_datapath})"],['sup_cap_energy2400', f"0x{self.sup_cap_energy2400:X} ({self.sup_cap_energy2400})"],['sup_cap_energy_sub1g', f"0x{self.sup_cap_energy_sub1g:X} ({self.sup_cap_energy_sub1g})"],['sup_cap_calibration', f"0x{self.sup_cap_calibration:X} ({self.sup_cap_calibration})"],['sup_cap_pwr_mgmt', f"0x{self.sup_cap_pwr_mgmt:X} ({self.sup_cap_pwr_mgmt})"],['sup_cap_sensors', f"0x{self.sup_cap_sensors:X} ({self.sup_cap_sensors})"],['sup_cap_custom', f"0x{self.sup_cap_custom:X} ({self.sup_cap_custom})"],['cfg_hash', f"0x{self.cfg_hash:X} ({self.cfg_hash})"]], tablefmt="texttable")

    def __eq__(self, other):
        if other and set(other.__dict__.keys()) == set(self.__dict__.keys()):
            return (
                self.module_type == other.module_type and
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac and
                self.board_type == other.board_type and
                self.bl_version == other.bl_version and
                self.major_ver == other.major_ver and
                self.minor_ver == other.minor_ver and
                self.patch_ver == other.patch_ver and
                self.sup_cap_glob == other.sup_cap_glob and
                self.sup_cap_datapath == other.sup_cap_datapath and
                self.sup_cap_energy2400 == other.sup_cap_energy2400 and
                self.sup_cap_energy_sub1g == other.sup_cap_energy_sub1g and
                self.sup_cap_calibration == other.sup_cap_calibration and
                self.sup_cap_pwr_mgmt == other.sup_cap_pwr_mgmt and
                self.sup_cap_sensors == other.sup_cap_sensors and
                self.sup_cap_custom == other.sup_cap_custom and
                self.cfg_hash == other.cfg_hash
            )
        return False

    def dump(self):
        string = bitstruct.pack("u4u4u8u8u48u8u8u8u8u8u1u1u1u1u1u1u1u1u32u40", self.module_type, self.msg_type, self.api_version, self.seq_id, self.brg_mac, self.board_type, self.bl_version, self.major_ver, self.minor_ver, self.patch_ver, self.sup_cap_glob, self.sup_cap_datapath, self.sup_cap_energy2400, self.sup_cap_energy_sub1g, self.sup_cap_calibration, self.sup_cap_pwr_mgmt, self.sup_cap_sensors, self.sup_cap_custom, self.cfg_hash, self.unused0)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u4u4u8u8u48u8u8u8u8u8u1u1u1u1u1u1u1u1u32u40", binascii.unhexlify(string))
        self.module_type = d[0]
        self.msg_type = d[1]
        self.api_version = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.board_type = d[5]
        self.bl_version = d[6]
        self.major_ver = d[7]
        self.minor_ver = d[8]
        self.patch_ver = d[9]
        self.sup_cap_glob = d[10]
        self.sup_cap_datapath = d[11]
        self.sup_cap_energy2400 = d[12]
        self.sup_cap_energy_sub1g = d[13]
        self.sup_cap_calibration = d[14]
        self.sup_cap_pwr_mgmt = d[15]
        self.sup_cap_sensors = d[16]
        self.sup_cap_custom = d[17]
        self.cfg_hash = d[18]
        self.unused0 = d[19]

class ModuleIfV11():
    def __init__(self, raw='', module_type=MODULE_IF, msg_type=BRG_MGMT_MSG_TYPE_CFG_INFO, api_version=API_VERSION_V11, seq_id=0, brg_mac=0, board_type=0, bl_version=0, major_ver=0, minor_ver=0, patch_ver=0, sup_cap_glob=0, sup_cap_datapath=0, sup_cap_energy2400=0, sup_cap_energy_sub1g=0, sup_cap_calibration=0, sup_cap_pwr_mgmt=0, sup_cap_sensors=0, sup_cap_custom=0, cfg_hash=0, unused0=0):
        self.module_type = module_type
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.board_type = board_type
        self.bl_version = bl_version
        self.major_ver = major_ver
        self.minor_ver = minor_ver
        self.patch_ver = patch_ver
        self.sup_cap_glob = sup_cap_glob
        self.sup_cap_datapath = sup_cap_datapath
        self.sup_cap_energy2400 = sup_cap_energy2400
        self.sup_cap_energy_sub1g = sup_cap_energy_sub1g
        self.sup_cap_calibration = sup_cap_calibration
        self.sup_cap_pwr_mgmt = sup_cap_pwr_mgmt
        self.sup_cap_sensors = sup_cap_sensors
        self.sup_cap_custom = sup_cap_custom
        self.cfg_hash = cfg_hash
        self.unused0 = unused0
        if raw:
            self.set(raw)

    def __repr__(self) -> str:
        return "\n==> Packet module_if_v11 <==\n" + tabulate.tabulate([['module_type', f"0x{self.module_type:X} ({self.module_type})"],['msg_type', f"0x{self.msg_type:X} ({self.msg_type})"],['api_version', f"0x{self.api_version:X} ({self.api_version})"],['seq_id', f"0x{self.seq_id:X} ({self.seq_id})"],['brg_mac', f"0x{self.brg_mac:X} ({self.brg_mac})"],['board_type', f"0x{self.board_type:X} ({self.board_type})"],['bl_version', f"0x{self.bl_version:X} ({self.bl_version})"],['major_ver', f"0x{self.major_ver:X} ({self.major_ver})"],['minor_ver', f"0x{self.minor_ver:X} ({self.minor_ver})"],['patch_ver', f"0x{self.patch_ver:X} ({self.patch_ver})"],['sup_cap_glob', f"0x{self.sup_cap_glob:X} ({self.sup_cap_glob})"],['sup_cap_datapath', f"0x{self.sup_cap_datapath:X} ({self.sup_cap_datapath})"],['sup_cap_energy2400', f"0x{self.sup_cap_energy2400:X} ({self.sup_cap_energy2400})"],['sup_cap_energy_sub1g', f"0x{self.sup_cap_energy_sub1g:X} ({self.sup_cap_energy_sub1g})"],['sup_cap_calibration', f"0x{self.sup_cap_calibration:X} ({self.sup_cap_calibration})"],['sup_cap_pwr_mgmt', f"0x{self.sup_cap_pwr_mgmt:X} ({self.sup_cap_pwr_mgmt})"],['sup_cap_sensors', f"0x{self.sup_cap_sensors:X} ({self.sup_cap_sensors})"],['sup_cap_custom', f"0x{self.sup_cap_custom:X} ({self.sup_cap_custom})"],['cfg_hash', f"0x{self.cfg_hash:X} ({self.cfg_hash})"]], tablefmt="texttable")

    def __eq__(self, other):
        if other and set(other.__dict__.keys()) == set(self.__dict__.keys()):
            return (
                self.module_type == other.module_type and
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac and
                self.board_type == other.board_type and
                self.bl_version == other.bl_version and
                self.major_ver == other.major_ver and
                self.minor_ver == other.minor_ver and
                self.patch_ver == other.patch_ver and
                self.sup_cap_glob == other.sup_cap_glob and
                self.sup_cap_datapath == other.sup_cap_datapath and
                self.sup_cap_energy2400 == other.sup_cap_energy2400 and
                self.sup_cap_energy_sub1g == other.sup_cap_energy_sub1g and
                self.sup_cap_calibration == other.sup_cap_calibration and
                self.sup_cap_pwr_mgmt == other.sup_cap_pwr_mgmt and
                self.sup_cap_sensors == other.sup_cap_sensors and
                self.sup_cap_custom == other.sup_cap_custom and
                self.cfg_hash == other.cfg_hash
            )
        return False

    def dump(self):
        string = bitstruct.pack("u4u4u8u8u48u8u8u8u8u8u1u1u1u1u1u1u1u1u32u40", self.module_type, self.msg_type, self.api_version, self.seq_id, self.brg_mac, self.board_type, self.bl_version, self.major_ver, self.minor_ver, self.patch_ver, self.sup_cap_glob, self.sup_cap_datapath, self.sup_cap_energy2400, self.sup_cap_energy_sub1g, self.sup_cap_calibration, self.sup_cap_pwr_mgmt, self.sup_cap_sensors, self.sup_cap_custom, self.cfg_hash, self.unused0)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u4u4u8u8u48u8u8u8u8u8u1u1u1u1u1u1u1u1u32u40", binascii.unhexlify(string))
        self.module_type = d[0]
        self.msg_type = d[1]
        self.api_version = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.board_type = d[5]
        self.bl_version = d[6]
        self.major_ver = d[7]
        self.minor_ver = d[8]
        self.patch_ver = d[9]
        self.sup_cap_glob = d[10]
        self.sup_cap_datapath = d[11]
        self.sup_cap_energy2400 = d[12]
        self.sup_cap_energy_sub1g = d[13]
        self.sup_cap_calibration = d[14]
        self.sup_cap_pwr_mgmt = d[15]
        self.sup_cap_sensors = d[16]
        self.sup_cap_custom = d[17]
        self.cfg_hash = d[18]
        self.unused0 = d[19]

class ModuleCalibrationV12():
    def __init__(self, raw='', module_type=MODULE_CALIBRATION, msg_type=BRG_MGMT_MSG_TYPE_CFG_SET, api_version=API_VERSION_V12, seq_id=0, brg_mac=0, interval=BRG_DEFAULT_CALIBRATION_INTERVAL, output_power=BRG_DEFAULT_OUTPUT_POWER_2_4, pattern=BRG_DEFAULT_CALIBRATION_PATTERN, unused0=0, unused1=0):
        self.module_type = module_type
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.interval = interval
        self.output_power = output_power
        self.pattern = pattern
        self.unused0 = unused0
        self.unused1 = unused1
        if raw:
            self.set(raw)

    def __repr__(self) -> str:
        return "\n==> Packet module_calibration_v12 <==\n" + tabulate.tabulate([['module_type', f"0x{self.module_type:X} ({self.module_type})"],['msg_type', f"0x{self.msg_type:X} ({self.msg_type})"],['api_version', f"0x{self.api_version:X} ({self.api_version})"],['seq_id', f"0x{self.seq_id:X} ({self.seq_id})"],['brg_mac', f"0x{self.brg_mac:X} ({self.brg_mac})"],['interval', f"0x{self.interval:X} ({self.interval})"],['output_power', f"0x{self.output_power:X} ({self.output_power})"],['pattern', f"0x{self.pattern:X} ({self.pattern})"]], tablefmt="texttable")

    def __eq__(self, other):
        if other and set(other.__dict__.keys()) == set(self.__dict__.keys()):
            return (
                self.module_type == other.module_type and
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac and
                self.interval == other.interval and
                self.output_power == other.output_power and
                self.pattern == other.pattern
            )
        return False

    def dump(self):
        string = bitstruct.pack("u4u4u8u8u48u8s8u4u4u96", self.module_type, self.msg_type, self.api_version, self.seq_id, self.brg_mac, self.interval, self.output_power, self.pattern, self.unused0, self.unused1)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u4u4u8u8u48u8s8u4u4u96", binascii.unhexlify(string))
        self.module_type = d[0]
        self.msg_type = d[1]
        self.api_version = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.interval = d[5]
        self.output_power = d[6]
        self.pattern = d[7]
        self.unused0 = d[8]
        self.unused1 = d[9]

class ModuleCalibrationV11():
    def __init__(self, raw='', module_type=MODULE_CALIBRATION, msg_type=BRG_MGMT_MSG_TYPE_CFG_SET, api_version=API_VERSION_V11, seq_id=0, brg_mac=0, interval=BRG_DEFAULT_CALIBRATION_INTERVAL, output_power=BRG_DEFAULT_OUTPUT_POWER_2_4, pattern=BRG_DEFAULT_CALIBRATION_PATTERN, unused0=0, unused1=0):
        self.module_type = module_type
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.interval = interval
        self.output_power = output_power
        self.pattern = pattern
        self.unused0 = unused0
        self.unused1 = unused1
        if raw:
            self.set(raw)

    def __repr__(self) -> str:
        return "\n==> Packet module_calibration_v11 <==\n" + tabulate.tabulate([['module_type', f"0x{self.module_type:X} ({self.module_type})"],['msg_type', f"0x{self.msg_type:X} ({self.msg_type})"],['api_version', f"0x{self.api_version:X} ({self.api_version})"],['seq_id', f"0x{self.seq_id:X} ({self.seq_id})"],['brg_mac', f"0x{self.brg_mac:X} ({self.brg_mac})"],['interval', f"0x{self.interval:X} ({self.interval})"],['output_power', f"0x{self.output_power:X} ({self.output_power})"],['pattern', f"0x{self.pattern:X} ({self.pattern})"]], tablefmt="texttable")

    def __eq__(self, other):
        if other and set(other.__dict__.keys()) == set(self.__dict__.keys()):
            return (
                self.module_type == other.module_type and
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac and
                self.interval == other.interval and
                self.output_power == other.output_power and
                self.pattern == other.pattern
            )
        return False

    def dump(self):
        string = bitstruct.pack("u4u4u8u8u48u8s8u4u4u96", self.module_type, self.msg_type, self.api_version, self.seq_id, self.brg_mac, self.interval, self.output_power, self.pattern, self.unused0, self.unused1)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u4u4u8u8u48u8s8u4u4u96", binascii.unhexlify(string))
        self.module_type = d[0]
        self.msg_type = d[1]
        self.api_version = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.interval = d[5]
        self.output_power = d[6]
        self.pattern = d[7]
        self.unused0 = d[8]
        self.unused1 = d[9]

class ModuleDatapathV12():
    def __init__(self, raw='', module_type=MODULE_DATAPATH, msg_type=BRG_MGMT_MSG_TYPE_CFG_SET, api_version=API_VERSION_V12, seq_id=0, brg_mac=0, rssi_threshold=BRG_DEFAULT_RSSI_THRESHOLD, pacer_interval=BRG_DEFAULT_PACER_INTERVAL, pkt_filter=BRG_DEFAULT_PKT_FILTER, tx_repetition=BRG_DEFAULT_TX_REPETITION, output_power=BRG_DEFAULT_DATAPATH_OUTPUT_POWER, pattern=BRG_DEFAULT_DATAPATH_PATTERN, rx_channel=BRG_DEFAULT_RX_CHANNEL, unused0=0):
        self.module_type = module_type
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.rssi_threshold = rssi_threshold
        self.pacer_interval = pacer_interval
        self.pkt_filter = pkt_filter
        self.tx_repetition = tx_repetition
        self.output_power = output_power
        self.pattern = pattern
        self.rx_channel = rx_channel
        self.unused0 = unused0
        if raw:
            self.set(raw)

    def __repr__(self) -> str:
        return "\n==> Packet module_datapath_v12 <==\n" + tabulate.tabulate([['module_type', f"0x{self.module_type:X} ({self.module_type})"],['msg_type', f"0x{self.msg_type:X} ({self.msg_type})"],['api_version', f"0x{self.api_version:X} ({self.api_version})"],['seq_id', f"0x{self.seq_id:X} ({self.seq_id})"],['brg_mac', f"0x{self.brg_mac:X} ({self.brg_mac})"],['rssi_threshold', f"0x{self.rssi_threshold:X} ({self.rssi_threshold})"],['pacer_interval', f"0x{self.pacer_interval:X} ({self.pacer_interval})"],['pkt_filter', f"0x{self.pkt_filter:X} ({self.pkt_filter})"],['tx_repetition', f"0x{self.tx_repetition:X} ({self.tx_repetition})"],['output_power', f"0x{self.output_power:X} ({self.output_power})"],['pattern', f"0x{self.pattern:X} ({self.pattern})"],['rx_channel', f"0x{self.rx_channel:X} ({self.rx_channel})"]], tablefmt="texttable")

    def __eq__(self, other):
        if other and set(other.__dict__.keys()) == set(self.__dict__.keys()):
            return (
                self.module_type == other.module_type and
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac and
                self.rssi_threshold == other.rssi_threshold and
                self.pacer_interval == other.pacer_interval and
                self.pkt_filter == other.pkt_filter and
                self.tx_repetition == other.tx_repetition and
                self.output_power == other.output_power and
                self.pattern == other.pattern and
                self.rx_channel == other.rx_channel
            )
        return False

    def dump(self):
        string = bitstruct.pack("u4u4u8u8u48s8u16u5u3s8u4u4u72", self.module_type, self.msg_type, self.api_version, self.seq_id, self.brg_mac, ((self.rssi_threshold-0)//-1), self.pacer_interval, self.pkt_filter, self.tx_repetition, self.output_power, self.pattern, self.rx_channel, self.unused0)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u4u4u8u8u48s8u16u5u3s8u4u4u72", binascii.unhexlify(string))
        self.module_type = d[0]
        self.msg_type = d[1]
        self.api_version = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.rssi_threshold = ((d[5]*-1)+0)
        self.pacer_interval = d[6]
        self.pkt_filter = d[7]
        self.tx_repetition = d[8]
        self.output_power = d[9]
        self.pattern = d[10]
        self.rx_channel = d[11]
        self.unused0 = d[12]

class ModuleDatapathV11():
    def __init__(self, raw='', module_type=MODULE_DATAPATH, msg_type=BRG_MGMT_MSG_TYPE_CFG_SET, api_version=API_VERSION_V11, seq_id=0, brg_mac=0, unused1=0, unused0=0, adaptive_pacer=0, unified_echo_pkt=1, pacer_interval=BRG_DEFAULT_PACER_INTERVAL, pkt_filter=BRG_DEFAULT_PKT_FILTER, tx_repetition=BRG_DEFAULT_TX_REPETITION, output_power=BRG_DEFAULT_DATAPATH_OUTPUT_POWER, pattern=BRG_DEFAULT_DATAPATH_PATTERN, rx_channel=BRG_DEFAULT_RX_CHANNEL, unused2=0):
        self.module_type = module_type
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.unused1 = unused1
        self.unused0 = unused0
        self.adaptive_pacer = adaptive_pacer
        self.unified_echo_pkt = unified_echo_pkt
        self.pacer_interval = pacer_interval
        self.pkt_filter = pkt_filter
        self.tx_repetition = tx_repetition
        self.output_power = output_power
        self.pattern = pattern
        self.rx_channel = rx_channel
        self.unused2 = unused2
        if raw:
            self.set(raw)

    def __repr__(self) -> str:
        return "\n==> Packet module_datapath_v11 <==\n" + tabulate.tabulate([['module_type', f"0x{self.module_type:X} ({self.module_type})"],['msg_type', f"0x{self.msg_type:X} ({self.msg_type})"],['api_version', f"0x{self.api_version:X} ({self.api_version})"],['seq_id', f"0x{self.seq_id:X} ({self.seq_id})"],['brg_mac', f"0x{self.brg_mac:X} ({self.brg_mac})"],['adaptive_pacer', f"0x{self.adaptive_pacer:X} ({self.adaptive_pacer})"],['unified_echo_pkt', f"0x{self.unified_echo_pkt:X} ({self.unified_echo_pkt})"],['pacer_interval', f"0x{self.pacer_interval:X} ({self.pacer_interval})"],['pkt_filter', f"0x{self.pkt_filter:X} ({self.pkt_filter})"],['tx_repetition', f"0x{self.tx_repetition:X} ({self.tx_repetition})"],['output_power', f"0x{self.output_power:X} ({self.output_power})"],['pattern', f"0x{self.pattern:X} ({self.pattern})"],['rx_channel', f"0x{self.rx_channel:X} ({self.rx_channel})"]], tablefmt="texttable")

    def __eq__(self, other):
        if other and set(other.__dict__.keys()) == set(self.__dict__.keys()):
            return (
                self.module_type == other.module_type and
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac and
                self.adaptive_pacer == other.adaptive_pacer and
                self.unified_echo_pkt == other.unified_echo_pkt and
                self.pacer_interval == other.pacer_interval and
                self.pkt_filter == other.pkt_filter and
                self.tx_repetition == other.tx_repetition and
                self.output_power == other.output_power and
                self.pattern == other.pattern and
                self.rx_channel == other.rx_channel
            )
        return False

    def dump(self):
        string = bitstruct.pack("u4u4u8u8u48u4u2u1u1u16u5u3s8u4u4u72", self.module_type, self.msg_type, self.api_version, self.seq_id, self.brg_mac, self.unused1, self.unused0, self.adaptive_pacer, self.unified_echo_pkt, self.pacer_interval, self.pkt_filter, self.tx_repetition, self.output_power, self.pattern, self.rx_channel, self.unused2)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u4u4u8u8u48u4u2u1u1u16u5u3s8u4u4u72", binascii.unhexlify(string))
        self.module_type = d[0]
        self.msg_type = d[1]
        self.api_version = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.unused1 = d[5]
        self.unused0 = d[6]
        self.adaptive_pacer = d[7]
        self.unified_echo_pkt = d[8]
        self.pacer_interval = d[9]
        self.pkt_filter = d[10]
        self.tx_repetition = d[11]
        self.output_power = d[12]
        self.pattern = d[13]
        self.rx_channel = d[14]
        self.unused2 = d[15]

MODULE_ENERGY_2400_V12_SIGNAL_INDICATOR_REP_ENC = {SIGNAL_INDICATOR_REP_1:0, SIGNAL_INDICATOR_REP_2:1, SIGNAL_INDICATOR_REP_3:2, SIGNAL_INDICATOR_REP_4:3}
MODULE_ENERGY_2400_V12_SIGNAL_INDICATOR_REP_DEC = {0:SIGNAL_INDICATOR_REP_1, 1:SIGNAL_INDICATOR_REP_2, 2:SIGNAL_INDICATOR_REP_3, 3:SIGNAL_INDICATOR_REP_4}
class ModuleEnergy2400V12():
    def __init__(self, raw='', module_type=MODULE_ENERGY_2400, msg_type=BRG_MGMT_MSG_TYPE_CFG_SET, api_version=API_VERSION_V12, seq_id=0, brg_mac=0, duty_cycle=BRG_DEFAULT_ENERGY_DUTY_CYCLE_2_4, pattern=BRG_DEFAULT_ENERGY_PATTERN_2_4, output_power=BRG_DEFAULT_OUTPUT_POWER_2_4, signal_indicator_cycle=BRG_DEFAULT_SIGNAL_INDICATOR_CYCLE, signal_indicator_rep=BRG_DEFAULT_SIGNAL_INDICATOR_REP, unused0=0):
        self.module_type = module_type
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.duty_cycle = duty_cycle
        self.pattern = pattern
        self.output_power = output_power
        self.signal_indicator_cycle = signal_indicator_cycle
        self.signal_indicator_rep = signal_indicator_rep
        self.unused0 = unused0
        if raw:
            self.set(raw)

    def __repr__(self) -> str:
        return "\n==> Packet module_energy_2400_v12 <==\n" + tabulate.tabulate([['module_type', f"0x{self.module_type:X} ({self.module_type})"],['msg_type', f"0x{self.msg_type:X} ({self.msg_type})"],['api_version', f"0x{self.api_version:X} ({self.api_version})"],['seq_id', f"0x{self.seq_id:X} ({self.seq_id})"],['brg_mac', f"0x{self.brg_mac:X} ({self.brg_mac})"],['duty_cycle', f"0x{self.duty_cycle:X} ({self.duty_cycle})"],['pattern', f"0x{self.pattern:X} ({self.pattern})"],['output_power', f"0x{self.output_power:X} ({self.output_power})"],['signal_indicator_cycle', f"0x{self.signal_indicator_cycle:X} ({self.signal_indicator_cycle})"],['signal_indicator_rep', f"0x{self.signal_indicator_rep:X} ({self.signal_indicator_rep})"]], tablefmt="texttable")

    def __eq__(self, other):
        if other and set(other.__dict__.keys()) == set(self.__dict__.keys()):
            return (
                self.module_type == other.module_type and
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac and
                self.duty_cycle == other.duty_cycle and
                self.pattern == other.pattern and
                self.output_power == other.output_power and
                self.signal_indicator_cycle == other.signal_indicator_cycle and
                self.signal_indicator_rep == other.signal_indicator_rep
            )
        return False

    def dump(self):
        string = bitstruct.pack("u4u4u8u8u48u8u8s8u14u2u80", self.module_type, self.msg_type, self.api_version, self.seq_id, self.brg_mac, self.duty_cycle, self.pattern, self.output_power, self.signal_indicator_cycle, MODULE_ENERGY_2400_V12_SIGNAL_INDICATOR_REP_ENC[self.signal_indicator_rep], self.unused0)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u4u4u8u8u48u8u8s8u14u2u80", binascii.unhexlify(string))
        self.module_type = d[0]
        self.msg_type = d[1]
        self.api_version = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.duty_cycle = d[5]
        self.pattern = d[6]
        self.output_power = d[7]
        self.signal_indicator_cycle = d[8]
        self.signal_indicator_rep = MODULE_ENERGY_2400_V12_SIGNAL_INDICATOR_REP_DEC[d[9]]
        self.unused0 = d[10]

MODULE_ENERGY_2400_V11_SIGNAL_INDICATOR_REP_ENC = {SIGNAL_INDICATOR_REP_1:0, SIGNAL_INDICATOR_REP_2:1, SIGNAL_INDICATOR_REP_3:2, SIGNAL_INDICATOR_REP_4:3}
MODULE_ENERGY_2400_V11_SIGNAL_INDICATOR_REP_DEC = {0:SIGNAL_INDICATOR_REP_1, 1:SIGNAL_INDICATOR_REP_2, 2:SIGNAL_INDICATOR_REP_3, 3:SIGNAL_INDICATOR_REP_4}
class ModuleEnergy2400V11():
    def __init__(self, raw='', module_type=MODULE_ENERGY_2400, msg_type=BRG_MGMT_MSG_TYPE_CFG_SET, api_version=API_VERSION_V11, seq_id=0, brg_mac=0, duty_cycle=BRG_DEFAULT_ENERGY_DUTY_CYCLE_2_4, pattern=BRG_DEFAULT_ENERGY_PATTERN_2_4, output_power=BRG_DEFAULT_OUTPUT_POWER_2_4, signal_indicator_cycle=BRG_DEFAULT_SIGNAL_INDICATOR_CYCLE, signal_indicator_rep=BRG_DEFAULT_SIGNAL_INDICATOR_REP, unused0=0):
        self.module_type = module_type
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.duty_cycle = duty_cycle
        self.pattern = pattern
        self.output_power = output_power
        self.signal_indicator_cycle = signal_indicator_cycle
        self.signal_indicator_rep = signal_indicator_rep
        self.unused0 = unused0
        if raw:
            self.set(raw)

    def __repr__(self) -> str:
        return "\n==> Packet module_energy_2400_v11 <==\n" + tabulate.tabulate([['module_type', f"0x{self.module_type:X} ({self.module_type})"],['msg_type', f"0x{self.msg_type:X} ({self.msg_type})"],['api_version', f"0x{self.api_version:X} ({self.api_version})"],['seq_id', f"0x{self.seq_id:X} ({self.seq_id})"],['brg_mac', f"0x{self.brg_mac:X} ({self.brg_mac})"],['duty_cycle', f"0x{self.duty_cycle:X} ({self.duty_cycle})"],['pattern', f"0x{self.pattern:X} ({self.pattern})"],['output_power', f"0x{self.output_power:X} ({self.output_power})"],['signal_indicator_cycle', f"0x{self.signal_indicator_cycle:X} ({self.signal_indicator_cycle})"],['signal_indicator_rep', f"0x{self.signal_indicator_rep:X} ({self.signal_indicator_rep})"]], tablefmt="texttable")

    def __eq__(self, other):
        if other and set(other.__dict__.keys()) == set(self.__dict__.keys()):
            return (
                self.module_type == other.module_type and
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac and
                self.duty_cycle == other.duty_cycle and
                self.pattern == other.pattern and
                self.output_power == other.output_power and
                self.signal_indicator_cycle == other.signal_indicator_cycle and
                self.signal_indicator_rep == other.signal_indicator_rep
            )
        return False

    def dump(self):
        string = bitstruct.pack("u4u4u8u8u48u8u8s8u14u2u80", self.module_type, self.msg_type, self.api_version, self.seq_id, self.brg_mac, self.duty_cycle, self.pattern, self.output_power, self.signal_indicator_cycle, MODULE_ENERGY_2400_V11_SIGNAL_INDICATOR_REP_ENC[self.signal_indicator_rep], self.unused0)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u4u4u8u8u48u8u8s8u14u2u80", binascii.unhexlify(string))
        self.module_type = d[0]
        self.msg_type = d[1]
        self.api_version = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.duty_cycle = d[5]
        self.pattern = d[6]
        self.output_power = d[7]
        self.signal_indicator_cycle = d[8]
        self.signal_indicator_rep = MODULE_ENERGY_2400_V11_SIGNAL_INDICATOR_REP_DEC[d[9]]
        self.unused0 = d[10]

MODULE_ENERGY_SUB1G_V12_SIGNAL_INDICATOR_REP_ENC = {SIGNAL_INDICATOR_SUB1G_REP_1:SIGNAL_INDICATOR_SUB1G_REP_PROFILE_1, SIGNAL_INDICATOR_SUB1G_REP_2:SIGNAL_INDICATOR_SUB1G_REP_PROFILE_2, SIGNAL_INDICATOR_SUB1G_REP_3:SIGNAL_INDICATOR_SUB1G_REP_PROFILE_3, SIGNAL_INDICATOR_SUB1G_REP_4:SIGNAL_INDICATOR_SUB1G_REP_PROFILE_4}
MODULE_ENERGY_SUB1G_V12_SIGNAL_INDICATOR_REP_DEC = {SIGNAL_INDICATOR_SUB1G_REP_PROFILE_1:SIGNAL_INDICATOR_SUB1G_REP_1, SIGNAL_INDICATOR_SUB1G_REP_PROFILE_2:SIGNAL_INDICATOR_SUB1G_REP_2, SIGNAL_INDICATOR_SUB1G_REP_PROFILE_3:SIGNAL_INDICATOR_SUB1G_REP_3, SIGNAL_INDICATOR_SUB1G_REP_PROFILE_4:SIGNAL_INDICATOR_SUB1G_REP_4}
class ModuleEnergySub1GV12():
    def __init__(self, raw='', module_type=MODULE_ENERGY_SUB1G, msg_type=BRG_MGMT_MSG_TYPE_CFG_SET, api_version=API_VERSION_V12, seq_id=0, brg_mac=0, pattern=BRG_DEFAULT_SUB1G_ENERGY_PATTERN, duty_cycle=BRG_DEFAULT_SUB1G_DUTY_CYCLE, signal_indicator_cycle=BRG_DEFAULT_SIGNAL_INDICATOR_SUB1G_CYCLE, signal_indicator_rep=BRG_DEFAULT_SIGNAL_INDICATOR_SUB1G_REP, unused0=0):
        self.module_type = module_type
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.pattern = pattern
        self.duty_cycle = duty_cycle
        self.signal_indicator_cycle = signal_indicator_cycle
        self.signal_indicator_rep = signal_indicator_rep
        self.unused0 = unused0
        if raw:
            self.set(raw)

    def __repr__(self) -> str:
        return "\n==> Packet module_energy_sub1g_v12 <==\n" + tabulate.tabulate([['module_type', f"0x{self.module_type:X} ({self.module_type})"],['msg_type', f"0x{self.msg_type:X} ({self.msg_type})"],['api_version', f"0x{self.api_version:X} ({self.api_version})"],['seq_id', f"0x{self.seq_id:X} ({self.seq_id})"],['brg_mac', f"0x{self.brg_mac:X} ({self.brg_mac})"],['pattern', f"0x{self.pattern:X} ({self.pattern})"],['duty_cycle', f"0x{self.duty_cycle:X} ({self.duty_cycle})"],['signal_indicator_cycle', f"0x{self.signal_indicator_cycle:X} ({self.signal_indicator_cycle})"],['signal_indicator_rep', f"0x{self.signal_indicator_rep:X} ({self.signal_indicator_rep})"]], tablefmt="texttable")

    def __eq__(self, other):
        if other and set(other.__dict__.keys()) == set(self.__dict__.keys()):
            return (
                self.module_type == other.module_type and
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac and
                self.pattern == other.pattern and
                self.duty_cycle == other.duty_cycle and
                self.signal_indicator_cycle == other.signal_indicator_cycle and
                self.signal_indicator_rep == other.signal_indicator_rep
            )
        return False

    def dump(self):
        string = bitstruct.pack("u4u4u8u8u48u8u8u14u2u88", self.module_type, self.msg_type, self.api_version, self.seq_id, self.brg_mac, self.pattern, self.duty_cycle, self.signal_indicator_cycle, MODULE_ENERGY_SUB1G_V12_SIGNAL_INDICATOR_REP_ENC[self.signal_indicator_rep], self.unused0)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u4u4u8u8u48u8u8u14u2u88", binascii.unhexlify(string))
        self.module_type = d[0]
        self.msg_type = d[1]
        self.api_version = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.pattern = d[5]
        self.duty_cycle = d[6]
        self.signal_indicator_cycle = d[7]
        self.signal_indicator_rep = MODULE_ENERGY_SUB1G_V12_SIGNAL_INDICATOR_REP_DEC[d[8]]
        self.unused0 = d[9]

MODULE_ENERGY_SUB1G_V11_OUTPUT_POWER_ENC = {SUB1G_OUTPUT_POWER_14:SUB1G_OUTPUT_POWER_PROFILE_14, SUB1G_OUTPUT_POWER_17:SUB1G_OUTPUT_POWER_PROFILE_17, SUB1G_OUTPUT_POWER_20:SUB1G_OUTPUT_POWER_PROFILE_20, SUB1G_OUTPUT_POWER_23:SUB1G_OUTPUT_POWER_PROFILE_23, SUB1G_OUTPUT_POWER_26:SUB1G_OUTPUT_POWER_PROFILE_26, SUB1G_OUTPUT_POWER_29:SUB1G_OUTPUT_POWER_PROFILE_29, SUB1G_OUTPUT_POWER_32:SUB1G_OUTPUT_POWER_PROFILE_32}
MODULE_ENERGY_SUB1G_V11_OUTPUT_POWER_DEC = {SUB1G_OUTPUT_POWER_PROFILE_14:SUB1G_OUTPUT_POWER_14, SUB1G_OUTPUT_POWER_PROFILE_17:SUB1G_OUTPUT_POWER_17, SUB1G_OUTPUT_POWER_PROFILE_20:SUB1G_OUTPUT_POWER_20, SUB1G_OUTPUT_POWER_PROFILE_23:SUB1G_OUTPUT_POWER_23, SUB1G_OUTPUT_POWER_PROFILE_26:SUB1G_OUTPUT_POWER_26, SUB1G_OUTPUT_POWER_PROFILE_29:SUB1G_OUTPUT_POWER_29, SUB1G_OUTPUT_POWER_PROFILE_32:SUB1G_OUTPUT_POWER_32}
MODULE_ENERGY_SUB1G_V11_SIGNAL_INDICATOR_REP_ENC = {SIGNAL_INDICATOR_SUB1G_REP_1:SIGNAL_INDICATOR_SUB1G_REP_PROFILE_1, SIGNAL_INDICATOR_SUB1G_REP_2:SIGNAL_INDICATOR_SUB1G_REP_PROFILE_2, SIGNAL_INDICATOR_SUB1G_REP_3:SIGNAL_INDICATOR_SUB1G_REP_PROFILE_3, SIGNAL_INDICATOR_SUB1G_REP_4:SIGNAL_INDICATOR_SUB1G_REP_PROFILE_4}
MODULE_ENERGY_SUB1G_V11_SIGNAL_INDICATOR_REP_DEC = {SIGNAL_INDICATOR_SUB1G_REP_PROFILE_1:SIGNAL_INDICATOR_SUB1G_REP_1, SIGNAL_INDICATOR_SUB1G_REP_PROFILE_2:SIGNAL_INDICATOR_SUB1G_REP_2, SIGNAL_INDICATOR_SUB1G_REP_PROFILE_3:SIGNAL_INDICATOR_SUB1G_REP_3, SIGNAL_INDICATOR_SUB1G_REP_PROFILE_4:SIGNAL_INDICATOR_SUB1G_REP_4}
class ModuleEnergySub1GV11():
    def __init__(self, raw='', module_type=MODULE_ENERGY_SUB1G, msg_type=BRG_MGMT_MSG_TYPE_CFG_SET, api_version=API_VERSION_V11, seq_id=0, brg_mac=0, output_power=BRG_DEFAULT_OUTPUT_POWER_SUB1G, sub1g_energy_pattern=BRG_DEFAULT_SUB1G_ENERGY_PATTERN, cycle=15, duty_cycle=BRG_DEFAULT_SUB1G_DUTY_CYCLE, signal_indicator_cycle=BRG_DEFAULT_SIGNAL_INDICATOR_SUB1G_CYCLE, signal_indicator_rep=BRG_DEFAULT_SIGNAL_INDICATOR_SUB1G_REP, unused0=0):
        self.module_type = module_type
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.output_power = output_power
        self.sub1g_energy_pattern = sub1g_energy_pattern
        self.cycle = cycle
        self.duty_cycle = duty_cycle
        self.signal_indicator_cycle = signal_indicator_cycle
        self.signal_indicator_rep = signal_indicator_rep
        self.unused0 = unused0
        if raw:
            self.set(raw)

    def __repr__(self) -> str:
        return "\n==> Packet module_energy_sub1g_v11 <==\n" + tabulate.tabulate([['module_type', f"0x{self.module_type:X} ({self.module_type})"],['msg_type', f"0x{self.msg_type:X} ({self.msg_type})"],['api_version', f"0x{self.api_version:X} ({self.api_version})"],['seq_id', f"0x{self.seq_id:X} ({self.seq_id})"],['brg_mac', f"0x{self.brg_mac:X} ({self.brg_mac})"],['output_power', f"0x{self.output_power:X} ({self.output_power})"],['sub1g_energy_pattern', f"0x{self.sub1g_energy_pattern:X} ({self.sub1g_energy_pattern})"],['cycle', f"0x{self.cycle:X} ({self.cycle})"],['duty_cycle', f"0x{self.duty_cycle:X} ({self.duty_cycle})"],['signal_indicator_cycle', f"0x{self.signal_indicator_cycle:X} ({self.signal_indicator_cycle})"],['signal_indicator_rep', f"0x{self.signal_indicator_rep:X} ({self.signal_indicator_rep})"]], tablefmt="texttable")

    def __eq__(self, other):
        if other and set(other.__dict__.keys()) == set(self.__dict__.keys()):
            return (
                self.module_type == other.module_type and
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac and
                self.output_power == other.output_power and
                self.sub1g_energy_pattern == other.sub1g_energy_pattern and
                self.cycle == other.cycle and
                self.duty_cycle == other.duty_cycle and
                self.signal_indicator_cycle == other.signal_indicator_cycle and
                self.signal_indicator_rep == other.signal_indicator_rep
            )
        return False

    def dump(self):
        string = bitstruct.pack("u4u4u8u8u48u8u8u8u8u14u2u72", self.module_type, self.msg_type, self.api_version, self.seq_id, self.brg_mac, MODULE_ENERGY_SUB1G_V11_OUTPUT_POWER_ENC[self.output_power], self.sub1g_energy_pattern, self.cycle, self.duty_cycle, self.signal_indicator_cycle, MODULE_ENERGY_SUB1G_V11_SIGNAL_INDICATOR_REP_ENC[self.signal_indicator_rep], self.unused0)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u4u4u8u8u48u8u8u8u8u14u2u72", binascii.unhexlify(string))
        self.module_type = d[0]
        self.msg_type = d[1]
        self.api_version = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.output_power = MODULE_ENERGY_SUB1G_V11_OUTPUT_POWER_DEC[d[5]]
        self.sub1g_energy_pattern = d[6]
        self.cycle = d[7]
        self.duty_cycle = d[8]
        self.signal_indicator_cycle = d[9]
        self.signal_indicator_rep = MODULE_ENERGY_SUB1G_V11_SIGNAL_INDICATOR_REP_DEC[d[10]]
        self.unused0 = d[11]

class ModulePwrMgmtV12():
    def __init__(self, raw='', module_type=MODULE_PWR_MGMT, msg_type=BRG_MGMT_MSG_TYPE_CFG_SET, api_version=API_VERSION_V12, seq_id=0, brg_mac=0, static_leds_on=PWR_MGMT_DEFAULTS_LEDS_ON, static_keep_alive_period=PWR_MGMT_DEFAULTS_KEEP_ALIVE_PERIOD, static_keep_alive_scan=PWR_MGMT_DEFAULTS_KEEP_ALIVE_SCAN, static_on_duration=PWR_MGMT_DEFAULTS_ON_DURATION, static_sleep_duration=PWR_MGMT_DEFAULTS_SLEEP_DURATION, dynamic_leds_on=PWR_MGMT_DEFAULTS_LEDS_ON, dynamic_keep_alive_period=PWR_MGMT_DEFAULTS_KEEP_ALIVE_PERIOD, dynamic_keep_alive_scan=PWR_MGMT_DEFAULTS_KEEP_ALIVE_SCAN, dynamic_on_duration=PWR_MGMT_DEFAULTS_ON_DURATION, dynamic_sleep_duration=PWR_MGMT_DEFAULTS_SLEEP_DURATION, unused0=0):
        self.module_type = module_type
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.static_leds_on = static_leds_on
        self.static_keep_alive_period = static_keep_alive_period # 5sec resolution
        self.static_keep_alive_scan = static_keep_alive_scan # 10msec resolution
        self.static_on_duration = static_on_duration # 30sec resolution
        self.static_sleep_duration = static_sleep_duration # 60sec resolution
        self.dynamic_leds_on = dynamic_leds_on
        self.dynamic_keep_alive_period = dynamic_keep_alive_period # 5sec resolution
        self.dynamic_keep_alive_scan = dynamic_keep_alive_scan # 10msec resolution
        self.dynamic_on_duration = dynamic_on_duration # 30sec resolution
        self.dynamic_sleep_duration = dynamic_sleep_duration # 60sec resolution
        self.unused0 = unused0
        if raw:
            self.set(raw)

    def __repr__(self) -> str:
        return "\n==> Packet module_pwr_mgmt_v12 <==\n" + tabulate.tabulate([['module_type', f"0x{self.module_type:X} ({self.module_type})"],['msg_type', f"0x{self.msg_type:X} ({self.msg_type})"],['api_version', f"0x{self.api_version:X} ({self.api_version})"],['seq_id', f"0x{self.seq_id:X} ({self.seq_id})"],['brg_mac', f"0x{self.brg_mac:X} ({self.brg_mac})"],['static_leds_on', f"0x{self.static_leds_on:X} ({self.static_leds_on})"],['static_keep_alive_period', f"0x{self.static_keep_alive_period:X} ({self.static_keep_alive_period})"],['static_keep_alive_scan', f"0x{self.static_keep_alive_scan:X} ({self.static_keep_alive_scan})"],['static_on_duration', f"0x{self.static_on_duration:X} ({self.static_on_duration})"],['static_sleep_duration', f"0x{self.static_sleep_duration:X} ({self.static_sleep_duration})"],['dynamic_leds_on', f"0x{self.dynamic_leds_on:X} ({self.dynamic_leds_on})"],['dynamic_keep_alive_period', f"0x{self.dynamic_keep_alive_period:X} ({self.dynamic_keep_alive_period})"],['dynamic_keep_alive_scan', f"0x{self.dynamic_keep_alive_scan:X} ({self.dynamic_keep_alive_scan})"],['dynamic_on_duration', f"0x{self.dynamic_on_duration:X} ({self.dynamic_on_duration})"],['dynamic_sleep_duration', f"0x{self.dynamic_sleep_duration:X} ({self.dynamic_sleep_duration})"]], tablefmt="texttable")

    def __eq__(self, other):
        if other and set(other.__dict__.keys()) == set(self.__dict__.keys()):
            return (
                self.module_type == other.module_type and
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac and
                self.static_leds_on == other.static_leds_on and
                self.static_keep_alive_period == other.static_keep_alive_period and
                self.static_keep_alive_scan == other.static_keep_alive_scan and
                self.static_on_duration == other.static_on_duration and
                self.static_sleep_duration == other.static_sleep_duration and
                self.dynamic_leds_on == other.dynamic_leds_on and
                self.dynamic_keep_alive_period == other.dynamic_keep_alive_period and
                self.dynamic_keep_alive_scan == other.dynamic_keep_alive_scan and
                self.dynamic_on_duration == other.dynamic_on_duration and
                self.dynamic_sleep_duration == other.dynamic_sleep_duration
            )
        return False

    def dump(self):
        string = bitstruct.pack("u4u4u8u8u48u8u8u8u8u16u8u8u8u8u16u24", self.module_type, self.msg_type, self.api_version, self.seq_id, self.brg_mac, self.static_leds_on, ((self.static_keep_alive_period-0)//5), ((self.static_keep_alive_scan-0)//10), ((self.static_on_duration-0)//30), ((self.static_sleep_duration-0)//60), self.dynamic_leds_on, ((self.dynamic_keep_alive_period-0)//5), ((self.dynamic_keep_alive_scan-0)//10), ((self.dynamic_on_duration-0)//30), ((self.dynamic_sleep_duration-0)//60), self.unused0)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u4u4u8u8u48u8u8u8u8u16u8u8u8u8u16u24", binascii.unhexlify(string))
        self.module_type = d[0]
        self.msg_type = d[1]
        self.api_version = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.static_leds_on = d[5]
        self.static_keep_alive_period = ((d[6]*5)+0)
        self.static_keep_alive_scan = ((d[7]*10)+0)
        self.static_on_duration = ((d[8]*30)+0)
        self.static_sleep_duration = ((d[9]*60)+0)
        self.dynamic_leds_on = d[10]
        self.dynamic_keep_alive_period = ((d[11]*5)+0)
        self.dynamic_keep_alive_scan = ((d[12]*10)+0)
        self.dynamic_on_duration = ((d[13]*30)+0)
        self.dynamic_sleep_duration = ((d[14]*60)+0)
        self.unused0 = d[15]

class ModulePwrMgmtV11():
    def __init__(self, raw='', module_type=MODULE_PWR_MGMT, msg_type=BRG_MGMT_MSG_TYPE_CFG_SET, api_version=API_VERSION_V11, seq_id=0, brg_mac=0, static_leds_on=PWR_MGMT_DEFAULTS_LEDS_ON, static_keep_alive_period=PWR_MGMT_DEFAULTS_KEEP_ALIVE_PERIOD, static_keep_alive_scan=PWR_MGMT_DEFAULTS_KEEP_ALIVE_SCAN, static_on_duration=PWR_MGMT_DEFAULTS_ON_DURATION, static_sleep_duration=PWR_MGMT_DEFAULTS_SLEEP_DURATION, dynamic_leds_on=PWR_MGMT_DEFAULTS_LEDS_ON, dynamic_keep_alive_period=PWR_MGMT_DEFAULTS_KEEP_ALIVE_PERIOD, dynamic_keep_alive_scan=PWR_MGMT_DEFAULTS_KEEP_ALIVE_SCAN, dynamic_on_duration=PWR_MGMT_DEFAULTS_ON_DURATION, dynamic_sleep_duration=PWR_MGMT_DEFAULTS_SLEEP_DURATION, unused0=0):
        self.module_type = module_type
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.static_leds_on = static_leds_on
        self.static_keep_alive_period = static_keep_alive_period # 5sec resolution
        self.static_keep_alive_scan = static_keep_alive_scan # 10msec resolution
        self.static_on_duration = static_on_duration # 30sec resolution
        self.static_sleep_duration = static_sleep_duration # 60sec resolution
        self.dynamic_leds_on = dynamic_leds_on
        self.dynamic_keep_alive_period = dynamic_keep_alive_period # 5sec resolution
        self.dynamic_keep_alive_scan = dynamic_keep_alive_scan # 10msec resolution
        self.dynamic_on_duration = dynamic_on_duration # 30sec resolution
        self.dynamic_sleep_duration = dynamic_sleep_duration # 60sec resolution
        self.unused0 = unused0
        if raw:
            self.set(raw)

    def __repr__(self) -> str:
        return "\n==> Packet module_pwr_mgmt_v11 <==\n" + tabulate.tabulate([['module_type', f"0x{self.module_type:X} ({self.module_type})"],['msg_type', f"0x{self.msg_type:X} ({self.msg_type})"],['api_version', f"0x{self.api_version:X} ({self.api_version})"],['seq_id', f"0x{self.seq_id:X} ({self.seq_id})"],['brg_mac', f"0x{self.brg_mac:X} ({self.brg_mac})"],['static_leds_on', f"0x{self.static_leds_on:X} ({self.static_leds_on})"],['static_keep_alive_period', f"0x{self.static_keep_alive_period:X} ({self.static_keep_alive_period})"],['static_keep_alive_scan', f"0x{self.static_keep_alive_scan:X} ({self.static_keep_alive_scan})"],['static_on_duration', f"0x{self.static_on_duration:X} ({self.static_on_duration})"],['static_sleep_duration', f"0x{self.static_sleep_duration:X} ({self.static_sleep_duration})"],['dynamic_leds_on', f"0x{self.dynamic_leds_on:X} ({self.dynamic_leds_on})"],['dynamic_keep_alive_period', f"0x{self.dynamic_keep_alive_period:X} ({self.dynamic_keep_alive_period})"],['dynamic_keep_alive_scan', f"0x{self.dynamic_keep_alive_scan:X} ({self.dynamic_keep_alive_scan})"],['dynamic_on_duration', f"0x{self.dynamic_on_duration:X} ({self.dynamic_on_duration})"],['dynamic_sleep_duration', f"0x{self.dynamic_sleep_duration:X} ({self.dynamic_sleep_duration})"]], tablefmt="texttable")

    def __eq__(self, other):
        if other and set(other.__dict__.keys()) == set(self.__dict__.keys()):
            return (
                self.module_type == other.module_type and
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac and
                self.static_leds_on == other.static_leds_on and
                self.static_keep_alive_period == other.static_keep_alive_period and
                self.static_keep_alive_scan == other.static_keep_alive_scan and
                self.static_on_duration == other.static_on_duration and
                self.static_sleep_duration == other.static_sleep_duration and
                self.dynamic_leds_on == other.dynamic_leds_on and
                self.dynamic_keep_alive_period == other.dynamic_keep_alive_period and
                self.dynamic_keep_alive_scan == other.dynamic_keep_alive_scan and
                self.dynamic_on_duration == other.dynamic_on_duration and
                self.dynamic_sleep_duration == other.dynamic_sleep_duration
            )
        return False

    def dump(self):
        string = bitstruct.pack("u4u4u8u8u48u8u8u8u8u16u8u8u8u8u16u24", self.module_type, self.msg_type, self.api_version, self.seq_id, self.brg_mac, self.static_leds_on, ((self.static_keep_alive_period-0)//5), ((self.static_keep_alive_scan-0)//10), ((self.static_on_duration-0)//30), ((self.static_sleep_duration-0)//60), self.dynamic_leds_on, ((self.dynamic_keep_alive_period-0)//5), ((self.dynamic_keep_alive_scan-0)//10), ((self.dynamic_on_duration-0)//30), ((self.dynamic_sleep_duration-0)//60), self.unused0)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u4u4u8u8u48u8u8u8u8u16u8u8u8u8u16u24", binascii.unhexlify(string))
        self.module_type = d[0]
        self.msg_type = d[1]
        self.api_version = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.static_leds_on = d[5]
        self.static_keep_alive_period = ((d[6]*5)+0)
        self.static_keep_alive_scan = ((d[7]*10)+0)
        self.static_on_duration = ((d[8]*30)+0)
        self.static_sleep_duration = ((d[9]*60)+0)
        self.dynamic_leds_on = d[10]
        self.dynamic_keep_alive_period = ((d[11]*5)+0)
        self.dynamic_keep_alive_scan = ((d[12]*10)+0)
        self.dynamic_on_duration = ((d[13]*30)+0)
        self.dynamic_sleep_duration = ((d[14]*60)+0)
        self.unused0 = d[15]

class ModuleExtSensorsV12():
    def __init__(self, raw='', module_type=MODULE_EXT_SENSORS, msg_type=BRG_MGMT_MSG_TYPE_CFG_SET, api_version=API_VERSION_V12, seq_id=0, brg_mac=0, sensor0=BRG_DEFAULT_EXTERNAL_SENSOR_CFG, sensor1=BRG_DEFAULT_EXTERNAL_SENSOR_CFG, rssi_threshold=BRG_DEFAULT_RSSI_THRESHOLD, sub1g_rssi_threshold=BRG_DEFAULT_RSSI_THRESHOLD, unused=0):
        self.module_type = module_type
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.sensor0 = sensor0
        self.sensor1 = sensor1
        self.rssi_threshold = rssi_threshold
        self.sub1g_rssi_threshold = sub1g_rssi_threshold
        self.unused = unused
        if raw:
            self.set(raw)

    def __repr__(self) -> str:
        return "\n==> Packet module_ext_sensors_v12 <==\n" + tabulate.tabulate([['module_type', f"0x{self.module_type:X} ({self.module_type})"],['msg_type', f"0x{self.msg_type:X} ({self.msg_type})"],['api_version', f"0x{self.api_version:X} ({self.api_version})"],['seq_id', f"0x{self.seq_id:X} ({self.seq_id})"],['brg_mac', f"0x{self.brg_mac:X} ({self.brg_mac})"],['sensor0', f"0x{self.sensor0:X} ({self.sensor0})"],['sensor1', f"0x{self.sensor1:X} ({self.sensor1})"],['rssi_threshold', f"0x{self.rssi_threshold:X} ({self.rssi_threshold})"],['sub1g_rssi_threshold', f"0x{self.sub1g_rssi_threshold:X} ({self.sub1g_rssi_threshold})"]], tablefmt="texttable")

    def __eq__(self, other):
        if other and set(other.__dict__.keys()) == set(self.__dict__.keys()):
            return (
                self.module_type == other.module_type and
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac and
                self.sensor0 == other.sensor0 and
                self.sensor1 == other.sensor1 and
                self.rssi_threshold == other.rssi_threshold and
                self.sub1g_rssi_threshold == other.sub1g_rssi_threshold
            )
        return False

    def dump(self):
        string = bitstruct.pack("u4u4u8u8u48u32u32s8s8u40", self.module_type, self.msg_type, self.api_version, self.seq_id, self.brg_mac, self.sensor0, self.sensor1, ((self.rssi_threshold-0)//-1), ((self.sub1g_rssi_threshold-0)//-1), self.unused)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u4u4u8u8u48u32u32s8s8u40", binascii.unhexlify(string))
        self.module_type = d[0]
        self.msg_type = d[1]
        self.api_version = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.sensor0 = d[5]
        self.sensor1 = d[6]
        self.rssi_threshold = ((d[7]*-1)+0)
        self.sub1g_rssi_threshold = ((d[8]*-1)+0)
        self.unused = d[9]

class ModuleExtSensorsV11():
    def __init__(self, raw='', module_type=MODULE_EXT_SENSORS, msg_type=BRG_MGMT_MSG_TYPE_CFG_SET, api_version=API_VERSION_V11, seq_id=0, brg_mac=0, sensor0=BRG_DEFAULT_EXTERNAL_SENSOR_CFG, sensor1=BRG_DEFAULT_EXTERNAL_SENSOR_CFG, unused=0):
        self.module_type = module_type
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.sensor0 = sensor0
        self.sensor1 = sensor1
        self.unused = unused
        if raw:
            self.set(raw)

    def __repr__(self) -> str:
        return "\n==> Packet module_ext_sensors_v11 <==\n" + tabulate.tabulate([['module_type', f"0x{self.module_type:X} ({self.module_type})"],['msg_type', f"0x{self.msg_type:X} ({self.msg_type})"],['api_version', f"0x{self.api_version:X} ({self.api_version})"],['seq_id', f"0x{self.seq_id:X} ({self.seq_id})"],['brg_mac', f"0x{self.brg_mac:X} ({self.brg_mac})"],['sensor0', f"0x{self.sensor0:X} ({self.sensor0})"],['sensor1', f"0x{self.sensor1:X} ({self.sensor1})"]], tablefmt="texttable")

    def __eq__(self, other):
        if other and set(other.__dict__.keys()) == set(self.__dict__.keys()):
            return (
                self.module_type == other.module_type and
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac and
                self.sensor0 == other.sensor0 and
                self.sensor1 == other.sensor1
            )
        return False

    def dump(self):
        string = bitstruct.pack("u4u4u8u8u48u32u32u56", self.module_type, self.msg_type, self.api_version, self.seq_id, self.brg_mac, self.sensor0, self.sensor1, self.unused)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u4u4u8u8u48u32u32u56", binascii.unhexlify(string))
        self.module_type = d[0]
        self.msg_type = d[1]
        self.api_version = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.sensor0 = d[5]
        self.sensor1 = d[6]
        self.unused = d[7]

class ModuleCustomV12():
    def __init__(self, raw='', module_type=MODULE_CUSTOM, msg_type=BRG_MGMT_MSG_TYPE_CFG_SET, api_version=API_VERSION_V12, seq_id=0, brg_mac=0, motion_sensitivity_threshold=LIS2DW12_DEFAULTS_STATE_THRESHOLD, s2d_transition_time=LIS2DW12_DEFAULTS_WAKE_UP_DURATION, d2s_transition_time=LIS2DW12_DEFAULTS_SLEEP_DURATION, unused1=0):
        self.module_type = module_type
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.motion_sensitivity_threshold = motion_sensitivity_threshold # 31 [mg] resolution
        self.s2d_transition_time = s2d_transition_time # 3 [sec] resolution
        self.d2s_transition_time = d2s_transition_time # 5 [sec] resolution
        self.unused1 = unused1
        if raw:
            self.set(raw)

    def __repr__(self) -> str:
        return "\n==> Packet module_custom_v12 <==\n" + tabulate.tabulate([['module_type', f"0x{self.module_type:X} ({self.module_type})"],['msg_type', f"0x{self.msg_type:X} ({self.msg_type})"],['api_version', f"0x{self.api_version:X} ({self.api_version})"],['seq_id', f"0x{self.seq_id:X} ({self.seq_id})"],['brg_mac', f"0x{self.brg_mac:X} ({self.brg_mac})"],['motion_sensitivity_threshold', f"0x{self.motion_sensitivity_threshold:X} ({self.motion_sensitivity_threshold})"],['s2d_transition_time', f"0x{self.s2d_transition_time:X} ({self.s2d_transition_time})"],['d2s_transition_time', f"0x{self.d2s_transition_time:X} ({self.d2s_transition_time})"]], tablefmt="texttable")

    def __eq__(self, other):
        if other and set(other.__dict__.keys()) == set(self.__dict__.keys()):
            return (
                self.module_type == other.module_type and
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac and
                self.motion_sensitivity_threshold == other.motion_sensitivity_threshold and
                self.s2d_transition_time == other.s2d_transition_time and
                self.d2s_transition_time == other.d2s_transition_time
            )
        return False

    def dump(self):
        string = bitstruct.pack("u4u4u8u8u48u8u8u8u96", self.module_type, self.msg_type, self.api_version, self.seq_id, self.brg_mac, ((self.motion_sensitivity_threshold-0)//31), ((self.s2d_transition_time-0)//3), ((self.d2s_transition_time-0)//5), self.unused1)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u4u4u8u8u48u8u8u8u96", binascii.unhexlify(string))
        self.module_type = d[0]
        self.msg_type = d[1]
        self.api_version = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.motion_sensitivity_threshold = ((d[5]*31)+0)
        self.s2d_transition_time = ((d[6]*3)+0)
        self.d2s_transition_time = ((d[7]*5)+0)
        self.unused1 = d[8]

class ModuleCustomV11():
    def __init__(self, raw='', module_type=MODULE_CUSTOM, msg_type=BRG_MGMT_MSG_TYPE_CFG_SET, api_version=API_VERSION_V11, seq_id=0, brg_mac=0, state_threshold=LIS2DW12_DEFAULTS_STATE_THRESHOLD, wake_up_duration=LIS2DW12_DEFAULTS_WAKE_UP_DURATION, sleep_duration=LIS2DW12_DEFAULTS_SLEEP_DURATION, unused1=0):
        self.module_type = module_type
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.state_threshold = state_threshold # 31 [mg] resolution
        self.wake_up_duration = wake_up_duration # 3 [sec] resolution
        self.sleep_duration = sleep_duration # 5 [sec] resolution
        self.unused1 = unused1
        if raw:
            self.set(raw)

    def __repr__(self) -> str:
        return "\n==> Packet module_custom_v11 <==\n" + tabulate.tabulate([['module_type', f"0x{self.module_type:X} ({self.module_type})"],['msg_type', f"0x{self.msg_type:X} ({self.msg_type})"],['api_version', f"0x{self.api_version:X} ({self.api_version})"],['seq_id', f"0x{self.seq_id:X} ({self.seq_id})"],['brg_mac', f"0x{self.brg_mac:X} ({self.brg_mac})"],['state_threshold', f"0x{self.state_threshold:X} ({self.state_threshold})"],['wake_up_duration', f"0x{self.wake_up_duration:X} ({self.wake_up_duration})"],['sleep_duration', f"0x{self.sleep_duration:X} ({self.sleep_duration})"]], tablefmt="texttable")

    def __eq__(self, other):
        if other and set(other.__dict__.keys()) == set(self.__dict__.keys()):
            return (
                self.module_type == other.module_type and
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac and
                self.state_threshold == other.state_threshold and
                self.wake_up_duration == other.wake_up_duration and
                self.sleep_duration == other.sleep_duration
            )
        return False

    def dump(self):
        string = bitstruct.pack("u4u4u8u8u48u8u8u8u96", self.module_type, self.msg_type, self.api_version, self.seq_id, self.brg_mac, ((self.state_threshold-0)//31), ((self.wake_up_duration-0)//3), ((self.sleep_duration-0)//5), self.unused1)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u4u4u8u8u48u8u8u8u96", binascii.unhexlify(string))
        self.module_type = d[0]
        self.msg_type = d[1]
        self.api_version = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.state_threshold = ((d[5]*31)+0)
        self.wake_up_duration = ((d[6]*3)+0)
        self.sleep_duration = ((d[7]*5)+0)
        self.unused1 = d[8]

