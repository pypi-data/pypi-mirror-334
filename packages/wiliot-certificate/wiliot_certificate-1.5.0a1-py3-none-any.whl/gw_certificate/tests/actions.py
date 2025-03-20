import datetime
import os
import time
import pandas as pd

from packaging import version

from gw_certificate.common.debug import debug_print
from gw_certificate.interface.mqtt import MqttClient, GwAction
from gw_certificate.tests.generic import PassCriteria, PERFECT_SCORE, MINIMUM_SCORE, INCONCLUSIVE_MINIMUM, GenericTest, GenericStage, OPTIONAL
from gw_certificate.tests.static.references import GW_ACTIONS_DOC, GW_BRIDGE_OTA_DOC
from gw_certificate.ag.ut_defines import STATUS_CODE_STR
from gw_certificate.interface.uart_if import FIRST_UNIFIED_BL_VERSION, UARTError


BL_INACTIVITY_TIMEOUT_SEC = 120


class GenericActionsStage(GenericStage):
    def __init__(self, mqttc:MqttClient, stage_name, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(stage_name=stage_name, **self.__dict__)        
        
        #Clients
        self.mqttc = mqttc
        
        #Stage Params
        self.action = ""
        
        #Paths
        self.summary_csv_path = os.path.join(self.test_dir, f'{self.stage_name}_summary.csv')

        
    def prepare_stage(self):
        super().prepare_stage()
        self.mqttc.flush_messages()
    
    def generate_stage_report(self):
        self.add_report_header()

class GatewayInfoStage(GenericActionsStage):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, stage_name=type(self).__name__)
        self.stage_tooltip = "Issues a Gateway Info action to the gateway. Expects the gateway to publish a response"
        self.error_summary = "Did not receive a response to the Gateway Info action"
        self.action = "getGwInfo"
        self.response = None
    
    def run(self):
        super().run()
        timeout = datetime.datetime.now() + datetime.timedelta(seconds=20)
        self.gw_info = None
        self.mqttc.flush_messages()

        self.mqttc.send_action(GwAction.GET_GW_INFO)
        while datetime.datetime.now() < timeout and self.gw_info is None:
            self.gw_info = self.mqttc.get_gw_info_message()
            time.sleep(5)


    def generate_stage_report(self):
        super().generate_stage_report()

        # Calculate whether stage pass/failed
        if self.gw_info == None:
            self.stage_pass = MINIMUM_SCORE
            self.add_to_stage_report(f'Did not receive a response to the Gateway Info action. For more info visit:')
            self.add_to_stage_report(f'{GW_ACTIONS_DOC}')
        else:
            self.stage_pass = PERFECT_SCORE
            self.response = repr(self.gw_info)
            self.add_to_stage_report('A Gateway Info response was receieved:')
            self.add_to_stage_report(self.response)

        # Export all stage data
        csv_data = {'Action': [self.action], 'Response': [self.response], 'Pass': [self.stage_pass > self.pass_min]}
        pd.DataFrame(csv_data).to_csv(self.summary_csv_path)
        self.add_to_stage_report(f'\nStage summary saved - {self.summary_csv_path}')
        debug_print(self.report)
        
        # Generate HTML
        self.report_html = self.template_engine.render_template('stage.html', stage=self, 
                                                                stage_report=self.report.split('\n'))
        return self.report


