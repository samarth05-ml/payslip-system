from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(payslip):
    file_name = f"payslip_{payslip.id}.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)

    c.drawString(100, 750, f"Payslip ID: {payslip.id}")
    c.drawString(100, 730, f"Employee ID: {payslip.employee_id}")
    c.drawString(100, 710, f"Month: {payslip.month}")
    c.drawString(100, 690, f"Basic Salary: {payslip.basic_salary}")
    c.drawString(100, 670, f"HRA: {payslip.hra}")
    c.drawString(100, 650, f"Deductions: {payslip.deductions}")
    c.drawString(100, 630, f"Net Salary: {payslip.net_salary}")

    c.save()

    return file_name