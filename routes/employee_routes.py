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

@employee_bp.route('/get_employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()

    result = []

    for emp in employees:
        result.append({
            "id": emp.id,
            "name": emp.name,
            "email": emp.email,
            "designation": emp.designation,
            "basic_salary": emp.basic_salary
        })

    return jsonify(result)

'''testing
@employee_bp.route('/test_employee')
def test_employee():
    employee = Employee(
        name="Samarth",
        email="samarth@email.com",
        designation="Developer",
        basic_salary=30000
    )

    db.session.add(employee)
    db.session.commit()

    return {"message": "Test employee added"}'''