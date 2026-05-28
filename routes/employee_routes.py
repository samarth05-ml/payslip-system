from flask import Blueprint, request, jsonify, session
from database.db import db
from database.models import Employee
from routes.decorators import admin_required
import hashlib


employee_bp = Blueprint('employee', __name__)


from routes.decorators import admin_required
import hashlib

@employee_bp.route('/add_employee', methods=['POST'])
@admin_required
def add_employee():
    data = request.json

    if not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    employee = Employee(
        name          = data['name'],
        email         = data['email'],
        designation   = data['designation'],
        basic_salary  = data['basic_salary'],
        role          = data.get('role', 'Employee'),
        password_hash = hashlib.sha256(data['password'].encode()).hexdigest()  # ← NEW
    )

    db.session.add(employee)
    db.session.commit()

    return jsonify({"message": "Employee added successfully"})

@employee_bp.route('/get_employees', methods=['GET'])
@admin_required
def get_employees():
    employees = Employee.query.all()

    result = []
    for emp in employees:
        result.append({
            "id":           emp.id,
            "name":         emp.name,
            "email":        emp.email,
            "designation":  emp.designation,
            "basic_salary": emp.basic_salary,
            "role":         emp.role
        })

    return jsonify(result)