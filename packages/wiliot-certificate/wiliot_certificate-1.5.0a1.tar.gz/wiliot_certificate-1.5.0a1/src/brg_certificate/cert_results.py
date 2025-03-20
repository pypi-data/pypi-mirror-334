import os
import tabulate
import subprocess
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# Local imports
import brg_certificate.cert_utils as cert_utils
import brg_certificate.cert_prints as cert_prints
from brg_certificate.cert_defines import BASE_DIR
from brg_certificate.cert_defines import CERT_VERSION, TEST_FAILED, TEST_SKIPPED, TEST_PASSED, TEST_INIT, UT_RESULT_FILE_HTML, UT_RESULT_FILE_PDF


##################################
# GENERIC
##################################
result_map = {TEST_FAILED: cert_prints.color("RED", "FAIL"), TEST_SKIPPED: cert_prints.color("WARNING", "SKIPPED"),
              TEST_PASSED: cert_prints.color("GREEN", "PASS"), TEST_INIT: cert_prints.color("CYAN", "INIT")}
pass_or_fail = lambda obj : result_map[obj.rc]
class TestResult:
    def __init__(self, name="", devices_to_print="", test_table=None, result=None, duration=0):
        self.name = name
        self.devices = devices_to_print
        self.result = result
        self.test_table = test_table
        self.duration = duration
    
    def __repr__(self):
        return self.name

def generate_tests_table(tests=[], html=False):
    headers = ["Module", "Test Name", "Device", "Result Breakdown", "Result", "Run Time"]
    inner_format = "unsafehtml" if html else "simple"
    _pass_or_fail = pass_or_fail_html if html else pass_or_fail
    tests_results = []
    for test in tests:
        brgs_to_print = (test.gw if not test.brg0 or test.gw_only else
                         (f"{test.brg0.id_str}\n{test.brg1.id_str}" if test.brg1 and test.multi_brg else test.brg0.id_str))
        inner_table = [[phase.name, _pass_or_fail(phase), phase.reason] for phase in test.phases]
        result_breakdown_table = tabulate.tabulate(inner_table, headers=["Phase", "Result", "Notes"], tablefmt=inner_format)
        tests_results.append([cert_utils.module2name(test.test_module),
                              test.module_name if (not test.internal_brg or "gw" in test.module_name) else f"{test.module_name} (internal brg)",
                              brgs_to_print,
                              result_breakdown_table,
                              _pass_or_fail(test),
                              test.duration])
    return tabulate.tabulate(tests_results, headers=headers, tablefmt="unsafehtml" if html else "fancy_grid")

def get_update_status_from_log_file(log_file="update_log.txt"):
    update_status = "No version update logs were found"
    if os.path.isfile("update_log.txt"):
        with open(os.path.join(BASE_DIR, log_file), "r") as update_log:
            for l in update_log.readlines():
                if "ERROR: Didn't get response from BRG" in l:
                    update_status = "Didn't get response from BRG in order to start the update!"
                    break
                elif "ERROR: Didn't get response from" in l:
                    update_status = "Didn't get response from GW in order to start the update!"
                    break
                elif "version_update_test failed!" in l:
                    update_status = "GW version update failed!"
                    break
                elif "ota_test failed!" in l:
                    update_status = "BRG OTA failed!"
                    break
                elif "PASSED!" in l:
                    update_status = "GW and BRG versions were updated to latest successfully!"
                    break
                elif "SKIPPED!" in l:
                    update_status = "GW and BRG versions update skipped!"
                    break
    return update_status

