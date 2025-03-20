# from http import client
import time
import os
import json
from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
from brg_certificate.wlt_types import *
import brg_certificate.cert_protobuf as cert_protobuf
import threading

# gw_sim defines
TAG_ID_OFFSET              = -16
TAG_ID_FROM_ADVA_LENGTH    = 8
TAG_ID_FROM_ADVA_OFFSET    = 2
HDR_BLE5_DEFAULT_PKT_SIZE  = 0x26
PIXEL_SIM_INDICATOR        = "ABCDEF"
PIXEL_SIM_MIN_CYCLE        = 20 # 20 is the CYCLE_PERIOD_MS_DEFAULT

def init_adva(flow_version_major=0x4, flow_version_minor=0x34):
    return "{0:02X}".format(flow_version_major) + os.urandom(4).hex().upper() + "{0:02X}".format(flow_version_minor)

random_bytes = lambda n: int.from_bytes(os.urandom(n), "big")

def write_to_data_sim_log_file(txt):
    f = open(os.path.join(BASE_DIR, DATA_SIM_LOG_FILE), "a")
    f.write(txt)
    f.close()

class WiliotPixelGen2:
    """Represents 1 Wiliot Gen2 BLE4 Pixel"""
    def __init__(self, pixel_sim_indicator=PIXEL_SIM_INDICATOR):
        self.adva = init_adva(flow_version_major=0x4, flow_version_minor=0x34)
        self.hdr = ag.DataHdr(uuid_msb=ag.HDR_DEFAULT_TAG_UUID_MSB, uuid_lsb=ag.HDR_DEFAULT_TAG_UUID_LSB, group_id_minor=0x0300)
        self.pixel_sim_indicator = pixel_sim_indicator
        self.payload0 = "010203040506070809"
        self.payload1 = "0A0B0C0D"
        self.pkt_id = 0

    def __repr__(self) -> str:
        return f'TagID: {self.get_tag_id()} PktID: {self.get_pkt_id()} PktType: {self.hdr.pkt_type} RawPkt: {self.get_pkt()}'

    def get_tag_id(self):
        return self.adva[TAG_ID_FROM_ADVA_OFFSET:TAG_ID_FROM_ADVA_OFFSET + TAG_ID_FROM_ADVA_LENGTH]

    def set_pkt_type(self, pkt_type):
        assert pkt_type in [0, 1, 2], "Packet type Must be 0, 1 or 2!"
        self.hdr.pkt_type = pkt_type

    def randomize_pkt_id(self):
        self.pkt_id = random_bytes(4)

    def randomize_payload1(self):
        self.payload1 = f"{random_bytes(4):08X}"

    def get_pkt_id(self):
        return "{0:08X}".format(self.pkt_id)

    def get_pkt(self):
        """Get current packet from generator (hex string)
        adva-6 hdr-7 sim_indicator-3 payload-13 tag_id-4 pkt_id-4 """
        return self.adva + self.hdr.dump() + self.get_pkt_id() + self.pixel_sim_indicator + self.payload0 + self.get_tag_id() + self.payload1

class WiliotPixelGen3:
    """Represents 1 Wiliot Gen3 BLE4 Pixel"""
    def __init__(self, pixel_sim_indicator=PIXEL_SIM_INDICATOR):
        self.adva = init_adva(flow_version_major=0x6, flow_version_minor=0x34) # 0x6 is the flow version for Gen3 (GEN3_FLOW_VER_MAJOR_MIN_VAL)
        self.hdr = ag.DataHdr(uuid_msb=ag.HDR_DEFAULT_TAG_UUID_MSB, uuid_lsb=ag.HDR_DEFAULT_TAG_UUID_LSB, group_id_minor=0x0500)
        self.pixel_sim_indicator = pixel_sim_indicator
        self.payload0 = "010203040506070809"
        self.payload1 = "0A0B0C0D"
        self.pkt_id = 0

    def __repr__(self) -> str:
        return f'TagID: {self.get_tag_id()} PktID: {self.get_pkt_id()} PktType: {self.hdr.pkt_type} RawPkt: {self.get_pkt()}'

    def get_tag_id(self):
        return self.adva[TAG_ID_FROM_ADVA_OFFSET:TAG_ID_FROM_ADVA_OFFSET + TAG_ID_FROM_ADVA_LENGTH]

    def set_pkt_type(self, pkt_type):
        assert pkt_type in [0, 1], "Packet type Must be 0 or 1!"
        self.hdr.pkt_type = pkt_type

    def randomize_pkt_id(self):
        self.pkt_id = random_bytes(4)

    def randomize_payload1(self):
        self.payload1 = f"{random_bytes(4):08X}"

    def get_pkt_id(self):
        return "{0:08X}".format(self.pkt_id)

    def get_pkt(self):
        """Get current packet from generator (hex string)
        adva-6 hdr-7 nonce/pkt_id-4 sim_indicator-3 payload0-9 tag_id-4 payload1-4 """
        return self.adva + self.hdr.dump() + self.get_pkt_id() + self.pixel_sim_indicator + self.payload0 + self.get_tag_id() + self.payload1
