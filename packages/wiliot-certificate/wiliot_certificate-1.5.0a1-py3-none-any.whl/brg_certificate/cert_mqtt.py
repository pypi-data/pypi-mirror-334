# from http import client
import paho.mqtt.client as mqtt
import ssl
import time
import os
import json
import datetime
import base64
import copy
import traceback
import brg_certificate.wltPb_pb2 as wpb
from google.protobuf.message import DecodeError
from google.protobuf.json_format import MessageToDict

# Local imports
from brg_certificate.wlt_types import *
from brg_certificate.cert_data_sim import PIXEL_SIM_INDICATOR, TAG_ID_OFFSET
from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *


SENSORS_DATA_SI_DUP = 6

class WltMqttPkt:
    def __init__(self, body, topic, userdata):
        self.body = body
        self.mqtt_topic = topic
        self.mqtt_timestamp = datetime.datetime.now()
        self.body_ex = {}
        if "data" in self.mqtt_topic:
            self.body_ex = copy.deepcopy(body)
            self.body_ex['undecrypted'] = 0
            for pkt in self.body_ex[PACKETS]:
                # if packet is not a mgmt packet or a side info packet it is a data packet
                wlt_pkt = WltPkt(pkt[PAYLOAD])
                if wlt_pkt.pkt != None:
                    if wlt_pkt.hdr.group_id == ag.GROUP_ID_BRG2GW:
                        pkt[MGMT_PKT] = copy.deepcopy(wlt_pkt)
                    elif wlt_pkt.data_hdr.group_id_major in ag.UNIFIED_GROUP_ID_LIST:
                        pkt[UNIFIED_PKT] = copy.deepcopy(wlt_pkt)
                        if PIXEL_SIM_INDICATOR in pkt[PAYLOAD]:
                            pkt[DECODED_DATA] = {TAG_ID: pkt[PAYLOAD][TAG_ID_OFFSET:TAG_ID_OFFSET+8], PACKET_TYPE: wlt_pkt.data_hdr.pkt_type, PACKET_CNTR: 0}
                        elif userdata["data"] != DATA_SIMULATION:
                            pkt[DECODED_DATA] = self.handle_data_pkt(wlt_pkt.dump())
                    elif wlt_pkt.hdr.group_id == ag.GROUP_ID_SIDE_INFO_SENSOR:
                        pkt[SIDE_INFO_SENSOR_PKT] = copy.deepcopy(wlt_pkt)
                    elif wlt_pkt.hdr.uuid_lsb == ag.HDR_DEFAULT_BRG_SENSOR_UUID_LSB and wlt_pkt.hdr.uuid_msb == ag.HDR_DEFAULT_BRG_SENSOR_UUID_MSB:
                        pkt[SENSOR_PKT] = copy.deepcopy(wlt_pkt)
                        pkt[DECODED_DATA] = {TAG_ID: None, PACKET_CNTR: None, PACKET_TYPE: None}
                else:
                    if userdata["data"] != DATA_SIMULATION:
                        pkt[DECODED_DATA] = self.handle_data_pkt(pkt)

    def handle_data_pkt(self, pkt):
        p, dec_data = "", {TAG_ID: None, PACKET_CNTR: None, PACKET_TYPE: None}
        if type(pkt) == str:
            p = pkt
        else:
            p = pkt[PAYLOAD]
        resolve = local_resolve(p) if p else None
        if resolve:
            for key in dec_data:
                if key in resolve[DECODED_DATA]:
                    dec_data[key] = resolve[DECODED_DATA][key]
        else:
            self.body_ex['undecrypted'] += 1
        return dec_data

class WltMqttPkts:
    def __init__(self):
        self.data = []
        self.status = []
        self.update = []
        self.all = []
    def insert(self, pkt):
        self.all.append(pkt)
        if "data" in pkt.mqtt_topic:
            self.data.append(pkt)
        elif "status" in pkt.mqtt_topic:
            self.status.append(pkt)
        elif "update" in pkt.mqtt_topic:
            self.update.append(pkt)
    def flush(self):
        self.all = []
        self.data = []
        self.status = []
        self.update = []
    def flush_data(self):
        self.data = []
    def flush_status(self):
        self.status = []

