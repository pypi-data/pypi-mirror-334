# This test runs tx repetitions value = 0 to examine the algo
# the BRG cfg is meant to stretch the BRG tx queue so the algo is actively changing the tx rep val

from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
from brg_certificate.wlt_types import *
import brg_certificate.cert_common as cert_common
import brg_certificate.cert_config as cert_config
import os, statistics, math
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from brg_certificate.cert_gw_sim import DEDUPLICATION_PKTS

SCAN_TIME = 60 * 30

def track_tx_rep(test, sorted_database):
    tx_reps = []
    times = []
    for rep in sorted_database:
        val = sorted_database[rep]
        tx_reps.append(val[0])
        times.append(val[1])

    # Plotting the graph
    plt.plot(times, tx_reps)
    plt.xlabel(f'Time (total of {SCAN_TIME} seconds)')
    plt.ylabel('TX Repetitions')
    plt.title('TX Rep Algo - pkts rep over time')
    plt.grid(True)

    # Close the Matplotlib plot
    plt.close()

    # Create a line plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times, y=tx_reps, mode='lines'))
    # Add titles and labels
    fig.update_layout(
        title='TX Rep Algo - pkts rep over time',
        xaxis_title=f'Time (total of {SCAN_TIME} seconds)',
        yaxis_title='TX Repetitions',
        showlegend=False,
        template="plotly_white"
    )

    # Save the graph as an HTML file
    html_file_path = os.path.join(test.dir, "tx_rep_algo_graph.html")
    fig.write_html(html_file_path)

    return test, tx_reps

def tx_rep_analysis(test):
    # Clear data path
    cert_common.wait_time_n_print(CLEAR_DATA_PATH_TIMEOUT)
    test.mqttc.flush_pkts()

    # Collect pkts
    mqtt_scan_wait(test, SCAN_TIME)
    pkts = cert_mqtt.get_unified_data_pkts(test)
    print("Found {} unified packets".format(len(pkts)))

    # Count payloads
    pkt_payload_counter = {} # idx 0 - payload, idx 1 - payload ts
    for p in pkts:
        cur_pkt = p[PAYLOAD]
        if cur_pkt in pkt_payload_counter:
            pkt_payload_counter[cur_pkt] = (pkt_payload_counter[cur_pkt][0] + 1, pkt_payload_counter[cur_pkt][1])
        else:
            pkt_payload_counter[cur_pkt] = (1, p[TIMESTAMP])
    generate_log_file(test, "0")

    # Sort the data according to the time value
    sorted_database = dict(sorted(pkt_payload_counter.items(), key=lambda item: item[1][1]))
    test, tx_reps = track_tx_rep(test, sorted_database)

    # Calculate total average, top val & min val
    avg = statistics.mean(tx_reps)
    ceil = math.ceil(avg)
    floor = math.floor(avg)
    print(f"Avraged {avg} repetitions. ceil[{ceil}] floor[{floor}]")

    not_in_range = 0
    for i in tx_reps:
        if i > ceil or i < floor:
            not_in_range += 1
    if not_in_range:
        test.rc = TEST_FAILED
        test.add_reason(f"There are a total of {not_in_range} payloads outside the average (out of {len(tx_reps)})")
    print(f"total counted tx_reps[{tx_reps}]")
    return test

def run(test):

    test = cert_common.test_prolog(test)
    if test.rc == TEST_FAILED:
        return cert_common.test_epilog(test)

    datapath_module = eval_pkt(f'ModuleDatapathV{test.active_brg.api_version}')

    print("Configuring GW")
    # Set packets deduplication off to count the number of pkts from the BRG
    cert_config.gw_action(test, f"{DEDUPLICATION_PKTS} 0")
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        return cert_common.test_epilog(test, revert_gws=True)

    test = cert_config.brg_configure(test, fields=[BRG_TX_REPETITION, BRG_PACER_INTERVAL], values=[0, 1], module=datapath_module)[0]
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        return cert_common.test_epilog(test, revert_brgs=True, revert_gws=True, modules=[datapath_module])
    test = tx_rep_analysis(test)

    # Re-enable unified packets deduplication
    cert_config.gw_action(test, f"{DEDUPLICATION_PKTS} 1")
    return cert_common.test_epilog(test, revert_brgs=True, revert_gws=True, modules=[datapath_module])
