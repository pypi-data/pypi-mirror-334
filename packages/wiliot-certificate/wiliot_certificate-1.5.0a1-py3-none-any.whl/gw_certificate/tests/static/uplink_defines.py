from gw_certificate.interface.if_defines import *
from gw_certificate.ag.ut_defines import *

RECEIVED = 'received'
SHARED_COLUMNS = [PAYLOAD]
INT64_COLUMNS = [RSSI]
OBJECT_COLUMNS = [PAYLOAD]
REPORT_COLUMNS = ['pkt_id', 'duplication', 'time_delay']

ADV_TIMESTAMP = 'adv_timestamp'
TS_DEVIATION = 1500
TS_TOLERANCE = 2500
REC_TIMESTAMP = 'rec_timestamp'