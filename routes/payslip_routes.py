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