class RebootStage(GenericActionsStage):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, stage_name=type(self).__name__)
        self.stage_tooltip = "Issues reboot action to the gateway. Expects it to reboot"
        self.error_summary = "The gateway did not reboot as expected"
        self.action = "rebootGw"
    
    def run(self):
        super().run()
        timeout = datetime.datetime.now() + datetime.timedelta(minutes=3)
        self.status_message = None

        debug_print("Sending a reboot action to the gateway and awaiting reboot.. (timeout = 3)")
        self.mqttc.send_action(GwAction.REBOOT_GW)
        while datetime.datetime.now() < timeout and self.status_message is None:
            self.status_message = self.mqttc.get_status_message()
            time.sleep(5)

    def generate_stage_report(self):
        super().generate_stage_report()

        # Calculate whether stage pass/failed
        if self.status_message is None:
            self.stage_pass = MINIMUM_SCORE
            self.add_to_stage_report(f"The gateway did not validly reboot")
            self.add_to_stage_report(f"Gateways are expected to upload a status(configuration) message upon establishing MQTT connection, which wasn't received.")
        else:
            self.stage_pass = PERFECT_SCORE
            self.add_to_stage_report(f"Gateway rebooted and uploaded a configuration message, as expected.")
        
        # Export all stage data
        csv_data = {'Action': [self.action], 'Pass': [self.stage_pass > self.pass_min]}
        pd.DataFrame(csv_data).to_csv(self.summary_csv_path)
        self.add_to_stage_report(f'\nStage summary saved - {self.summary_csv_path}')

        # Generate HTML
        self.report_html = self.template_engine.render_template('stage.html', stage=self, 
                                                                stage_report=self.report.split('\n'))
        return self.report

