from gw_certificate.tests.registration import RegistrationTest
from gw_certificate.tests.connection import ConnectionTest
from gw_certificate.tests.uplink import UplinkTest
from gw_certificate.tests.downlink import DownlinkTest 
from gw_certificate.tests.actions import ActionsTest
from gw_certificate.tests.throughput import StressTest

TESTS = [RegistrationTest, ConnectionTest, UplinkTest, DownlinkTest, ActionsTest, StressTest]

TESTS_NO_UART = [RegistrationTest]
