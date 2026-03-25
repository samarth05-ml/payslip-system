from .db import db

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    designation = db.Column(db.String(100))
    basic_salary = db.Column(db.Float)

class Payslip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer)
    month = db.Column(db.String(20))
    basic_salary = db.Column(db.Float)
    hra = db.Column(db.Float)
    deductions = db.Column(db.Float)
    net_salary = db.Column(db.Float)