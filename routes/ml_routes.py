from flask import Blueprint, jsonify
from services.ml_service import predict_leave

ml_bp = Blueprint('ml', __name__)


@ml_bp.route('/predict_leave/<int:emp_id>', methods=['GET'])
def predict(emp_id):
    try:
        result = predict_leave(emp_id)

        return jsonify({
            "status": "success",
            "employee_id": emp_id,
            "will_take_leave": result
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
    
#anamoly route

from services.ml_service import detect_anomalies


@ml_bp.route('/detect_anomaly', methods=['GET'])
def anomaly():
    try:
        result = detect_anomalies()

        return jsonify({
            "status": "success",
            "anomalies": result
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
    
#behvaior

from services.ml_service import get_employee_behavior


@ml_bp.route('/employee_behavior', methods=['GET'])
def behavior():
    try:
        result = get_employee_behavior()

        return jsonify({
            "status": "success",
            "data": result
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