class WiliotPixelGen3Extended:
    """Represents 1 Wiliot Gen3 BLE4 Pixel"""
    def __init__(self, pixel_sim_indicator=PIXEL_SIM_INDICATOR):
        self.adi = '0000'
        self.adva = init_adva(flow_version_major=0x6, flow_version_minor=0x34) # 0x6 is the flow version for Gen3 (GEN3_FLOW_VER_MAJOR_MIN_VAL)
        self.hdr = ag.DataHdr(pkt_size=HDR_BLE5_DEFAULT_PKT_SIZE, uuid_msb=ag.HDR_DEFAULT_TAG_UUID_MSB, uuid_lsb=ag.HDR_DEFAULT_TAG_UUID_LSB, group_id_minor=0x0500)
        self.uid = "010203040506" # 6 bytes UID
        self.mic = pixel_sim_indicator + pixel_sim_indicator # 6 bytes MIC (mico and mic1 are set to the sim indicator)
        self.payload0 = self.get_tag_id() + f"{random_bytes(4):08X}" # 8 bytes payload. We will use first 4 bytes for the tag_id to keep the same location as in Gen2 and Gen3 BLE4
        self.payload1 = self.get_tag_id() + f"{random_bytes(4):08X}" # 8 bytes payload. We will use first 4 bytes for the tag_id to keep the same location as in Gen2 and Gen3 BLE4
        self.pkt_id = 0

    def __repr__(self) -> str:
        return f'TagID: {self.get_tag_id()} PktID: {self.get_pkt_id()} RawPkt: {self.get_pkt()}'

    def get_tag_id(self):
        return self.adva[TAG_ID_FROM_ADVA_OFFSET:TAG_ID_FROM_ADVA_OFFSET + TAG_ID_FROM_ADVA_LENGTH]

    def set_pkt_type(self, pkt_type):
        assert pkt_type in [2, 3], "Packet type Must be 2 or 3!"
        self.hdr.pkt_type = pkt_type

    def randomize_pkt_id(self):
        self.pkt_id = random_bytes(4)

    def get_pkt_id(self):
        return "{0:08X}".format(self.pkt_id)

    def get_pkt(self):
        """ Get current packet from generator (hex string) - 47 bytes
        adva-6 adi-2 hdr-7 nonce/pkt_id-4 uid-6 mic-6 payload0-8 payload1-8 """
        return self.adva + self.adi + self.hdr.dump() + self.get_pkt_id() + self.uid + self.mic + self.payload0 + self.payload1

class DataSimThread(threading.Thread):
    def __init__(self, test, num_of_pixels, duplicates, delay, pkt_types, pixels_type=GEN2):
        super().__init__()
        self.test = test
        self.num_of_pixels = num_of_pixels
        # Create pixels list
        if pixels_type == GEN2:
            self.pixels = [WiliotPixelGen2() for _ in range(self.num_of_pixels)]
        elif pixels_type == GEN3:
            self.pixels = [WiliotPixelGen3() for _ in range(self.num_of_pixels)]
        elif pixels_type == GEN3_EXTENDED:
            self.pixels = [WiliotPixelGen3Extended() for _ in range(self.num_of_pixels)]
        else:
            print(f"Didn't define pixels type")
        self.duplicates = duplicates
        self.delay = delay
        self.pkt_types = pkt_types
        self._stop_event = threading.Event()
        self.daemon = True

    def run(self):
        write_to_data_sim_log_file(f"num_of_pixels={self.num_of_pixels} duplicates={self.duplicates} delay={self.delay} pkt_types={self.pkt_types}\n")
        # Run pixel_sim loop
        while not self._stop_event.is_set():
            for i in range(self.num_of_pixels):
                for pkt_type in self.pkt_types:
                    pkt = self.pixels[i]
                    pkt.set_pkt_type(pkt_type)
                    # Set pkt_id, in Gen3 pkt_type_1 has pkt_id_0+1
                    if type(pkt) == WiliotPixelGen3:
                        if pkt_type == 1:
                            if self.pkt_types == [0,1]:
                                pkt.pkt_id += 1
                            else:
                                pkt.randomize_pkt_id()
                            pkt.randomize_payload1() # In the FW we assume data is random at the place gen2 pkt id was (4 last bytes)
                        else:
                            # pkt type 0
                            pkt.randomize_pkt_id()
                            pkt.randomize_payload1() # In the FW we assume data is random at the 4 last bytes
                    else:
                        pkt.randomize_pkt_id()
                        if type(pkt) == WiliotPixelGen2:
                            pkt.randomize_payload1() # In the FW we assume data is random at the 4 last bytes
                    # Publish pkt to MQTT
                    msg = {TX_PKT: pkt.get_pkt(),
                        TX_MAX_RETRIES: self.duplicates,
                        TX_MAX_DURATION_MS: 100,
                        ACTION: 0}
                    if self.test.protobuf == True:
                        payload = cert_protobuf.downlink_to_pb(msg)
                    else:
                        payload = json.dumps(msg)
                    self.test.mqttc.publish(self.test.mqttc.update_topic, payload=payload)
                    write_to_data_sim_log_file(f"{pkt}" + " {}\n".format(datetime.datetime.now().strftime("%d/%m,%H:%M:%S.%f")[:-4]))
                    actual_delay = max(self.delay, self.duplicates*(PIXEL_SIM_MIN_CYCLE))
                    time.sleep(actual_delay/1000)

    def stop(self):
        self._stop_event.set()