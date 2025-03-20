# Files
import os
import importlib.metadata
# BASE_DIR should be initiated in the same dir as brg_certificate.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# CERT_VERSION handling - local/PyPi
if "wiliot-certificate" in importlib.metadata.packages_distributions():
    CERT_VERSION = importlib.metadata.version("wiliot-certificate")
else:
    CERT_VERSION = "local-dev"
CERT_MQTT_LOG_FILE =            "cert_mqtt_log.json"
DATA_SIM_LOG_FILE =             "data_sim_log.txt"
UT_RESULT_FILE_HTML =           "results.html"
UT_RESULT_FILE_PDF =            "results.pdf"
UT_RESULT_FILE =                "results.html"
UTILS_BASE_REL_PATH = "../../../utils"

# GW defines
GW_ID =                         "gatewayId"
ADDITIONAL =                    "additional"
REPORTED_CONF =                 "reportedConf"
GW_CONF =                       "gatewayConf"
GW_NAME =                       "gatewayName"
GW_API_VERSION =                "apiVersion"
LAT =                           "lat"
LNG =                           "lng"
WLT_SERVER =                    "wiliotServer"
PACER_INTERVAL =                "pacerInterval"
PKT_TYPES_MASK =                "packetTypesMask"
RX_TX_PERIOD =                  "rxTxPeriodMs"
TX_PERIOD =                     "txPeriodMs"
OUTPUT_POWER_2_4 =              "2.4GhzOutputPower"
NFPKT =                         "nfpkt"
TBC =                           "tbc"
RSSI =                          "rssi"
SRC_ID =                        "src_id"

INTERNAL_BRG_RSSI =             1
BRIDGE_ID =                     "bridgeId"
ALIAS_BRIDGE_ID =               "aliasBridgeId"
GROUP_ID =                      "group_id"
BRG_ACTION =                    "bridgeAction"

GW_DATA_MODE =                  "gwDataMode"
TAGS_AND_BRGS =                 "Tags & Bridges"
TAGS_ONLY =                     "Tags only"
BRGS_ONLY_37 =                  "Bridges only (ch37)"
BRGS_ONLY_38 =                  "Bridges only (ch38)"
BRGS_ONLY_39 =                  "Bridges only (ch39)"
HIBERNATE =                     "Hibernate"

BLE_WIFI =                      "ble_wifi"
BLE_LAN =                       "ble_lan"

WLT_SERVER =                    "wiliotServer"
PACER_INTERVAL =                "pacerInterval"
OUTPUT_POWER_2_4 =              "2.4GhzOutputPower"
USE_STAT_LOC =                  "useStaticLocation"
GW_ENERGY_PATTERN =             "energizingPattern"
VERSION =                       "version"
WIFI_VERSION =                  "interfaceChipSwVersion"
BLE_VERSION =                   "bleChipSwVersion"
BLE_MAC_ADDR =                  "bleChipMacAddress"
GW_MODE =                       "gwMode"
PROD =                          "prod"
SERIALIZATION_FORMAT =          "serializationFormat"
PROTOBUF =                      "Protobuf"
JSON =                          "JSON"
ACL =                           "accessControlList"
ACL_MODE =                      "mode"
ACL_MODE_ALLOW =                "mode_allow"
ACL_BRIDGE_IDS =                "bridgeIds"
ACL_IDS =                       "ids"
ACL_DENY =                      "deny"
ACL_ALLOW =                     "allow"
ACL_DENY_VALUE =                 0
ACL_ALLOW_VALUE =                1

GET_INFO_ACTION =               "getGwInfo"
REBOOT_GW_ACTION =              "rebootGw"
LOG_PERIOD_ACTION =             "LogPeriodSet"
GET_LOGS =                      "getLogs"
GW_INFO =                       "gatewayInfo"
GW_LOGS =                       "gatewayLogs"
LOGS =                          "logs"
GW_LATITUDE =                   "Latitude"
GW_LONGITUDE =                  "Longitude"
GW_LOG_PERIOD =                 30

