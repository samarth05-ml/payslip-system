import os
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from database.models import Employee

BASE_DIR  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LOGO_PATH = os.path.join(BASE_DIR, 'frontend', 'assets', 'ymgm-logo.jpg')
PDF_DIR   = os.path.join(BASE_DIR, 'data', 'pdfs')

def generate_pdf(payslip):
    os.makedirs(PDF_DIR, exist_ok=True)
    file_name = os.path.join(PDF_DIR, f"payslip_{payslip.id}.pdf")

    doc = SimpleDocTemplate(file_name, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    employee = Employee.query.get(payslip.employee_id)
    if not employee:
        raise ValueError("Employee not found")

    # Header
    if os.path.exists(LOGO_PATH):
        logo = Image(LOGO_PATH, width=80, height=50)
        header = Table([
            [logo, Paragraph("Mahatma Gandhi Memorial Evening College", styles['Title'])]
        ])
    else:
        header = Table([
            [Paragraph("Mahatma Gandhi Memorial Evening College", styles['Title'])]
        ])

    header.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(header)

    # Payslip Title
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("PAYSLIP", styles['Heading2']))
    elements.append(Spacer(1, 20))

    # Employee Info
    emp_table = Table([
        ["Name",        employee.name],
        ["Designation", employee.designation],
        ["Month",       payslip.month]
    ], colWidths=[150, 250])
    emp_table.setStyle(TableStyle([
        ('GRID',       (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (0,-1),     colors.lightgrey)
    ]))
    elements.append(emp_table)
    elements.append(Spacer(1, 20))

    # Salary Table
    salary_table = Table([
        ["Component",    "Amount"],
        ["Basic Salary", f"Rs. {payslip.basic_salary:,.2f}"],
        ["HRA",          f"Rs. {payslip.hra:,.2f}"],
        ["Deductions",   f"Rs. {payslip.deductions:,.2f}"],
        ["Net Salary",   f"Rs. {payslip.net_salary:,.2f}"]
    ], colWidths=[200, 200])
    salary_table.setStyle(TableStyle([
        ('GRID',      (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND',(0,0), (-1,0),     colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0),     colors.white)
    ]))
    elements.append(salary_table)
    elements.append(Spacer(1, 30))

    # Footer
    elements.append(Paragraph("This is a system generated payslip.", styles['Normal']))

    doc.build(elements)
    return file_name