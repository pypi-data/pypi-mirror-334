# Brownout / OTA Defines
SEP = "#" * 50
BO_DICT = {
    'datapath': {'config': {'pktFilter': 'Disable forwarding'}},
    'energy2400': {'config': {'energyPattern2400': 'No Energizing'}},
    'energySub1g': {'config': {'sub1gEnergyPattern': 'No Energizing'}},
    'calibration': {'config': {'calibPattern': 'Disable calibration beaconing'}}
}
BROADCAST_DST_MAC = 'FFFFFFFFFFFF'

colors = ['red', 'blue', 'yellow', 'cyan', 'green', 'brown', 'orange', 'pink', 'purple', 'black']

# Test Tool
GW_DATA_SRC = 'gwDataSrc'
GW_DATA_MODE = 'gwDataMode'
