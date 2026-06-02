from .db import db
from datetime import datetime

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100),unique=True)
    designation = db.Column(db.String(100))
    basic_salary = db.Column(db.Float)
    role = db.Column(db.String(50), default="Employee")
    password_hash = db.Column(db.String(256))
    leave_balance = db.Column(db.Float, default=12)
    pf_balance = db.Column(db.Float, default=0)
    employee_status = db.Column(db.String(20), default="Active")
    
class Payslip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer)
    month = db.Column(db.String(20))
    basic_salary = db.Column(db.Float)
    hra = db.Column(db.Float)
    deductions = db.Column(db.Float)
    net_salary = db.Column(db.Float)
    pf_deduction = db.Column(db.Float, default=0)
    leave_deduction = db.Column(db.Float, default=0)
    ot_amount = db.Column(db.Float, default=0)
    bonus_amount = db.Column(db.Float, default=0)
    expense_reimbursement = db.Column(db.Float, default=0)

class Leave(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    employee_id = db.Column(db.Integer, nullable=False)

    leave_type = db.Column(db.String(50))

    from_date = db.Column(db.DateTime)

    to_date = db.Column(db.DateTime)

    days = db.Column(db.Float, nullable=False)

    is_half_day = db.Column(db.Boolean, default=False)

    reason = db.Column(db.Text)

    status = db.Column(db.String(20), default="Pending")

    approver_id = db.Column(db.Integer)

    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer)
    prediction = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Anomaly(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer)
    net_salary = db.Column(db.Float)
    status = db.Column(db.String(20))  # "Anomaly" or "Normal"
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date)
    in_time = db.Column(db.DateTime)
    out_time = db.Column(db.DateTime)
    working_hours = db.Column(db.Float, default=0)
    ot_hours = db.Column(db.Float, default=0)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer)
    amount = db.Column(db.Float)
    description = db.Column(db.String(255))
    status = db.Column(db.String(20), default="Pending")

class Bonus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer)
    year = db.Column(db.Integer)
    amount = db.Column(db.Float)

class Holiday(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    holiday_name = db.Column(db.String(100))
    holiday_date = db.Column(db.Date)