# Thin gw defines
THIN_GW_PROTOCOL_VERSION =      "protocolVersion"
TX_PKT =                        "txPacket"
TX_MAX_DURATION_MS =            "txMaxDurationMs"
TX_MAX_RETRIES =                "txMaxRetries"
TRANPARENT_PKT_LEN =            31 * 2

# Simulator defines
GW_SIM_BLE_MAC_ADDRESS =       'GW_SIM_BLE_MAC_ADDRESS'
GW_APP_VERSION_HEADER =        'WILIOT_GW_BLE_CHIP_SW_VER'
GW_SIM_PREFIX =                'SIM'
DATA_SIMULATION =              'sim'
DATA_REAL_TAGS =               'tags'
GEN2 =                         2
GEN3 =                         3
GEN3_EXTENDED =                4

# Configurable brg fields' names by modules
# common #
BRG_OUTPUT_POWER =              "output_power"
BRG_PATTERN =                   "pattern"
BRG_DUTY_CYCLE =                "duty_cycle"
BRG_SIGNAL_INDICATOR_CYCLE =    "signal_indicator_cycle"
BRG_SIGNAL_INDICATOR_REP =      "signal_indicator_rep"
# Datapath #
BRG_UNIFIED_ECHO_PKT =          "unified_echo_pkt"
BRG_ADAPTIVE_PACER =            "adaptive_pacer"
BRG_PACER_INTERVAL =            "pacer_interval"
BRG_RSSI_THRESHOLD =            "rssi_threshold"
BRG_SUB1G_RSSI_THRESHOLD =      "sub1g_rssi_threshold"
BRG_TX_REPETITION =             "tx_repetition"
BRG_PKT_FILTER =                "pkt_filter"
BRG_RX_CHANNEL =                "rx_channel"
# Calibration #
BRG_CALIB_INTERVAL =            "interval"
# Energy Sub1g #
BRG_CYCLE =                     "cycle"
# 3rd party sensors #
BRG_SENSOR0 =                   "sensor0"
BRG_SENSOR1 =                   "sensor1"

# Common defines
PACKETS =                       "packets"
TIMESTAMP =                     "timestamp"
ACTION =                        "action"
ACTION_STATUS =                 "actionStatus" # Protobuf
PAYLOAD =                       "payload"
SEQUENCE_ID =                   "sequenceId"
MODULE_IF =                     "module IF"
HB =                            "HB"
DATETIME =                      "datetime"
TIME =                          "time"
TIMESTAMP_DELTA =               "timestamp_delta"
TAGS_COUNT =                    "tags_count"
NEW_TAGS =                      "new_tags"
TTFP =                          "ttfp"

# Protobuf related
ENTRIES =                       "entries"
STR_VAL =                       "stringValue"
NUM_VAL =                       "numberValue"
GW_STATUS =                     "gatewayStatus"
BRG_UPGRADE =                   "bridgeUpgrade"
REBOOT_PKT =                    "rebootPacket"
CONFIG =                        "config"
ACL_VALUE =                     "aclValue"

# Custom broker
CUSTOM_BROKER_ENABLE       = "customBroker"
CUSTOM_BROKER_PORT         = "port"
CUSTOM_BROKER_BROKER_URL   = "brokerUrl"
CUSTOM_BROKER_USERNAME     = "username"
CUSTOM_BROKER_PASSWORD     = "password"
CUSTOM_BROKER_UPDATE_TOPIC = "updateTopic"
CUSTOM_BROKER_STATUS_TOPIC = "statusTopic"
CUSTOM_BROKER_DATA_TOPIC   = "dataTopic"

# External Sensors
IS_SENSOR =                      "isSensor"
IS_EMBEDDED =                    "isEmbedded"
IS_SCRAMBLED =                   "isScrambled"
SENSOR_UUID =                    "sensorServiceId"
SENSOR_ID =                      "sensorId"
PKT_ID_CTR =                     "pkt_id_ctr"

