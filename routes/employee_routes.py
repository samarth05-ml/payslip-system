from flask import Blueprint, request, jsonify
from database.db import db
from database.models import Employee

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/add_employee', methods=['POST'])
def add_employee():
    data = request.json

    employee = Employee(
        name=data['name'],
        email=data['email'],
        designation=data['designation'],
        basic_salary=data['basic_salary']
    )

    db.session.add(employee)
    db.session.commit()

    return jsonify({"message": "Employee added successfully"})