from .db import db
from datetime import datetime

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    designation = db.Column(db.String(100))
    basic_salary = db.Column(db.Float)
    role = db.Column(db.String(50), default="Employee")
    password_hash = db.Column(db.String(256))
    
class Payslip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer)
    month = db.Column(db.String(20))
    basic_salary = db.Column(db.Float)
    hra = db.Column(db.Float)
    deductions = db.Column(db.Float)
    net_salary = db.Column(db.Float)

class Leave(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    employee_id = db.Column(db.Integer, nullable=False)

    leave_type = db.Column(db.String(50))

    from_date = db.Column(db.DateTime)

    to_date = db.Column(db.DateTime)

    days = db.Column(db.Integer, nullable=False)

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