# OTA
STATUS_CODE_STR =                "statusCode"
STATUS_CODE =                    "status" # Protobuf
IMG_DIR_URL =                    "imageDirUrl"
UPGRADE_BLSD =                   "upgradeBlSd"
VER_UUID_STR =                   "versionUUID"
VER_MAX_LEN =                    31

# Versions
VERSIONS = {
    "1.5.0" : {WIFI_VERSION: "3.5.32", BLE_VERSION: "3.7.25"},
    "1.5.2" : {WIFI_VERSION: "3.5.132", BLE_VERSION: "3.7.25"},
    "1.6.1" : {WIFI_VERSION: "3.5.51", BLE_VERSION: "3.8.18"},
    "1.7.0" : {WIFI_VERSION: "3.9.8", BLE_VERSION: "3.9.24"},
    "1.7.1" : {WIFI_VERSION: "3.10.6", BLE_VERSION: "3.10.13"},
    "1.8.0" : {WIFI_VERSION: "3.11.36", BLE_VERSION: "3.11.40"},
    "1.8.2" : {WIFI_VERSION: "3.11.36", BLE_VERSION: "3.11.42"},
    "1.9.0" : {WIFI_VERSION: "3.12.10", BLE_VERSION: "3.12.36"},
    "1.10.1" : {WIFI_VERSION: "3.13.29", BLE_VERSION: "3.13.25"},
    "3.14.0" : {WIFI_VERSION: "3.14.33", BLE_VERSION: "3.14.64"},
    "3.15.0" : {WIFI_VERSION: "3.15.38", BLE_VERSION: "3.15.72"},
    "3.16.3" : {WIFI_VERSION: "3.16.20", BLE_VERSION: "3.16.96"},
    "3.17.0" : {WIFI_VERSION: "3.17.25", BLE_VERSION: "3.17.90"},
    "4.0.0" : {WIFI_VERSION: "4.0.8", BLE_VERSION: "4.0.65"},
    "4.1.0" : {WIFI_VERSION: "4.1.8", BLE_VERSION: "4.1.33"},
    "4.1.2" : {WIFI_VERSION: "4.1.11", BLE_VERSION: "4.1.35"},
    "4.2.0" : {WIFI_VERSION: "4.2.22", BLE_VERSION: "4.2.115"},
    "4.2.5" : {WIFI_VERSION: "4.2.26", BLE_VERSION: "4.2.125"},
    "4.3.0" : {WIFI_VERSION: "4.3.24", BLE_VERSION: "4.3.96"},
    "4.3.1" : {WIFI_VERSION: "4.3.24", BLE_VERSION: "4.3.98"},
    "4.3.2" : {WIFI_VERSION: "4.3.24", BLE_VERSION: "4.3.100"},
}

# Tests defines
DEFAULT_GW_FIELD_UPDATE_TIMEOUT =   10
DEFAULT_BRG_FIELD_UPDATE_TIMEOUT =  10
HB_PERIOD =                         30
VER_UPDATE_TIMEOUT =                400
GW_LATITUDE_DEFAULT =               33.0222
GW_LONGITUDE_DEFAULT =              -117.0839
# Set to work with default when versions tests only pass through new api ver
GW_API_VER_DEFAULT =                "201"
GW_API_VER_OLD =                    "200"
GW_API_VER_LATEST =                 "205"
BRG_CFG_HAS_LEN =                   2
CLEAR_DATA_PATH_TIMEOUT =           10
ACTION_LONG_TIMEOUT =               120
ACTION_SI_PKT_TIMEOUT =             10
ACTION_SHORT_TIMEOUT =              5

