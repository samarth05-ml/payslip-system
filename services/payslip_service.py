from database.models import Employee, Payslip, Leave
from database.db import db
from utils.salary_calculator import calculate_salary

def generate_payslip(employee_id, month):

    employee = Employee.query.get(employee_id)

    if not employee:
        raise ValueError("Employee not found")

    #Get base salary calculations
    hra, deductions, net_salary = calculate_salary(employee.basic_salary)

    #NEW: Get approved leaves
    approved_leaves = Leave.query.filter_by(
        employee_id=employee_id,
        status="Approved"
    ).all()

    total_leave_days = sum([leave.days for leave in approved_leaves])

    #Calculate leave deduction
    per_day_salary = employee.basic_salary / 30
    leave_deduction = total_leave_days * per_day_salary

    #Adjust net salary
    net_salary = net_salary - leave_deduction

    #Save payslip
    payslip = Payslip(
        employee_id=employee_id,
        month=month,
        basic_salary=employee.basic_salary,
        hra=hra,
        deductions=deductions + leave_deduction,
        net_salary=net_salary
    )

    db.session.add(payslip)
    db.session.commit()

    return payslip