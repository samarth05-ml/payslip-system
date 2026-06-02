from flask import Blueprint, request, jsonify
from database.db import db
from database.models import Holiday

holiday_bp = Blueprint("holiday", __name__)

@holiday_bp.route("/add_holiday", methods=["POST"])
def add_holiday():

    data = request.json

    holiday = Holiday(
        holiday_name=data["holiday_name"],
        holiday_date=data["holiday_date"]
    )

    db.session.add(holiday)
    db.session.commit()

    return jsonify({"message":"Holiday Added"})