def local_resolve(p):
    import brg_certificate.ut.ut_resolve as ut_resolve
    irresolvable_payloads = ["1E16C6FC0000EE", "1E16AFFD0000EC", "1E16C6FC0000EC"]
    try:
        if any(substring in p for substring in irresolvable_payloads):
            # brg2gw mgmt pkt - skip
            return None
        elif p.startswith("1E16"):
            payload = p
        elif p.startswith("2916"):
            payload = '26' + p[2:-6] # change 29 to 26 and remove side info
        else:
            payload = "1E16" + p
        group_id_minor = int(p[8:10], 16)
        if group_id_minor == 0x05 or group_id_minor == 0xFE: # BLE5 group id minor
            version=3.0
        else:
            version=2.4
        resolve = ut_resolve.DecryptedPacket(ut_resolve.convert_cloud_to_packet(payload), packet_version_by_user=version)
        return {PACKET_DATA:resolve.packet_data, DECODED_DATA:resolve.decoded_data, GW_DATA:resolve.gw_data}
    except Exception as e:
        print(traceback.format_exc())
        print(e)
        print(f"Failed in local_resolve with packet: {p}\n")
        return None

def is_json(msg):
    is_utf = True
    try:
        json.loads(msg.decode("utf-8"))
    except:
        is_utf = False
    return is_utf

def on_connect(mqttc, userdata, flags, rc):
    print("python_mqtt_connect, rc: " + str(rc))

def on_disconnect(mqttc, userdata, rc):
    txt = f"ERROR: python_mqtt_disconnect, rc: {rc} {mqtt.error_string(rc)}"
    print(txt)
    write_to_mqtt_log_file(txt)

def on_subscribe(mqttc, userdata, mid, granted_qos):
    print("python_mqtt_subscribe, " + str(mid) + " " + str(granted_qos))

def on_unsubscribe(mqttc, userdata, mid):
    print("ERROR: python_mqtt_unsubscribe, " + str(mid))

def on_message(mqttc, userdata, message):
    if is_json(message.payload):
        on_message_json(mqttc, userdata, message)
    else:
        on_message_protobuf(mqttc, userdata, message)

def on_message_json(mqttc, userdata, message):
    wlt_mqtt_pkts = userdata[PKTS]
    data = json.loads(message.payload.decode("utf-8"))
    wlt_mqtt_pkts.insert(WltMqttPkt(data, message.topic, userdata))
    write_to_mqtt_log_file("// JSON message received at {}, topic={}:\n{}\n".format(datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), message.topic, str(message.payload.decode("utf-8"))))

def on_message_protobuf(mqttc, userdata, message):
    pb_msg = None
    pb_decoded = False

    # Decode message according to the schema used on each topic
    if 'status' in message.topic:
        pb_msg = wpb.UplinkMessage()
    elif 'data' in message.topic:
        pb_msg = wpb.GatewayData()
    elif 'update' in message.topic:
        pb_msg = wpb.DownlinkMessage()
    try:
        pb_msg.ParseFromString(message.payload)
        pb_decoded = True
    except DecodeError as e: 
        print(f'ERROR: failed decoding {message.topic} message: \n{e}\n')

    if pb_decoded is True:
        pb_msg_dict = MessageToDict(pb_msg)
        # Align formats with JSON (bytes to hex strings)
        if 'status' in message.topic:
            if GW_STATUS in pb_msg_dict and ACL_IDS in pb_msg_dict[GW_STATUS][CONFIG][ACL][ACL_VALUE]:
                ids_list = pb_msg_dict[GW_STATUS][CONFIG][ACL][ACL_VALUE][ACL_IDS]
                for idx, id in enumerate(ids_list):
                    ids_list[idx] = base64.b64decode(id).hex().upper()
        if 'data' in message.topic and PACKETS in pb_msg_dict.keys():
            for idx, pkt in enumerate(pb_msg_dict[PACKETS]):
                pb_msg_dict[PACKETS][idx][PAYLOAD] = base64.b64decode(pkt[PAYLOAD]).hex().upper()
                pb_msg_dict[PACKETS][idx][TIMESTAMP] = int(pkt[TIMESTAMP])
        if 'update' in message.topic:
            if TX_PKT in pb_msg_dict.keys():
                pb_msg_dict[TX_PKT][PAYLOAD] = base64.b64decode(pb_msg_dict[TX_PKT][PAYLOAD]).hex().upper()
            elif BRG_UPGRADE in pb_msg_dict.keys():
                pb_msg_dict[BRG_UPGRADE][REBOOT_PKT] = base64.b64decode(pb_msg_dict[BRG_UPGRADE][REBOOT_PKT]).hex().upper()

        # Push & log
        wlt_mqtt_pkts = userdata[PKTS]
        wlt_mqtt_pkts.insert(WltMqttPkt(pb_msg_dict, message.topic, userdata))
        write_to_mqtt_log_file("// Protobuf message {} at {}, topic={}:\n{}\n".format('published' if 'update' in message.topic else 'received',
            datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), message.topic, json.dumps(pb_msg_dict, indent=4)))

