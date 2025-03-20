
import os
import random
import tabulate
import importlib # needed for importing all of the tests
from requests import codes as r_codes

# Local imports
import brg_certificate.cert_config as cert_config
import brg_certificate.cert_common as cert_common
import brg_certificate.cert_results as cert_results
from brg_certificate.wlt_types import *
from brg_certificate.cert_defines import *
from brg_certificate.cert_prints import *

MULTI_BRG_STR =    "multi_brg"  # used for multi brg tests
GW_ONLY_STR =      "gw_only"  # used for gw only tests
INTERNAL_BRG_STR = "internal_brg"
ORIGINAL_AG_FILE = "wlt_types_ag.py"

##################################
# Utils
##################################

TEST_MODULES_MAP = {"calibration": ag.MODULE_CALIBRATION, "datapath": ag.MODULE_DATAPATH, "energy2400": ag.MODULE_ENERGY_2400, "energy_sub1g": ag.MODULE_ENERGY_SUB1G,
                    "pwr_mgmt": ag.MODULE_PWR_MGMT, "sensors": ag.MODULE_EXT_SENSORS, "custom": ag.MODULE_CUSTOM}

STATIC_RANDOM_ADDR_MASK = 0x0000000000C0
hex2alias_id_get = lambda id_str: cert_common.int2mac_get(int(id_str, 16) | STATIC_RANDOM_ADDR_MASK)

def module2name(module_id):
    for k, v in TEST_MODULES_MAP.items():
        if module_id == v:
            return k
    return ''