class BridgeOTAStage(GenericActionsStage):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, stage_name=type(self).__name__)
        self.stage_tooltip = "Issues a bridge OTA action to the gateway. Expects it to upgrade the bridge"
        self.error_summary = "The target bridge was not upgraded"
        self.action = "Bridge Upgrade"

        OTA_VERSIONS_TO_USE = ("4.4.52", "4.4.53")
        if version.parse(OTA_VERSIONS_TO_USE[0]) != self.uart.fw_version:
            self.desired_version = version.parse(OTA_VERSIONS_TO_USE[0])
        else:
            self.desired_version = version.parse(OTA_VERSIONS_TO_USE[1])
    
    def prepare_stage(self):
        super().prepare_stage()
        debug_print(f"Important: For the gateway to be able to download the file, it must use a valid token in the HTTP GET request.")
        debug_print(f"Meaning It must be registered under an owner, and the certificate '-env' should correspond to that owner.")
        debug_print(f"BridgeOTAStage attempt: {str(self.uart.fw_version)} -> {str(self.desired_version)}")
        # Reset to remove any log/cert mode we had in the kit so it behaves as a bridge
        self.uart.reset_gw()

    def run(self):
        super().run()
        timeout = datetime.datetime.now() + datetime.timedelta(minutes=10)
        self.action_status = None
        self.status_code = None
        self.reboot_packet_ts = None
        self.action_status_ts = None

        self.mqttc.send_bridge_ota_action(self.uart.mac, str(self.desired_version), 200, False, self.gw_id, "aws", self.env)
        debug_print("Sent a BridgeOTA action to the gateway")
        debug_print("Waiting for an actionStatus message from the gateway... (timeout=10)")
        while datetime.datetime.now() < timeout and self.action_status is None:
            line = self.uart.read_line()
            if line != None and 'reset' in line:
                self.uart.reset_gw(stop_advertising=False)
                self.reboot_packet_ts = datetime.datetime.now()
                debug_print("A reboot packet was received by the bridge")
            self.action_status = self.mqttc.get_action_status_message()
            time.sleep(2)
        
        if self.action_status != None:
            debug_print("actionStatus was received from the gateway")
            self.action_status_ts = datetime.datetime.now()
            self.status_code = self.action_status.get(STATUS_CODE_STR)
            if self.status_code == None:
                self.status_code = self.action_status.get('status')
            
            if self.status_code != 0 and self.reboot_packet_ts != None:
                debug_print(f"Reported status {self.status_code} indicates failure, waiting for the bridge bootloader inactivity timer (2 minutes)..")
                time.sleep(BL_INACTIVITY_TIMEOUT_SEC)

            debug_print('Waiting for the bridge to boot...')
            time.sleep(40)

        cur_ver = self.uart.get_version()
        if cur_ver == None:
            debug_print("ERROR: The certificate kit, acting as bridge in this stage, is not responding!")
            self.uart.flush()
            cur_ver = self.uart.get_version()
            if cur_ver == None:
                raise UARTError("Communication to the certificate kit halted! "
                                "Please unplug and replug its power source, wait for 5 minutes and retry. "
                                "If the error persist, contact Wiliot Support and attach your results directory.")
        self.current_version = version.parse(cur_ver)

    def generate_stage_report(self):
        super().generate_stage_report()

        # Calculate whether stage pass/failed
        if self.action_status is None or self.status_code != 0:
            self.stage_pass = MINIMUM_SCORE
            self.add_to_stage_report(f"The bridge OTA test failed")
            if self.action_status is None:
                self.add_to_stage_report(f"Gateways are expected to upload an actionStatus message upon establishing MQTT connection, which wasn't received.")
            elif self.status_code is None:
                self.add_to_stage_report(f"Uploaded actionStatus messages should contain the status field, which wasn't detected.")
            elif self.status_code != 0:
                self.add_to_stage_report(f"Uploaded actionStatus status value received is {self.status_code}.")
            if self.current_version == self.desired_version:
                self.add_to_stage_report(f"Note that the bridge was actually upgraded successfully.")
            self.add_to_stage_report(f"{GW_BRIDGE_OTA_DOC}")
        else:
            if self.current_version == self.desired_version:
                self.stage_pass = PERFECT_SCORE
                self.add_to_stage_report(f"Bridge was upgraded and an actionStatus message was received from the gateway.")
                self.add_to_stage_report(f"Action status received {(self.action_status_ts - self.start_time).total_seconds():.1f}s after start.")
                self.add_to_stage_report(f"Reboot packet received {(self.reboot_packet_ts - self.start_time).total_seconds():.1f}s after start.")
                self.add_to_stage_report(f"Action status received {(self.action_status_ts - self.reboot_packet_ts).total_seconds():.1f}s after reboot.")
            else:
                self.stage_pass = MINIMUM_SCORE
                self.add_to_stage_report(f"The bridge OTA test failed")
                self.add_to_stage_report(f"Uploaded actionStatus message indicated success although the bridge was not upgraded.")

        # Export all stage data
        csv_data = {'Action': [self.action], 'Pass': [self.stage_pass > self.pass_min]}
        if self.stage_pass == PERFECT_SCORE:
            csv_data.update({'start_ts': self.start_time, 'reboot_packet_ts': self.reboot_packet_ts, 'action_status_ts': self.action_status_ts})
        pd.DataFrame(csv_data).to_csv(self.summary_csv_path)
        self.add_to_stage_report(f'\nStage summary saved - {self.summary_csv_path}')

        # Generate HTML
        self.report_html = self.template_engine.render_template('stage.html', stage=self, 
                                                                stage_report=self.report.split('\n'))
        return self.report

ACTIONS_STAGES = [GatewayInfoStage, RebootStage, BridgeOTAStage]

class ActionsTest(GenericTest):
    def __init__(self, **kwargs):        
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, test_name=type(self).__name__)
        self.test_tooltip = "Stages publishing different actions (via the 'update' topic). Optional"
        self.result_indication = OPTIONAL
        # Actions stages are determined by the CLI argument
        stages = self.actions

        if BridgeOTAStage in stages and self.uart.fw_version < FIRST_UNIFIED_BL_VERSION:
            debug_print("Certificate kit's firmware should be upgraded with the '-update' flag to run the BridgeOTAStage")
            stages.remove(BridgeOTAStage)
        self.stages = [stage(**self.__dict__) for stage in stages]
    
    def run(self):
        super().run()
        for stage in self.stages:
            stage.prepare_stage()
            stage.run()
            self.add_to_test_report(stage.generate_stage_report())
            self.test_pass = PassCriteria.calc_for_test(self, stage)
