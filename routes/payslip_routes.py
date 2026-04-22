from flask import Blueprint, request, jsonify
from services.payslip_service import generate_payslip
from services.pdf_service import generate_pdf
from database.models import Payslip

payslip_bp = Blueprint('payslip', __name__)

@payslip_bp.route('/generate_payslip', methods=['POST'])
def generate():
    try:
        data = request.json

        # Basic validation
        if not data.get('employee_id') or not data.get('month'):
            return jsonify({
                "status": "error",
                "message": "Missing required fields"
            }), 400

        payslip = generate_payslip(
            data['employee_id'],
            data['month']
        )

        return jsonify({
            "status": "success",
            "message": "Payslip generated",
            "net_salary": payslip.net_salary
        })

    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 404

    except Exception:
        return jsonify({
            "status": "error",
            "message": "Something went wrong"
        }), 500


@payslip_bp.route('/get_payslip/<int:emp_id>', methods=['GET'])
def get_payslip(emp_id):
    payslips = Payslip.query.filter_by(employee_id=emp_id).all()

    if not payslips:
        return jsonify({
            "status": "error",
            "message": "No payslips found"
        }), 404

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

    return jsonify({
        "status": "success",
        "data": result
    })