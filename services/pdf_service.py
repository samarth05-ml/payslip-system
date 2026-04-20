from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from database.models import Employee

def generate_pdf(payslip):
    file_name = f"payslip_{payslip.id}.pdf"

    #Create document
    doc = SimpleDocTemplate(file_name, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()

    #Get employee details (JOIN)
    employee = Employee.query.get(payslip.employee_id)

    if not employee:
        raise ValueError("Employee not found")

    #Logo
    logo = Image("ymgm-logo.jpg", width=80, height=50)

    #Header (Logo + Company Name)
    header = Table([
        [logo, Paragraph("Mahatma Gandhi Memorial Evening College", styles['Title'])]
    ])

    header.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))

    elements.append(header)

    #Payslip Title
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("PAYSLIP", styles['Heading2']))
    elements.append(Spacer(1, 20))

    #Employee Info Table
    emp_data = [
        ["Name", employee.name],
        ["Designation", employee.designation],
        ["Month", payslip.month]
    ]

    emp_table = Table(emp_data, colWidths=[150, 250])
    emp_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (0,-1), colors.lightgrey)
    ]))

    elements.append(emp_table)

    elements.append(Spacer(1, 20))

    #Salary Table
    salary_data = [
        ["Component", "Amount"],
        ["Basic Salary", payslip.basic_salary],
        ["HRA", payslip.hra],
        ["Deductions", payslip.deductions],
        ["Net Salary", payslip.net_salary]
    ]

    salary_table = Table(salary_data, colWidths=[200, 200])
    salary_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white)
    ]))

    elements.append(salary_table)

    elements.append(Spacer(1, 30))

    #Footer
    elements.append(Paragraph("This is a system generated payslip.", styles['Normal']))

    #Build PDF
    doc.build(elements)

    return file_name