def pkts_to_log(pkts):
    text = ""
    for p in pkts:
        text += "// {} topic={}".format(p.mqtt_timestamp.strftime("%d/%m/%Y, %H:%M:%S"), p.mqtt_topic)
        text += "\n"+json.dumps(p.body, indent=4)+"\n"
    return text

def write_to_log_file(file_name, pkts):
    f = open(os.path.join(BASE_DIR, file_name), "w")
    f.write(pkts_to_log(pkts))
    f.close()

def write_to_mqtt_log_file(txt):
    f = open(os.path.join(BASE_DIR, CERT_MQTT_LOG_FILE), "a")
    f.write(txt)
    f.close()

def load_custom_broker(gw, rel_path="."):
    f = open(os.path.join(BASE_DIR, rel_path, "config", "eclipse.json"))
    # f = open(os.path.join(BASE_DIR, rel_path, "config", "hivemq.json"))
    # f = open(os.path.join(BASE_DIR, rel_path, "config", "mosquitto.json"))
    # f = open(os.path.join(BASE_DIR, rel_path, "config", "wiliot-dev.json"))
    data = json.load(f)
    data[CUSTOM_BROKER_UPDATE_TOPIC] += gw
    data[CUSTOM_BROKER_STATUS_TOPIC] += gw
    data[CUSTOM_BROKER_DATA_TOPIC] += gw
    return data

def mqttc_init(gw_id, userdata={PKTS: WltMqttPkts()}, rel_path=".", data=DATA_REAL_TAGS):

    custom_broker = load_custom_broker(gw=gw_id, rel_path=rel_path)
    client_id = '{}-republish'.format(gw_id)
    userdata["data"] = data
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id, userdata=userdata)
    mqttc.username_pw_set(custom_broker[CUSTOM_BROKER_USERNAME], custom_broker[CUSTOM_BROKER_PASSWORD])
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_disconnect = on_disconnect
    mqttc.on_subscribe = on_subscribe
    mqttc.on_unsubscribe = on_unsubscribe
    if not 1883 == custom_broker[CUSTOM_BROKER_PORT]:
        mqttc.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)
    mqttc.connect(custom_broker[CUSTOM_BROKER_BROKER_URL].replace("mqtts://", ""), port=custom_broker[CUSTOM_BROKER_PORT], keepalive=60)
    mqttc.loop_start()

    mqttc.update_topic = custom_broker[CUSTOM_BROKER_UPDATE_TOPIC]
    mqttc.subscribe(mqttc.update_topic)
    mqttc.data_topic = custom_broker[CUSTOM_BROKER_DATA_TOPIC]
    mqttc.subscribe(mqttc.data_topic)
    mqttc.status_topic = custom_broker[CUSTOM_BROKER_STATUS_TOPIC]
    mqttc.subscribe(mqttc.status_topic)

    mqttc.flush_pkts = mqttc._userdata[PKTS].flush
    mqttc.flush_data_pkts = mqttc._userdata[PKTS].flush_data
    mqttc.flush_status_pkts = mqttc._userdata[PKTS].flush_status
    time.sleep(2)

    return mqttc

