from flask import Blueprint, request, jsonify
from database.db import db
from database.models import Leave, Employee

leave_bp = Blueprint('leave', __name__)

# Apply Leave
@leave_bp.route('/apply_leave', methods=['POST'])
def apply_leave():
    data = request.json

    employee_id = data.get('employee_id')
    days = data.get('days')

    #Check employee exists
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    #Decide approver based on role
    if employee.role == "Employee":
        approver = Employee.query.filter_by(role="HR").first()
    elif employee.role == "HR":
        approver = Employee.query.filter_by(role="MD").first()
    else:
        approver = None

    if not approver:
        return jsonify({"error": "Approver not found"}), 404

    #Create leave request
    leave = Leave(
        employee_id=employee_id,
        days=days,
        status="Pending",
        approver_id=approver.id
    )

    db.session.add(leave)
    db.session.commit()

    return jsonify({
        "message": "Leave applied successfully",
        "approver_id": approver.id
    })


# Approve / Reject Leave
@leave_bp.route('/approve_leave', methods=['POST'])
def approve_leave():
    data = request.json

    leave_id = data.get('leave_id')
    status = data.get('status')  # Approved / Rejected

    #Get leave request
    leave = Leave.query.get(leave_id)
    if not leave:
        return jsonify({"error": "Leave not found"}), 404

    #Get approver (who is approving)
    approver_id = data.get('approver_id')
    if leave.approver_id != approver_id:
        return jsonify({"error": "You are not authorized to approve this leave"}), 403

    #Update status
    leave.status = status

    db.session.commit()

    return jsonify({
        "message": f"Leave {status.lower()} successfully"
    })