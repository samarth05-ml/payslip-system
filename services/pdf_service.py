import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from database.models import Employee

BASE_DIR  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LOGO_PATH = os.path.join(BASE_DIR, 'frontend', 'assets', 'ymgm-logo.jpg')
PDF_DIR   = os.path.join(BASE_DIR, 'data', 'pdfs')

# ── Colour palette ───────────────────────────────────────────
DARK_BLUE   = (0.10, 0.18, 0.38)   # header / footer bg
ACCENT_BLUE = (0.18, 0.42, 0.78)   # section headings bar
LIGHT_GREY  = (0.96, 0.96, 0.97)   # alternating row bg
MID_GREY    = (0.55, 0.55, 0.60)   # secondary text
WHITE       = (1, 1, 1)
BLACK       = (0, 0, 0)
GREEN       = (0.13, 0.62, 0.40)   # net salary highlight


def _set(c, rgb):
    c.setFillColorRGB(*rgb)


def _rect(c, x, y, w, h, rgb, stroke=False):
    c.setFillColorRGB(*rgb)
    if stroke:
        c.setStrokeColorRGB(*rgb)
    c.rect(x, y, w, h, fill=1, stroke=int(stroke))


def generate_pdf(payslip):
    os.makedirs(PDF_DIR, exist_ok=True)
    file_path = os.path.join(PDF_DIR, f"payslip_{payslip.id}.pdf")

    employee = Employee.query.get(payslip.employee_id)
    if not employee:
        raise ValueError("Employee not found")

    W, H = A4          # 595 x 842 pts
    M    = 30          # margin
    c    = canvas.Canvas(file_path, pagesize=A4)

    # ── HEADER BAND ──────────────────────────────────────────
    _rect(c, 0, H - 90, W, 90, DARK_BLUE)

    # Logo (if present)
    logo_x = M
    if os.path.exists(LOGO_PATH):
        c.drawImage(LOGO_PATH, logo_x, H - 75, width=55, height=55,
                    preserveAspectRatio=True, mask='auto')
        logo_x += 65

    # College name + subtitle
    _set(c, WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(logo_x, H - 38, "Mahatma Gandhi Memorial Evening College")
    c.setFont("Helvetica", 9)
    _set(c, (0.75, 0.85, 1.0))
    c.drawString(logo_x, H - 53, "Corporate Payroll Processing Centre  |  Udupi, Karnataka")

    # PAYSLIP badge (right side)
    badge_w = 110
    _rect(c, W - M - badge_w, H - 68, badge_w, 34, ACCENT_BLUE)
    _set(c, WHITE)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(W - M - badge_w / 2, H - 48, "PAYSLIP")
    c.setFont("Helvetica", 7)
    ref = f"REF-MS-{payslip.id:05d}"
    c.drawCentredString(W - M - badge_w / 2, H - 60, ref)

    # ── THIN ACCENT LINE ─────────────────────────────────────
    _rect(c, 0, H - 93, W, 3, ACCENT_BLUE)

    # ── EMPLOYEE INFO SECTION ────────────────────────────────
    y = H - 115
    _set(c, ACCENT_BLUE)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(M, y, "EMPLOYEE DETAILS")
    _rect(c, M, y - 3, W - 2*M, 1, ACCENT_BLUE)

    y -= 18
    col1_x, col2_x, col3_x = M, W/2 - 20, W/2 + 80
    label_font, val_font = "Helvetica", "Helvetica-Bold"

    def info_row(label1, val1, label2, val2, yy):
        _set(c, MID_GREY);  c.setFont(label_font, 8)
        c.drawString(col1_x, yy, label1)
        c.drawString(col3_x, yy, label2)
        _set(c, BLACK);     c.setFont(val_font, 9)
        c.drawString(col2_x, yy, str(val1))
        c.drawString(col3_x + 70, yy, str(val2))

    info_row("Employee Name",  employee.name,
             "Pay Period",     payslip.month,        y)
    y -= 16
    info_row("Designation",    employee.designation,
             "Employee ID",    f"EMP-{employee.id:04d}", y)
    y -= 16
    info_row("Department",     employee.role,
             "Date of Issue",  datetime.today().strftime("%d %b %Y"), y)

    # ── EARNINGS & DEDUCTIONS TABLE ──────────────────────────
    y -= 30
    _set(c, ACCENT_BLUE)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(M, y, "SALARY BREAKDOWN")
    _rect(c, M, y - 3, W - 2*M, 1, ACCENT_BLUE)

    # Table header
    y -= 18
    col_w   = (W - 2*M) / 4
    headers = ["Component", "Earnings (Rs.)", "Deductions (Rs.)", "Net (Rs.)"]
    _rect(c, M, y - 4, W - 2*M, 18, DARK_BLUE)
    _set(c, WHITE)
    c.setFont("Helvetica-Bold", 8)
    for i, h in enumerate(headers):
        c.drawString(M + i * col_w + 5, y + 2, h)

    # Rows
    rows = [
        ("Basic Salary",   f"{payslip.basic_salary:,.2f}", "",                          ""),
        ("HRA (40%)",      f"{payslip.hra:,.2f}",          "",                          ""),
        ("Gross Salary",   f"{payslip.basic_salary + payslip.hra:,.2f}", "", ""),
        ("PF / Deductions","",                              f"{payslip.deductions:,.2f}", ""),
    ]

    for idx, (comp, earn, ded, net) in enumerate(rows):
        y -= 18
        bg = LIGHT_GREY if idx % 2 == 0 else WHITE
        _rect(c, M, y - 4, W - 2*M, 18, bg)
        _set(c, BLACK)
        c.setFont("Helvetica", 8.5)
        c.drawString(M + 5,             y + 2, comp)
        c.setFont("Helvetica-Bold", 8.5)
        if earn: c.drawString(M + col_w + 5,   y + 2, earn)
        if ded:  c.drawString(M + 2*col_w + 5, y + 2, ded)

    # ── NET SALARY HIGHLIGHT ─────────────────────────────────
    y -= 26
    _rect(c, M, y - 6, W - 2*M, 26, GREEN)
    _set(c, WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M + 10, y + 6, "NET SALARY PAYABLE")
    c.setFont("Helvetica-Bold", 14)
    c.drawRightString(W - M - 10, y + 5, f"Rs. {payslip.net_salary:,.2f}")

    # ── SUMMARY BOXES ────────────────────────────────────────
    y -= 40
    box_w = (W - 2*M - 20) / 3
    boxes = [
        ("Basic Salary",  f"Rs. {payslip.basic_salary:,.2f}",  ACCENT_BLUE),
        ("Total Deductions", f"Rs. {payslip.deductions:,.2f}", (0.78, 0.22, 0.22)),
        ("Net Pay",       f"Rs. {payslip.net_salary:,.2f}",    GREEN),
    ]
    for i, (label, val, col) in enumerate(boxes):
        bx = M + i * (box_w + 10)
        _rect(c, bx, y - 30, box_w, 44, col)
        _set(c, WHITE)
        c.setFont("Helvetica", 7.5)
        c.drawCentredString(bx + box_w/2, y + 7, label)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(bx + box_w/2, y - 14, val)

    # ── NOTES SECTION ────────────────────────────────────────
    y -= 60
    _rect(c, M, y - 18, W - 2*M, 30, LIGHT_GREY)
    _set(c, MID_GREY)
    c.setFont("Helvetica-Oblique", 7.5)
    c.drawString(M + 8, y - 4,
                 "This is a computer-generated payslip and does not require a signature. "
                 "For queries contact HR at hr@mgmeveningcollege.ac.in")

    # ── FOOTER BAND ──────────────────────────────────────────
    _rect(c, 0, 0, W, 36, DARK_BLUE)
    _set(c, (0.75, 0.85, 1.0))
    c.setFont("Helvetica", 7.5)
    c.drawString(M, 22, "MGM Evening College  |  Udupi, Karnataka  |  Confidential Payroll Document")
    c.drawRightString(W - M, 22,
                      f"Generated: {datetime.today().strftime('%d %b %Y, %H:%M')}")
    _set(c, WHITE)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(W/2, 10, f"Page 1 of 1  |  {ref}")

    c.save()
    return file_path