def load_module(module_name, module_path, rel_path="."):
    spec = importlib.util.spec_from_file_location(module_name, os.path.join(BASE_DIR, rel_path, module_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def handle_error(error, start_time):
    utPrint(error, "red")
    duration = (datetime.datetime.now()-start_time)
    cert_results.generate_results_files(html=True, pdf=True, start_time=start_time, duration=duration, error=error, pipeline=cert_common.pipeline_running())
    sys.exit(-1)

##################################
# Test
##################################
class WltTest:
    def __init__(self, line, gw, mqttc, brg0=None, brg1=None, exit_on_param_failure=False, gw_lan=False,
                 gw_orig_versions={}, server=PROD, latest=False, release_candidate=False, private_setup=False,
                 internal_brg_obj=None, gw_sim='', data='', port='', protobuf=False):
        if line:
            test_list_line = line.strip().split()
            self.name = test_list_line[0]
            self.test_module = TEST_MODULES_MAP[self.name.split('/')[0]] if self.name.split('/')[0] in TEST_MODULES_MAP else ag.MODULE_EMPTY
            line_params = test_list_line[1:]
            self.dir = os.path.join("tests", self.name)
            self.module_name = os.path.join(os.path.basename(self.name))
            self.file = os.path.join(self.dir, os.path.basename(self.name)+".py")
            # Load test json
            test_json_file = open(os.path.join(BASE_DIR, self.dir, os.path.basename(self.name)+".json"))
            self.test_json = json.load(test_json_file)
            self.gw_only = self.test_json[GW_ONLY_TEST]
            self.multi_brg = self.test_json[MULTI_BRG_TEST]
            self.internal_brg = INTERNAL_BRG_STR in line_params
            if INTERNAL_BRG_STR in line_params: line_params.remove(INTERNAL_BRG_STR)
            self.create_test_phases_and_params(line_params)
        else:
            self.test_json = {}
            self.internal_brg = False
            self.multi_brg = False
            self.phases = [Phase(PRE_CONFIG), Phase(TEST_BODY), Phase(RESTORE_CONFIG)]
            self.params = []

        self.gw = gw
        self.internal_brg_obj = internal_brg_obj
        # Actual brg to cfg - can be brg0 or brg1
        self.active_brg = brg0
        self.brg0 = brg0
        self.brg1 = brg1
        self.rc = TEST_PASSED
        self.reason = ""
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.mqttc = mqttc
        self.rtsa = ""
        self.exit_on_param_failure = exit_on_param_failure
        self.rand = random.randrange(255)
        self.gw_lan = gw_lan
        self.gw_orig_versions = gw_orig_versions
        self.server = server
        self.latest = latest
        self.release_candidate = release_candidate
        self.private_setup = private_setup
        self.gw_sim = gw_sim
        self.data = data
        self.port = port
        self.protobuf = protobuf

    def create_test_phases_and_params(self, line_params):
        self.params = []
        if len(self.test_json[ALL_SUPPORTED_VALUES]) > 0:
            self.phases = [Phase(PRE_CONFIG)] + [Phase(param) for param in self.test_json[ALL_SUPPORTED_VALUES]] + [Phase(RESTORE_CONFIG)]
            for param_phase in self.phases:
                param = Param(param_phase.name)
                if (param.name in line_params or param.value in [eval_param(p) for p in line_params]):
                    self.params += [param]
                else:
                    param_phase.tested = False
                    param_phase.rc = TEST_SKIPPED
            if all([param_phase.rc == TEST_SKIPPED for param_phase in self.phases]):
                error = f"ERROR: All params skipped for test {self.name}! Check test list file and update the supported values!\n{[f.__dict__ for f in self.phases]}"
                handle_error(error, datetime.datetime.now())
        else:
            if line_params:
                error = f"ERROR: For {self.name} params exist in test_list but not in test_json!\nline_params:{line_params}"
                handle_error(error, datetime.datetime.now())
            self.phases = [Phase(PRE_CONFIG), Phase(TEST_BODY), Phase(RESTORE_CONFIG)]

    # Phase rc
    def set_phase_rc(self, phase_name, rc):
        phase = self.get_phase_by_name(phase_name)
        phase.rc = rc
    
    def get_phase_rc(self, phase_name):
        phase = self.get_phase_by_name(phase_name)
        return phase.rc
    
    # Phase reason
    def add_phase_reason(self, phase_name, reason):
        phase = self.get_phase_by_name(phase_name)
        if phase.reason:
            phase.reason += "\n"
        if reason not in phase.reason:
            phase.reason += reason
    
    def get_phase_reason(self, phase_name):
        phase = self.get_phase_by_name(phase_name)
        return phase.reason

    # Test funcs
    def get_phase_by_name(self, phase_name):
        for phase in self.phases:
            if phase.name == phase_name:
                return phase
        return None
    
    def update_overall_rc(self):
        if any([phase.rc == TEST_FAILED for phase in self.phases]):
            self.rc = TEST_FAILED
    
    def reset_result(self):
        self.rc = TEST_PASSED
        self.reason = ""

    def get_seq_id(self):
        self.rand = (self.rand + 1) % 256
        return self.rand

    # TODO - remove when test reason is re-designed
    def add_reason(self, reason):
        if self.reason:
            self.reason += "\n"
        if reason not in self.reason:
            self.reason += reason

    def internal_id_alias(self):
        return self.internal_brg_obj.id_alias

##################################
# Phases
##################################
class Phase:
    def __init__(self, input=None, tested=True, rc=TEST_INIT, reason=""):
        self.name = str(input)
        self.tested = tested
        self.rc = rc
        self.reason = reason
    
    def __repr__(self):
        return self.name

##################################
# Param
##################################
class Param:
    def __init__(self, input=None):
        self.name = str(input)
        self.value = eval_param(input)
    
    def __repr__(self):
        return self.name

##################################
# Bridge
##################################
class Bridge:
    def __init__(self, id_str="", board_type=0, cfg_hash=0, api_version=ag.API_VERSION_LATEST, interface_pkt=None, import_defs=True, rel_path="."):
        self.id_str = id_str
        self.id_int = hex_str2int(id_str)
        self.id_alias = hex2alias_id_get(id_str)
        self.board_type = interface_pkt.board_type if interface_pkt else board_type
        self.version = f"{interface_pkt.major_ver}.{interface_pkt.minor_ver}.{interface_pkt.patch_ver}" if interface_pkt else ""
        self.bl_version = interface_pkt.bl_version if interface_pkt else ""
        self.cfg_hash = interface_pkt.cfg_hash if interface_pkt else cfg_hash
        self.api_version = interface_pkt.api_version if interface_pkt else api_version
        if import_defs:
            self.defines_file_name = f'{ag.BOARD_TYPES_LIST[self.board_type]}_defines.py'
            # Override auto-generated defines and classes for the specific bridge
            if os.path.exists(f"./ag/{self.defines_file_name}"):
                new_defines = load_module(self.defines_file_name, f"./ag/{self.defines_file_name}", rel_path)
            else:
                new_defines = load_module(ORIGINAL_AG_FILE, f"./ag/{ORIGINAL_AG_FILE}", rel_path)
            ag.__dict__.update(new_defines.__dict__)
        self.sup_caps = []
        self.modules = []
        if interface_pkt:
            for key, value in interface_pkt.__dict__.items():
                if 'sup_cap_' in key and value:
                    module = key.replace('sup_cap_','')
                    if module in TEST_MODULES_MAP:
                        self.sup_caps += [TEST_MODULES_MAP[module]]
                        self.modules += [eval_pkt(ag.MODULES_DICT[TEST_MODULES_MAP[module]] + str(self.api_version))]

    def update_modules(self):
        self.modules = []
        for sup_cap in self.sup_caps:
            self.modules += [eval_pkt(ag.MODULES_DICT[sup_cap] + str(self.api_version))]
    
    def is_sup_cap(self, test):
        return test.test_module in self.sup_caps if test.test_module and self.sup_caps else True


def cfg_brg_defaults_ret_after_fail(test):
    utPrint(f"Configuring bridge {test.active_brg.id_str} to defaults", "BLUE")
    modules = test.active_brg.modules
    for module in modules:
        utPrint(f"Configuring {module.__name__} to defaults", "BLUE")
        cfg_pkt = cert_config.get_default_brg_pkt(test, module)
        res = cert_config.brg_configure(test=test, cfg_pkt=cfg_pkt)[1]
        if res == NO_RESPONSE:
            utPrint(f"FAILURE: {module.__name__} configuration to defaults", "RED")
            return NO_RESPONSE
        else:
            utPrint(f"SUCCESS: {module.__name__} configured to defaults", "GREEN")
    return DONE

def handle_prep_brg_for_latest(test, interface, start_time):
    if test.rc == TEST_FAILED:
        utPrint(f"No ModuleIf pkts found, try again", "BLUE")
        test.rc = ""
        test, interface = cert_common.get_module_if_pkt(test)
    if test.rc == TEST_FAILED:
        error = f"ERROR: No ModuleIf pkts found for 2 tries, couldn't perform OTA for bridge"
        handle_error(error, start_time)
    version = f"{interface.major_ver}.{interface.minor_ver}.{interface.patch_ver}"
    board_type = interface.board_type
    utPrint(f"BRG version [{version}], board type [{board_type}]", "BLUE")
    utPrint(f"Skipping configurations for BRG {test.brg0.id_str} to defaults because of latest/rc flag", "BLUE")
    return Bridge(test.brg0.id_str, interface_pkt=interface)

# Check BRGs are online and configure to defaults
def ut_prep_brg(args, mqttc, start_time, gw, brg, gw_server, protobuf):
    brg = Bridge(brg)
    utPrint(SEP)
    if not args.port:
        versions_mgmt = load_module('versions_mgmt.py', f'{UTILS_BASE_REL_PATH}/versions_mgmt.py')
        brg_owner = versions_mgmt.gw_brg_owner(env="aws", server="prod", brg=brg.id_str)
        if brg_owner and not brg_owner in r_codes:
            print_warn(f"BRG {brg.id_str} owned by account {brg_owner}")
    test = WltTest("", gw, mqttc, brg0=brg, gw_lan=args.lan, server=gw_server, exit_on_param_failure=args.exit_on_param_failure,
                   protobuf=protobuf)
    utPrint(f"Getting BRG {brg.id_str} version and board type", "BLUE")
    test, interface = cert_common.get_module_if_pkt(test)
    if args.latest or args.rc:
        return handle_prep_brg_for_latest(test, interface, start_time)
    elif test.rc == TEST_FAILED:
        error = f"ERROR: Didn't get ModuleIfV{test.active_brg.api_version} from BRG:{brg.id_str}!"
        handle_error(error, start_time)
    version = f"{interface.major_ver}.{interface.minor_ver}.{interface.patch_ver}"
    board_type = interface.board_type
    utPrint(f"BRG version [{version}], board type [{board_type}]", "BLUE")
    test.active_brg = Bridge(brg.id_str, interface_pkt=interface)
    modules_support = []
    for module in TEST_MODULES_MAP:
        modules_support.append([module, color("GREEN", "SUPPORTED") if TEST_MODULES_MAP[module] in test.active_brg.sup_caps else color("RED", "UNSUPPORTED")])
    utPrint(f"BRG {brg.id_str} modules support coverage:", "BLUE")
    print(tabulate.tabulate(modules_support, headers=['Module', 'Support'], tablefmt="fancy_grid"))
    test.active_brg.board_type = board_type
    cfg_output = cfg_brg_defaults_ret_after_fail(test=test)[1]
    if cfg_output == NO_RESPONSE:
        error = f"ERROR: Didn't get response from BRG:{brg.id_str}!"
        handle_error(error, start_time)
    test, interface = cert_common.get_module_if_pkt(test)
    if test.rc == TEST_FAILED:
        error = f"ERROR: Didn't get ModuleIfV{test.active_brg.api_version} from BRG:{brg.id_str}!"
        handle_error(error, start_time)
    utPrint(f"Received cfg hash {hex(interface.cfg_hash)}", "BLUE")
    if not interface.cfg_hash or len(str(interface.cfg_hash)) < BRG_CFG_HAS_LEN:
        error = f"ERROR: invalid cfg_hash for BRG:{brg.id_str}!"
        handle_error(error, start_time)
    utPrint(f"BRG {brg.id_str} cfg_hash_default={hex(interface.cfg_hash)}", "BLUE")
    return Bridge(brg.id_str, interface_pkt=interface)

##################################
# Gateway
##################################
# Used when gw is not really important for the test (e.g: gw_sim)
def get_random_gw():
    return ''.join([random.choice('0123456789ABCDEF') for i in range(12)])

def get_gw_id(gw):
    if gw.startswith(GW_SIM_PREFIX) and len(gw) == len(GW_SIM_PREFIX):
        return f"GW_SIM_{get_random_gw()}"
    else:
        return gw

def ut_prep_gw(args, mqttc, start_time):
    # Check GW is online and configure to defaults
    utPrint(SEP)
    gw = args.gw
    test = WltTest("", gw, mqttc, gw_lan=args.lan)
    utPrint(f"Getting GW {gw} Information", "BLUE")
    response = cert_common.get_gw_info(test)
    if response == NO_RESPONSE:
        error = f"ERROR: Didn't get response from {gw} !"
        handle_error(error, start_time)
    if ENTRIES in response[GW_INFO]:
        # Protobuf
        test.protobuf = True
        gw_version = {BLE_VERSION : response[GW_INFO][ENTRIES][BLE_VERSION][STR_VAL], WIFI_VERSION : response[GW_INFO][ENTRIES][WIFI_VERSION][STR_VAL]}
        internal_brg_mac_addr = response[GW_INFO][ENTRIES][BLE_MAC_ADDR][STR_VAL]
        gw_server = response[GW_INFO][ENTRIES][WLT_SERVER][STR_VAL] if WLT_SERVER in response[GW_INFO][ENTRIES] else PROD
    else:
        test.protobuf = False
        gw_version = {BLE_VERSION : response[GW_INFO][BLE_VERSION], WIFI_VERSION : response[GW_INFO][WIFI_VERSION]}
        internal_brg_mac_addr = response[GW_INFO][BLE_MAC_ADDR]
        gw_server = response[GW_INFO][WLT_SERVER] if WLT_SERVER in response[GW_INFO] else PROD
    if gw_server != args.server:
        handle_error(f"ERROR: Test server [{args.server}] does not match GW server [{gw_server}]!", start_time)
    print(f"Starting UT with GW ID {test.gw} and internal BRG ID {internal_brg_mac_addr}")
    if not args.latest and not args.rc:
        res = cert_config.config_gw_defaults(test, version=gw_version)[1]
        if res == NO_RESPONSE:
            handle_error("ERROR: Config GW to defaults failed!", start_time)
    else:
        utPrint(f"Skipping configurations for GW {gw} to defaults because of latest/rc flag", "BLUE")
    internal_brg = ut_prep_brg(args, mqttc, start_time, gw, internal_brg_mac_addr, gw_server, test.protobuf)
    return gw, internal_brg, gw_server, gw_version, test.protobuf
