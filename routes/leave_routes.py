from flask import Blueprint, request, jsonify, session
from database.db import db
from database.models import Leave, Employee
from routes.decorators import login_required, admin_required

leave_bp = Blueprint('leave', __name__)

ADMIN_ROLES = ('Admin', 'HR', 'MD')


# ── POST /apply_leave ─────────────────────────────────────────
# Employees submit their own leave; admins can submit on behalf of any employee.
@leave_bp.route('/apply_leave', methods=['POST'])
@login_required
def apply_leave():
    data = request.json

    # Employees can only apply for themselves
    if session['user_role'] not in ADMIN_ROLES:
        employee_id = session['user_id']
    else:
        employee_id = data.get('employee_id')

    days = data.get('days')

    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    # Decide approver based on role
    if employee.role == "Employee":
        approver = Employee.query.filter_by(role="HR").first()
    elif employee.role == "HR":
        approver = Employee.query.filter_by(role="MD").first()
    else:
        approver = None

    if not approver:
        approver = Employee.query.first()

    if not approver:
        return jsonify({"error": "Approver not found"}), 404

    leave = Leave(
        employee_id=employee_id,
        days=days,
        status="Pending",
        approver_id=approver.id
    )

    db.session.add(leave)
    db.session.commit()

    return jsonify({
        "message":     "Leave applied successfully",
        "approver_id": approver.id
    })


# ── POST /approve_leave ───────────────────────────────────────
@leave_bp.route('/approve_leave', methods=['POST'])
@admin_required
def approve_leave():
    data = request.json

    leave_id    = data.get('leave_id')
    status      = data.get('status')   # "Approved" / "Rejected"
    approver_id = data.get('approver_id')

    leave = Leave.query.get(leave_id)
    if not leave:
        return jsonify({"error": "Leave not found"}), 404

    if leave.approver_id != approver_id:
        return jsonify({"error": "You are not authorized to approve this leave"}), 403

    leave.status = status
    db.session.commit()

    return jsonify({"message": f"Leave {status.lower()} successfully"})


# ── GET /leave_status/<employee_id> ──────────────────────────
# Employees can only see their own; admins can see anyone's.
@leave_bp.route('/leave_status/<int:employee_id>', methods=['GET'])
@login_required
def leave_status(employee_id):
    # Block employee from querying another employee's leaves
    if session['user_role'] not in ADMIN_ROLES:
        if session['user_id'] != employee_id:
            return jsonify({"error": "Forbidden"}), 403

    leaves = Leave.query.filter_by(employee_id=employee_id).all()

    result = []
    for leave in leaves:
        result.append({
            "leave_id":   leave.id,
            "days":       leave.days,
            "status":     leave.status,
            "approver_id":leave.approver_id
        })

    return jsonify(result)


# ── GET /my_leaves  (employee portal shortcut) ────────────────
@leave_bp.route('/my_leaves', methods=['GET'])
@login_required
def my_leaves():
    leaves = Leave.query.filter_by(employee_id=session['user_id']).all()
    result = []
    for leave in leaves:
        result.append({
            "leave_id":   leave.id,
            "days":       leave.days,
            "status":     leave.status,
            "approver_id":leave.approver_id
        })
    return jsonify(result)