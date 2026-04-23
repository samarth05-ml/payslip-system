import random
from database.db import db
from database.models import Employee, Leave, Payslip

def generate_data():

    roles = ["Employee", "HR", "MD"]

    #Create Employees
    for i in range(10):
        emp = Employee(
            name=f"Employee_{i}",
            email=f"emp{i}@mail.com",
            designation="Developer",
            basic_salary=random.randint(20000, 50000),
            role=random.choice(roles)
        )
        db.session.add(emp)

    db.session.commit()

    employees = Employee.query.all()

    # Create Leaves
    for emp in employees:
        for _ in range(random.randint(1, 5)):
            leave = Leave(
                employee_id=emp.id,
                days=random.randint(1, 5),
                status=random.choice(["Approved", "Pending", "Rejected"]),
                approver_id=None
            )
            db.session.add(leave)

    db.session.commit()

    #Create Payslips
    for emp in employees:
        for _ in range(3):
            payslip = Payslip(
                employee_id=emp.id,
                month=random.choice(["Jan", "Feb", "Mar"]),
                basic_salary=emp.basic_salary,
                hra=emp.basic_salary * 0.2,
                deductions=emp.basic_salary * 0.1,
                net_salary=emp.basic_salary * 1.1
            )
            db.session.add(payslip)

    db.session.commit()

    print("Dummy data generated successfully!")

from app import app

if __name__ == "__main__":
    with app.app_context():
        generate_data()

