import pandas as pd
import joblib

from database.models import Employee, Leave, Payslip, Prediction


def predict_leave(employee_id):

    # Load model (only this)
    model = joblib.load("ml/leave_model.pkl")

    employee = Employee.query.get(employee_id)

    if not employee:
        raise ValueError("Employee not found")

    leaves = Leave.query.filter_by(employee_id=employee_id).all()
    payslips = Payslip.query.filter_by(employee_id=employee_id).all()

    approved_leaves = sum([l.days for l in leaves if l.status == "Approved"])

    avg_salary = 0
    if payslips:
        avg_salary = sum([p.net_salary for p in payslips]) / len(payslips)

    sample = pd.DataFrame([{
        "basic_salary": employee.basic_salary,
        "approved_leaves": approved_leaves,
        "avg_salary": avg_salary
    }])

    prediction = model.predict(sample)[0]
    # SAVE TO DATABASE
    new_prediction = Prediction(
        employee_id=employee_id,
        prediction=int(prediction)
    )

    from app import db
    db.session.add(new_prediction)
    db.session.commit()

    return int(prediction)
    

# anamoly

from sklearn.ensemble import IsolationForest
import pandas as pd
from app import db
from database.models import Payslip, Anomaly


def detect_anomalies():

    payslips = Payslip.query.all()

    data = []

    for p in payslips:
        data.append({
            "id": p.id,
            "employee_id": p.employee_id,
            "basic_salary": p.basic_salary,
            "hra": p.hra,
            "deductions": p.deductions,
            "net_salary": p.net_salary
        })

    df = pd.DataFrame(data)

    if df.empty:
        raise ValueError("No payslip data available")

    # Features
    features = df[["basic_salary", "hra", "deductions", "net_salary"]]

    # Model
    model = IsolationForest(contamination=0.1, random_state=42)
    df["anomaly"] = model.fit_predict(features)

    anomalies = df[df["anomaly"] == -1]

    result = []

    # OPTIONAL: Clear old records (to avoid duplicates)
    Anomaly.query.delete()

    for _, row in anomalies.iterrows():

        # SAVE TO DB
        anomaly = Anomaly(
            employee_id=int(row["employee_id"]),
            net_salary=float(row["net_salary"]),
            status="Anomaly"
        )

        db.session.add(anomaly)

        result.append({
            "payslip_id": int(row["id"]),
            "employee_id": int(row["employee_id"]),
            "net_salary": float(row["net_salary"]),
            "status": "Anomaly"
        })

    db.session.commit()

    return result
#behavior 

from sklearn.cluster import KMeans
import pandas as pd

from database.models import Employee, Leave, Payslip


def get_employee_behavior():

    employees = Employee.query.all()
    leaves = Leave.query.all()
    payslips = Payslip.query.all()

    data = []

    for emp in employees:
        emp_leaves = [l for l in leaves if l.employee_id == emp.id]
        emp_payslips = [p for p in payslips if p.employee_id == emp.id]

        total_leaves = sum([l.days for l in emp_leaves])

        avg_salary = 0
        if emp_payslips:
            avg_salary = sum([p.net_salary for p in emp_payslips]) / len(emp_payslips)

        data.append({
            "employee_id": emp.id,
            "total_leaves": total_leaves,
            "avg_salary": avg_salary
        })

    df = pd.DataFrame(data)

    if df.empty:
        raise ValueError("No data available")

    # Features
    X = df[["total_leaves", "avg_salary"]]

    # KMeans
    model = KMeans(n_clusters=3, random_state=42)
    df["cluster"] = model.fit_predict(X)

    # Label clusters
    labels = {}

    for cluster in df["cluster"].unique():
        subset = df[df["cluster"] == cluster]

        avg_leaves = subset["total_leaves"].mean()

        if avg_leaves > 5:
            labels[cluster] = "Frequent Leave Taker"
        elif avg_leaves > 2:
            labels[cluster] = "High Risk"
        else:
            labels[cluster] = "Normal"

    df["behavior"] = df["cluster"].map(labels)

    # Final result
    result = []

    for _, row in df.iterrows():
        result.append({
            "employee_id": int(row["employee_id"]),
            "behavior": row["behavior"]
        })

    return result

def get_dashboard_summary():
    from database.models import Employee, Payslip, Prediction, Anomaly

    # Total employees
    total_employees = Employee.query.count()

    # Total payslips
    total_payslips = Payslip.query.count()

    # Use Prediction table
    total_predictions = Prediction.query.count()

    # Use Anomaly table
    anomaly_count = Anomaly.query.filter_by(status="Anomaly").count()

    return {
        "total_employees": total_employees,
        "payslips_generated": total_payslips,
        "leave_predictions": total_predictions,
        "anomalies": anomaly_count
    }

def get_analytics():
    from database.models import Payslip, Leave
    from collections import defaultdict

    salary_data = defaultdict(float)
    leave_data = defaultdict(int)

    payslips = Payslip.query.all()
    leaves = Leave.query.all()

    # Salary trend (using month from Payslip)
    for p in payslips:
        month = p.month
        salary_data[month] += p.net_salary

    salary_trend = []
    for month, total in salary_data.items():
        salary_trend.append({
            "month": month,
            "total_salary": total
        })

    #Leave trend (FIXED bug here)
    for l in leaves:
        
        if hasattr(l, "month"):
            month = l.month
        else:
            # fallback if no month field
            month = "Unknown"

        leave_data[month] += l.days

    leave_trend = []
    for month, total in leave_data.items():
        leave_trend.append({
            "month": month,
            "leaves": total
        })

    return {
        "salary_trend": salary_trend,
        "leave_trend": leave_trend
    }