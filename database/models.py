from .db import db

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    designation = db.Column(db.String(100))
    basic_salary = db.Column(db.Float)
    role = db.Column(db.String(50), default="Employee")

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
    # who applied leave

    days = db.Column(db.Integer, nullable=False)  
    # number of leave days

    status = db.Column(db.String(20), default="Pending")  
    # Pending / Approved / Rejected

    approver_id = db.Column(db.Integer)  
    # who will approve (HR or MD)

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