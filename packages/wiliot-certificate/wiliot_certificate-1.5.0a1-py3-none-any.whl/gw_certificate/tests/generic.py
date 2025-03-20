import datetime
import os
from typing import Literal
import math

from gw_certificate.common.debug import debug_print
from gw_certificate.api_if.gw_capabilities import GWCapabilities
from gw_certificate.interface.ble_simulator import BLESimulator
from gw_certificate.interface.mqtt import MqttClient
from gw_certificate.ag.ut_defines import TEST_PASSED, TEST_FAILED, TEST_INCONCLUSIVE, TEST_OPTIONAL, TEST_WARNING, TEST_INFO

PASS_STATUS = {True: 'PASS', False: 'FAIL'}

# Score values for pass/inconclusive/fail
PERFECT_SCORE = 100
PASS_MINIMUM = 80
INCONCLUSIVE_MINIMUM = 70
INIT_INCONCLUSIVE_MINIMUM = 40
MINIMUM_SCORE = 0

# Results indications for stages. Must always be synced with frontend. 
# 'score' shows as pass/inconclusive/fail. 'info' shows as info/warning.
SCORE_BASED = 'score'
INFORMATIVE = 'info'
OPTIONAL = 'optional'

ERR_SUMMARY_DEFAULT = 'View the stage report for more info. '

class PassCriteria():
    def __init__(self):
        pass
        
    @staticmethod
    def to_string(pass_value:int) -> str:
        if pass_value >= PASS_MINIMUM:
            return 'Pass'
        elif pass_value >= INCONCLUSIVE_MINIMUM:
            return 'Inconclusive'
        else:
            return 'Fail'
    
    @staticmethod
    def calc_for_stage_downlink(rsquared, slope, stage_name:str):
        error_msg = ''
        if 'Sanity' in stage_name:
            if not math.isnan(rsquared) and rsquared != 0:
                return PERFECT_SCORE, error_msg
            else:
                error_msg = 'No advertisements were received from the gateway.'
                return MINIMUM_SCORE, error_msg
        else:
            if rsquared > 0.8 and slope > 0:
                return PERFECT_SCORE, error_msg
            elif rsquared > 0.5 and slope > 0:
                error_msg = "The correlation between 'txMaxDuration' and the board advertisements is suboptimal."
                return INCONCLUSIVE_MINIMUM, error_msg
            else:
                error_msg = "The correlation between 'txMaxDuration' and the board advertisements is weak."
                return MINIMUM_SCORE, error_msg

    @staticmethod
    def calc_for_test(test, stage) -> int:
        # Some stages shouldn't affect test score
        if 'Geolocation' in stage.stage_name or 'info' in stage.result_indication:
            return test.test_pass

        if stage.score_inconclusive() and test.score_pass():
            return test.inconclusive_min
        elif stage.score_fail():
            return MINIMUM_SCORE
        else:
            return test.test_pass


class GenericTest:
    def __init__(self, mqttc: MqttClient, 
                 gw_capabilities:GWCapabilities, gw_id, owner_id, test_name, ble_sim: BLESimulator = None, **kwargs):
        # Clients
        self.mqttc = mqttc
        self.ble_sim = ble_sim
        
        # Test-Related
        self.gw_capabilities = gw_capabilities
        self.report = ''
        self.report_html = ''
        self.test_pass = PERFECT_SCORE
        self.pass_min = PASS_MINIMUM
        self.inconclusive_min = INCONCLUSIVE_MINIMUM
        self.start_time = None
        self.duration = None
        self.test_name = test_name
        self.test_dir = os.path.join(self.certificate_dir, self.test_name)
        self.env_dirs.create_dir(self.test_dir)
        self.stages = []
        self.test_tooltip = kwargs.get('test_tooltip', 'Missing tooltip')
        self.result_indication = kwargs.get('result_indication', SCORE_BASED)
        self.rc = TEST_PASSED
        
    def __repr__(self):
        return self.test_name
    
    def prepare_test(self):
        pass
    
    def run(self):
        self.start_time = datetime.datetime.now()
        debug_print(f"Starting Test {self.test_name} : {self.start_time}")
        
    def runtime(self):
        return datetime.datetime.now() - self.start_time
    
    def add_to_test_report(self, report):
        self.report += '\n' + report
    
    def create_test_html(self):
        self.report_html = self.template_engine.render_template('test.html', test=self,
                                                                running_time = self.runtime())

    def end_test(self):
        self.determine_rc()
        for stage in self.stages:
            stage.determine_rc()
        self.duration = self.runtime()
        self.create_test_html()

    def score_pass(self):
        if self.test_pass >= self.pass_min:
            return True
        return False

    def score_inconclusive(self):
        if self.inconclusive_min <= self.test_pass < self.pass_min:
            return True
        return False
    
    def score_fail(self):
        if self.test_pass < self.inconclusive_min:
            return True
        return False
    
    def determine_rc(self):
        # Set test rc - defaults to TEST_PASSED (rc=0)
        if self.result_indication == 'info':
            if self.score_pass():
                self.rc = TEST_INFO
            else:
                self.rc = TEST_WARNING
        elif self.result_indication == 'optional':
            self.rc = TEST_OPTIONAL
        else:
            if self.score_inconclusive():
                self.rc = TEST_INCONCLUSIVE
            elif self.score_fail():
                self.rc = TEST_FAILED


