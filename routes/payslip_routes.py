from flask import Blueprint, request, jsonify, session
from services.payslip_service import generate_payslip
from services.pdf_service import generate_pdf
from database.models import Payslip
from routes.decorators import login_required, admin_required

payslip_bp = Blueprint('payslip', __name__)

ADMIN_ROLES = ('Admin', 'HR', 'MD')


# ── POST /generate_payslip  (admin only) ─────────────────────
@payslip_bp.route('/generate_payslip', methods=['POST'])
@admin_required
def generate():
    try:
        data = request.json

        if not data.get('employee_id') or not data.get('month'):
            return jsonify({
                "status":  "error",
                "message": "Missing required fields"
            }), 400

        payslip = generate_payslip(data['employee_id'], data['month'])

        return jsonify({
            "status":     "success",
            "message":    "Payslip generated",
            "net_salary": payslip.net_salary
        })

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 404
    except Exception:
        return jsonify({"status": "error", "message": "Something went wrong"}), 500


# ── GET /get_payslip/<emp_id>  (admin only) ───────────────────
@payslip_bp.route('/get_payslip/<int:emp_id>', methods=['GET'])
@admin_required
def get_payslip(emp_id):
    payslips = Payslip.query.filter_by(employee_id=emp_id).all()

    if not payslips:
        return jsonify({"status": "error", "message": "No payslips found"}), 404

    result = []
    for p in payslips:
        result.append({
            "id":           p.id,
            "employee_id":  p.employee_id,
            "month":        p.month,
            "basic_salary": p.basic_salary,
            "hra":          p.hra,
            "deductions":   p.deductions,
            "net_salary":   p.net_salary
        })

    return jsonify({"status": "success", "data": result})


# ── GET /my_payslips  (logged-in employee sees only their own) ─
@payslip_bp.route('/my_payslips', methods=['GET'])
@login_required
def my_payslips():
    payslips = Payslip.query.filter_by(employee_id=session['user_id']).all()

    result = []
    for p in payslips:
        result.append({
            "id":           p.id,
            "month":        p.month,
            "basic_salary": p.basic_salary,
            "hra":          p.hra,
            "deductions":   p.deductions,
            "net_salary":   p.net_salary
        })

    return jsonify({"status": "success", "data": result})