# Internal python ut defines - used only in ut
PACER_INTERVAL_MIN_TAGS_COUNT =                     20
PACER_INTERVAL_MAX_FAILED_TAGS =                    2
PACER_INTERVAL_THRESHOLD_HIGH =                     0.90
PACER_INTERVAL_CEIL_THRESHOLD =                     1.1
PACER_INTERVAL_THRESHOLD =                          0.80
PACKETS_ECHO_OFF =                                  16
TEST_PASSED =                                       0
TEST_FAILED =                                       -1
TEST_SKIPPED =                                      1
TEST_INIT =                                         2
NO_RESPONSE =                                       "NO_RESPONSE"
DONE =                                              "DONE"
MGMT_PKT =                                          "mgmt_pkt"
UNIFIED_PKT =                                       "unified_pkt"
SIDE_INFO_SENSOR_PKT =                              "side_info_sensor_pkt"
SENSOR_PKT =                                        "sensor_pkt"
DECODED_DATA =                                      "decoded_data"
TAG_ID =                                            "tag_id"
BRG_LATENCY =                                       "brg_latency"
PACKET_CNTR =                                       "packet_cntr"
PACKET_TYPE =                                       "packet_type"
PACKET_DATA =                                       "packet_data"
PKTS =                                              "pkts"
MQTT_LOG_PRE_STR =                                  "mqtt_log_"
GW_DATA =                                           "gw_data"
GW_ID =                                             "gw_id"
CER =                                               "cer"
PKT_CNTR_DIFF =                                     "packet_cntr_diff"
AVG =                                               "avg_"
CER_PER_TAG =                                       "cer_per_tag"
AWS =                                               "aws"
TEST =                                              "test"
MULTI_BRG_TEST =                                    "multiBridgeTest" # used for multi brg tests
GW_ONLY_TEST =                                      "gwOnlyTest" # used for gw only tests
ALL_SUPPORTED_VALUES =                              "allSupportedValues"
PRE_CONFIG =                                        "Pre config"
TEST_BODY =                                         "Test Body"
RESTORE_CONFIG =                                    "Restore config"

# test reasons
NO_PARAMS_GIVEN =           "No parameters given!"
BRG_VER_SUCCESS =           "SUCCESS - BRG version matches expected version!"
BRG_BL_VER_SUCCESS =        "SUCCESS - BRG Bootloader version matches expected version!"
WANTED_VER_SAME =           "Wanted version is same as original one!"
WANTED_VER_SAME_MUL =       "Wanted versions are same as original ones!"
VER_UPDATE_PASSED =         "Version Update Ran Successfully!"
VER_UPDATE_FAILED =         "The Update Process Has Been Interrupted!"

# ---------------------------------------------------RTSA defines---------------------------------------------------
# common defines
TRACE_LOG_FILE_NAME =                   "TRACELOG"
TRACE_LOG_FILE_PATH =                   "C:/SignalVu-PC Files/" + TRACE_LOG_FILE_NAME + ".TOV"

# freq defines
FREQ_2_4_GHZ =                          {'37':2.402, '38':2.426, '39':2.480}
FREQ_SUB1G_MHZ =                        {'865_7':865.700, '915':915.000, '916_3':916.300, '917_5':917.500, '918':918.000, '919_1':919.100}

# SignalVu API commands defines
TRACE_DETECTION =                       {'average':'AVERage', 'positive':'POSitive', 'negative':'NEGative', 'positive-negative':'POSNegative', 'sample':'SAMPle'}
MAX_TRACE_POINTS =                      {'1K':'ONEK', '10K':'TENK', '100K':'HUNDredk', 'never_decimate':'NEVerdecimate' }

# default values
DEFAULT_LENGTH_MS =                     30
DEFAULT_TIME_PER_DIVISION_SEC =         5
DEFAULT_RX_TX_PERIOD_SEC =              0.015
BEACON_MIN_LENGTH_SEC =                 375e-6
BEACON_MAX_LENGTH_SEC =                 500e-6
ENERGIZING_TIME_THRESHOLD =             0.3
BEACON_POWER_THRESHOLD =                0.9
BEACON_POWER_CURVE_38 =                 0.7
BEACON_POWER_CURVE_39 =                 0.625
DEFAULT_SPAN_MHZ =                      5
RXTX_MAX_CFG =                          255
RXTX_CFG_DEFAULT =                      100

# test times
FREQ_BEACONS_ANALYSIS_TIME_DELTA =      10

