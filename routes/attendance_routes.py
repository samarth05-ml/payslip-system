from flask import Blueprint, request, jsonify
from database.db import db
from database.models import Attendance
from datetime import datetime

attendance_bp = Blueprint("attendance", __name__)

@attendance_bp.route("/checkin", methods=["POST"])
def checkin():

    data = request.json

    record = Attendance(
        employee_id=data["employee_id"],
        date=datetime.now().date(),
        in_time=datetime.now()
    )

    db.session.add(record)
    db.session.commit()

    return jsonify({"message":"Checked In"})

@attendance_bp.route("/checkout", methods=["POST"])
def checkout():

    data = request.json

    attendance = Attendance.query.filter_by(
        employee_id=data["employee_id"]
    ).order_by(
        Attendance.id.desc()
    ).first()

    attendance.out_time = datetime.now()

    total_hours = (
        attendance.out_time -
        attendance.in_time
    ).total_seconds()/3600

    attendance.working_hours = total_hours

    if total_hours > 8:
        attendance.ot_hours = total_hours - 8

    db.session.commit()

    return jsonify({"message":"Checked Out"})