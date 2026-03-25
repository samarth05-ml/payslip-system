from database.models import Employee, Payslip
from database.db import db
from utils.salary_calculator import calculate_salary

def generate_payslip(employee_id, month):

    employee = Employee.query.get(employee_id)

    hra, deductions, net_salary = calculate_salary(employee.basic_salary)

    payslip = Payslip(
        employee_id=employee_id,
        month=month,
        basic_salary=employee.basic_salary,
        hra=hra,
        deductions=deductions,
        net_salary=net_salary
    )

    db.session.add(payslip)
    db.session.commit()

    return payslip