import os
import tabulate
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# Local imports
from gw_certificate.ag.ut_defines import TEST_FAILED, TEST_INCONCLUSIVE, TEST_PASSED, TEST_INFO, TEST_WARNING, TEST_OPTIONAL
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
format_timedelta = lambda delta: f"{int(delta.total_seconds()//3600):02}:{int((delta.total_seconds()%3600)//60):02}:{int(delta.total_seconds()%60):02}"

##################################
# GENERIC
##################################
def generate_pdf_results_file(gw_cert):
    # Extract GW certificate tests results
    failures, inconclusive = 0, 0
    for test in gw_cert.tests:
        if test.rc == TEST_INCONCLUSIVE:
            inconclusive += 1
        elif test.rc == TEST_FAILED:
            failures += 1

    # Generate PDF file
    doc = SimpleDocTemplate(gw_cert.result_pdf_path, pagesize=letter)
    doc.title = f"Wiliot Gateway Certificate Results"
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
    text_style_bold = STYLES_PDF.get("BLACK_BOLD", ParagraphStyle("Default"))
    if gw_cert.error:
        title = Paragraph(f"<b>Wiliot Gateway Certificate Error!</b>", red_header)
        hdr_page.append(title)
        hdr_page.append(Spacer(1, 20))
        hdr_page.append(Paragraph(f"{gw_cert.error}", text_style_bold))
    else:
        title = Paragraph(f"<b>Wiliot Gateway Certificate Passed!</b>", green_header) if not failures else Paragraph(f"<b>Wiliot Gateway Certificate Failed!</b>", red_header)
        hdr_page.append(title)
        hdr_page.append(Spacer(1, 20))
        hdr_page.append(Paragraph(f"<b>Summary</b>", module_header))
        hdr_page.append(Spacer(1, 20))
        hdr_page.append(Paragraph(f"Run date: {gw_cert.current_datetime.strftime('%d/%m/%Y, %H:%M:%S')}", text_style_bold))
        hdr_page.append(Paragraph(f"Tests duration: {format_timedelta(gw_cert.runtime())}", text_style_bold))
        hdr_page.append(Paragraph(f"Certificate version: {gw_cert.gw_cert_version}", text_style_bold))
        hdr_page.append(Paragraph(f"BLE simulator mac: {gw_cert.uart.mac}", text_style_bold))
        hdr_page.append(Paragraph(f"BLE simulator version: {gw_cert.uart.fw_version}", text_style_bold))
        hdr_page.append(Paragraph(f"Tested gateway ID: {gw_cert.gw_id}", text_style_bold))
        hdr_page.append(Spacer(1, 20))

        # Count Table
        count_data = [
            ["PASSED", "INCONCLUSIVE", "FAILED", "TOTAL"],
            [len(gw_cert.tests)-(failures+inconclusive), inconclusive, failures, len(gw_cert.tests)]
        ]
        count_table = Table(count_data)
        count_table.setStyle(INNER_TABLE_STYLE)
        hdr_page.append(count_table)
        hdr_page.append(Spacer(1, 20))

        # Test Results
        summary_data = []
        text_style_center = STYLES_PDF.get("BLACK", ParagraphStyle("Default"))
        text_style_left = STYLES_PDF.get("BLACK_LEFT", ParagraphStyle("Default"))
        for test in gw_cert.tests:
            summary_data += [[test, pass_or_fail_pdf(test), format_timedelta(test.duration)]]
            elements.append(Paragraph(f"<b>{test.test_name}</b>", module_header))
            elements.append(Spacer(1, 20))
            elements.append(pass_or_fail_pdf(test))
            elements.append(Spacer(1, 10))
            elements.append(Paragraph(f"Test duration: {format_timedelta(test.duration)}", text_style_bold))
            elements.append(Spacer(1, 10))
            inner_table, stages_breakdown = [["Phase", "Result", "Duration"]], []
            for stage in test.stages:
                stages_breakdown += [KeepTogether([Paragraph(stage.stage_name, test_header), Spacer(1, 10), pass_or_fail_pdf(stage), Spacer(1, 10)]
                                                + [Paragraph(l, text_style_left) for l in stage.report.split('\n')]
                                                + [Spacer(1, 10)])]
                inner_table += [[Paragraph(stage.stage_name, text_style_center), pass_or_fail_pdf(stage), Paragraph(format_timedelta(stage.duration), text_style_center)]]
            test_table = Table(inner_table)
            test_table.setStyle(INNER_TABLE_STYLE)
            elements.append(test_table)
            elements.append(Spacer(1, 20))
            elements += stages_breakdown
            elements.append(PageBreak())
        summary_table = Table([["Name", "Result", "Duration"]] + summary_data)
        summary_table.setStyle(INNER_TABLE_STYLE)
        elements = hdr_page + [summary_table, PageBreak()] + elements

    doc.build(elements)


