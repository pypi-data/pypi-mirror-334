
import pkg_resources
import pandas as pd

from gw_certificate.common.debug import debug_print
from gw_certificate.interface.pkt_generator import BrgPktGeneratorNetwork
from gw_certificate.interface.if_defines import *

CSV_NAME = 'packet_table.csv'
PACKET_TABLE_CSV_PATH = pkg_resources.resource_filename(__name__, CSV_NAME)

TEST_STRESS = 'stress'
TEST_COUPLING = 'coupling'
TEST_DOWNLINK = 'downlink'
TEST_UPLINK = 'uplink'
TEST_UNIFIED = 'unified'
TEST_SENSOR = 'sensor'

TESTS = [TEST_COUPLING, TEST_UPLINK, TEST_UNIFIED]
class GeneratedPacketTable:
    
    def __init__(self) -> None:
        self.brg_network = BrgPktGeneratorNetwork()
        self.table = pd.read_csv(PACKET_TABLE_CSV_PATH)
    
    def get_data(self, test, duplication, time_delay, bridge_idx) -> list:    
        assert test in TESTS, 'Invalid Test'
        assert (duplication in UPLINK_DUPLICATIONS) or (duplication in UNIFIED_DUPLICATIONS), 'Invalid Duplication'
        assert (time_delay in UPLINK_TIME_DELAYS) or (time_delay in UNIFIED_TIME_DELAYS), 'Invalid Time Delay'
        assert bridge_idx in BRIDGES, 'Invalid Bridge'
        
        t = self.table
        return t.loc[((t['test'] == test) &
                      (t['duplication'] == duplication) &
                      (t['time_delay'] == time_delay) &
                      (t['bridge_idx'] == bridge_idx))].to_dict('records')[0]
            
    def get_df(self, columns=None):
        if columns is not None:
            return self.table[columns]
        return self.table

    # def get_unified_data(self) -> pd.DataFrame:
    #     t = self.table
    #     return t.loc[((t['test'] == 'stress'))] 
    
    def get_stress_data(self) -> pd.DataFrame:
        t = self.table
        return t.loc[((t['test'] == 'stress'))] 
    
    def get_sensor_data(self) -> pd.DataFrame:
        t = self.table
        return t.loc[((t['test'] == 'sensor'))] 

    def get_mgmt_data(self) -> pd.DataFrame:
        t = self.table
        return t.loc[((t['test'] == 'mgmt'))] 

    def get_unified_data(self) -> pd.DataFrame:
        t = self.table
        return t.loc[((t['test'] == 'unified'))] 
    
    def _generate_packet_table(self):
        packet_list = []
        
        # UNIFIED TEST
        for duplication in UNIFIED_DUPLICATIONS:
            debug_print(f'Duplication {duplication}')
            for time_delay in UNIFIED_TIME_DELAYS:
                debug_print(f'Time Delay {time_delay}')
                pkts = self.brg_network.get_new_pkt_unified()
                for idx, brg in enumerate(self.brg_network.brg_list):
                    debug_print(f'Bridge {idx}')
                    data = pkts[idx]['data_packet']
                    brg_id = self.brg_network.brg_list[idx].bridge_id
                    # log the sent packet with relevant info from run
                    expected_pkt = brg.get_expected_mqtt_unified(full_data_pkt=data)
                    for pkt in expected_pkt:
                        pkt.update({'duplication': duplication, 'time_delay': time_delay})
                    packet_list.append({'test': TEST_UNIFIED,
                                        'duplication': duplication,
                                        'time_delay': time_delay,
                                        'bridge_idx': idx,
                                        'expected_mqtt': expected_pkt
                                        ,ADVA_PAYLOAD: data, 'bridge_id': brg_id,
                                        'adva': data[:12], 'payload': data[16:], 'pkt_id': data[-8:]
                                        })        

        #STRESS TEST
        i = 0
        while i < 10000:
            i += 1
            pkts = self.brg_network.get_new_pkt_unified()
            target_idx = 0  
            brg = self.brg_network.brg_list[target_idx]
            debug_print(f'Bridge {target_idx}')
            data = pkts[target_idx]['data_packet']
            brg_id = brg.bridge_id
            expected_pkt = brg.get_expected_mqtt_unified(full_data_pkt=data)
            packet_list.append({
                'test': TEST_STRESS,
                'duplication': 1,
                'bridge_idx': target_idx,
                'expected_mqtt': expected_pkt,
                ADVA_PAYLOAD: data,
                'bridge_id': brg_id,
                'adva': data[:12],
                'payload': data[16:],
                'pkt_id': data[-8:]
            })          

        def _sensor_data(df):
            hardcoded_data = [
                {"test": "sensor", "duplication": "5", "time_delay": "20", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "90FCA1016417913C42FD38AF3F23AC0201060303E1FF060000FA0EAB04", "duplication": 3, "time_delay": 20}, {"timestamp": 4278768225950047766, "payload": "C6FC0000EB3B613D08177B00003600AC233FAF38FD16E1FF05FA0EAB04", "duplication": 3, "time_delay": 20}], ADVA_PAYLOAD: "3B613D0817FB101690FCA1016417913C42FD38AF3F23AC0201060303E1FF060000FA0EAB04", "payload":"90FCA1016417913C42FD38AF3F23AC0201060303E1FF060000FA0EAB04" ,"si": "3B613D0817FB1E16C6FC0000EB3B613D08177B00003600AC233FAF38FD16E1FF05FA0EAB04", "bridge_id": "3B613D08177B", "adva": "3B613D0817FB", "pkt_id": "FA0EAB04"},
                {"test": "sensor", "duplication": "5", "time_delay": "20", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "90FCA10164157D358A0E39AF3F23AC0201060303E1FF0600007EE3A33F", "duplication": 3, "time_delay": 20}, {"timestamp": 4278768225950047766, "payload": "C6FC0000EB3B613D08177B00004300AC233FAF390E16E1FF057EE3A33F", "duplication": 3, "time_delay": 20}], ADVA_PAYLOAD: "3B613D0817FB101690FCA10164157D358A0E39AF3F23AC0201060303E1FF0600007EE3A33F", "payload":"90FCA10164157D358A0E39AF3F23AC0201060303E1FF0600007EE3A33F" ,"si": "3B613D0817FB1E16C6FC0000EB3B613D08177B00004300AC233FAF390E16E1FF057EE3A33F", "bridge_id": "3B613D08177B", "adva": "3B613D0817FB", "pkt_id": "7EE3A33F"},
                {"test": "sensor", "duplication": "5", "time_delay": "20", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "90FCA1085CCA5BF13F23AC4D425330310201060303E1FF0500E16ED8EA", "duplication": 3, "time_delay": 20}, {"timestamp": 4278768225950047766, "payload": "C6FC0000EB3B613D08177B00004700AC233FF15BCA16E1FF05E16ED8EA", "duplication": 3, "time_delay": 20}], ADVA_PAYLOAD: "3B613D0817FB111690FCA1085CCA5BF13F23AC4D425330310201060303E1FF0500E16ED8EA", "payload":"90FCA1085CCA5BF13F23AC4D425330310201060303E1FF0500E16ED8EA" ,"si": "3B613D0817FB1E16C6FC0000EB3B613D08177B00004700AC233FF15BCA16E1FF05E16ED8EA", "bridge_id": "3B613D08177B", "adva": "3B613D0817FB", "pkt_id": "E16ED8EA"},
                {"test": "sensor", "duplication": "5", "time_delay": "20", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "90FCA10164157D358A0E39AF3F23AC0201060303E1FF06000003E3A33F", "duplication": 3, "time_delay": 20}, {"timestamp": 4278768225950047766, "payload": "C6FC0000EB3B613D08177B00073E00AC233FAF390E16E1FF0503E3A33F", "duplication": 3, "time_delay": 20}], ADVA_PAYLOAD: "3B613D0817FB101690FCA10164157D358A0E39AF3F23AC0201060303E1FF06000003E3A33F", "payload":"90FCA10164157D358A0E39AF3F23AC0201060303E1FF06000003E3A33F" ,"si": "3B613D0817FB1E16C6FC0000EB3B613D08177B00073E00AC233FAF390E16E1FF0503E3A33F", "bridge_id": "3B613D08177B", "adva": "3B613D0817FB", "pkt_id": "03E3A33F"},
                {"test": "sensor", "duplication": "5", "time_delay": "20", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "90FCA10858CA5BF13F23AC4D425330310201060303E1FF0500996ED8EE", "duplication": 3, "time_delay": 20}, {"timestamp": 4278768225950047766, "payload": "C6FC0000EB3B613D08177B00043F00AC233FF15BCA16E1FF05996ED8EE", "duplication": 3, "time_delay": 20}], ADVA_PAYLOAD: "3B613D0817FB111690FCA10858CA5BF13F23AC4D425330310201060303E1FF0500996ED8EE", "payload":"90FCA10858CA5BF13F23AC4D425330310201060303E1FF0500996ED8EE" ,"si": "3B613D0817FB1E16C6FC0000EB3B613D08177B00043F00AC233FF15BCA16E1FF05996ED8EE", "bridge_id": "3B613D08177B", "adva": "3B613D0817FB", "pkt_id": "996ED8EE"},
                {"test": "sensor", "duplication": "5", "time_delay": "20", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "90FCA10864FD38AF3F23AC53310201060303E1FF0800000000157A359C", "duplication": 3, "time_delay": 20}, {"timestamp": 4278768225950047766, "payload": "C6FC0000EB3B613D08177B000E3600AC233FAF38FD16E1FF05157A359C", "duplication": 3, "time_delay": 20}], ADVA_PAYLOAD: "3B613D0817FB0E1690FCA10864FD38AF3F23AC53310201060303E1FF0800000000157A359C", "payload":"90FCA10864FD38AF3F23AC53310201060303E1FF0800000000157A359C" ,"si": "3B613D0817FB1E16C6FC0000EB3B613D08177B000E3600AC233FAF38FD16E1FF05157A359C", "bridge_id": "3B613D08177B", "adva": "3B613D0817FB", "pkt_id": "157A359C"},
                {"test": "sensor", "duplication": "5", "time_delay": "20", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "90FC0200002CC60917A02CB02367771BE9EA20F9666ED8A06F6612745B", "duplication": 3, "time_delay": 20}, {"timestamp": 4278768225950047766, "payload": "C6FC0000EB3B613D08177BF1EBC500000000000000000000006612745B", "duplication": 3, "time_delay": 20}], ADVA_PAYLOAD: "3B613D0817FB1E1690FC0200002CC60917A02CB02367771BE9EA20F9666ED8A06F6612745B", "payload":"90FC0200002CC60917A02CB02367771BE9EA20F9666ED8A06F6612745B" ,"si": "3B613D0817FB1E16C6FC0000EB3B613D08177BF1EBC500000000000000000000006612745B", "bridge_id": "3B613D08177B", "adva": "3B613D0817FB", "pkt_id": "6612745B"},
                {"test": "sensor", "duplication": "5", "time_delay": "20", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "90FC02000007EFE229109B044DB995A506179C99094720AE8BF9F78C1A", "duplication": 3, "time_delay": 20}, {"timestamp": 4278768225950047766, "payload": "C6FC0000EB3B613D08177B6CEC9A0000000000000000000000F9F78C1A", "duplication": 3, "time_delay": 20}], ADVA_PAYLOAD: "3B613D0817FB1E1690FC02000007EFE229109B044DB995A506179C99094720AE8BF9F78C1A", "payload":"90FC02000007EFE229109B044DB995A506179C99094720AE8BF9F78C1A" ,"si": "3B613D0817FB1E16C6FC0000EB3B613D08177B6CEC9A0000000000000000000000F9F78C1A", "bridge_id": "3B613D08177B", "adva": "3B613D0817FB", "pkt_id": "F9F78C1A"},
                {"test": "sensor", "duplication": "5", "time_delay": "20", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "90FC0200002CA1E008E364D0DCF65631718BCD659DE3323A69A674F7B9", "duplication": 3, "time_delay": 20}, {"timestamp": 4278768225950047766, "payload": "C6FC0000EB3B613D08177B1051900000000000000000000000A674F7B9", "duplication": 3, "time_delay": 20}], ADVA_PAYLOAD: "3B613D0817FB1E1690FC0200002CA1E008E364D0DCF65631718BCD659DE3323A69A674F7B9", "payload":"90FC0200002CA1E008E364D0DCF65631718BCD659DE3323A69A674F7B9" ,"si": "3B613D0817FB1E16C6FC0000EB3B613D08177B1051900000000000000000000000A674F7B9", "bridge_id": "3B613D08177B", "adva": "3B613D0817FB", "pkt_id": "A674F7B9"},
                {"test": "sensor", "duplication": "5", "time_delay": "20", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "90FC02000049ADD722F535679C37983927655C974A4980B080045DA6C2", "duplication": 3, "time_delay": 20}, {"timestamp": 4278768225950047766, "payload": "C6FC0000EB3B613D08177B5280B20000000000000000000000045DA6C2", "duplication": 3, "time_delay": 20}], ADVA_PAYLOAD: "3B613D0817FB1E1690FC02000049ADD722F535679C37983927655C974A4980B080045DA6C2", "payload":"90FC02000049ADD722F535679C37983927655C974A4980B080045DA6C2" ,"si": "3B613D0817FB1E16C6FC0000EB3B613D08177B5280B20000000000000000000000045DA6C2", "bridge_id": "3B613D08177B", "adva": "3B613D0817FB", "pkt_id": "045DA6C2"},
                {"test": "sensor", "duplication": "5", "time_delay": "20", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "90FC0200004C8AD49C6D96923BFB70DF06554F5E8F438F1DF57E063773", "duplication": 3, "time_delay": 20}, {"timestamp": 4278768225950047766, "payload": "C6FC0000EB3B613D08177BB4085900000000000000000000007E063773", "duplication": 3, "time_delay": 20}], ADVA_PAYLOAD: "3B613D0817FB1E1690FC0200004C8AD49C6D96923BFB70DF06554F5E8F438F1DF57E063773", "payload":"90FC0200004C8AD49C6D96923BFB70DF06554F5E8F438F1DF57E063773" ,"si": "3B613D0817FB1E16C6FC0000EB3B613D08177BB4085900000000000000000000007E063773", "bridge_id": "3B613D08177B", "adva": "3B613D0817FB", "pkt_id": "7E063773"},
                {"test": "sensor", "duplication": "5", "time_delay": "20", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "90FC02000064A5B54285BB6BCDB457ABBED8EE26B4EB43B27A8C26781C", "duplication": 3, "time_delay": 20}, {"timestamp": 4278768225950047766, "payload": "C6FC0000EB3B613D08177B27363800000000000000000000008C26781C", "duplication": 3, "time_delay": 20}], ADVA_PAYLOAD: "3B613D0817FB1E1690FC02000064A5B54285BB6BCDB457ABBED8EE26B4EB43B27A8C26781C", "payload":"90FC02000064A5B54285BB6BCDB457ABBED8EE26B4EB43B27A8C26781C" ,"si": "3B613D0817FB1E16C6FC0000EB3B613D08177B27363800000000000000000000008C26781C", "bridge_id": "3B613D08177B", "adva": "3B613D0817FB", "pkt_id": "8C26781C"},
            ]
        
            hardcoded_df = pd.DataFrame(hardcoded_data)
            return pd.concat([df, hardcoded_df], ignore_index=True)

        def _mgmt_data(df):
            hardcoded_data = [
                # First pkt is HB, second is CFG_INFO of MODULE_IF
                {"test": "mgmt", "duplication": "10", "time_delay": "20", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "C6FC0000EE020AD2A365FEC65912095E9101FF1104EB0958D400110100", "duplication": 10, "time_delay": 20}], ADVA_PAYLOAD: "A365FEC659D21E16C6FC0000EE020AD2A365FEC65912095E9101FF1104EB0958D400110100", "payload": "C6FC0000EE020AD2A365FEC65912095E9101FF1104EB0958D400110100", "si": "", "bridge_id": "A365FEC65912", "adva": "A365FEC659D2", "pkt_id": "00110100"},
                {"test": "mgmt", "duplication": "10", "time_delay": "20", "bridge_idx": 2, "expected_mqtt": [{"timestamp": 17305216968476073494, "payload": "C6FC0000EE110BD3A365FEC6591203040121E8F2FDB000000000000000", "duplication": 10, "time_delay": 20}], ADVA_PAYLOAD: "A365FEC659D21E16C6FC0000EE110BD3A365FEC6591203040121E8F2FDB000000000000000", "payload": "C6FC0000EE110BD3A365FEC6591203040121E8F2FDB000000000000000", "si": "", "bridge_id": "A365FEC65912", "adva": "A365FEC659D2", "pkt_id": "00000000"},
            ]
        
            hardcoded_df = pd.DataFrame(hardcoded_data)
            return pd.concat([df, hardcoded_df], ignore_index=True)
        
        df = pd.DataFrame(packet_list)
        df = _sensor_data(df)
        df = _mgmt_data(df)
        df.to_csv(PACKET_TABLE_CSV_PATH)
    
class UnifiedRunData:
    def __init__(self) -> None:
        self.data = GeneratedPacketTable().get_unified_data()

class StressRunData:
    def __init__(self) -> None:
        self.data = GeneratedPacketTable().get_stress_data()

class SensorRunData:
    def __init__(self) -> None:
        self.data = GeneratedPacketTable().get_sensor_data()

class MgmtRunData:
    def __init__(self) -> None:
        self.data = GeneratedPacketTable().get_mgmt_data()

class PacketTableHelper():
    def __init__(self):
        self.table = GeneratedPacketTable().get_df()

    def set_field(self, data_payload, field, value):
        self.table.loc[self.table[ADVA_PAYLOAD].str.contains(data_payload) == True, field] = value

    def get_field(self, data_payload, field):
        return self.table[self.table[ADVA_PAYLOAD].str.contains(data_payload) == True][field]
        
if __name__ == "__main__":
    GeneratedPacketTable()._generate_packet_table()
