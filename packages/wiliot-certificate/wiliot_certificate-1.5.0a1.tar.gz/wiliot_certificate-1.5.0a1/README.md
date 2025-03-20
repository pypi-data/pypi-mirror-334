# wiliot-certificate

<!-- Description -->
wiliot-certificate is a python library with tools used to test & certify boards and their compatibility with Wiliot's echosystem.
This python package includes the following CLI utilities:
 - Gateway Certificate (`wlt-gw-certificate`)
 - Bridge Certificate (`wlt-cert-brg`)

## Installing wiliot-certificate
````commandline
pip install wiliot-certificate
````

## Using wiliot-certificate
### Gateway Certificate
Test Wiliot GWs capabilities.
The GW Certificate includes different test that run sequentially to test each capability reported by the GW.
To run the GW Certificate the GW needs to use a public MQTT Broker (Eclipse):

Host:	mqtt.eclipseprojects.io
TLS TCP Port:	8883
TLS Websocket Port:	443
TCP Port:	1883
Websocket Port:	80

More information can be found at https://mqtt.eclipseprojects.io/.

#### Connection Test
Processes status packet sent by the GW to the MQTT Broker and validates it according to API Version.

#### Uplink Test
Simulates Wiliot MEL and validates that data is uploaded correctly to the cloud.

#### Downlink Test
Sends advertising actions (txPacket) via MQTT to the GW and validates their advertisements.

#### Stress Test
Increments time delays between packets to evaluate GW's capability in handling increasing packets per second rates.

#### GW Certificate Release Notes:
1.4.0:
 - Released in a standalone wiliot-certificate package
 - Python 3.13 support
 - Gw API version 205 support
 - Registration test added
 - Bridge OTA stage added under actions
 - Aggregation flag supported by StressTest
 - -update flag compatibility fix. Upgrades bootloader as well
 - -actions flag to select specific actions to test

```
usage: wlt-gw-certificate [-h] -owner OWNER -gw GW [-suffix SUFFIX] [-tests {connection,uplink,downlink,stress}]

Gateway Certificate - CLI Tool to test Wiliot GWs

required arguments:
  -gw GW        Gateway ID

optional arguments:
  -owner OWNER  Owner ID (Required for non-registration tests)
  -tests        Pick specific tests to run
  -actions      Pick specific actions to test during the ActionsTest
  -update       Update the firmware of the test board
  -pps          Pick specific PPS rate for the stress test
  -agg          Time the uplink stages should wait before processing packets
  -suffix       Allow for different suffixes after the GW ID in MQTT topics
  -env          Wiliot envrionment for Registration and bridgeOTA tests
  -h, --help    show this help message and exit
  ```

### Bridge Certificate
Test Wiliot BRGs capabilities.
The BRG Certificate includes different tests that run sequentially to test each capability reported by the BRG.
The BRG Certificate tool uses a public MQTT Broker (Eclipse):

Host:	mqtt.eclipseprojects.io
TLS TCP Port:	8883
TLS Websocket Port:	443
TCP Port:	1883
Websocket Port:	80

More information can be found at https://mqtt.eclipseprojects.io/.

#### XXX Test
TEST EXPLANATION

#### BRG Certificate Release Notes:
1.3.0:
 - FIRST VERSION


```
usage: wlt-cert-brg [-h] [-h] [-b BRG] [-b1 BRG1] --gw GW [--data {tags,sim}] [--port PORT] [--clean] [--tl TL] [--run RUN] [--drun DRUN] [--exit_on_test_failure] [--exit_on_param_failure] [--analyze_interference]

Gateway Certificate - CLI Tool to test Wiliot BRGs

required arguments:
  --gw, -g GW        Gateway ID
  --port, -p PORT    COM Port
  --brg, -b BRG      Bridge ID

optional arguments:
  --brg1, -b1 BRG1                              Second bridge id to run on tests two bridges needed
  --data, -d {tags,sim}                         Choose if data generated from real tags or by simulation
  --port, -p PORT                               Enable UT using UART connection for Gateway Simulation or Data Simulation
  --clean                                       Clean all logs
  --tl TL                                       Test list file to use
  --run RUN                                     String to filter tests to run
  --drun DRUN                                   String to filter tests not to run
  --exit_on_test_failure                        Stop running the tests if a test failed
  --exit_on_param_failure                       Sets exit_on_param_failure mode to true in order to prevent tests from continuing iteration over all possibilities in case of failure
  --analyze_interference, -ai                   Analyze interference before tests start (relevant only for Gateway Simulator)
  ```