##################################
# PDF
##################################
STYLES_PDF = {
    "GREEN_HEADER": ParagraphStyle("Green Header", fontName="Helvetica-Bold", fontSize=20, textColor=colors.green, alignment=TA_CENTER),
    "RED_HEADER": ParagraphStyle("Red Header", fontName="Helvetica-Bold", fontSize=20, textColor=colors.red, alignment=TA_CENTER),
    "MODULE_HEADER": ParagraphStyle("Module Header", fontName="Helvetica-Bold", fontSize=16, textColor=colors.navy, alignment=TA_CENTER),
    "TEST_HEADER": ParagraphStyle("Test Header", fontName="Helvetica-Bold", fontSize=12, textColor=colors.black, alignment=TA_CENTER),
    "BLACK": ParagraphStyle("Black", fontName="Helvetica", fontSize=9, textColor=colors.black, splitLongWords=False, alignment=TA_CENTER, wordWrap = 'CJK'),
    "BLACK_LEFT": ParagraphStyle("Black Left", fontName="Helvetica", fontSize=9, textColor=colors.black, splitLongWords=False, alignment=TA_LEFT, wordWrap = 'CJK'),
    "BLACK_BOLD": ParagraphStyle("Black Bold", fontName="Helvetica-Bold", fontSize=9, textColor=colors.black, splitLongWords=False, alignment=TA_LEFT, wordWrap = 'CJK'),
    "BLUE": ParagraphStyle("Blue", fontName="Helvetica-Bold", fontSize=9, textColor=colors.navy, splitLongWords=False, alignment=TA_CENTER),
    "CYAN": ParagraphStyle("Cyan", fontName="Helvetica-Bold", fontSize=9, textColor=colors.cyan, splitLongWords=False, alignment=TA_CENTER),
    "GREEN": ParagraphStyle("Green", fontName="Helvetica-Bold", fontSize=9, textColor=colors.green, splitLongWords=False, alignment=TA_CENTER),
    "WARNING": ParagraphStyle("Warning", fontName="Helvetica-Bold", fontSize=9, textColor=colors.gold, splitLongWords=False, alignment=TA_CENTER),
    "RED": ParagraphStyle("Red", fontName="Helvetica-Bold", fontSize=9, textColor=colors.red, splitLongWords=False, alignment=TA_CENTER),
    "GRAY": ParagraphStyle("Gray", fontName="Helvetica-Bold", fontSize=9, textColor=colors.gray, splitLongWords=False, alignment=TA_CENTER),
}
def color_pdf(c, t):
    style = STYLES_PDF.get(c, ParagraphStyle("Default"))
    return Paragraph(t, style)
pdf_result_map = {TEST_FAILED: color_pdf("RED", "FAILED"), TEST_INCONCLUSIVE: color_pdf("WARNING", "INCONCLUSIVE"), 
                  TEST_PASSED: color_pdf("GREEN", "PASSED"),  TEST_INFO: color_pdf("CYAN", "INFO"),
                  TEST_WARNING: color_pdf("WARNING", "WARNING"), TEST_OPTIONAL: color_pdf("GRAY", "OPTIONAL")}
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
