# External Imports
import time
import datetime
import os
import webbrowser
from jinja2 import Environment, FileSystemLoader
import pkg_resources
import time
import importlib.metadata
from wiliot_core.utils.utils import WiliotDir

# Internal Imports
from gw_certificate.common.analysis_data_bricks import initialize_logger
from gw_certificate.common.debug import debug_print
from gw_certificate.interface.ble_sniffer import BLESniffer
from gw_certificate.interface.uart_if import UARTError, UARTInterface
from gw_certificate.interface.ble_simulator import BLESimulator
from gw_certificate.interface.mqtt import MqttClient
from gw_certificate.tests import *
from gw_certificate.interface.uart_ports import get_uart_ports
from gw_certificate.api_if.gw_capabilities import GWCapabilities
from gw_certificate.tests import TESTS_NO_UART
import gw_certificate.cert_results as cert_results

GW_CERT_VERSION = importlib.metadata.version("wiliot-certificate")

class GWCertificateError(Exception):
    pass


class TemplateEngine:
    def __init__(self):
        self.template_dir = pkg_resources.resource_filename(__name__, 'templates')
        self.env = Environment(loader=FileSystemLoader(self.template_dir))

    def get_template(self, template_name):
        return self.env.get_template(template_name)

    def render_template(self, template_name, **kwargs):
        template = self.get_template(template_name)
        return template.render(**kwargs)


class GWCertificate:
    def __init__(self, gw_id, owner_id, actions:list, tests:list, topic_suffix='', update_fw=False, stress_pps=None,
                 aggregation_time=0, env='prod'):
        # Runtime
        self.env_dirs = WiliotDir()
        self.current_datetime = datetime.datetime.now()
        self.duration = None
        self.certificate_dir = os.path.join(self.env_dirs.get_wiliot_root_app_dir(), 'gw-certificate', self.current_datetime.strftime('%Y%m%d_%H%M%S'))
        self.env_dirs.create_dir(self.certificate_dir)
        self.logger_filename = initialize_logger(self.certificate_dir)
        self.logger_filepath = os.path.join(self.certificate_dir, f'{self.logger_filename}.log')
        self.mqtt_logger_filepath = os.path.join(self.certificate_dir, f'{self.logger_filename}_mqtt.log')
        self.sniffer_logger_filepath = os.path.join(self.certificate_dir, f'{self.logger_filename}_sniffer.log')
        self.result_html_path = os.path.join(self.certificate_dir, f'results_{self.current_datetime.strftime('%Y%m%d_%H%M%S')}.html')
        self.result_pdf_path = os.path.join(self.certificate_dir, f'results_{self.current_datetime.strftime('%Y%m%d_%H%M%S')}.pdf')
        self.template_engine = TemplateEngine()
        self.env = env

        # Version 
        self.gw_cert_version = GW_CERT_VERSION
        
        # GW & specific tests related
        self.gw_id = gw_id
        self.owner_id = owner_id
        self.topic_suffix = topic_suffix
        self.mqttc = MqttClient(gw_id, owner_id, self.mqtt_logger_filepath, topic_suffix=topic_suffix, broker='eclipse')
        self.gw_capabilities = GWCapabilities()
        self.stress_pps = stress_pps
        self.aggregation_time = aggregation_time
        self.actions = actions
        self.error = ""
        
        # UART-related. Require only when running tests that need it
        self.use_uart = not all(test in TESTS_NO_UART for test in tests)
        if self.use_uart:
            self.uart = None
            self.uart_comports = get_uart_ports()
            debug_print(f'UART Ports:{self.uart_comports}')
            if len(self.uart_comports) < 1:
                self.error = "A Wiliot certification kit must be connected to USB!"
                cert_results.generate_pdf_results_file(self)
                raise GWCertificateError(self.error)
        
            for port in self.uart_comports:
                try:
                    self.uart = UARTInterface(port, update_fw=update_fw)
                    break
                except UARTError as e:
                    debug_print(f'Port: {port} - {e}')
            if type(self.uart) is not UARTInterface:
                self.error = "Cannot initialize any port!"
                cert_results.generate_pdf_results_file(self)
                raise GWCertificateError(self.error)
            self.ble_sim = BLESimulator(self.uart)
            self.sniffer = BLESniffer(self.uart, logger_filepath=self.sniffer_logger_filepath)
        
        # Tests
        self.tests = [t(**self.__dict__) for t in tests]
        debug_print(f'Running Tests: {self.tests}')

    def runtime(self):
        datetime.timedelta
        return datetime.datetime.now() - self.current_datetime
    
    def run_tests(self):
        debug_print("Sleeping 20 seconds after mqtt connect")
        time.sleep(20)

        # capabilities_received = ConnectionTest in self.tests
        for test in self.tests:
            # if capabilities_received:
            #     if (type(test) == DownlinkTest and self.gw_capabilities.downlinkSupported == False):
            #         debug_print(f'# Skipping {type(test)} since it is not a supported capability. #')
            #         continue
            test.prepare_test()
            test.run()
            test.end_test()
        
    def create_results_html(self):
        with open(self.logger_filepath, 'r') as f:
            log = f.read().split('\n')
        with open(self.mqtt_logger_filepath, 'r') as f:
            mqtt_log = f.read().split('\n')
        if self.use_uart:
            with open(self.sniffer_logger_filepath, 'r') as f:
                sniffer_log = f.read().split('\n')
        else:
            sniffer_log = []

        
        html = self.template_engine.render_template('results.html', tests=self.tests,
                                                    log = log,
                                                    mqtt_log = mqtt_log,
                                                    sniffer_log = sniffer_log,
                                                    gw_id = self.gw_id,
                                                    version = self.gw_cert_version,
                                                    datetime = self.current_datetime.strftime('%Y%m%d_%H%M%S'))
        with open(self.result_html_path, 'w', encoding="utf-8") as f:
            f.write(html)
        cert_results.generate_pdf_results_file(self)
        debug_print("Test Finished. Results HTML Saved: " + self.result_html_path)
        webbrowser.open('file://' + os.path.realpath(self.result_html_path))
        webbrowser.open('file://' + os.path.realpath(self.result_pdf_path))

if __name__ == "__main__":
    from api_secrets import *
    gw_id = 'gw_id'
    owner_id = 'owner_id'
    gwc = GWCertificate(gw_id=gw_id,owner_id=owner_id, tests=[ConnectionTest, DownlinkTest, UplinkTest, StressTest])
    gwc.run_tests()
    gwc.create_results_html()