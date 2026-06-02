from flask import Blueprint, request, jsonify
from database.db import db
from database.models import Expense

expense_bp = Blueprint("expense", __name__)

@expense_bp.route("/add_expense", methods=["POST"])
def add_expense():

    data = request.json

    expense = Expense(
        employee_id=data["employee_id"],
        amount=data["amount"],
        description=data["description"]
    )

    db.session.add(expense)
    db.session.commit()

    return jsonify({"message":"Expense Added"})