# structured energizing patterns information
class energizingPattern:
    def __init__(self, ble_calibration_beacons = [], ble_energy = {}, ble_post_energy_beacons = [], sub1G_energy = False, info = ""):
        self.ble_calibration_beacons = ble_calibration_beacons
        self.ble_energy = ble_energy
        self.ble_post_energy_beacons = ble_post_energy_beacons
        self.sub1G_energy = sub1G_energy
        self.info = info

EP_INFO = {
        '17' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39']]),
        '18' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39']], ble_energy={FREQ_2_4_GHZ['39'] : 1.0}),
        '20' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39']], ble_energy={FREQ_2_4_GHZ['37'] : 0.2, FREQ_2_4_GHZ['39'] : 0.8}),
        '24' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39']], ble_energy={FREQ_2_4_GHZ['37'] : 1.0}),
        '25' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39']], ble_energy={FREQ_2_4_GHZ['38'] : 1.0}),
        '26' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39']], ble_energy={2.454 : 1.0}),
        '27' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39'], FREQ_2_4_GHZ['39']]),
        '29' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39']], ble_energy={FREQ_2_4_GHZ['38'] : 0.3333, 2.454 : 0.3333, FREQ_2_4_GHZ['39'] : 0.3333}),
        '36' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'],FREQ_2_4_GHZ['38'],FREQ_2_4_GHZ['39']], info="idle"),
        '37' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], 2.415, FREQ_2_4_GHZ['39'], 2.441, 2.428, 2.454, 2.467], ble_energy={2.450 : 1.0}, info="euro"),
        '50' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39']], sub1G_energy=True),
        '51' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39']], ble_energy={FREQ_2_4_GHZ['39'] : 1.0}, sub1G_energy=True),
        '52' : energizingPattern(sub1G_energy=True),
        '55' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39']], ble_energy={FREQ_2_4_GHZ['37'] : 1.0}, sub1G_energy=True),
        '56' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39']], ble_energy={FREQ_2_4_GHZ['38'] : 1.0}, sub1G_energy=True),
        '57' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39']], ble_energy={2.454 : 1.0}, sub1G_energy=True),
        '61' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], 2.415, FREQ_2_4_GHZ['39'], 2.441, 2.428, 2.454, 2.467], sub1G_energy=True, info="euro"),
        '62' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], 2.415, FREQ_2_4_GHZ['39'], 2.441, 2.428, 2.454, 2.467], ble_energy={2.475 : 1.0}, sub1G_energy=True, info="euro"),
        '99' : energizingPattern(ble_calibration_beacons=[i/1000.0 for i in range(2402, 2481, 2)])
                }

EP_FREQ_BREAKDOWN_COUNTER_SETUP = {
    2.402 : {'beacons':0, 'energy_in_ms': 0.0},
    2.426 : {'beacons':0, 'energy_in_ms': 0.0},
    2.480 : {'beacons':0, 'energy_in_ms': 0.0},
    2.403 : {'beacons':0, 'energy_in_ms': 0.0},
    2.427 : {'beacons':0, 'energy_in_ms': 0.0},
    2.483 : {'beacons':0, 'energy_in_ms': 0.0},
    2.454 : {'beacons':0, 'energy_in_ms': 0.0},
    2.481 : {'beacons':0, 'energy_in_ms': 0.0},
    2.415 : {'beacons':0, 'energy_in_ms': 0.0},
    2.441 : {'beacons':0, 'energy_in_ms': 0.0},
    2.428 : {'beacons':0, 'energy_in_ms': 0.0},
    2.467 : {'beacons':0, 'energy_in_ms': 0.0},
    2.475 : {'beacons':0, 'energy_in_ms': 0.0},
    0.8657 : {'beacons':0, 'energy_in_ms': 0.0},
    0.915 : {'beacons':0, 'energy_in_ms': 0.0},
    0.9163 : {'beacons':0, 'energy_in_ms': 0.0},
    0.9175 : {'beacons':0, 'energy_in_ms': 0.0},
    0.918 : {'beacons':0, 'energy_in_ms': 0.0},
    0.9191 : {'beacons':0, 'energy_in_ms': 0.0}
}