def generate_results_files(html=True, pdf=True, failures=0, skipped=0, start_time=0, duration=0, brg='', brg_version='', gw_ble_version = '', gw_ble_mac='', tests=[], error=None, pipeline=False):
    # Generate HTML file
    if html:
        f = open(os.path.join(BASE_DIR, UT_RESULT_FILE_HTML), "w", encoding="utf-8")
        f.write(HTML_START)
        update_status = get_update_status_from_log_file()
        if pipeline:
            p = subprocess.Popen('git log --format=%B -n 1 {}'.format(os.environ['BITBUCKET_COMMIT']),
                                stdout=subprocess.PIPE, shell=True, cwd=os.environ['BITBUCKET_CLONE_DIR'])
            output, err = p.communicate()
        if error:
            f.write("<br><h1 style='color:#ab0000'>Wiliot Certificate Error!</h1><br>")
            if pipeline:
                f.write("<hr>" + output.decode("utf-8") + "<br>")
                f.write("<p><a href='https://bitbucket.org/wiliot/wiliot-nordic-firmware/commits/{}'>Commit page on bitbucket</a><hr>".format(os.environ['BITBUCKET_COMMIT']))
            f.write(update_status + "<br><br>")
            f.write(error + "<br><br>")
            f.write("Run duration: {} <br><br>".format(str(duration).split(".")[0]))
            if brg_version:
                f.write("Bridge version: {} <br><br>".format(brg_version))
        elif tests:
            if not failures and ("successfully!" in update_status or "skipped!" in update_status or not pipeline):
                f.write("<br><h1 style='color:#00AB83'>Wiliot Certificate Passed!</h1>")
            else:
                f.write("<br><h1 style='color:#ab0000'>Wiliot Certificate Failed!</h1>")
            if pipeline:
                f.write("<hr>" + output.decode("utf-8") + "<br>")
                f.write("<p><a href='https://bitbucket.org/wiliot/wiliot-nordic-firmware/commits/{}'>Commit page on bitbucket</a><hr>".format(os.environ['BITBUCKET_COMMIT']))
                f.write(update_status + "<br><br>")
            f.write("Run date: {} <br><br>".format(start_time.strftime('%d/%m/%Y, %H:%M:%S')))
            f.write("Tests duration: {} <br><br>".format(str(duration).split(".")[0]))
            f.write("Certificate version: {} <br><br>".format(CERT_VERSION))
            if gw_ble_mac:
                f.write("BLE simulator mac: {} <br><br>".format(gw_ble_mac))
            if gw_ble_version:
                f.write("BLE simulator version: {} <br><br>".format(gw_ble_version))
            f.write("Tested bridge ID: {} <br><br>".format(brg))
            if brg_version:
                f.write("Bridge version: {} <br><br>".format(brg_version))
            f.write(tabulate.tabulate([[len(tests)-(failures+skipped), skipped, failures, len(tests)]], headers=["PASSED", "SKIPPED", "FAILED", "TOTAL"], tablefmt="html"))
            f.write(generate_tests_table(tests, html=True))
            f.write("<br><br>")
        if pipeline:
            f.write("<p><a href='https://bitbucket.org/wiliot/wiliot-nordic-firmware/pipelines/results/{}'>Build's page and artifacts on bitbucket</a></p><br><br>".format(os.environ['BITBUCKET_BUILD_NUMBER']))
        f.write("<img src='https://www.wiliot.com/src/img/svg/logo.svg' width='100' height='40' alt='Wiliot logo'>")
        f.write(HTML_END)
        f.close()
    
    # Generate PDF file
    if pdf:
        doc = SimpleDocTemplate(os.path.join(BASE_DIR, UT_RESULT_FILE_PDF), pagesize=letter)
        doc.title = "Wiliot Certificate Results"
        elements, hdr_page = [], []

        # Add Wiliot Logo
        img = Image(os.path.join(BASE_DIR, "../common", "wlt_logo.png"), width=100, height=40)  # Adjust size as needed
        hdr_page.append(img)
        hdr_page.append(Spacer(1, 20))

        # Title and Summary
        red_header = STYLES_PDF.get("RED_HEADER", ParagraphStyle("Default"))
        green_header = STYLES_PDF.get("GREEN_HEADER", ParagraphStyle("Default"))
        module_header = STYLES_PDF.get("MODULE_HEADER", ParagraphStyle("Default"))
        test_header = STYLES_PDF.get("TEST_HEADER", ParagraphStyle("Default"))
        text_style = STYLES_PDF.get("BLACK_BOLD", ParagraphStyle("Default"))
        if error:
            title = Paragraph("<b>Wiliot Certificate Error!</b>", red_header)
            hdr_page.append(title)
            hdr_page.append(Spacer(1, 20))
            hdr_page.append(Paragraph(f"{error}", text_style))
        else:
            title = Paragraph("<b>Wiliot Certificate Passed!</b>", green_header) if not failures else Paragraph("<b>Wiliot Certificate Failed!</b>", red_header)
            hdr_page.append(title)
        hdr_page.append(Spacer(1, 20))
        hdr_page.append(Paragraph(f"<b>Summary</b>", module_header))
        hdr_page.append(Spacer(1, 20))
        hdr_page.append(Paragraph(f"Run date: {start_time.strftime('%d/%m/%Y, %H:%M:%S')}", text_style))
        hdr_page.append(Paragraph(f"Tests duration: {str(duration).split('.')[0]}", text_style))
        hdr_page.append(Paragraph(f"Certificate version: {CERT_VERSION}", text_style))
        if gw_ble_mac:
            hdr_page.append(Paragraph(f"BLE simulator mac: {gw_ble_mac}", text_style))
        if gw_ble_version:
            hdr_page.append(Paragraph(f"BLE simulator version: {gw_ble_version}", text_style))
        hdr_page.append(Paragraph(f"Tested bridge ID: {brg}", text_style))
        if brg_version:
            hdr_page.append(Paragraph(f"Tested bridge version: {brg_version}", text_style))
        hdr_page.append(Spacer(1, 20))

        # Count Table
        count_data = [
            ["PASSED", "SKIPPED", "FAILED", "TOTAL"],
            [len(tests)-(failures+skipped), skipped, failures, len(tests)]
        ]
        count_table = Table(count_data)
        count_table.setStyle(INNER_TABLE_STYLE)
        hdr_page.append(count_table)
        hdr_page.append(Spacer(1, 20))

        # Test Results
        results_per_module = generate_results_per_module_for_pdf(tests=tests)
        summary_data = []
        for module, test_results in results_per_module.items():
            elements.append(Paragraph(f"<b>{module + ' Module' if module else 'Edge Management'}</b>", module_header))
            elements.append(Spacer(1, 20))
            for test_result in test_results:
                group = []
                summary_data += [[module, test_result.name, test_result.result, test_result.duration]]
                group.append(Paragraph(f"<b>{test_result.name}</b>", test_header))
                group.append(Spacer(1, 10))

                group.append(test_result.result)
                group.append(Spacer(1, 10))

                group.append(Paragraph(f"Tested Devices: {test_result.devices}", text_style))
                group.append(Paragraph(f"Test duration: {test_result.duration}", text_style))
                group.append(Spacer(1, 10))

                group.append(test_result.test_table)
                group.append(Spacer(1, 20))
                elements.append(KeepTogether(group))
            elements.append(PageBreak())
        summary_table = Table([["Module", "Name", "Result", "Duration"]] + summary_data)
        summary_table.setStyle(INNER_TABLE_STYLE)
        elements = hdr_page + [summary_table, PageBreak()] + elements

        doc.build(elements)


