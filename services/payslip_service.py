from database.models import Employee, Payslip, Leave
from database.db import db
from utils.salary_calculator import calculate_salary
from datetime import datetime

def generate_payslip(employee_id, month):

    employee = Employee.query.get(employee_id)

    if not employee:
        raise ValueError("Employee not found")

    #Get base salary calculations
    salary_details = calculate_salary(employee.basic_salary)
    hra = salary_details["hra"]
    deductions = salary_details["deductions"]
    net_salary = salary_details["net_salary"]

    #Get approved leaves for this month only
    try:
        month_dt = datetime.strptime(f"{month} 2026", "%B %Y")
    except ValueError:
        month_dt = datetime.strptime(month, "%Y-%m")

    month_start = month_dt.replace(day=1)
    month_end   = month_dt.replace(day=28)

    approved_leaves = Leave.query.filter(
        Leave.employee_id == employee_id,
        Leave.status      == "Approved",
        Leave.from_date   >= month_start,
        Leave.from_date   <= month_end
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