def dump_pkts(test, log):
    write_to_log_file(os.path.join(test.dir, MQTT_LOG_PRE_STR+log+"_all.json"), test.mqttc._userdata[PKTS].all)
    write_to_log_file(os.path.join(test.dir, MQTT_LOG_PRE_STR+log+"_data.json"), test.mqttc._userdata[PKTS].data)
    write_to_log_file(os.path.join(test.dir, MQTT_LOG_PRE_STR+log+"_status.json"), test.mqttc._userdata[PKTS].status)
    write_to_log_file(os.path.join(test.dir, MQTT_LOG_PRE_STR+log+"_update.json"), test.mqttc._userdata[PKTS].update)

# Get data/tags functions
def get_all_data_pkts(mqttc):
    data_pkts = []
    for p in mqttc._userdata[PKTS].data:
        gw_id = p.body_ex[GW_ID] if GW_ID in p.body_ex else ""
        if PACKETS in p.body_ex:
            for pkt in p.body_ex[PACKETS]:
                pkt[GW_ID] = gw_id
                data_pkts += [pkt]
    return data_pkts

def get_all_sim_data_pkts(mqttc):
    data_pkts = []
    for p in mqttc._userdata[PKTS].data:
        gw_id = p.body_ex[GW_ID] if GW_ID in p.body_ex else ""
        if PACKETS in p.body_ex:
            for pkt in p.body_ex[PACKETS]:
                if PIXEL_SIM_INDICATOR in pkt[PAYLOAD]:
                    pkt[GW_ID] = gw_id
                    data_pkts += [pkt]
    return data_pkts

def get_undecrypted_data_pkts_count(mqttc):
    undecrypted = 0
    for p in mqttc._userdata[PKTS].data:
        if 'undecrypted' in p.body_ex:
            undecrypted += p.body_ex['undecrypted']
    return undecrypted

def get_all_sensor_pkts(mqttc, test, is_embedded=False):
    all_sensor_pkts = couple_sensor_data_si_coupling(test)
    all_sensor_pkts = [p for p in all_sensor_pkts if test.active_brg.id_str == p[BRIDGE_ID] and (p[IS_EMBEDDED] == is_embedded)]
    return all_sensor_pkts

def couple_sensor_data_si_coupling(test):
    all_pkts = get_all_data_pkts(test.mqttc)
    all_sensor_data_pkts = [p for p in all_pkts if SENSOR_PKT in p]
    all_sensor_side_info_pkts = [p for p in all_pkts if SIDE_INFO_SENSOR_PKT in p]
    # Couple data and side info
    coupled_sensor_pkts = []
    for p_data in all_sensor_data_pkts:
        for p_si in all_sensor_side_info_pkts:
            data_pkt = p_data[SENSOR_PKT].pkt
            si_pkt = p_si[SIDE_INFO_SENSOR_PKT].pkt
            # Packet not coupled yet and (same pkt id & timestamp diff < 1 sec)
            if (not coupled_pkt_exists(coupled_sensor_pkts, p_si) and
                data_pkt.pkt_id == si_pkt.pkt_id and abs(p_data[TIMESTAMP] - p_si[TIMESTAMP]) < 1000):
                p_coupled = {
                                TIMESTAMP : p_data[TIMESTAMP],
                                SEQUENCE_ID : str(p_data[SEQUENCE_ID]),
                                NFPKT : si_pkt.nfpkt,
                                RSSI : si_pkt.rssi,
                                IS_SENSOR : si_pkt.is_sensor,
                                IS_EMBEDDED : si_pkt.is_sensor_embedded,
                                IS_SCRAMBLED : si_pkt.is_scrambled,
                                SENSOR_ID : hex(si_pkt.sensor_mac)[2:].upper(),
                                SENSOR_UUID : "{:02X}{:02X}{:02X}".format(si_pkt.sensor_ad_type, si_pkt.sensor_uuid_msb, si_pkt.sensor_uuid_lsb),
                                BRIDGE_ID: "{:012X}".format(si_pkt.brg_mac),
                                PAYLOAD: p_data[PAYLOAD],
                                SENSOR_PKT: p_data[SENSOR_PKT],
                            }
                coupled_sensor_pkts += [p_coupled]
    # Count the number of packet duplications:
    count_pkt_id_duplications(test, all_sensor_data_pkts, all_sensor_side_info_pkts, coupled_sensor_pkts)
    return coupled_sensor_pkts