##################################
# HTML
##################################
COLORS_HTML = {
    "HEADER": "color: #ff00ff;",  # Purple
    "BLUE": "color: #0000ff;",   # Blue
    "CYAN": "color: #00ffff;",   # Cyan
    "GREEN": "color: #00ff00;",  # Green
    "WARNING": "color: #ffff00;",  # Yellow
    "RED": "color: #ff0000;",    # Red
    "BOLD": "font-weight: bold;",
    "UNDERLINE": "text-decoration: underline;",
}
color_html = lambda c, t: f'<span style="{COLORS_HTML.get(c, "")}{COLORS_HTML["BOLD"]}">{t}</span>'
html_result_map = {TEST_FAILED: color_html("RED", "FAIL"), TEST_SKIPPED: color_html("WARNING", "SKIPPED"),
                   TEST_PASSED: color_html("GREEN", "PASS"), TEST_INIT: color_html("CYAN", "INIT")}
pass_or_fail_html = lambda obj : html_result_map[obj.rc]

HTML_START = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset='utf-8'>
        <meta http-equiv='X-UA-Compatible' content='IE=edge'>
        <title>Wiliot Certificate Results</title>
        <meta name='viewport' content='width=device-width, initial-scale=1'>
        <style>
        html, body {{
                height: 100%;
            }}

            html {{
                display: table;
                margin: auto;
            }}

            body {{
                display: table-cell;
                vertical-align: middle;
            }}
        table {{
            border-collapse: collapse;
            font-family: Tahoma, Geneva, sans-serif;
        }}
        table td {{
            padding: 15px;
        }}
        table thead td {{
            background-color: #54585d;
            color: #ffffff;
            font-weight: bold;
            font-size: 13px;
            border: 1px solid #54585d;
        }}
        table tbody td {{
            color: #636363;
            border: 1px solid #dddfe1;
        }}
        table tbody tr {{
            background-color: #f9fafb;
        }}
        table tbody tr:nth-child(odd) {{
            background-color: #ffffff;
        }}
        </style>
    </head>
    <body>
    """
HTML_END = """
    </body>
    </html>
    """

##################################
# PDF
##################################
STYLES_PDF = {
    "GREEN_HEADER": ParagraphStyle("Green Header", fontName="Helvetica-Bold", fontSize=20, textColor=colors.green, alignment=TA_CENTER),
    "RED_HEADER": ParagraphStyle("Red Header", fontName="Helvetica-Bold", fontSize=20, textColor=colors.red, alignment=TA_CENTER),
    "MODULE_HEADER": ParagraphStyle("Module Header", fontName="Helvetica-Bold", fontSize=16, textColor=colors.navy, alignment=TA_CENTER),
    "TEST_HEADER": ParagraphStyle("Test Header", fontName="Helvetica-Bold", fontSize=12, textColor=colors.black, alignment=TA_CENTER),
    "BLACK": ParagraphStyle("Black", fontName="Helvetica", fontSize=9, textColor=colors.black, splitLongWords=False, alignment=TA_CENTER, wordWrap = 'CJK'),
    "BLACK_BOLD": ParagraphStyle("Black Bold", fontName="Helvetica-Bold", fontSize=9, textColor=colors.black, splitLongWords=False, alignment=TA_LEFT, wordWrap = 'CJK'),
    "BLUE": ParagraphStyle("Blue", fontName="Helvetica-Bold", fontSize=9, textColor=colors.navy, splitLongWords=False, alignment=TA_CENTER),
    "CYAN": ParagraphStyle("Cyan", fontName="Helvetica-Bold", fontSize=9, textColor=colors.cyan, splitLongWords=False, alignment=TA_CENTER),
    "GREEN": ParagraphStyle("Green", fontName="Helvetica-Bold", fontSize=9, textColor=colors.green, splitLongWords=False, alignment=TA_CENTER),
    "WARNING": ParagraphStyle("Warning", fontName="Helvetica-Bold", fontSize=9, textColor=colors.gold, splitLongWords=False, alignment=TA_CENTER),
    "RED": ParagraphStyle("Red", fontName="Helvetica-Bold", fontSize=9, textColor=colors.red, splitLongWords=False, alignment=TA_CENTER),
}
def color_pdf(c, t):
    style = STYLES_PDF.get(c, ParagraphStyle("Default"))
    return Paragraph(t, style)
pdf_result_map = {TEST_FAILED: color_pdf("RED", "FAILED"), TEST_SKIPPED: color_pdf("WARNING", "SKIPPED"), 
                  TEST_PASSED: color_pdf("GREEN", "PASSED"),  TEST_INIT: color_pdf("CYAN", "INIT")}
pass_or_fail_pdf = lambda obj : pdf_result_map[obj.rc]

INNER_TABLE_STYLE = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                ('WORDWRAP', (0, 0), (-1, -1), False),
            ])

def generate_results_per_module_for_pdf(tests=[]):
    text_style = STYLES_PDF.get("BLACK", ParagraphStyle("Default"))
    results_per_module = {}
    for test in tests:
        name=test.module_name if (not test.internal_brg or "gw" in test.module_name) else f"{test.module_name} (internal brg)"
        devices_to_print = (test.gw if not test.brg0 or test.gw_only else
                        (f"{test.brg0.id_str}\n{test.brg1.id_str}" if test.brg1 and test.multi_brg else test.brg0.id_str))
        inner_table = [[Paragraph(phase.name, text_style), pass_or_fail_pdf(phase), Paragraph(phase.reason, text_style)] for phase in test.phases]
        test_table = Table([["Phase", "Result", "Notes"]] + inner_table)
        test_table.setStyle(INNER_TABLE_STYLE)
        test_result = TestResult(name=name, devices_to_print=devices_to_print,
                                 test_table=test_table, result=pass_or_fail_pdf(test), duration=test.duration)
        module_name = cert_utils.module2name(test.test_module)
        if module_name not in results_per_module:
                results_per_module[module_name] = [test_result]
        else:
            results_per_module[module_name] += [test_result]
    return results_per_module
