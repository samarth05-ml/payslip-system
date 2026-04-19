from flask import Blueprint, request, jsonify
from services.payslip_service import generate_payslip

payslip_bp = Blueprint('payslip', __name__)

@payslip_bp.route('/generate_payslip', methods=['POST'])
def generate():
    data = request.json

    payslip = generate_payslip(
        data['employee_id'],
        data['month']
    )

    return jsonify({
        "message": "Payslip generated",
        "net_salary": payslip.net_salary
    })

from database.models import Payslip

# GET PAYSLIP BY EMPLOYEE ID
@payslip_bp.route('/get_payslip/<int:emp_id>', methods=['GET'])
def get_payslip(emp_id):
    payslips = Payslip.query.filter_by(employee_id=emp_id).all()

    result = []

    for p in payslips:
        result.append({
            "id": p.id,
            "employee_id": p.employee_id,
            "month": p.month,
            "basic_salary": p.basic_salary,
            "hra": p.hra,
            "deductions": p.deductions,
            "net_salary": p.net_salary
        })

    return jsonify(result)
'''testing 
@payslip_bp.route('/test_payslip')
def test_payslip():
    from services.payslip_service import generate_payslip

    payslip = generate_payslip(1, "April")

    return {
        "message": "Payslip generated",
        "net_salary": payslip.net_salary
    }'''
from services.pdf_service import generate_pdf