def coupled_pkt_exists(coupled_list, pkt):
    for coupled_pkt in coupled_list:
        if ((abs(coupled_pkt[TIMESTAMP] - pkt[TIMESTAMP]) < 1000) and
            coupled_pkt[SENSOR_PKT].pkt.pkt_id == pkt[SIDE_INFO_SENSOR_PKT].pkt.pkt_id):
            return True
    return False

def count_pkt_id_duplications(test, all_sensor_data_pkts, all_sensor_side_info_pkts, all_coupled_pkts):
    pkt_ids = [p_data[SENSOR_PKT].pkt.pkt_id for p_data in all_sensor_data_pkts]
    pkt_ids += [p_si[SIDE_INFO_SENSOR_PKT].pkt.pkt_id for p_si in all_sensor_side_info_pkts]
    for coupled_pkt in all_coupled_pkts:
        _pkt_id = coupled_pkt[SENSOR_PKT].pkt.pkt_id
        coupled_pkt[PKT_ID_CTR] = pkt_ids.count(_pkt_id)
        if coupled_pkt[PKT_ID_CTR] > SENSORS_DATA_SI_DUP:
            print(f"pkt_id {_pkt_id:08X}: {coupled_pkt[PKT_ID_CTR]} occurrences")
            test.reason = f'Warning: {coupled_pkt[PKT_ID_CTR]} sensor data and si with pkt id 0x{_pkt_id:08X}'

def get_all_brg1_ext_sensor_pkts(mqttc, test=None):
    test.active_brg = test.brg1
    pkts = get_all_sensor_pkts(mqttc, test)
    test.active_brg = test.brg0
    return pkts

def get_all_custom_pkts(mqttc, test=None):
    return get_all_sensor_pkts(mqttc, test, is_embedded=True)

def get_all_mgmt_pkts(mqttc):
    all_data_pkts = get_all_data_pkts(mqttc)
    return [p for p in all_data_pkts if MGMT_PKT in p]

def get_brg2gw_mgmt_pkts(mqttc, test=None, mgmt_types=[]):
    brg2gw_mgmt_pkts = [p for p in get_all_mgmt_pkts(mqttc) if ((p[MGMT_PKT].hdr.group_id == ag.GROUP_ID_BRG2GW) and
                                                                (not mgmt_types or type(p[MGMT_PKT].pkt) in mgmt_types))]
    pkts = [p for p in brg2gw_mgmt_pkts if test.active_brg.id_str in p[PAYLOAD]]
    return pkts

def get_unified_data_pkts(test, only_active_brg=True):
    all_unified_pkts, pkts = [], get_all_sim_data_pkts(test.mqttc) if test.data == DATA_SIMULATION else get_all_data_pkts(test.mqttc)
    for p in pkts:
        if UNIFIED_PKT in p:
            all_unified_pkts += [p]
    pkts = all_unified_pkts
    if only_active_brg:
        pkts = [p for p in all_unified_pkts if p[ALIAS_BRIDGE_ID] == test.active_brg.id_alias]
    print(f"\nCollected {len(pkts)} unified data pkts")
    return pkts

def get_internal_brg_unified_data_pkts(test):
    all_unified_pkts, pkts = [], get_all_sim_data_pkts(test.mqttc) if test.data == DATA_SIMULATION else get_all_data_pkts(test.mqttc)
    for p in pkts:
        if UNIFIED_PKT in p:
            all_unified_pkts += [p]
    pkts = [p for p in all_unified_pkts if p[ALIAS_BRIDGE_ID] == test.internal_id_alias()]
    print(f"\nCollected {len(pkts)} unified gw_tag_pkts")
    return pkts