class GenericStage():
    def __init__(self, stage_name, **kwargs):
        #Stage Params
        self.stage_name = stage_name
        self.result_indication = kwargs.get('result_indication', SCORE_BASED)
        self.stage_pass = MINIMUM_SCORE
        self.pass_min = kwargs.get('pass_min', PASS_MINIMUM)
        self.inconclusive_min = INCONCLUSIVE_MINIMUM
        self.report = ''
        self.report_html = ''
        self.start_time = None
        self.duration = None
        self.csv_path = os.path.join(self.test_dir, f'{self.stage_name}.csv')
        self.stage_tooltip = kwargs.get('stage_tooltip', 'Missing tooltip')
        self.error_summary = kwargs.get('error_summary', ERR_SUMMARY_DEFAULT)
        self.rc = TEST_PASSED
        
    def __repr__(self):
        return self.stage_name
    
    def prepare_stage(self):
        debug_print(f'### Starting Stage: {self.stage_name}')

    def run(self):
        self.start_time = datetime.datetime.now()

    def add_to_stage_report(self, report):
        self.report += f'{report}\n'
    
    def generate_stage_report(self):
        return self.report
    
    def add_report_line_separator(self):
        self.add_to_stage_report('-' * 50)
    
    def add_report_header(self):
        uncapitalize = lambda s: s[:1].lower() + s[1:] if s else ''
        self.duration = datetime.datetime.now() - self.start_time
        self.add_to_stage_report(f'Stage run time: {self.duration}')
        self.add_to_stage_report(f'This stage {uncapitalize(self.stage_tooltip)}.')
        self.add_report_line_separator()
    
    def add_report_topic_validation(self, topic:Literal['status', 'data']):
        pass
        # Pass until validated
        if self.topic_suffix != '':
            return
        valid_topic, invalid_msg, invalid_topic = self.mqttc.validate_serialization_topic(topic)
        if valid_topic == False:
            # For now not failing stage since the customBroker command include topics explicitly
            # self.stage_pass = MINIMUM_SCORE
            # self.error_summary += "Invalid serialization-topic combination. "
            self.add_to_stage_report(f'Note: Received message on {invalid_topic} although serialization is {self.mqttc.get_serialization()}')
    
    def score_pass(self):
        if self.stage_pass >= self.pass_min:
            return True
        return False

    def score_inconclusive(self):
        if self.inconclusive_min <= self.stage_pass < self.pass_min:
            return True
        return False
    
    def score_fail(self):
        if self.stage_pass < self.inconclusive_min:
            return True
        return False
            
    def determine_rc(self):
        # Set stage rc - defaults to TEST_PASSED (rc=0)
        if self.result_indication == 'info':
            if self.score_pass():
                self.rc = TEST_INFO
            else:
                self.rc = TEST_WARNING
        else:
            if self.score_inconclusive():
                self.rc = TEST_INCONCLUSIVE
            elif self.score_fail():
                self.rc = TEST_FAILED
